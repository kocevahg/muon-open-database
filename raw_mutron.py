"""
(Matsuno, S. et al. "Cosmic-ray muon spectrum up to 20 TeV at 89 deg
zenith angle," Physical Review D 29, No. 1 (1984), pp. 1-11.)

SOURCE SECTIONS USED (page numbers refer to Physical Review D 29):
----------------------------------------------------------------------
  - Table I, p.3        : spectrometer characteristics, including the
                           zenith-angle range 86-90 deg and the two
                           azimuthal viewing directions (NW and SE).
  - Sec. II C, p.6      : geomagnetic-field corrections for the NW and
                           SE directions; the two directions are combined
                           into one dataset.
  - Sec. V A, p.8       : mean zenith angle (88.8 deg), correction factors,
                           and total correction factor for the absolute
                           intensity.
  - Table IV, pp.9-10   : data for both muon charges, including
                           momentum-bin edges, weighted mean momentum,
                           event counts, and statistical errors.

TABLE IV, pp.9-10
----------------------------------------------------------------------
Table IV gives the corrected muon spectrum for 24 momentum bins.
The published weighted-mean momentum is used directly rather than
calculating an arithmetic bin center.

!The intensity values in Table IV already include the published total
correction factor of 1.15 +/- 0.07 and therefore must not be corrected
again. The statistical-error column is kept as the statistical
uncertainty reported in the table.

ANGULAR RANGE
----------------------------------------------------------------------
The spectrum covers 86 deg < theta < 90 deg with a mean zenith angle
of 88.8 deg. The NW and SE viewing directions are combined into the
same dataset, as described in Sec. II C.
"""

# ---------------------------------------------------------------------------
# 1. RAW_TABLE_IV - "Differential muon momentum spectrum" sub-table (both signs
#    of muons, NW+SE combined). One parallel array per column, in table order
#    (lowest to highest momentum bin).
# ---------------------------------------------------------------------------

# Bin edges as printed in the "Momentum bin (GeV/c)" column.
RAW_MOMENTUM_BIN_MIN = [
    100, 126, 158, 200, 251, 316, 398, 501, 631, 794,
    1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943,
    10000, 12589, 15849, 19953,
]
RAW_MOMENTUM_BIN_MAX = [
    126, 158, 200, 251, 316, 398, 501, 631, 794, 1000,
    1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000,
    12589, 15849, 19953, 25119,
]

# "Weighted mean momentum value (GeV/c)" column.
RAW_WEIGHTED_MEAN_MOMENTUM = [
    112, 141, 177, 223, 281, 354, 444, 559, 704, 886,
    1115, 1403, 1766, 2222, 2797, 3520, 4431, 5576, 7018, 8832,
    11116, 13990, 17606, 22162,
]

# "Muon number" column - event count per bin.
RAW_MUON_NUMBER = [
    70142, 60560, 50136, 40643, 31519, 23608, 16946, 11765, 7893, 5628,
    3114, 1858, 1104, 646, 350, 221, 135, 81, 47, 31,
    13, 8, 7, 4,
]

# "Differential intensity (GeV/c)^-1 cm^-2 s^-1 sr^-1" column.
RAW_INTENSITY = [
    5.69e-8, 3.99e-8, 2.41e-8, 1.60e-8, 9.88e-9, 5.90e-9, 3.37e-9, 1.88e-9,
    1.02e-9, 5.29e-10, 2.71e-10, 1.31e-10, 6.23e-11, 2.97e-11, 1.29e-11,
    6.62e-12, 3.25e-12, 1.59e-12, 7.33e-13, 3.76e-13, 1.18e-13, 5.18e-14,
    3.50e-14, 1.10e-14,
]

# "Statistical error" column.
RAW_STAT_ERROR = [
    2.15e-10, 1.62e-10, 1.08e-10, 7.94e-11, 5.57e-11, 3.84e-11, 2.59e-11,
    1.73e-11, 1.15e-11, 7.05e-12, 4.86e-12, 3.04e-12, 1.88e-12, 1.17e-12,
    6.90e-13, 4.45e-13, 2.80e-13, 1.77e-13, 1.07e-13, 6.75e-14, 3.27e-14,
    1.83e-14, 1.32e-14, 5.50e-15,
]

# Check that all columns are the same length (24 momentum bins).
assert len(RAW_MOMENTUM_BIN_MIN) == len(RAW_MOMENTUM_BIN_MAX) == \
    len(RAW_WEIGHTED_MEAN_MOMENTUM) == len(RAW_MUON_NUMBER) == \
    len(RAW_INTENSITY) == len(RAW_STAT_ERROR) == 24


# ---------------------------------------------------------------------------
# 2. RAW_SYSTEMATICS - p. 8, from Sec. V A, "The absolute intensity
#    of cosmic-ray muons".
# ---------------------------------------------------------------------------
RAW_SYSTEMATICS = {
    # Individual correction factors applied to the raw event rates before
    # Table IV was tabulated:
    "mdm_correction": {"factor": 0.96, "error": 0.02,
                        "note": "Maximum-detectable-momentum correction (Sec. III A)."},
    "trigger_efficiency_correction": {"factor": 1.11, "error": 0.06,
                                       "note": "MWPC trigger-efficiency correction (Sec. III B)."},
    "shadowing_correction": {"factor": 1.08, "error": 0.01,
                              "note": "Correction for shadowing by mountains in the "
                                      "spectrometer aperture."},
    # Product of the three factors above, as explicitly printed in the paper:
    "total_correction_factor": {
        "factor": 1.15,
        "error": 0.07,
        # IMPORTANT: this is a MULTIPLICATIVE correction that has ALREADY
        # been applied to every intensity value in Table IV.
        # !Do not multiply RAW_INTENSITY by this factor again.
        "already_applied_to_table_iv": True,
        "relative_uncertainty": 0.07 / 1.15,  # ~0.0609 -> ~6.1%
        "note": ("Product of the MDM, trigger-efficiency, and shadowing "
                 "corrections. Already folded into RAW_INTENSITY. The "
                 "~6.1% relative uncertainty (0.07/1.15) is NOT included "
                 "in RAW_STAT_ERROR and must be added as a separate "
                 "systematic term (see sys_error in transform())."),
    }
}

# ---------------------------------------------------------------------------
# 3. Geometry / angular data from Table I, Sec. II A, and Sec. V A.
# ---------------------------------------------------------------------------
THETA_MIN_DEG = 86.0       # Table I & Sec. II A: "zenith angle 86 deg-90 deg"
THETA_MAX_DEG = 90.0
THETA_CENTER_DEG = 88.8    # Sec. V A (PDF p. 8): "mean zenith angle of 88.8 deg"

AZIMUTH_DESCRIPTION = ("Northwest (325.4 deg +/- 15.0 deg) and Southeast "
                        "(145.4 deg +/- 15.0 deg) views combined -- MUTRON's "
                        "two magnet arms view opposite azimuths "
                        "simultaneously and Table IV reports the merged "
                        "single spectrum (Sec. II C).")


def transform():
    """Convert the raw MUTRON Table IV values into the common data format.

    1. Use the published weighted-mean momentum.

    2. Keep the published momentum-bin edges in momentum_min and momentum_max.

    3. Copy the published intensity and statistical error directly; the
       1.15 +/- 0.07 correction factor is already included in Table IV.

    4. Estimate the systematic error from the relative uncertainty of the
       total correction factor:
           sys_error = intensity * (0.07 / 1.15)

    5. Copy the published event count for each momentum bin.
    """
    rows = []

    total_factor = RAW_SYSTEMATICS["total_correction_factor"]["factor"]
    total_factor_err = RAW_SYSTEMATICS["total_correction_factor"]["error"]
    rel_sys = total_factor_err / total_factor

    # Use the published weighted-mean momentum and bin quantities.
    for i, momentum in enumerate(RAW_WEIGHTED_MEAN_MOMENTUM):
        intensity = RAW_INTENSITY[i]
        stat_error = RAW_STAT_ERROR[i]
        n_events = RAW_MUON_NUMBER[i]

        sys_error = intensity * rel_sys

        rows.append({
            "experiment": "MUTRON",
            "reference": "Matsuno et al. 1984",
            "theta_center": THETA_CENTER_DEG,
            "theta_min": THETA_MIN_DEG,
            "theta_max": THETA_MAX_DEG,
            "azimuth": AZIMUTH_DESCRIPTION,
            "altitude_m": 0,
            "momentum": momentum,
            "momentum_min": RAW_MOMENTUM_BIN_MIN[i],
            "momentum_max": RAW_MOMENTUM_BIN_MAX[i],
            "intensity": intensity,
            "stat_error": stat_error,
            "sys_error": sys_error,
            "n_events": n_events,
            "source_table": "Table IV, Matsuno et al. 1984",
        })

    return rows


def print_rawdata():
    # Print the values as stored from the original paper.
    for i in range(len(RAW_WEIGHTED_MEAN_MOMENTUM)):
        print(
            RAW_MOMENTUM_BIN_MIN[i],
            RAW_MOMENTUM_BIN_MAX[i],
            RAW_WEIGHTED_MEAN_MOMENTUM[i],
            RAW_INTENSITY[i],
            RAW_STAT_ERROR[i],
            RAW_MUON_NUMBER[i]
        )


def print_transformed():
    # Print the main quantities after transformation.
    rows = transform()

    for row in rows:
        print(
            f"p={row['momentum']:8.2f}  "
            f"I={row['intensity']:.4e}  "
            f"stat={row['stat_error']}  "
            f"sys={row['sys_error']:.4e}"
        )

if __name__ == "__main__":
    data = transform()

    print(f"MUTRON transform(): {len(data)} rows extracted.")

    print_rawdata()
    print_transformed()
