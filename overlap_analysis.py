"""
Quantitative cross-dataset comparison
================================================================

For every pair of experiments that overlap in BOTH zenith angle and momentum, this module:

  * auto-detects the best-matched overlap (closest angles, widest momentum span),
  * computes a chi-squared per degree of freedom between the two spectra,
  * produces a ratio plot with a 1-sigma band,

Run:
    python overlap_analysis.py                # prints table, writes figures
    python overlap_analysis.py --no-figures   # table only

Outputs (next to this script):
    overlap_ratios.png / .svg   -- grid of ratio panels, one per comparison
    overlap_summary.csv         -- chi2/ndf and mean ratio per comparison

Method
------
Two datasets rarely sit at exactly the same momenta, so we cannot difference
them point-by-point. For each pair we:

  1. Restrict to the shared momentum window [max(p_min), min(p_max)].
  2. Use the dataset with fewer points in that window as the evaluation grid.
  3. Interpolate the other dataset onto those momenta in log10(p)-log10(I) space
     (muon spectra are locally power laws, so they are near-linear in log()).
     Points needing extrapolation are dropped.
  4. Combine uncertainties in quadrature:  sigma_i^2 = sigma_ref,i^2 + sigma_oth,i^2
     (relative errors are interpolated in log space).
  5. chi^2 = sum_i (I_ref,i - I_oth,i)^2 / sigma_i^2 ,  ndf = N compared points.

chi^2/ndf ~ 1 means agreement consistent with the quoted uncertainties;
>> 1 means a real discrepancy (e.g. a normalization offset). The ratio is
always reported as other / ref so values are comparable across comparisons.

Caveats reported to the reader:
  * Where the two central angles differ (dtheta > 0) that gap is a real physical
    difference, not measurement scatter, and is printed with each result.
  * chi^2 treats each point's error as independent; the systematic
    (normalization) component is actually correlated within a dataset, so these
    chi^2 values are conservative for pure-shape agreement.
"""

from __future__ import annotations

import sqlite3
import sys
import numpy as np
from collections import defaultdict

DB = "muon_data.db"
ANGLE_TOL_DEG = 5.0     # treat two datasets as angle-comparable within this region
MIN_POINTS = 3          # need at least this many compared points for a chi2


# ---------------------------------------------------------------------------
# DATA IMPORT
# ---------------------------------------------------------------------------
def _segments(cur):
    cur.execute(
        "SELECT experiment, theta_center, MIN(momentum), MAX(momentum), COUNT(*) "
        "FROM muon_data WHERE intensity IS NOT NULL AND theta_center IS NOT NULL "
        "GROUP BY experiment, theta_center"
    )
    return [dict(exp=r[0], th=r[1], pmin=r[2], pmax=r[3], n=r[4]) for r in cur.fetchall()]


def _load(cur, experiment, theta):
    cur.execute(
        "SELECT momentum, intensity, total_error FROM muon_data "
        "WHERE experiment=? AND theta_center=? AND intensity IS NOT NULL "
        "ORDER BY momentum",
        (experiment, theta),
    )
    rows = cur.fetchall()
    p = np.array([r[0] for r in rows], float)
    I = np.array([r[1] for r in rows], float)
    e = np.array([(r[2] if r[2] is not None else 0.0) for r in rows], float)
    return p, I, e


# ---------------------------------------------------------------------------
# OVERLAP DETECTION
# ---------------------------------------------------------------------------
def detect_comparisons(cur, angle_tol=ANGLE_TOL_DEG):
    """Return one best-matched (expA, thetaA, expB, thetaB) per experiment pair
    that overlaps in angle and momentum."""
    segs = _segments(cur)
    byexp = defaultdict(list)
    for s in segs:
        byexp[s["exp"]].append(s)
    exps = sorted(byexp)

    out = []
    for i in range(len(exps)):
        for j in range(i + 1, len(exps)):
            A, B = exps[i], exps[j]
            best = None
            for a in byexp[A]:
                for b in byexp[B]:
                    dth = abs(a["th"] - b["th"])
                    if dth > angle_tol:
                        continue
                    lo = max(a["pmin"], b["pmin"])
                    hi = min(a["pmax"], b["pmax"])
                    if hi <= lo:
                        continue
                    span = np.log10(hi) - np.log10(lo)
                    score = span * 2 - dth * 0.5 + min(a["n"], b["n"]) * 0.05
                    if best is None or score > best[0]:
                        best = (score, a["th"], b["th"])
            if best:
                out.append((A, best[1], B, best[2]))
    return out


# ---------------------------------------------------------------------------
# COMPARISON
# ---------------------------------------------------------------------------
def _log_interp(p_eval, p_src, I_src, e_src):
    lp, lI = np.log10(p_src), np.log10(I_src)
    rel = np.divide(e_src, I_src, out=np.zeros_like(e_src), where=I_src > 0)
    le = np.log10(p_eval)
    valid = (le >= lp.min()) & (le <= lp.max())
    I_out = np.full_like(p_eval, np.nan, float)
    e_out = np.full_like(p_eval, np.nan, float)
    I_out[valid] = 10.0 ** np.interp(le[valid], lp, lI)
    e_out[valid] = I_out[valid] * np.interp(le[valid], lp, rel)
    return I_out, e_out, valid


def compare(cur, ref, other, label=None):
    """ref, other = (experiment, theta).
    Ratio is reported as other / ref."""
    p_r, I_r, e_r = _load(cur, *ref)
    p_o, I_o, e_o = _load(cur, *other)
    if len(p_r) == 0 or len(p_o) == 0:
        return None
    lo = max(p_r.min(), p_o.min())
    hi = min(p_r.max(), p_o.max())
    if hi <= lo:
        return None
    in_r = (p_r >= lo) & (p_r <= hi)
    in_o = (p_o >= lo) & (p_o <= hi)
    if in_r.sum() == 0 or in_o.sum() == 0:
        return None

    if in_r.sum() <= in_o.sum():
        p_eval = p_r[in_r]
        I_ref_e, e_ref_e = I_r[in_r], e_r[in_r]
        I_oth_e, e_oth_e, valid = _log_interp(p_eval, p_o, I_o, e_o)
    else:
        p_eval = p_o[in_o]
        I_oth_e, e_oth_e = I_o[in_o], e_o[in_o]
        I_ref_e, e_ref_e, valid = _log_interp(p_eval, p_r, I_r, e_r)

    p_eval = p_eval[valid]
    I_ref_e, e_ref_e = I_ref_e[valid], e_ref_e[valid]
    I_oth_e, e_oth_e = I_oth_e[valid], e_oth_e[valid]
    if len(p_eval) < MIN_POINTS:
        return None

    sigma2 = e_ref_e**2 + e_oth_e**2
    good = sigma2 > 0
    if good.sum() < MIN_POINTS:
        return None
    chi2 = float(np.sum((I_ref_e[good] - I_oth_e[good]) ** 2 / sigma2[good]))
    ndf = int(good.sum())
    ratio = I_oth_e / I_ref_e
    ratio_err = np.sqrt((e_oth_e / I_ref_e) ** 2 + (I_oth_e * e_ref_e / I_ref_e**2) ** 2)

    return {
        "label": label or f"{other[0]} vs {ref[0]}",
        "ref": ref, "other": other,
        "theta_ref": ref[1], "theta_other": other[1],
        "dtheta": abs(ref[1] - other[1]),
        "window": (lo, hi),
        "n": ndf,
        "chi2": chi2,
        "chi2_ndf": chi2 / ndf,
        "p": p_eval, "ratio": ratio, "ratio_err": ratio_err,
        "mean_ratio": float(np.mean(ratio)),
    }


def run_all(db=DB):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    results = []
    for A, thA, B, thB in detect_comparisons(cur):
        label = f"{B} ({thB:g}\u00b0) vs {A} ({thA:g}\u00b0)"
        r = compare(cur, (A, thA), (B, thB), label=label)
        if r:
            results.append(r)
    conn.close()
    results.sort(key=lambda r: (r["theta_ref"], r["label"]))
    return results


# ---------------------------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------------------------
def print_summary(results):
    print(f"{'comparison':40} {'th_ref':>6} {'th_oth':>6} {'dth':>4} "
          f"{'window (GeV/c)':>20} {'N':>3} {'chi2/ndf':>9} {'mean ratio':>11}")
    print("-" * 108)
    for r in results:
        lo, hi = r["window"]
        print(f"{r['label']:40} {r['theta_ref']:>6.1f} {r['theta_other']:>6.1f} "
              f"{r['dtheta']:>4.1f} {lo:>8.1f}-{hi:<9.1f} {r['n']:>3} "
              f"{r['chi2_ndf']:>9.2f} {r['mean_ratio']:>11.3f}")


def write_csv(results, path="overlap_summary.csv"):
    with open(path, "w", encoding="utf-8-sig") as f:
        f.write("comparison,ref_exp,ref_theta,other_exp,other_theta,dtheta,"
                "p_min,p_max,n_points,chi2,chi2_ndf,mean_ratio\n")
        for r in results:
            lo, hi = r["window"]
            f.write(f"{r['label']},{r['ref'][0]},{r['ref'][1]:g},{r['other'][0]},"
                    f"{r['other'][1]:g},{r['dtheta']:g},{lo:g},{hi:g},{r['n']},"
                    f"{r['chi2']:.4g},{r['chi2_ndf']:.4g},{r['mean_ratio']:.4g}\n")
    print(f"wrote {path}")


def plot(results, png="overlap_ratios.png", svg="overlap_ratios.svg"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n = len(results)
    ncol = 3
    nrow = (n + ncol - 1) // ncol
    fig, axes = plt.subplots(nrow, ncol, figsize=(4.3 * ncol, 2.9 * nrow))
    axes = np.atleast_1d(axes).flatten()

    for ax, r in zip(axes, results):
        p, ratio, err = r["p"], r["ratio"], r["ratio_err"]
        mr, sd = r["mean_ratio"], float(np.std(r["ratio"]))
        ax.axhline(1.0, color="#888", lw=1, ls="--", zorder=1)
        ax.axhspan(mr - sd, mr + sd, color="#0072B2", alpha=0.08, zorder=0)
        ax.axhline(mr, color="#0072B2", lw=0.8, alpha=0.5, zorder=1)
        ax.errorbar(p, ratio, yerr=err, fmt="o", ms=4, capsize=2.5,
                    color="#0072B2", ecolor="#0072B2", elinewidth=0.8,
                    markerfacecolor="none", zorder=3)
        ax.set_xscale("log")
        ax.set_title(r["label"], fontsize=9.5)
        ax.set_ylabel("ratio (other / ref)", fontsize=8)
        ax.set_xlabel("Momentum [GeV/c]", fontsize=8)
        ax.grid(True, which="both", alpha=0.25)
        ax.tick_params(labelsize=7.5)
        lo, hi = ax.get_ylim()
        ax.set_ylim(lo, hi + 0.28 * (hi - lo))   # headroom for the annotation
        dtxt = f", d\u03b8={r['dtheta']:.1f}\u00b0" if r["dtheta"] > 0 else ""
        txt = f"$\\chi^2$/ndf = {r['chi2_ndf']:.1f}  (N={r['n']}{dtxt})\nmean = {mr:.2f}"
        ax.text(0.97, 0.96, txt, transform=ax.transAxes, fontsize=7.8,
                va="top", ha="right",
                bbox=dict(facecolor="white", edgecolor="#ccc", boxstyle="round,pad=0.3"))

    for ax in axes[n:]:
        ax.set_visible(False)

    fig.suptitle("Cross-dataset comparison in all overlap regions",
                 fontsize=13, y=0.997)
    fig.tight_layout(rect=[0, 0, 1, 0.99])
    fig.savefig(png, dpi=140)
    fig.savefig(svg)
    plt.close(fig)
    print(f"wrote {png} and {svg}")


if __name__ == "__main__":
    res = run_all()
    print_summary(res)
    write_csv(res)