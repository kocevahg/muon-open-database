"""
(Green, P. J., Duller, N. M., Magnuson, C. E., Choate, L. M., Sheldon, W. R.,
Osborne, A. R., Benbrook, J. R., and Abdel-Monem, M. S.
"Absolute intensities of medium-energy muons in the vertical and at zenith
angles 55 deg - 85 deg," Physical Review D 20 (1979) 1598-1607.)

SOURCE SECTIONS USED (page numbers refer to Phys. Rev. D 20 (1979) 1598-1607):
----------------------------------------------------------------------
  - Table III, p.1603        : measured differential muon intensities in
                               seven 5 deg zenith-angle bins; mean momentum,
                               mean zenith angle, intensity, and quoted
                               uncertainty for each point.
  - Table II, p.1602         : momentum-bin interval definitions used only
                               to document the underlying momentum-row
                               structure (Table III itself lists only the
                               mean momentum values).
  - Sec. III "Corrections to
    the Measured Intensities",
    p.1601-1602              : description of instrumental corrections,
                               momentum-resolution effects, and treatment
                               of the quoted uncertainties.
  - Sec. IV "Discussion of
    Results", p.1601         : explanation that the tabulated mean zenith
                               angles differ from the nominal 5 deg bin
                               midpoints because of the spectrometer
                               acceptance.

Table III, p.1603
----------------------------------------------------------------------
Table III contains 9 momentum rows x 7 zenith-angle columns.

Each entry gives:
    - mean momentum (GeV/c),
    - mean zenith angle,
    - differential intensity,
    - quoted uncertainty.

The intensities are printed directly in units of:

    cm^-2 s^-1 sr^-1 (GeV/c)^-1

and are transcribed without unit conversion.

The quoted uncertainties are taken directly from Table III. The paper does
not provide a separate point-by-point systematic uncertainty for the AMH
measurements; therefore we recorded only the published uncertainty,
while any discussion of instrumental systematics is documented separately.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# RAW_TABLE_III
# ---------------------------------------------------------------------------
# Table III (Green et al. 1979, p. 1603).
# Units: cm^-2 sr^-1 sec^-1 (GeV/c)^-1 (absolute differential intensity).
#
# Each bin carries:
#   - theta_nominal_min / theta_nominal_max: the nominal 5-deg bin edges
#   - theta_bar: the true mean angle of the bin, as explicitly tabulated
#     by Green et al.
#   - axis_orientation: which physical spectrometer tilt orientation
#     the bin's data were taken at (55-75 deg data from the "65 deg"
#     orientation, 70-90 deg data from the "80 deg" orientation; the
#     70-75 deg / theta_bar=72.5 bin is explicitly described by the
#     authors, p. 1601, as derived from BOTH orientations' overlapping
#     aperture)
#   - rows: list of (momentum_GeV, intensity, stat_error) tuples, in the
#     same order/units as printed, one row per momentum point in Table III
#     (9 momentum points per bin, spanning ~2-251 GeV/c)
#
#   !The 20-50 GeV/c filter in transform(); it is not part of the raw
#   transcription itself.

RAW_TABLE_III = [
    {
        "theta_nominal_min": 55,
        "theta_nominal_max": 60,
        "theta_bar": 58.6,
        "axis_orientation": "65 deg",
        "rows": [
            (2.87, 2.70e-4, 0.08e-4),
            (5.40, 1.47e-4, 0.05e-4),
            (8.40, 7.55e-5, 0.42e-5),
            (12.36, 4.24e-5, 0.26e-5),
            (19.68, 1.46e-5, 0.11e-5),
            (31.70, 4.82e-6, 0.53e-6),
            (52.60, 1.68e-6, 0.28e-6),
            (87.40, 4.05e-7, 1.1e-7),
            (251.1, 5.02e-8, 1.3e-8),
        ],
    },
    {
        "theta_nominal_min": 60,
        "theta_nominal_max": 65,
        "theta_bar": 63.0,
        "axis_orientation": "65 deg",
        "rows": [
            (2.87, 1.36e-4, 0.05e-4),
            (5.40, 9.38e-5, 0.25e-5),
            (8.40, 5.80e-5, 0.19e-5),
            (12.36, 3.42e-5, 0.11e-5),
            (19.68, 1.51e-5, 0.05e-5),
            (31.70, 5.15e-6, 0.25e-6),
            (52.60, 1.53e-6, 0.10e-6),
            (87.40, 4.34e-7, 0.52e-7),
            (251.1, 4.10e-8, 0.51e-8),
        ],
    },
    {
        "theta_nominal_min": 65,
        "theta_nominal_max": 70,
        "theta_bar": 67.0,
        "axis_orientation": "65 deg",
        "rows": [
            (2.87, 6.65e-5, 0.32e-5),
            (5.40, 5.33e-5, 0.18e-5),
            (8.40, 3.55e-5, 0.14e-5),
            (12.36, 2.31e-5, 0.09e-5),
            (19.68, 1.16e-5, 0.04e-5),
            (31.70, 4.10e-6, 0.22e-6),
            (52.60, 1.46e-6, 0.10e-6),
            (87.40, 5.40e-7, 0.69e-7),
            (251.1, 5.04e-8, 0.80e-8),
        ],
    },
    {
        # Footnote "a" in Table III: the lowest-momentum row for this
        # column is 2.77 GeV/c.
        "theta_nominal_min": 70,
        "theta_nominal_max": 75,
        "theta_bar": 72.5,
        "axis_orientation": "65 deg and 80 deg (overlap region)",
        "rows": [
            (2.77, 4.85e-5, 0.27e-5),
            (5.40, 3.09e-5, 0.20e-5),
            (8.40, 2.29e-5, 0.18e-5),
            (12.36, 1.39e-5, 0.11e-5),
            (19.68, 6.56e-6, 0.56e-6),
            (31.70, 2.82e-6, 0.32e-6),
            (52.60, 8.79e-7, 1.3e-7),
            (87.40, 2.75e-7, 0.62e-7),
            (251.1, 3.09e-8, 1.1e-8),
        ],
    },
    {
        "theta_nominal_min": 75,
        "theta_nominal_max": 80,
        "theta_bar": 78.0,
        "axis_orientation": "80 deg",
        "rows": [
            (2.68, 1.61e-5, 0.11e-5),
            (5.40, 1.40e-5, 0.07e-5),
            (8.40, 1.19e-5, 0.06e-5),
            (12.36, 9.23e-6, 0.41e-6),
            (19.68, 5.92e-6, 0.23e-6),
            (31.70, 2.35e-6, 0.12e-6),
            (52.60, 8.27e-7, 0.52e-7),
            (87.40, 3.04e-7, 0.28e-7),
            (251.1, 3.60e-8, 0.28e-8),
        ],
    },
    {
        "theta_nominal_min": 80,
        "theta_nominal_max": 85,
        "theta_bar": 82.0,
        "axis_orientation": "80 deg",
        "rows": [
            (2.68, 4.66e-6, 0.61e-6),
            (5.40, 4.26e-6, 0.37e-6),
            (8.40, 3.53e-6, 0.33e-6),
            (12.36, 3.03e-6, 0.23e-6),
            (19.68, 2.36e-6, 0.15e-6),
            (31.70, 1.28e-6, 0.09e-6),
            (52.60, 5.53e-7, 0.42e-7),
            (87.40, 2.09e-7, 0.22e-7),
            (251.1, 2.65e-8, 0.26e-8),
        ],
    },
    {
        "theta_nominal_min": 85,
        "theta_nominal_max": 90,
        "theta_bar": 86.5,
        "axis_orientation": "80 deg",
        "rows": [
            (2.68, 3.85e-6, 1.9e-6),
            (5.40, 1.12e-6, 0.31e-6),
            (8.40, 1.07e-6, 0.34e-6),
            (12.36, 7.71e-7, 2.3e-7),
            (19.68, 3.50e-7, 1.1e-7),
            (31.70, 5.91e-7, 3.1e-7),
            (52.60, 2.77e-7, 0.61e-7),
            (87.40, 4.96e-8, 2.3e-8),
            (251.1, 9.95e-9, 3.2e-9),
        ],
    },
]

# Row index (0-8, matching the row order used in every RAW_TABLE_III bin
# above) -> underlying momentum interval in GeV/c, as given by Table II
# (p. 1602) for the matching orientation. Used ONLY to decide which rows
# fall inside the authors' recommended cross-comparison window in
# transform() The first row's lower edge differs slightly by orientation
# (2 GeV/c for 0/65 deg, 1.6 GeV/c for 80 deg) but this does not affect
# which rows land inside 20-50 GeV/c, so a single representative edge is
# used here.
_ROW_MOMENTUM_INTERVALS = [
    (2.0, 4.0),      # row 0  (~2.68-2.87 GeV/c mean)
    (4.0, 7.0),      # row 1  (5.40 GeV/c mean)
    (7.0, 10.0),     # row 2  (8.40 GeV/c mean)
    (10.0, 15.0),    # row 3  (12.36 GeV/c mean)
    (15.0, 25.0),    # row 4  (19.68 GeV/c mean)
    (25.0, 40.0),    # row 5  (31.70 GeV/c mean)
    (40.0, 70.0),    # row 6  (52.60 GeV/c mean)
    (70.0, 110.0),   # row 7  (87.40 GeV/c mean)
    (110.0, 700.0),  # row 8  (251.1 GeV/c mean) -- NB: Table II's printed
                      # upper edge of 700 GeV/c is itself inconsistent with
                      # the paper's stated overall coverage of 250-300 GeV/c;
]

# Reference metadata shared by every emitted row.
_EXPERIMENT = "AMH"
_REFERENCE = "Green et al. 1979"
_SOURCE_TABLE = "Table III, Green et al. 1979"
_AZIMUTH_DESCRIPTION = (
    "movable axis: single rotatable-axis spectrometer (rocker-beam "
    "mounted), tilted within one vertical plane to fixed orientations of "
    "0, 65, and 80 deg from vertical; no fixed/multi-azimuth array and no "
    "geographic (compass) azimuth is reported in the source paper"
)


def _make_notes(theta_bar: float) -> str:
    """
    Build the per-row provenance/caveat note.

    Every row gets:
      (1) the aperture-asymmetry caveat (nominal bin midpoint != theta_bar),
      (2) the calibration-quality-only-in-20-50-GeV/c caveat,
    and the 85-90 deg bin additionally gets:
      (3) the large-error caveat specific to that bin.
    """
    base = (
        "Nominal 5-deg zenith bin midpoint differs from the true mean "
        "angle theta_bar due to aperture asymmetry in the 5-deg bins "
        "(Green et al. 1979, p. 1601: 'The lack of symmetry of the "
        "aperture in the 5 deg bins causes the average angles to differ "
        "significantly from the midpoints of the zenithal bins.'); use "
        "theta_bar, not the nominal midpoint, for physics comparisons. "
        "The authors state their absolute-normalization intensities are "
        "of 'calibration standard quality' only over 20-50 GeV/c, and "
        "recommend intensities be considered reliable only up to 100 "
        "GeV/c generally; use transform(momentum_range=None) to access "
        "full-table (2-251 GeV/c) points outside that recommended window."
    )
    if abs(theta_bar - 86.5) < 1e-6:
        base += (
            " This is the 85-90 deg (theta_bar=86.5 deg) bin, which the "
            "authors' own quoted uncertainties show carries the largest "
            "fractional errors in Table III (roughly 20-50%); treat with "
            "extra caution in any downstream fit or comparison."
        )
    return base


def transform(momentum_range=(20, 50)):
    """
    Turn RAW_TABLE_III into a flat list of row dicts ready for loading into
    the unified database.

    Parameters
    ----------
    momentum_range : tuple(float, float) or None, default (20, 50)
        If a (low, high) tuple, only momentum rows whose underlying Table-II
        -derived momentum interval overlaps [low, high] are returned. This
        implements the authors own recommendation that only the 20-50 GeV/c
        window be used for cross-comparison with other experiments. Because
        Table III's mean momenta are log-spaced bin averages (not
        exact grid points), a literal "value must be between 20 and 50"
        filter would keep only a single point (31.70 GeV/c);
        we instead keep whichever whole momentum bins overlap the requested
        range (by default: the 15-25, 25-40, and 40-70 GeV/c bins, i.e.
        mean momenta 19.68 / 31.70 / 52.60 GeV/c), matching how the authors
        themselves describe their "20-50 GeV/c" emphasis region.
        If None, no momentum filtering is applied and the FULL table
        (all 9 momentum points, ~2-251 GeV/c, all 7 angular bins) is
        returned.

    Returns
    -------
    list[dict]
        One dict per (angular bin, momentum point), with keys:
        experiment, reference, theta_center, theta_min, theta_max, azimuth,
        altitude_m, momentum, momentum_min, momentum_max, intensity,
        stat_error, sys_error, error_note, source_table, notes.
    """
    rows_out = []

    for bin_data in RAW_TABLE_III:
        theta_bar = bin_data["theta_bar"]
        theta_min = bin_data["theta_nominal_min"]
        theta_max = bin_data["theta_nominal_max"]
        notes = _make_notes(theta_bar)

        for row_index, (momentum, intensity, stat_error) in enumerate(
            bin_data["rows"]
        ):
            if momentum_range is not None:
                lo_req, hi_req = momentum_range
                lo_bin, hi_bin = _ROW_MOMENTUM_INTERVALS[row_index]
                overlaps = (lo_bin <= hi_req) and (hi_bin >= lo_req)
                if not overlaps:
                    continue

            rows_out.append(
                {
                    "experiment": _EXPERIMENT,
                    "reference": _REFERENCE,
                    # True mean angle of the bin (see caveat above) --
                    # this, not the nominal midpoint, is theta_center.
                    "theta_center": theta_bar,
                    "theta_min": theta_min,
                    "theta_max": theta_max,
                    "azimuth": _AZIMUTH_DESCRIPTION,
                    "altitude_m": 0,
                    "momentum": momentum,
                    # Table III does not itself restate momentum-interval
                    # edges (only Table II does, for a related but not
                    # identical quantity)
                    "momentum_min": None,
                    "momentum_max": None,
                    "intensity": intensity,
                    "stat_error": stat_error,
                    "sys_error": None,
                    "error_note": (
                        "Error as printed in Table III (statistical / "
                        "measurement uncertainty from the resolution- and "
                        "multiple-Coulomb-scattering-corrected best fit, "
                        "Eqs. 1-2 of Green et al. 1979). No additional "
                        "per-point systematic error is tabulated by the "
                        "authors for the AMH instrument; sys_error is left "
                        "as None rather than assumed to be zero."
                    ),
                    "source_table": _SOURCE_TABLE,
                    "notes": notes,
                }
            )

    return rows_out

def print_rawdata():
    #Print the raw Table III values exactly as transcribed.
    print("RAW TABLE III")

    for bin_data in RAW_TABLE_III:
        print(
            f"\nTheta bin "
            f"{bin_data['theta_nominal_min']}-{bin_data['theta_nominal_max']} deg "
            f"(theta_bar={bin_data['theta_bar']}, "
            f"orientation={bin_data['axis_orientation']})"
        )

        for momentum, intensity, stat_error in bin_data["rows"]:
            print(
                f"  p={momentum:7.2f} GeV/c   "
                f"I={intensity:.4e}   "
                f"err={stat_error:.2e}"
            )

def print_transformed(momentum_range=(20, 50)):
        #Print the transformed rows returned by transform().

        rows = transform(momentum_range=momentum_range)

        for row in rows:
            print(
                f"theta={row['theta_center']:5.1f}  "
                f"p={row['momentum']:7.2f}  "
                f"I={row['intensity']:.4e}  "
                f"stat={row['stat_error']:.2e}"
            )

if __name__ == "__main__":
    filtered_rows = transform()  # default: authors' recommended 20-50 GeV/c
    full_rows = transform(momentum_range=None)  # full table, 2-251 GeV/c

    print(f"AMH filtered (20-50 GeV/c recommended) row count: {len(filtered_rows)}")
    print(f"AMH full table (2-251 GeV/c, all bins) row count: {len(full_rows)}")

    #print_rawdata()
    print_transformed()                    # filtered (default)
    #print_transformed(momentum_range=None) # full table