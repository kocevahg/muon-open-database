"""
(Achard, P., et al. [L3 Collaboration]. "Measurement of the Atmospheric Muon
Spectrum from 20 to 3000 GeV." Physics Letters B 598 (2004) 15-32.
arXiv:hep-ex/0408114, CERN-PH-EP-2004-023.)

SOURCE SECTIONS USED (page numbers refer to the arXiv:hep-ex/0408114
preprint, which paginates identically to the CERN-PH-EP-2004-023 report):
----------------------------------------------------------------------
  - Tables 2-9, p.20-23    : measured muon flux (as Phi * <p>^3) and charge
                              ratio in eight cos(theta) zenith bins; mean
                              momentum, statistical and systematic percentage
                              uncertainty, and bin-to-bin statistical
                              correlation coefficient for each momentum
                              interval. Only the flux (Phi) columns are used.
  - "Results", p.19-20      : definition of <p> (Eq. 12), statement that
                              fluxes are NOT altitude/atmosphere-corrected,
                              and the L3+C altitude/location (450 m a.s.l.,
                              46.25 N, 6.02 E).
  - "Total uncertainty",
    p.18                    : statement that individual stat/syst
                              contributions are added in quadrature, and that
                              the minimal total flux uncertainty is 2.3% at
                              150 GeV (vertical).
  - Table 1, p.19           : correlation coefficients of the *systematic*
                              uncertainties between different zenith bins
                              (documented for completeness; not used
                              point-by-point in transform()).

Tables 2-9, p.20-23
----------------------------------------------------------------------
Each of the eight tables covers one cos(theta) bin (edges given in the
table caption) and contains, per momentum interval:

    - momentum interval edges [GeV] (as printed),
    - mean momentum <p> [GeV],
    - Phi * <p>^3 [GeV^2 cm^-2 s^-1 sr^-1],
    - statistical uncertainty on Phi [%],
    - statistical correlation coefficient rho_Phi with the neighboring
      momentum bin (not used downstream; see caveat in _make_notes),
    - systematic uncertainty on Phi [%].

"""

from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# RAW_TABLES
# ---------------------------------------------------------------------------
# Tables 2-9 (Achard et al. 2004, p. 20-23).
# Units: Phi * <p>^3 in GeV^2 cm^-2 s^-1 sr^-1; momenta in GeV.
#
# Each bin carries:
#   - cos_theta_min / cos_theta_max: the bin edges as printed in the table
#     caption
#   - source_table: which of Tables 2-9 this bin corresponds to.
#   - rows: list of (p_min, p_max, p_mean, phi_p3, stat_pct, sys_pct)
#     tuples, in the same order/units as printed, one row per momentum
#     interval in the table.

RAW_TABLES = [
    {
        "cos_theta_min": 0.975,
        "cos_theta_max": 1.000,
        "source_table": "Achard et al. 2004, Table 2",
        "rows": [
            (20.0, 27.0, 23.18, 0.217, 0.4, 4.4),
            (27.0, 34.5, 30.47, 0.231, 0.3, 3.7),
            (34.5, 42.0, 38.02, 0.244, 0.4, 3.3),
            (42.0, 50.0, 45.78, 0.252, 0.5, 3.0),
            (50.0, 58.5, 54.04, 0.257, 0.5, 2.8),
            (58.5, 68.5, 63.25, 0.261, 0.5, 2.6),
            (68.5, 81.5, 74.63, 0.266, 0.5, 2.5),
            (81.5, 100.0, 90.13, 0.262, 0.6, 2.4),
            (100.0, 132.0, 114.5, 0.264, 0.5, 2.3),
            (132.0, 200.0, 161.3, 0.250, 0.5, 2.2),
            (200.0, 300.0, 243.0, 0.233, 0.8, 2.2),
            (300.0, 500.0, 381.9, 0.203, 1.2, 2.4),
            (500.0, 1000.0, 687.2, 0.151, 2.3, 3.5),
            (1000.0, 3000.0, 1599.0, 0.087, 6.0, 8.4),
        ],
    },
    {

        "cos_theta_min": 0.938,
        "cos_theta_max": 0.975,
        "source_table": "Achard et al. 2004, Table 3",
        "rows": [
            (27.0, 34.5, 30.47, 0.237, 0.3, 4.5),
            (34.5, 42.0, 38.02, 0.254, 0.4, 4.1),
            (42.0, 50.0, 45.78, 0.259, 0.5, 3.8),
            (50.0, 58.5, 54.04, 0.264, 0.5, 3.7),
            (58.5, 68.5, 63.25, 0.266, 0.6, 3.5),
            (68.5, 81.5, 74.63, 0.270, 0.6, 3.4),
            (81.5, 100.0, 90.13, 0.271, 0.6, 3.3),
            (100.0, 132.0, 114.5, 0.270, 0.5, 3.2),
            (132.0, 200.0, 161.3, 0.262, 0.6, 3.1),
            (200.0, 300.0, 243.0, 0.241, 0.9, 3.1),
            (300.0, 500.0, 382.1, 0.219, 1.3, 3.2),
            (500.0, 1000.0, 687.8, 0.165, 2.4, 4.2),
            (1000.0, 3000.0, 1604.0, 0.093, 6.5, 9.2),
        ],
    },
    {
        "cos_theta_min": 0.900,
        "cos_theta_max": 0.938,
        "source_table": "Achard et al. 2004, Table 4",
        "rows": [
            (27.0, 34.5, 30.47, 0.245, 0.4, 4.3),
            (34.5, 42.0, 38.02, 0.257, 0.4, 3.9),
            (42.0, 50.0, 45.78, 0.265, 0.5, 3.6),
            (50.0, 58.5, 54.04, 0.273, 0.5, 3.4),
            (58.5, 68.5, 63.25, 0.279, 0.5, 3.2),
            (68.5, 81.5, 74.64, 0.282, 0.5, 3.1),
            (81.5, 100.0, 90.14, 0.283, 0.5, 3.0),
            (100.0, 132.0, 114.5, 0.284, 0.5, 2.9),
            (132.0, 200.0, 161.3, 0.274, 0.5, 2.8),
            (200.0, 300.0, 243.0, 0.255, 0.7, 2.8),
            (300.0, 500.0, 382.0, 0.220, 1.1, 2.9),
            (500.0, 1000.0, 687.3, 0.172, 1.9, 4.2),
            (1000.0, 3000.0, 1599.0, 0.091, 5.7, 11.3),
        ],
    },
    {
        "cos_theta_min": 0.825,
        "cos_theta_max": 0.900,
        "source_table": "Achard et al. 2004, Table 5",
        "rows": [
            (34.5, 42.0, 38.02, 0.263, 0.4, 3.9),
            (42.0, 50.0, 45.78, 0.269, 0.5, 3.5),
            (50.0, 58.5, 54.04, 0.274, 0.5, 3.3),
            (58.5, 68.5, 63.25, 0.284, 0.6, 3.1),
            (68.5, 81.5, 74.64, 0.280, 0.6, 2.9),
            (81.5, 100.0, 90.14, 0.288, 0.6, 2.8),
            (100.0, 132.0, 114.5, 0.290, 0.5, 2.6),
            (132.0, 200.0, 161.3, 0.279, 0.6, 2.6),
            (200.0, 300.0, 243.1, 0.264, 0.8, 2.5),
            (300.0, 500.0, 382.1, 0.232, 1.3, 2.6),
            (500.0, 1000.0, 686.8, 0.167, 2.5, 4.2),
            (1000.0, 3000.0, 1587.0, 0.087, 7.9, 10.4),
        ],
    },
    {
        "cos_theta_min": 0.750,
        "cos_theta_max": 0.825,
        "source_table": "Achard et al. 2004, Table 6",
        "rows": [
            (34.5, 42.0, 38.02, 0.255, 0.5, 4.6),
            (42.0, 50.0, 45.78, 0.265, 0.5, 4.2),
            (50.0, 58.5, 54.04, 0.275, 0.6, 3.9),
            (58.5, 68.5, 63.25, 0.283, 0.6, 3.7),
            (68.5, 81.5, 74.64, 0.283, 0.6, 3.6),
            (81.5, 100.0, 90.14, 0.290, 0.6, 3.4),
            (100.0, 132.0, 114.6, 0.290, 0.5, 3.3),
            (132.0, 200.0, 161.3, 0.292, 0.5, 3.2),
            (200.0, 300.0, 243.1, 0.271, 0.8, 3.2),
            (300.0, 500.0, 382.2, 0.244, 1.2, 3.3),
            (500.0, 1000.0, 687.5, 0.191, 2.2, 4.0),
            (1000.0, 3000.0, 1594.0, 0.087, 7.6, 8.4),
        ],
    },
    {
        "cos_theta_min": 0.675,
        "cos_theta_max": 0.750,
        "source_table": "Achard et al. 2004, Table 7",
        "rows": [
            (34.5, 42.0, 38.02, 0.253, 0.6, 4.6),
            (42.0, 50.0, 45.78, 0.265, 0.6, 4.1),
            (50.0, 58.5, 54.04, 0.275, 0.5, 3.7),
            (58.5, 68.5, 63.25, 0.281, 0.6, 3.4),
            (68.5, 81.5, 74.64, 0.291, 0.6, 3.1),
            (81.5, 100.0, 90.15, 0.293, 0.6, 2.9),
            (100.0, 132.0, 114.6, 0.298, 0.5, 2.7),
            (132.0, 200.0, 161.4, 0.298, 0.5, 2.5),
            (200.0, 300.0, 243.2, 0.285, 0.7, 2.4),
            (300.0, 500.0, 382.3, 0.256, 1.1, 2.6),
            (500.0, 1000.0, 688.2, 0.203, 2.0, 3.5),
            (1000.0, 3000.0, 1601.0, 0.120, 5.3, 7.8),
        ],
    },
    {
        "cos_theta_min": 0.600,
        "cos_theta_max": 0.675,
        "source_table": "Achard et al. 2004, Table 8",
        "rows": [
            (42.0, 50.0, 45.79, 0.256, 0.6, 4.7),
            (50.0, 58.5, 54.05, 0.269, 0.6, 4.3),
            (58.5, 68.5, 63.26, 0.282, 0.6, 4.0),
            (68.5, 81.5, 74.65, 0.290, 0.6, 3.7),
            (81.5, 100.0, 90.16, 0.299, 0.6, 3.5),
            (100.0, 132.0, 114.6, 0.307, 0.5, 3.3),
            (132.0, 200.0, 161.4, 0.312, 0.5, 3.1),
            (200.0, 300.0, 243.2, 0.300, 0.8, 3.0),
            (300.0, 500.0, 382.5, 0.277, 1.2, 3.1),
            (500.0, 1000.0, 688.5, 0.231, 2.0, 3.8),
            (1000.0, 3000.0, 1602.0, 0.117, 6.3, 8.7),
        ],
    },
    {
        "cos_theta_min": 0.525,
        "cos_theta_max": 0.600,
        "source_table": "Achard et al. 2004, Table 9",
        "rows": [
            (42.0, 50.0, 45.79, 0.256, 1.4, 5.6),
            (50.0, 58.5, 54.05, 0.255, 0.9, 5.3),
            (58.5, 68.5, 63.26, 0.273, 0.8, 5.1),
            (68.5, 81.5, 74.65, 0.284, 0.8, 4.9),
            (81.5, 100.0, 90.16, 0.294, 0.7, 4.7),
            (100.0, 132.0, 114.6, 0.305, 0.5, 4.6),
            (132.0, 200.0, 161.5, 0.316, 0.6, 4.5),
            (200.0, 300.0, 243.4, 0.315, 0.8, 4.4),
            (300.0, 500.0, 382.7, 0.297, 1.3, 4.4),
            (500.0, 1000.0, 689.3, 0.243, 2.3, 4.8),
            (1000.0, 3000.0, 1604.0, 0.153, 5.9, 9.4),
        ],
    },
]

# Reference metadata shared by every emitted row.
_EXPERIMENT = "L3+C"
_REFERENCE = (
    "Achard, P. et al. (L3 Collaboration) 2004, "
    "\"Measurement of the Atmospheric Muon Spectrum from 20 to 3000 GeV,\" "
    "Phys. Lett. B 598, 15-32, arXiv:hep-ex/0408114. "
    "(The manuscript's short proceedings citation, Le Coultre 2005, "
    "Nucl. Phys. B Proc. Suppl. 145, 136-140, introduces this experiment "
    "but contains only plots, not the numeric tables used here.)"
)
_ALTITUDE_M = 450  # L3+C detector hall, CERN; 450 m a.s.l., 46.25 N, 6.02 E


def _cos_edges_to_theta_deg(cos_min: float, cos_max: float):
    """theta = arccos(cos_theta) is DECREASING in cos_theta, so cos_max
    maps to theta_min and cos_min maps to theta_max. theta_center is the
    arithmetic midpoint of the resulting degree edges."""
    theta_min_deg = math.degrees(math.acos(cos_max))
    theta_max_deg = math.degrees(math.acos(cos_min))
    theta_center_deg = 0.5 * (theta_min_deg + theta_max_deg)
    return theta_min_deg, theta_max_deg, theta_center_deg


def _make_notes(cos_theta_min: float, cos_theta_max: float) -> str:
    """
    Build the per-row provenance/caveat note.

    Every row gets:
      (1) the non-altitude-corrected-flux caveat (Achard et al. deliberately
          do not correct for L3+C's 450 m altitude or the atmospheric
          profile, to avoid extra theoretical uncertainty),
      (2) the bin-to-bin statistical correlation caveat (rho_Phi is printed
          per row in the source but not carried into this row-level schema).
    """
    return (
        "Flux is Phi = (Phi*<p>^3)/<p>^3, NOT corrected for L3+C's 450 m "
        "altitude or atmospheric profile (Achard et al. 2004 state this is "
        "deliberate, 'to avoid additional theoretical uncertainties', "
        "p.19-20); compare against sea-level fluxes only after applying an "
        "altitude/atmosphere model such as the paper's own TARGET-based "
        "extrapolation. Statistical uncertainties between neighboring "
        "momentum bins within this cos(theta) bin ({:.3f}-{:.3f}) are "
        "correlated (rho_Phi, printed per-row in Table {} but not stored "
        "in this row-level schema); treat stat_error as independent only "
        "for a quick look, not for a rigorous joint fit.".format(
            cos_theta_min, cos_theta_max,
            [t["source_table"] for t in RAW_TABLES
             if t["cos_theta_min"] == cos_theta_min][0].rsplit(" ", 1)[-1],
        )
    )


def transform():
    """
    Turn RAW_TABLES into a flat list of row dicts ready for loading into
    the unified database.

    MATH performed:
      1. intensity = (Phi * <p>^3) / <p>^3
      2. stat_error = intensity * stat_pct/100, sys_error = intensity *
         sys_pct/100 -- kept seperate

    Returns
    -------
    list[dict]
        One dict per (zenith bin, momentum point), with keys:
        experiment, reference, theta_center, theta_min, theta_max, azimuth,
        altitude_m, momentum, momentum_min, momentum_max, intensity,
        stat_error, sys_error, error_note, source_table, notes.
    """
    rows_out = []

    for bin_data in RAW_TABLES:
        cos_min = bin_data["cos_theta_min"]
        cos_max = bin_data["cos_theta_max"]
        theta_min, theta_max, theta_center = _cos_edges_to_theta_deg(
            cos_min, cos_max
        )
        notes = _make_notes(cos_min, cos_max)

        for p_min, p_max, p_mean, phi_p3, stat_pct, sys_pct in bin_data["rows"]:
            intensity = phi_p3 / (p_mean ** 3)
            stat_error = intensity * (stat_pct / 100.0)
            sys_error = intensity * (sys_pct / 100.0)

            rows_out.append(
                {
                    "experiment": _EXPERIMENT,
                    "reference": _REFERENCE,
                    "theta_center": round(theta_center, 2),
                    "theta_min": round(theta_min, 2),
                    "theta_max": round(theta_max, 2),
                    "azimuth": None,
                    "altitude_m": _ALTITUDE_M,
                    "momentum": p_mean,
                    "momentum_min": p_min,
                    "momentum_max": p_max,
                    "intensity": intensity,
                    "stat_error": stat_error,
                    "sys_error": sys_error,
                    "error_note": (
                        "intensity = (Phi*<p>^3)/<p>^3 from {}. stat_error "
                        "= intensity * {:.1f}%, sys_error = intensity * "
                        "{:.1f}%, kept independent (not summed). Both "
                        "percentages transcribed directly from the source "
                        "table for this point.".format(
                            bin_data["source_table"], stat_pct, sys_pct
                        )
                    ),
                    "source_table": bin_data["source_table"],
                    "notes": notes,
                }
            )

    return rows_out


def print_rawdata():
    # Print the raw Tables 2-9 values exactly as transcribed.
    print("RAW TABLES 2-9")

    for bin_data in RAW_TABLES:
        print(
            f"\ncos(theta) bin {bin_data['cos_theta_min']}-"
            f"{bin_data['cos_theta_max']} ({bin_data['source_table']})"
        )

        for p_min, p_max, p_mean, phi_p3, stat_pct, sys_pct in bin_data["rows"]:
            print(
                f"  p=[{p_min:7.1f},{p_max:7.1f}]  <p>={p_mean:7.2f} GeV/c   "
                f"Phi*p3={phi_p3:.3f}   stat={stat_pct:.1f}%   sys={sys_pct:.1f}%"
            )


def print_transformed():
    # Print the transformed rows returned by transform().
    rows = transform()

    for row in rows:
        print(
            f"theta={row['theta_center']:5.1f}  "
            f"p={row['momentum']:7.2f}  "
            f"I={row['intensity']:.4e}  "
            f"stat={row['stat_error']:.2e}  "
            f"sys={row['sys_error']:.2e}"
        )


if __name__ == "__main__":
    all_rows = transform()

    print(f"L3+C transform() produced {len(all_rows)} row(s) across "
          f"{len(RAW_TABLES)} zenith bins.")


    #print_rawdata()
    #print_transformed()