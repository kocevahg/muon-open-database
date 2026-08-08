"""
(Kellogg, R. G., Kasha, H., and Larsen, R. C.
"Momentum spectra, charge ratio, and zenith-angle dependence of
cosmic-ray muons," Physical Review D 17 (1978) 98-113.)

SOURCE SECTIONS USED (page numbers refer to Phys. Rev. D 17 (1978) 98-113):
----------------------------------------------------------------------
  - Table IX, p.108          : measured differential muon intensities at
                               zenith angles 30 deg and 75 deg; mean
                               momentum, differential intensity, and
                               quoted point-to-point uncertainty for
                               each momentum point.
  - Table I, p.100           : spectrometer angular acceptance
                               (± 11.8 deg), used to define the
                               zenith-angle acceptance of each
                               measurement.
  - Sec. II B and Table I,
    p.100-101                : description of the spectrometer geometry
                               and angular acceptance.
  - Sec. III E, p.108-109    : discussion of the finite angular
                               acceptance correction applied to the
                               75 deg measurements.
  - Table IX caption, p.108  : definition of the quoted uncertainties
                               and the separate normalization
                               uncertainties (5.2% at 75 deg,
                               6.7% at 30 deg).

Table IX, p.108
----------------------------------------------------------------------
Table IX contains 9 momentum rows measured at two zenith angles
(30 deg and 75 deg).

Each entry gives:
    - mean momentum (GeV/c),
    - differential intensity,
    - point-to-point uncertainty.

The intensities are printed in units of:

    [m^2 s sr GeV]^-1

and are converted to the database convention:

    cm^-2 s^-1 sr^-1 (GeV/c)^-1

by applying only the area conversion 1 m^-2 = 10^-4 cm^-2.

The quoted uncertainties are the point-to-point (statistical)
uncertainties listed in Table IX. The paper states separately that
overall normalization uncertainties of 6.7% (30 deg) and 5.2%
(75 deg) should be included when absolute uncertainties are required.
These normalization uncertainties are therefore recorded separately
from the published point-to-point uncertainties.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


# ---------------------------------------------------------------------------
# 1. RAW_TABLE as printed in Table IX, p. 108.
#    Units, AS PRINTED BY KELLOGG ET AL. (NOT converted):
#      momentum        : GeV        (= GeV/c, c = 1)
#      intensity       : (m^2 sr sec GeV)^-1
#      stat_error      : (m^2 sr sec GeV)^-1   -- "point-to-point" statistical
#                                                  error only
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RawRow:
    momentum: float        # GeV (= GeV/c), as printed
    intensity: float       # (m^2 sr s GeV)^-1, as printed
    stat_error: float      # (m^2 sr s GeV)^-1, as printed ("point-to-point" only)


# theta = 30 degrees, from Table IX right-hand column
RAW_TABLE_30DEG: List[RawRow] = [
    RawRow(momentum=55.9,  intensity=1.58e-2, stat_error=0.031e-2),
    RawRow(momentum=70.6,  intensity=7.49e-3, stat_error=0.15e-3),
    RawRow(momentum=89.0,  intensity=3.64e-3, stat_error=0.09e-3),
    RawRow(momentum=111.3, intensity=1.80e-3, stat_error=0.055e-3),
    RawRow(momentum=140.6, intensity=9.31e-4, stat_error=0.33e-4),
    RawRow(momentum=178.1, intensity=4.50e-4, stat_error=0.21e-4),
    RawRow(momentum=222.6, intensity=2.25e-4, stat_error=0.13e-4),
    RawRow(momentum=309.9, intensity=7.09e-5, stat_error=0.43e-5),
    RawRow(momentum=1067,  intensity=2.04e-6, stat_error=0.15e-6),
]

# theta = 75 degrees, from Table IX left-hand column
RAW_TABLE_75DEG: List[RawRow] = [
    RawRow(momentum=55.9,  intensity=9.98e-3, stat_error=0.24e-3),
    RawRow(momentum=70.6,  intensity=5.41e-3, stat_error=0.12e-3),
    RawRow(momentum=89.0,  intensity=3.07e-3, stat_error=0.08e-3),
    RawRow(momentum=111.3, intensity=1.74e-3, stat_error=0.054e-3),
    RawRow(momentum=140.6, intensity=9.50e-4, stat_error=0.33e-4),
    RawRow(momentum=178.1, intensity=4.60e-4, stat_error=0.21e-4),
    RawRow(momentum=222.6, intensity=2.52e-4, stat_error=0.13e-4),
    RawRow(momentum=309.9, intensity=1.09e-4, stat_error=0.052e-4),
    RawRow(momentum=1067,  intensity=2.99e-6, stat_error=0.18e-6),
]

RAW_TABLE = {
    30: RAW_TABLE_30DEG,
    75: RAW_TABLE_75DEG,
}

# ----------------------------------------------------------------------
# 2. RAW_NORMALIZATION_ERROR_PCT
#
# Overall normalization uncertainties quoted in the Table IX caption
# (p. 108). These are reported separately from the point-to-point
# uncertainties listed in the table.
# ----------------------------------------------------------------------
RAW_NORMALIZATION_ERROR_PCT = {
    30: 6.7,   # percent, Table IX caption, p. 108
    75: 5.2,   # percent, Table IX caption, p. 108
}

# ----------------------------------------------------------------------
# 3. RAW_MOMENTUM_BIN_EDGES
#
# Momentum-bin intervals corresponding to the Table IX measurements.
# These bin edges are inferred from the momentum-bin structure used
# throughout the paper (Tables III, IV, VI, and VII). The final bin is
# open-ended and is represented by None.
# ----------------------------------------------------------------------

RAW_MOMENTUM_BIN_EDGES = [
    (50.0, 63.0),
    (63.0, 80.0),
    (80.0, 100.0),
    (100.0, 125.0),
    (125.0, 160.0),
    (160.0, 200.0),
    (200.0, 250.0),
    (250.0, 400.0),
    (400.0, None),   # paper gives no upper edge
]

# ---------------------------------------------------------------------------
# 4. Angular acceptance, from Table I / Sec. II B text, p. 100-101.
# ---------------------------------------------------------------------------
FULL_ANGULAR_ACCEPTANCE_DEG = 11.8   # Z +/- 11.8 deg, full geometric acceptance
HALF_APERTURE_ACCEPTANCE_DEG = 4.1   # Z +/- 4.1 deg contains half the total aperture

# ---------------------------------------------------------------------------
# 5. Unit conversion factor: printed units are per m^2; target is per cm^2.
# ---------------------------------------------------------------------------
CONVERSION_FACTOR_M2_TO_CM2 = 1e-4


def transform() -> List[dict]:
    """
    Apply the documented unit conversion to RAW_TABLE and emit one row
    dict per (angle, momentum) point. Statistical and normalization
    uncertainties are recorded separately, following the treatment
    described in Table IX.
    """
    rows: List[dict] = []

    for theta_center, raw_rows in RAW_TABLE.items():
        norm_pct = RAW_NORMALIZATION_ERROR_PCT[theta_center]

        theta_min = theta_center - FULL_ANGULAR_ACCEPTANCE_DEG
        theta_max = theta_center + FULL_ANGULAR_ACCEPTANCE_DEG

        for i, raw in enumerate(raw_rows):
            intensity_cm2 = raw.intensity * CONVERSION_FACTOR_M2_TO_CM2
            stat_error_cm2 = raw.stat_error * CONVERSION_FACTOR_M2_TO_CM2

            sys_error_cm2 = intensity_cm2 * (norm_pct / 100.0)


            if i < len(RAW_MOMENTUM_BIN_EDGES):
                mom_min, mom_max = RAW_MOMENTUM_BIN_EDGES[i]
            else:
                mom_min, mom_max = None, None

            rows.append({
                "experiment": "Kellogg",
                "reference": "Kellogg et al. 1978",
                "theta_center": theta_center,
                "theta_min": theta_min,
                "theta_max": theta_max,
                "azimuth": None,   #not reported by the paper
                "altitude_m": 0,   # sea-level measurement (Brookhaven National Lab)
                "momentum": raw.momentum,
                "momentum_min": mom_min,
                "momentum_max": mom_max,
                "intensity": intensity_cm2,                   # (GeV/c)^-1 cm^-2 s^-1 sr^-1
                "stat_error": stat_error_cm2,
                "sys_error": sys_error_cm2,
                "error_note": (
                "stat_error is the published point-to-point uncertainty. "
                "sys_error is the quoted normalization uncertainty. "
                ),
                "source_table": "Table IX, p. 108",
                "notes": (
                "Intensity converted from m^-2 to cm^-2. "
                "theta_min/theta_max use the full spectrometer acceptance. "
                "The 75 deg data are corrected for angular acceptance. "
                "Momentum-bin limits are inferred; the final bin is open-ended."
                ),
            })

    return rows

def print_raw_data() -> None:
    """Print the raw values from Table IX."""

    print("RAW TABLE (as printed)")
    print(
        f"{'theta':>6} {'p(GeV)':>10} "
        f"{'intensity':>14} {'stat_error':>14}"
    )

    for theta, rows in RAW_TABLE.items():
        for row in rows:
            print(
                f"{theta:>6} "
                f"{row.momentum:>10.1f} "
                f"{row.intensity:>14.4e} "
                f"{row.stat_error:>14.4e}"
            )


def print_transformed_data(rows: List[dict]) -> None:
    """Print the transformed dataset."""

    print(f"Total rows: {len(rows)}")
    print()
    print(
        f"{'theta':>6} {'p(GeV/c)':>10} "
        f"{'intensity':>14} {'stat_error':>14} {'sys_error':>14}"
    )

    for row in rows:
        print(
            f"{row['theta_center']:>6} "
            f"{row['momentum']:>10.1f} "
            f"{row['intensity']:>14.4e} "
            f"{row['stat_error']:>14.4e} "
            f"{row['sys_error']:>14.4e}"
        )



if __name__ == "__main__":
    #print_raw_data()
    print()
    #print_transformed_data(transform())

