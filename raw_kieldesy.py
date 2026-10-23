"""
(Jokisch, H., Carstensen, K., Dau, W. D., Meyer, H. J., Allkofer, O. C.
"Cosmic-ray muon spectrum up to 1 TeV at 75 deg zenith angle,"
Physical Review D 19 (1979) 1368-1372.)

SOURCE SECTIONS USED (page numbers refer to Phys. Rev. D 19 (1979) 1368-1372):
----------------------------------------------------------------------
  - Table I, p.1369         : spectrometer parameters (viewing direction,
                              azimuth, magnetic field, detector geometry,
                              calibration information).
  - Table II, p.1370        : measured differential muon intensities,
                              momentum-bin limits, and quoted statistical
                              uncertainties (given as percentages).
  - Sec. III "Data analysis",
    p.1370                  : fit procedure and momentum range over which
                              geomagnetic deflection is negligible.
  - Sec. IV "Results",
    p.1371                  : explanation that the published 75 deg
                              spectrum is derived from measurements over
                              the 68-82 deg zenith range using the fitted
                              angular dependence.

Table II, p.1370
----------------------------------------------------------------------
Table II contains 16 momentum bins.

Each row gives:
    - momentum interval (GeV/c),
    - differential intensity,
    - quoted statistical uncertainty (percent).

The intensities are printed directly in units of:

    cm^-2 s^-1 sr^-1 (GeV/c)^-1

The quoted uncertainties are percentages. Absolute statistical
uncertainties are calculated during transform() as:

    stat_error = intensity × (percent_error / 100)

preserving the original values printed in Table II.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# 1. RAW TABLE I -- "Main properties of the experimental setup" (p. 1369)
# ---------------------------------------------------------------------------

RAW_TABLE_I = {
    "magnet": "air gap 27x135 cm^2; deflection power: integral(B dl) = 1.83 Tm",
    "magnet_type": "air-gap magnet",
    "mdm_mean_value_GeV_c": 745,  # "maximum detectable momentum", mean value across the 7 zenith-angle bins
    "collecting_power_full_cm2_sr": 360,
    "collecting_power_reduced_cm2_sr": 274.7,  # reduced in off-line analysis to avoid edge misalignment/inefficiency
    "total_number_of_events": 1000000,
    "number_of_momenta_above_1GeV_reduced": 590958,
    "zenith_angle_center_deg": 75,
    "zenith_angle_half_width_deg": 7,   # printed as "75 deg +/- 7 deg"  ->  68 deg to 82 deg range
    "zenith_angle_as_printed": "75 deg +/- 7 deg",
    "azimuth_as_printed": "288 deg +/- 20 deg (east)",
    "azimuth_center_deg": 288,
    "azimuth_half_width_deg": 20,
    "azimuth_direction": "east",
    "detectors": "4 scintillation counters, 14 wire spark chambers",
    "rate_corrected_as_printed": "9.7 min^-1 +/- 5% (95% confidence)",
    "rate_corrected_per_min": 9.7,
    "rate_absolute_calibration_error_pct": 5.0,   # the +/-5% (95% CL) absolute calibration error
    "rate_absolute_calibration_CL": "95%",
    "site": "DESY (Deutsches Elektronen Synchrotron), Hamburg, Germany",  #
    "altitude_note": "Sea level. Fig. 3-5 axis labels explicitly say "
                      "'p Muon Momentum at Sea Level (GeV/c)'; DESY/Hamburg site is at sea level.",
}
# ---------------------------------------------------------------------------
# 2. RAW TABLE II -- "Differential intensities" (p. 1370)
# ---------------------------------------------------------------------------
# Columns as printed: Momentum p (GeV/c) | Intensity [cm^-1 sr^-1 sec^-1
# (GeV/c)^-1] | Error (%) | Measured number
#
# NOTE: the column header shows "cm^-1 sr^-1 sec^-1 (GeV/c)^-1".
# This is almost certainly a typo artifact of "cm^-2"???!!!
#
# The "Error (%)" column is the RAW, AS-PRINTED value -- a *relative*
# percentage error on the intensity, NOT an absolute error. Do not use
# these numbers as absolute uncertainties directly; see transform().
#
# The "Measured number" column is the raw (uncorrected) bin count and is
# kept for provenance/completeness; it is not used in transform().

RAW_TABLE_II_UNIT = "cm^-2 sr^-1 sec^-1 (GeV/c)^-1"
RAW_TABLE_II_SOURCE = "Table II, Jokisch et al. 1979, Phys. Rev. D 19, 1370"

# Each tuple: (momentum p [GeV/c], intensity [RAW_TABLE_II_UNIT], error [%], measured_number)
RAW_TABLE_II = [
    (1.12,   2.973e-5, 1.45, 4782),
    (1.41,   3.111e-5, 1.07, 8751),
    (1.76,   3.263e-5, 0.85, 13876),
    (2.29,   3.168e-5, 0.71, 19604),
    (2.85,   3.068e-5, 0.63, 25368),
    (3.57,   2.848e-5, 0.57, 30900),
    (4.49,   2.606e-5, 0.53, 36244),
    (5.66,   2.332e-5, 0.49, 40920),
    (7.12,   2.021e-5, 0.48, 44192),
    (8.95,   1.705e-5, 0.46, 46468),
    (11.26,  1.373e-5, 0.46, 46910),
    (14.17,  1.070e-5, 0.47, 45497),
    (17.83,  8.029e-6, 0.48, 42596),
    (22.44,  5.708e-6, 0.51, 37938),
    (28.23,  3.964e-6, 0.55, 33075),
    (35.52,  2.637e-6, 0.60, 27560),
    (44.70,  1.712e-6, 0.67, 22421),
    (56.25,  1.064e-6, 0.76, 17488),
    (70.79,  6.479e-7, 0.86, 13465),
    (89.09,  3.751e-7, 1.01, 9771),
    (112.13, 2.208e-7, 1.18, 7241),
    (141.12, 1.234e-7, 1.41, 5027),
    (177.62, 6.632e-8, 1.70, 3440),
    (223.56, 3.735e-8, 2.06, 2408),
    (281.39, 1.869e-8, 2.53, 1559),
    (354.18, 9.689e-9, 3.15, 1008),
    (445.81, 5.436e-9, 3.92, 759),
    (625.46, 1.770e-9, 3.87, 793),
    (990.22, 3.982e-10, 6.30, 370),
]

# ---------------------------------------------------------------------------
# 3. Model-dependence (Sec. IV, p. 1371)
# ---------------------------------------------------------------------------
# The published "75 deg" spectrum is not a narrow-bin measurement centered
# at exactly 75 deg. Jokisch et al. state that it combines all data taken
# between 68 deg and 82 deg by applying the fitted angular dependence
# ("modulating the 75 deg form fit with the average deviation curves").
# Downstream users should therefore interpret theta=75 deg as a
# representative spectrum for the 68-82 deg angular range rather than a
# direct measurement at exactly 75 deg.

MODEL_DEPENDENCE_CAVEAT = (
    "The published 75 deg spectrum is derived from measurements spanning "
    "68-82 deg zenith angle using the fitted angular dependence described "
    "by Jokisch et al. (1979, Sec. IV, p. 1371). It should therefore be "
    "interpreted as a representative 75 deg spectrum rather than a direct "
    "measurement made only at theta = 75 deg."
)
# ---------------------------------------------------------------------------
# 4. Geomagnetic-deflection caveat -- exact quote, p. 1370
# ---------------------------------------------------------------------------
# Jokisch et al. state that their angular-spectrum fits were restricted to
# momenta above 30 GeV/c, where geomagnetic deflection and atmospheric
# multiple scattering are negligible. The lower-momentum points in Table II
# are measured values, but they lie outside the stated validity range of
# the fitted model.

GEOMAGNETIC_DEFLECTION_CAVEAT = (
    "The fitted spectrum is stated to be valid only for momenta above "
    "30 GeV/c, where geomagnetic deflection and atmospheric multiple "
    "scattering are negligible (Jokisch et al. 1979, Sec. III, p. 1370). "
    "Measurements below 30 GeV/c should therefore be interpreted with "
    "additional caution."
)

# Combined notes field used in transform() output rows.
COMBINED_NOTES = MODEL_DEPENDENCE_CAVEAT + " || " + GEOMAGNETIC_DEFLECTION_CAVEAT


# ---------------------------------------------------------------------------
# 5. transform() -- turns RAW_TABLE_II (+ RAW_TABLE_I) into unified rows
# ---------------------------------------------------------------------------
Z_95 = 1.96

def transform() -> list[dict]:
    """
    Convert the raw Table II values into the common data format.

        1. The statistical uncertainty is calculated from the percentage
        reported in Table II:

                stat_error = intensity × error_percent / 100

        2. The systematic uncertainty is calculated from the ±5%
        absolute-calibration uncertainty reported in Table I:

                sys_error = intensity × 0.05 / 1.96

        3. The published 75 deg spectrum represents measurements over
        the 68-82 deg zenith range, as described in Sec. IV.
    """
    rows = []
    for momentum, intensity, error_pct, measured_number in RAW_TABLE_II:
        # percent -> absolute statistical error
        stat_error = intensity * (error_pct / 100.0)

        # absolute calibration systematic error (Table I, +/-5%, 95% CL)
        sys_error = intensity * (RAW_TABLE_I["rate_absolute_calibration_error_pct"] / 100.0) / Z_95

        rows.append({
            "experiment": "Kiel-DESY",
            "reference": "Jokisch et al. 1979",
            "theta_center": 75,
            "theta_min": 68,
            "theta_max": 82,
            "azimuth": "~288 deg (East)",  # Table I: "288 deg +/- 20 deg (east)"
            "altitude_m": 0,
            "momentum": momentum,
            "momentum_min": None,
            "momentum_max": None,
            "intensity": intensity,
            "intensity_unit": RAW_TABLE_II_UNIT,
            "stat_error": stat_error,
            "stat_error_pct_raw": error_pct,   # keep the raw printed % alongside the derived absolute value
            "sys_error": sys_error,
            "sys_error_pct_raw": RAW_TABLE_I["rate_absolute_calibration_error_pct"],
            "error_note": (
                "sys_error = intensity * 0.05 / 1.96 (absolute calibration error, Table I, "
                "quoted at 95% CL, converted to 1 sigma = 2.55%), independent of "
                "stat_error (not pre-combined)."
            ),
            "source_table": "Table II, Jokisch et al. 1979",
            "measured_number_raw": measured_number,  # raw bin count
            "notes": COMBINED_NOTES + (
                f" || This row's momentum ({momentum} GeV/c) is "
                + ("BELOW the 30 GeV/c fit-validity threshold -- geomagnetic "
                   "deflection not certified negligible for this point."
                   if momentum < 30 else
                   "above the 30 GeV/c fit-validity threshold.")
            ),
        })
    return rows

def print_rawdata():
    # Print the values exactly as stored from the original paper.
    print("RAW TABLE II")
    for row in RAW_TABLE_II:
        print(row)

def print_transformed():
    # Print the main quantities for each transformed measurement.
    rows = transform()
    for row in rows:
        print(
            f"theta={row['theta_center']:5.1f}  "
            f"p={row['momentum']:8.2f}  "
            f"I={row['intensity']:.4e}  "
            f"stat={row['stat_error']:.4e}  "
            f"sys={row['sys_error']:.4e}"
        )
# ---------------------------------------------------------------------------
# 6. Self-test / sanity check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    all_rows = transform()

    print(f"Kiel-DESY transform(): {len(all_rows)} rows total")

    #print_rawdata()
    #print_transformed()
