"""
(De Pascale, M. P., Morselli, A., Picozza, P., Golden, R. L., Grimani, C.,
Kimbell, B. L., Stephens, S. A., Stochaj, S. J., Webber, W. R., Basini, G.,
Bongiorno, F., Brancaccio, F. M., Ricci, M., Ormes, J. F., Seo, E. S.,
Streitmatter, R. E., Papini, P., Spillantini, P., Brunetti, M. T., Codino,
A., Menichelli, M., and Salvatori, I.
"Absolute Spectrum and Charge Ratio of Cosmic Ray Muons in the Energy Region
From 0.2 GeV to 100 GeV at 600 m Above Sea Level,"
J. Geophys. Res. 98(A3) (1993) 3501-3508.)

SOURCE SECTIONS USED
----------------------------------------------------------------------
  - Table 3, p.3505         : differential muon flux as a function of
                              rigidity (momentum), including separate
                              μ− and μ+ intensities, statistical
                              uncertainties, and event counts.
  - Sec. 3.3, p.3504        : approximately 5% systematic uncertainty in
                              the absolute flux normalization.
  - Sec. 4.1, p.3505        : median momentum values used to represent
                              each momentum interval.
  - Introduction, p.3501    : experimental site (Prince Albert,
                              Saskatchewan, Canada) and altitude
                              (600 m above sea level).

RAW TABLE
----------------------------------------------------------------------
RAW_TABLE reproduces Table 3 exactly as printed.

The source reports separate μ− and μ+ differential fluxes together with
their statistical uncertainties and event counts. No arithmetic or unit
conversion is performed in the raw transcription.

TRANSFORMATION
----------------------------------------------------------------------
transform() converts the published fluxes from

    m^-2 sr^-1 s^-1 (GeV/c)^-1

to the database units

    cm^-2 sr^-1 s^-1 (GeV/c)^-1

by multiplying by 1e-4.

The source tabulates rigidity (GV/c). Since muons have |Z| = 1, rigidity
is numerically equal to momentum (GeV/c), so the published median
rigidity values are used directly as the momentum values.

The statistical uncertainties for μ− and μ+ are converted separately,
then combined in quadrature for the summed intensity. The 5% systematic
uncertainty reported by the authors is propagated separately as the
absolute normalization uncertainty.

ALTITUDE
----------------------------------------------------------------------
The source reports an experimental altitude of 600 m above sea level.
"""

import math

# ---------------------------------------------------------------------------
# 1. RAW SITE / EPOCH METADATA (p. 3501, Introduction)
# ---------------------------------------------------------------------------
SITE_METADATA = {
    "site": "Prince Albert, Saskatchewan, Canada",
    "latitude_deg": 53.0,          # "latitude 53 N", p. 3501
    "longitude_deg": -106.0,       # "longitude 106 W", p. 3501 (negative = West)
    "altitude_m": 600,             # "600 m above sea level", p. 3501 title/abstract.
    "run_date": "1989-08-30",      # "a ground run on August 30, 1989", p. 3501.
    "run_duration_s": 61920,       # "recorded over a period of 61,920 s", p. 3502.
    "n_events_selected": 29088,    # "A total of 29,088 events passed...", p. 3502.
}

# ---------------------------------------------------------------------------
# 2. RAW SYSTEMATIC UNCERTAINTY (p. 3504 and p. 3505)
# ---------------------------------------------------------------------------
RAW_SYSTEMATIC = {
    "value_fraction": 0.05,  # "a possible systematic uncertainty of about 5%"
                              # (p. 3504, end of Sec. 3.3) and "the quoted possible
                              # systematic uncertainty of 5% in determining the
                              # absolute flux" (p. 3505, Sec. 4.2).
    "applies_to": (
        "Overall absolute normalization / scale of the flux measurement, "
        "arising from uncertainty in the combined detector efficiencies "
        "(spectrometer, calorimeter, scintillator, trigger, tape-reading, "
        "live-time) used to compute the instrument's collecting power. "
        "It is explicitly described by the authors as separate from the "
        "per-bin statistical percent errors already listed in Table 3."
    ),
    "source": "De Pascale et al. 1993, JGR 98, p. 3504 (Sec. 3.3) and p. 3505 (Sec. 4.2)",
}

# ---------------------------------------------------------------------------
# 3. RAW DATA TABLE -- Table 3, "Differential Flux of Muons", p. 3505
# ---------------------------------------------------------------------------
RAW_TABLE = [
    # (p_min_GV, p_max_GV, p_median_GV,
    #  n_mu_minus, n_mu_plus,
    #  flux_mu_minus, pct_err_mu_minus,
    #  flux_mu_plus,  pct_err_mu_plus)
    (0.247, 0.321, 0.283, 133, 164, 0.1595e+2, 11.0, 0.2390e+2, 10.0),
    (0.321, 0.393, 0.356, 231, 188, 0.2064e+2, 7.9, 0.2013e+2, 8.8),
    (0.393, 0.463, 0.428, 232, 260, 0.1759e+2, 7.4, 0.2279e+2, 7.1),
    (0.463, 0.564, 0.513, 418, 439, 0.1788e+2, 5.9, 0.2128e+2, 5.8),
    (0.564, 0.633, 0.598, 299, 326, 0.1660e+2, 6.5, 0.2023e+2, 6.3),
    (0.633, 0.722, 0.677, 418, 442, 0.1673e+2, 5.8, 0.1961e+2, 5.6),
    (0.722, 0.841, 0.780, 577, 637, 0.1649e+2, 5.1, 0.1939e+2, 4.8),
    (0.841, 1.008, 0.922, 698, 904, 0.1365e+2, 4.7, 0.1814e+2, 4.1),
    (1.008, 1.198, 1.101, 795, 794, 0.1316e+2, 4.5, 0.1609e+2, 4.0),
    (1.198, 1.478, 1.334, 992, 1240, 0.1094e+2, 4.1, 0.1328e+2, 3.6),
    (1.478, 1.931, 1.694, 1313, 1674, 0.8756e+1, 3.3, 0.1093e+2, 3.2),
    (1.931, 2.508, 2.205, 1299, 1512, 0.6789e+1, 3.6, 0.7705e+1, 3.3),
    (2.508, 3.579, 3.004, 1514, 1976, 0.4244e+1, 3.3, 0.5404e+1, 2.9),
    (3.579, 5.008, 4.238, 1252, 1535, 0.2634e+1, 3.5, 0.3145e+1, 3.1),
    (5.008, 8.341, 6.456, 1408, 1700, 0.1274e+1, 3.3, 0.1506e+1, 3.1),
    (8.341, 12.51, 10.19, 696, 839, 0.5025e+0, 4.3, 0.5983e+0, 3.9),
    (12.51, 16.68, 14.42, 290, 349, 0.2124e+0, 6.2, 0.2523e+0, 5.7),
    (16.68, 25.01, 20.36, 245, 349, 0.8653e-1, 6.7, 0.1246e+0, 5.7),
    (25.01, 33.34, 28.80, 105, 134, 0.3788e-1, 9.9, 0.4709e-1, 8.8),
    (33.34, 50.01, 40.64, 87, 87, 0.1389e-1, 11.5, 0.1430e-1, 11.3),
    (50.01, 100.01, 70.16, 54, 101, 0.2423e-2, 15.8, 0.5176e-2, 10.7),
]

RAW_TABLE_COLUMNS = (
    "p_min_GV", "p_max_GV", "p_median_GV",
    "n_mu_minus", "n_mu_plus",
    "flux_mu_minus_per_m2_s_sr_GVc", "pct_err_mu_minus",
    "flux_mu_plus_per_m2_s_sr_GVc", "pct_err_mu_plus",
)

# Unit conversion factor: m^-2 -> cm^-2 (1 m^2 = 1e4 cm^2).
M2_TO_CM2_FACTOR = 1e-4


def transform():
    """
    Convert RAW_TABLE into flat database rows.
    Applies unit conversion, combines μ+ and μ− intensities.
    """
    rows = []

    for entry in RAW_TABLE:
        (p_min, p_max, p_median,
         n_minus, n_plus,
         flux_minus_raw, pct_err_minus,
         flux_plus_raw, pct_err_plus) = entry

        # Raw table units: muons / (m^2 s sr GeV/c)
        # for singly-charged muons (rigidity == momentum numerically).
        mu_minus_intensity = flux_minus_raw * M2_TO_CM2_FACTOR
        mu_plus_intensity = flux_plus_raw * M2_TO_CM2_FACTOR

        # Convert percent error to an absolute
        mu_minus_stat_error = mu_minus_intensity * (pct_err_minus / 100.0)
        mu_plus_stat_error = mu_plus_intensity * (pct_err_plus / 100.0)

        # Sum the two charges to get the total (unsigned) muon
        # intensity, as required by the unified database
        intensity = mu_plus_intensity + mu_minus_intensity

        # Combine the two charges' statistical errors in
        # quadrature
        stat_error = math.sqrt(mu_plus_stat_error ** 2 + mu_minus_stat_error ** 2)

        # Absolute systematic error, applied to the summed intensity
        sys_error = intensity * RAW_SYSTEMATIC["value_fraction"]

        row = {
            "experiment": "De Pascale",
            "reference": "De Pascale et al. 1993",
            "theta_center": 0,
            "theta_min": 0,
            "theta_max": 0,
            "azimuth": None,
            "altitude_m": 600,
            "momentum": p_median,
            "momentum_min": p_min,
            "momentum_max": p_max,
            # Total (mu+ + mu-) intensity, converted to cm^-2 s^-1 sr^-1 (GeV/c)^-1
            "intensity": intensity,
            "stat_error": stat_error,
            "sys_error": sys_error,
            "error_note": (
                "stat_error = sqrt((mu+_intensity * pct_err_mu+/100)^2 + "
                "(mu-_intensity * pct_err_mu-/100)^2), combining the two "
                "charges' independent statistical percent errors from Table 3 "
                "in quadrature, converted to absolute units. sys_error = "
                "intensity * 0.05"
            ),
            "source_table": "Table 3, De Pascale et al. 1993, JGR 98, p. 3505",
            "notes": (
                f"Site: {SITE_METADATA['site']} "
                f"(lat {SITE_METADATA['latitude_deg']} deg, "
                f"lon {SITE_METADATA['longitude_deg']} deg), "
                f"altitude {SITE_METADATA['altitude_m']} m ASL. "
                f"Ground run date: {SITE_METADATA['run_date']} "
                f"(single-day run, duration {SITE_METADATA['run_duration_s']} s, "
                f"{SITE_METADATA['n_events_selected']} events selected). "
            ),
            #Charge-resolved fields
            "mu_plus_intensity": mu_plus_intensity,
            "mu_plus_stat_error": mu_plus_stat_error,
            "mu_plus_pct_error_raw": pct_err_plus,
            "n_mu_plus_observed": n_plus,
            "mu_minus_intensity": mu_minus_intensity,
            "mu_minus_stat_error": mu_minus_stat_error,
            "mu_minus_pct_error_raw": pct_err_minus,
            "n_mu_minus_observed": n_minus,
        }
        rows.append(row)

    return rows

def print_raw_table():
    """
    Print RAW_TABLE exactly as transcribed from Table 3 (p.3505).

    No unit conversion, summing, or error propagation is applied.
    """

    print("De Pascale et al. 1993 -- RAW TABLE (Table 3)")
    print("=" * 100)
    print()

    print(
        f"{'p_min':>8} "
        f"{'p_max':>8} "
        f"{'p_med':>8} "
        f"{'N_mu-':>8} "
        f"{'N_mu+':>8} "
        f"{'Flux_mu-':>15} "
        f"{'Err_mu- %':>10} "
        f"{'Flux_mu+':>15} "
        f"{'Err_mu+ %':>10}"
    )

    print("-" * 100)

    for row in RAW_TABLE:
        (
            p_min, p_max, p_med,
            n_minus, n_plus,
            flux_minus, err_minus,
            flux_plus, err_plus,
        ) = row

        print(
            f"{p_min:8.3f} "
            f"{p_max:8.3f} "
            f"{p_med:8.3f} "
            f"{n_minus:8d} "
            f"{n_plus:8d} "
            f"{flux_minus:15.4e} "
            f"{err_minus:10.1f} "
            f"{flux_plus:15.4e} "
            f"{err_plus:10.1f}"
        )


def print_transformed_data():
    """
    Print database-ready rows after transform().

    Shows summed mu+ + mu- intensity,
    statistical uncertainty,
    and systematic uncertainty.
    """

    rows = transform()

    print()
    print("De Pascale et al. 1993 -- TRANSFORMED DATA")
    print("=" * 100)

    print(f"Row count: {len(rows)}")
    print()

    print(
        f"{'p':>8} "
        f"{'range':>18} "
        f"{'Intensity':>15} "
        f"{'Stat.err':>15} "
        f"{'Sys.err':>15}"
    )

    print("-" * 100)

    for r in rows:
        print(
            f"{r['momentum']:8.3f} "
            f"[{r['momentum_min']:7.3f},"
            f"{r['momentum_max']:7.3f}] "
            f"{r['intensity']:15.5e} "
            f"{r['stat_error']:15.5e} "
            f"{r['sys_error']:15.5e}"
        )

if __name__ == "__main__":
    # print_raw_table()
    print()
    # print_transformed_data()



