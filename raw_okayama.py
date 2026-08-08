"""
(Tsuji, S., Katayama, T., Okei, K., Wada, T., Yamamoto, I., and
Yamashita, Y.
"Measurements of muons at sea level," J. Phys. G: Nucl. Part. Phys. 24 (1998) 1805-1822.)

SOURCE SECTIONS USED (page numbers refer to J. Phys. G 24 (1998) 1805-1822):
----------------------------------------------------------------------
  - Table 1, p.1806         : experimental setup; telescope geometry,
                              altitude, and pointing information.
  - Table 2, p.1807-1808    : differential muon intensities as a function
                              of zenith angle for three fixed momentum
                              windows (12.5±2.5, 22.5±2.5, 45±5 GeV/c).
  - Tables 3-5, p.1809-1814 : differential muon intensities as a function
                              of momentum for five zenith-angle bins
                              (0±1°, 30±4°, 60±1°, 75±6°, 80±1°).
  - Sec. 4, p.1812          : discussion of the telescope pointing
                              direction (north-west; azimuth 130° in the
                              authors' convention) and comparison with the
                              Kiel-DESY experiment.

RAW TABLES
----------------------------------------------------------------------
This module transcribes two independent sets of measurements:

  - RAW_FINE_SCAN (Table 2):
      Zenith-angle scan at fixed momentum windows.

  - RAW_WIDE_BINS (Tables 3-5):
      Momentum spectra measured at five fixed zenith-angle bins.

These tables represent different projections of the same measurement
campaign. They are therefore kept as separate raw datasets rather than
merged.

At θ = 0° and p = 12.5, 22.5, and 45 GeV/c, Table 2 and Table 3 contain
identical published values. These duplicate rows are removed in
transform(). Measurements at θ = 60° and 80° are retained independently,
since the published values differ slightly.

Table 3 contains three cells at θ = 80° where the printed entry is "--",
indicating that no intensity was reported. These are stored as None and
are not emitted by transform().

ALTITUDE
----------------------------------------------------------------------
Table 1 reports the experimental site at 5.3 m above sea level.
Following the database convention for sea-level measurements,
transform() reports altitude_m = 0.

AZIMUTH
----------------------------------------------------------------------
The telescope pointed toward the north-west (authors' azimuth 130°).
The database records this as "Northwest-Southeast", describing the
instrument axis rather than a compass bearing.
"""

from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# RAW DATA
# ---------------------------------------------------------------------------
# Values are transcribed directly from Tables 2-5 of Tsuji et al. (1998)
# without unit conversion or other modification. Cells printed as "--"
# in the source are stored as None.
# Units: cm^-2 sr^-1 sec^-1 (GeV/c)^-1 (absolute differential intensity).

@dataclass
class WideBin:
    """One zenith bin from Table 3 (theta=0,60,80), Table 4 (theta=30) or
    Table 5 (theta=75): a full 1.5-250 GeV/c momentum scan at one theta."""

    theta_center: float
    theta_min: float
    theta_max: float
    source_table: str            # which printed table this came from
    source_page: str             # printed journal page number(s)
    momentum_min: list           # GeV/c, lower edge of each momentum bin
    momentum_max: list           # GeV/c, upper edge of each momentum bin
    momentum: list               # GeV/c, bin center (as quoted in-text)
    measured_number: list        # raw event counts (None where uncertain, None where "--")
    intensity: list              # cm^-2 sr^-1 s^-1 (GeV/c)^-1; None where "--"
    stat_error: list             # same units; None="--"


@dataclass
class FineScanRow:
    """One zenith bin (theta = 0, then 8..80 in steps of 2 deg) from
    Table 2: three fixed momentum windows (12.5, 22.5, 45.0 GeV/c)."""

    theta_center: float
    theta_min: float
    theta_max: float
    momentum: list
    momentum_halfwidth: list
    measured_number: list
    intensity: list
    stat_error: list


# --- Table 3 (p1809): theta = 0 deg +1 deg -----------------------------
# Momentum bins 1.5-2.0 through 200.0-250.0 GeV/c (23 bins, all populated).
_T3_MOM_EDGES = [
    (1.5, 2.0), (2.0, 3.0), (3.0, 4.0), (4.0, 5.0), (5.0, 6.0), (6.0, 7.0),
    (7.0, 8.0), (8.0, 9.0), (9.0, 10.0), (10.0, 15.0), (15.0, 20.0),
    (20.0, 25.0), (25.0, 30.0), (30.0, 40.0), (40.0, 50.0), (50.0, 60.0),
    (60.0, 70.0), (70.0, 80.0), (80.0, 90.0), (90.0, 100.0),
    (100.0, 150.0), (150.0, 200.0), (200.0, 250.0),
]
_T3_MOM_CENTER = [
    1.75, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 12.5, 17.5, 22.5, 27.5,
    35, 45, 55, 65, 75, 85, 95, 125, 175, 225,
]

theta0 = WideBin(
    theta_center=0, theta_min=0, theta_max=1,
    source_table="Table 3, Tsuji et al. 1998", source_page="1809",
    momentum_min=[e[0] for e in _T3_MOM_EDGES],
    momentum_max=[e[1] for e in _T3_MOM_EDGES],
    momentum=list(_T3_MOM_CENTER),
    measured_number=[
        3496, 6450, 4569, 3400, 2358, 1809, 1388, 1074, 826, 2468, 1051,
        540, 292, 277, 129, 50, 28, 23, 10, 4, 10, 2, 2,
    ],
    intensity=[
        1.51e-3, 1.21e-3, 7.93e-4, 5.73e-4, 3.93e-4, 3.01e-4, 2.30e-4,
        1.78e-4, 1.38e-4, 8.37e-5, 3.75e-5, 2.04e-5, 1.17e-5, 6.12e-6,
        3.21e-6, 1.39e-6, 8.68e-7, 8.07e-7, 3.73e-7, 1.69e-7, 1.00e-7,
        2.84e-8, 3.59e-8,
    ],
    stat_error=[
        0.03e-3, 0.02e-3, 0.12e-4, 0.10e-4, 0.08e-4, 0.07e-4, 0.05e-4,
        0.05e-4, 0.05e-4, 0.17e-5, 0.12e-5, 0.09e-5, 0.07e-5, 0.37e-6,
        0.28e-6, 0.20e-6, 1.64e-7, 1.68e-7, 1.18e-7, 0.85e-7, 0.32e-7,
        2.01e-8, 2.54e-8,
    ],
)

# --- Table 3 (p1809): theta = 60 deg +-1 deg ----------------------------
# First two momentum bins (1.5-2.0, 2.0-3.0) are printed as "--" (no
# events reported below ~3 GeV/c at this zenith -- geomagnetic cutoff).
theta60 = WideBin(
    theta_center=60, theta_min=59, theta_max=61,
    source_table="Table 3, Tsuji et al. 1998", source_page="1809",
    momentum_min=[e[0] for e in _T3_MOM_EDGES[2:]],
    momentum_max=[e[1] for e in _T3_MOM_EDGES[2:]],
    momentum=list(_T3_MOM_CENTER[2:]),
    measured_number=[
        476, 435, 336, 249, 236, 194, 146, 540, 265, 122, 75, 74, 27,
        26, 12, 3, 4, 3, 3, 2, 1,
    ],
    intensity=[
        2.22e-4, 1.91e-4, 1.42e-4, 1.07e-4, 9.94e-5, 8.01e-5, 6.35e-5,
        4.71e-5, 2.35e-5, 1.18e-5, 7.46e-6, 4.08e-6, 1.78e-6, 1.64e-6,
        1.08e-6, 2.19e-7, 4.26e-7, 2.38e-7, 7.37e-8, 1.17e-7, 3.49e-8,
    ],
    stat_error=[
        0.10e-4, 0.09e-4, 0.08e-4, 0.07e-4, 0.65e-5, 0.58e-5, 0.53e-5,
        0.20e-5, 0.14e-5, 0.11e-5, 0.86e-6, 0.47e-6, 0.34e-6, 0.32e-6,
        0.31e-6, 1.27e-7, 2.13e-7, 1.37e-7, 4.26e-8, 0.83e-7, 3.49e-8,
    ],
)

# --- Table 3 (p1809): theta = 80 deg +-1 deg ----------------------------
# First two bins "--"; also 80-90, 150-200 and 200-250 GeV/c bins are "--"

_T3_80_EDGES = _T3_MOM_EDGES[2:]
_T3_80_CENTER = _T3_MOM_CENTER[2:]
_t3_80_N = [23, 12, 16, 17, 29, 14, 10, 81, 41, 33, 16, 21, 14, 1, 4, 1,
            0, 1, 2, 0, 0]
_t3_80_I = [1.85e-5, 8.14e-6, 1.29e-5, 1.15e-5, 2.07e-5, 8.88e-6, 6.23e-6,
            1.12e-5, 6.07e-6, 4.95e-6, 2.92e-6, 1.79e-6, 1.24e-6, 1.40e-7,
            3.82e-7, 1.17e-7, None, 1.12e-7, 1.01e-7, None, None]
_t3_80_E = [0.39e-5, 2.35e-6, 0.32e-5, 0.28e-5, 0.38e-5, 2.37e-6, 1.97e-6,
            0.12e-5, 0.95e-6, 0.86e-6, 0.73e-6, 0.39e-6, 0.33e-6, 1.40e-7,
            1.91e-7, 1.17e-7, None, 1.12e-7, 0.71e-7, None, None]

theta80 = WideBin(
    theta_center=80, theta_min=79, theta_max=81,
    source_table="Table 3, Tsuji et al. 1998", source_page="1809",
    momentum_min=[e[0] for e in _T3_80_EDGES],
    momentum_max=[e[1] for e in _T3_80_EDGES],
    momentum=list(_T3_80_CENTER),
    measured_number=_t3_80_N,
    intensity=_t3_80_I,
    stat_error=_t3_80_E,
)

# --- Table 4 (p1811): theta = 30 deg +-4 deg ----------------------------
# First bin (1.5-2.0) is "--".
_T4_EDGES = _T3_MOM_EDGES[1:]
_T4_CENTER = _T3_MOM_CENTER[1:]
theta30 = WideBin(
    theta_center=30, theta_min=26, theta_max=34,
    source_table="Table 4, Tsuji et al. 1998", source_page="1811",
    momentum_min=[e[0] for e in _T4_EDGES],
    momentum_max=[e[1] for e in _T4_EDGES],
    momentum=list(_T4_CENTER),
    measured_number=[
        7434, 6048, 4517, 3425, 2594, 1961, 1512, 1276, 3624, 1575, 782,
        450, 399, 177, 89, 41, 27, 21, 8, 13, 5, 1,
    ],
    intensity=[
        9.57e-4, 6.85e-4, 4.95e-4, 3.70e-4, 2.74e-4, 2.06e-4, 1.61e-4,
        1.37e-4, 7.74e-5, 3.61e-5, 1.88e-5, 1.17e-5, 5.72e-6, 2.79e-6,
        1.57e-6, 8.42e-7, 5.97e-7, 5.20e-7, 2.16e-7, 8.10e-8, 4.29e-8,
        1.31e-8,
    ],
    stat_error=[
        0.11e-4, 0.09e-4, 0.07e-4, 0.06e-4, 0.05e-4, 0.05e-4, 0.04e-4,
        0.04e-4, 0.13e-5, 0.09e-5, 0.07e-5, 0.05e-5, 0.29e-6, 0.21e-6,
        0.17e-6, 1.31e-7, 1.15e-7, 1.13e-7, 0.76e-7, 2.25e-8, 1.92e-8,
        1.31e-8,
    ],
)

# --- Table 5 (p1814): theta = 75 deg +-6 deg ----------------------------
# First two bins "--".
_T5_EDGES = _T3_MOM_EDGES[2:]
_T5_CENTER = _T3_MOM_CENTER[2:]
theta75 = WideBin(
    theta_center=75, theta_min=69, theta_max=81,
    source_table="Table 5, Tsuji et al. 1998", source_page="1814",
    momentum_min=[e[0] for e in _T5_EDGES],
    momentum_max=[e[1] for e in _T5_EDGES],
    momentum=list(_T5_CENTER),
    measured_number=[
        572, 575, 507, 476, 429, 391, 357, 1391, 730, 468, 284, 284, 147,
        60, 37, 20, 16, 14, 21, 2, 7,
    ],
    intensity=[
        4.59e-5, 4.16e-5, 3.67e-5, 3.33e-5, 2.97e-5, 2.76e-5, 2.43e-5,
        1.98e-5, 1.09e-5, 7.14e-6, 4.82e-6, 2.51e-6, 1.50e-6, 7.19e-7,
        4.77e-7, 2.79e-7, 2.43e-7, 2.26e-7, 8.98e-8, 1.27e-8, 4.43e-8,
    ],
    stat_error=[
        0.19e-5, 0.17e-5, 0.16e-5, 0.15e-5, 0.14e-5, 0.14e-5, 0.13e-5,
        0.05e-5, 0.04e-5, 0.33e-6, 0.29e-6, 0.15e-6, 0.12e-6, 0.93e-7,
        0.78e-7, 0.62e-7, 0.61e-7, 0.60e-7, 1.96e-8, 0.90e-8, 1.67e-8,
    ],
)

RAW_WIDE_BINS = [theta0, theta30, theta60, theta75, theta80]


# --- Table 2 (p1807-1808): fine 2-degree zenith scan --------------------
# Table 2 contains measurements at θ = 0°, then θ = 8°–80° in 2° steps
# (38 zenith-angle bins total). Each zenith angle includes measurements
# in three fixed momentum windows: 12.5±2.5, 22.5±2.5, and 45±5 GeV/c.

_FINE_THETA = [0] + list(range(8, 81, 2))

# columns, in printed order: N(12.5), I(12.5), N(22.5), I(22.5), N(45.0), I(45.0)
_FINE_ROWS = {
    0:  (2468, 8.37e-5, 0.17e-5, 540, 2.04e-5, 0.09e-5, 129, 3.21e-6, 0.28e-6),
    8:  (3158, 8.22e-5, 0.15e-5, 688, 2.00e-5, 0.08e-5, 159, 2.97e-6, 0.24e-6),
    10: (2612, 8.90e-5, 0.17e-5, 517, 1.94e-5, 0.09e-5, 113, 2.84e-6, 0.27e-6),
    12: (2319, 8.78e-5, 0.17e-5, 485, 2.02e-5, 0.09e-5, 118, 3.20e-6, 0.29e-6),
    14: (2005, 7.78e-5, 0.17e-5, 428, 1.88e-5, 0.09e-5, 92, 2.66e-6, 0.28e-6),
    16: (2076, 8.52e-5, 0.19e-5, 447, 2.08e-5, 0.10e-5, 107, 3.15e-6, 0.30e-6),
    18: (2077, 8.58e-5, 0.19e-5, 424, 1.91e-5, 0.09e-5, 92, 2.90e-6, 0.30e-6),
    20: (2021, 8.52e-5, 0.19e-5, 442, 2.03e-5, 0.10e-5, 96, 3.03e-6, 0.31e-6),
    22: (1912, 7.98e-5, 0.18e-5, 403, 1.92e-5, 0.10e-5, 86, 2.66e-6, 0.29e-6),
    24: (1929, 8.17e-5, 0.19e-5, 407, 1.91e-5, 0.09e-5, 105, 3.27e-6, 0.32e-6),
    26: (975, 8.31e-5, 0.27e-5, 198, 1.88e-5, 0.13e-5, 54, 3.37e-6, 0.46e-6),
    28: (869, 7.24e-5, 0.25e-5, 197, 1.89e-5, 0.13e-5, 49, 2.98e-6, 0.43e-6),
    30: (957, 8.44e-5, 0.27e-5, 231, 2.23e-5, 0.15e-5, 51, 3.34e-6, 0.47e-6),
    32: (868, 7.37e-5, 0.25e-5, 200, 1.94e-5, 0.14e-5, 33, 2.04e-6, 0.35e-6),
    34: (849, 7.43e-5, 0.26e-5, 203, 2.01e-5, 0.14e-5, 47, 3.07e-6, 0.45e-6),
    36: (765, 6.37e-5, 0.23e-5, 176, 1.71e-5, 0.13e-5, 39, 2.35e-6, 0.38e-6),
    38: (788, 6.82e-5, 0.24e-5, 160, 1.54e-5, 0.12e-5, 44, 2.72e-6, 0.41e-6),
    40: (834, 7.07e-5, 0.24e-5, 181, 1.67e-5, 0.12e-5, 36, 2.41e-6, 0.40e-6),
    42: (819, 7.08e-5, 0.25e-5, 180, 1.76e-5, 0.13e-5, 32, 2.17e-6, 0.38e-6),
    44: (808, 7.04e-5, 0.25e-5, 170, 1.68e-5, 0.13e-5, 51, 3.24e-6, 0.45e-6),
    46: (743, 6.38e-5, 0.23e-5, 203, 1.93e-5, 0.14e-5, 31, 2.13e-6, 0.38e-6),
    48: (731, 6.27e-5, 0.23e-5, 188, 1.81e-5, 0.13e-5, 47, 2.87e-6, 0.42e-6),
    50: (726, 6.25e-5, 0.23e-5, 173, 1.66e-5, 0.13e-5, 41, 2.36e-6, 0.37e-6),
    52: (651, 5.52e-5, 0.22e-5, 160, 1.57e-5, 0.12e-5, 43, 2.60e-6, 0.40e-6),
    54: (628, 5.37e-5, 0.21e-5, 139, 1.37e-5, 0.11e-5, 34, 2.09e-6, 0.36e-6),
    56: (621, 5.33e-5, 0.21e-5, 151, 1.38e-5, 0.11e-5, 37, 2.08e-6, 0.34e-6),
    58: (565, 4.97e-5, 0.21e-5, 151, 1.54e-5, 0.13e-5, 31, 1.94e-6, 0.35e-6),
    60: (548, 4.81e-5, 0.21e-5, 122, 1.19e-5, 0.11e-5, 27, 1.79e-6, 0.35e-6),
    62: (477, 4.11e-5, 0.19e-5, 126, 1.21e-5, 0.11e-5, 34, 2.11e-6, 0.36e-6),
    64: (424, 3.65e-5, 0.18e-5, 129, 1.20e-5, 0.11e-5, 25, 1.64e-6, 0.33e-6),
    66: (419, 3.68e-5, 0.18e-5, 124, 1.20e-5, 0.11e-5, 37, 2.21e-6, 0.36e-6),
    68: (387, 3.39e-5, 0.17e-5, 132, 1.27e-5, 0.11e-5, 38, 2.41e-6, 0.39e-6),
    70: (343, 2.86e-5, 0.15e-5, 112, 1.02e-5, 0.10e-5, 31, 1.88e-6, 0.34e-6),
    72: (319, 2.60e-5, 0.15e-5, 112, 9.97e-6, 0.94e-6, 27, 1.50e-6, 0.29e-6),
    74: (287, 2.36e-5, 0.14e-5, 89, 7.79e-6, 0.83e-6, 31, 1.79e-6, 0.32e-6),
    76: (208, 1.64e-5, 0.11e-5, 79, 7.01e-6, 0.79e-6, 24, 1.34e-6, 0.27e-6),
    78: (175, 1.36e-5, 0.10e-5, 60, 4.80e-6, 0.62e-6, 21, 1.24e-6, 0.27e-6),
    80: (81, 1.13e-5, 0.13e-5, 33, 4.99e-6, 0.87e-6, 15, 1.37e-6, 0.35e-6),
}

RAW_FINE_SCAN = []
for _theta in _FINE_THETA:
    _row = _FINE_ROWS[_theta]
    _tmin = 0 if _theta == 0 else _theta - 1
    _tmax = 1 if _theta == 0 else _theta + 1
    RAW_FINE_SCAN.append(
        FineScanRow(
            theta_center=_theta, theta_min=_tmin, theta_max=_tmax,
            momentum=[12.5, 22.5, 45.0],
            momentum_halfwidth=[2.5, 2.5, 5.0],
            measured_number=[_row[0], _row[3], _row[6]],
            intensity=[_row[1], _row[4], _row[7]],
            stat_error=[_row[2], _row[5], _row[8]],
        )
    )


# ---------------------------------------------------------------------------
# TRANSFORM -- turns the RAW arrays above into flat row dicts matching the
# compilation database.
# ---------------------------------------------------------------------------

EXPERIMENT = "OKAYAMA"
REFERENCE = "Tsuji et al. 1998"
AZIMUTH = "Northwest-Southeast"
ALTITUDE_M = 0
STAT_ONLY_NOTE = (
    "Statistical error only, as stated in the source text (p1810: "
    "'The error bars show statistical errors only.'); no systematic "
    "error is reported anywhere in the source paper."
)

def _wide_bin_rows(bin_: WideBin) -> list:
    """Expand one WideBin into row dicts, skipping '--' (None) cells."""
    rows = []
    n = len(bin_.momentum)
    for i in range(n):
        intensity = bin_.intensity[i]
        if intensity is None:
            # printed "--": genuinely no measurement
            continue
        notes = (
            f"Wide momentum-scan bin from {bin_.source_table} (p{bin_.source_page}); "
            f"theta bin printed as {bin_.theta_center} deg "
            f"({'+' if bin_.theta_center == 0 else '+-'}"
            f"{bin_.theta_max - bin_.theta_center} deg); "
            f"momentum bin printed as {bin_.momentum_min[i]}-{bin_.momentum_max[i]} GeV/c."
        )

        key = (EXPERIMENT, bin_.theta_center, bin_.momentum[i], intensity)
        rows.append(dict(
            experiment=EXPERIMENT,
            reference=REFERENCE,
            theta_center=bin_.theta_center,
            theta_min=bin_.theta_min,
            theta_max=bin_.theta_max,
            azimuth=AZIMUTH,
            altitude_m=ALTITUDE_M,
            momentum=bin_.momentum[i],
            momentum_min=bin_.momentum_min[i],
            momentum_max=bin_.momentum_max[i],
            intensity=intensity,
            stat_error=bin_.stat_error[i],
            sys_error=None,
            error_note=STAT_ONLY_NOTE,
            source_table=bin_.source_table,
            measured_number=bin_.measured_number[i],
            notes=notes,
            _dedupe_key=key,
        ))
    return rows


def _fine_scan_rows(row: FineScanRow) -> list:
    """Expand one FineScanRow (Table 2) into row dicts."""
    rows = []
    for i in range(3):
        intensity = row.intensity[i]
        if intensity is None:
            continue
        hw = row.momentum_halfwidth[i]
        notes = (
            "Fine zenith-scan bin from Table 2 (p1807-1808); theta bin "
            f"printed as {row.theta_center} deg "
            f"({'+' if row.theta_center == 0 else '+-'}"
            f"{row.theta_max - row.theta_center} deg); momentum window "
            f"printed as {row.momentum[i]}+-{hw} GeV/c "
            f"(equivalent to a {row.momentum[i]-hw}-{row.momentum[i]+hw} GeV/c bin). "
        )
        key = (EXPERIMENT, row.theta_center, row.momentum[i], intensity)
        rows.append(dict(
            experiment=EXPERIMENT,
            reference=REFERENCE,
            theta_center=row.theta_center,
            theta_min=row.theta_min,
            theta_max=row.theta_max,
            azimuth=AZIMUTH,
            altitude_m=ALTITUDE_M,
            momentum=row.momentum[i],
            momentum_min=row.momentum[i] - hw,
            momentum_max=row.momentum[i] + hw,
            intensity=intensity,
            stat_error=row.stat_error[i],
            sys_error=None,
            error_note=STAT_ONLY_NOTE,
            source_table="Table 2, Tsuji et al. 1998",
            measured_number=row.measured_number[i],
            notes=notes,
            _dedupe_key=key,
        ))
    return rows


def transform(include_80deg: bool = True, dedupe: bool = True) -> list:
    """
    Build the flat list of row dictionaries for the OKAYAMA experiment.

    Parameters
    ----------
    include_80deg : bool
        Include the θ = 80° measurements from Tables 2 and 3.
        Default is True because the source paper contains these measurements.

    dedupe : bool
        Remove exact duplicate measurements occurring between Table 2 and
        Tables 3-5. Only rows with identical theta, momentum, and intensity
        values are removed.

    Returns
    -------
    list[dict]
        One dictionary per measurement with keys:
        experiment, reference, theta_center, theta_min, theta_max, azimuth,
        altitude_m, momentum, momentum_min, momentum_max, intensity,
        stat_error, sys_error, error_note, source_table, notes,
        measured_number.
    """
    rows = []

    # 1. Wide momentum-scan bins (Tables 3, 4, 5).
    for bin_ in RAW_WIDE_BINS:
        if not include_80deg and bin_.theta_center == 80:
            continue
        rows.extend(_wide_bin_rows(bin_))

    # 2. Fine zenith-scan bins (Table 2).
    for row in RAW_FINE_SCAN:
        if not include_80deg and row.theta_center == 80:
            continue
        rows.extend(_fine_scan_rows(row))

    if dedupe:
        seen = set()
        deduped = []
        for r in rows:
            k = r["_dedupe_key"]
            if k in seen:
                continue
            seen.add(k)
            deduped.append(r)
        rows = deduped

    # Strip the internal bookkeeping key before returning to callers.
    for r in rows:
        r.pop("_dedupe_key", None)

    return rows

# ---------------------------------------------------------------------------
# PRINT
# ---------------------------------------------------------------------------

def print_raw_tables():
    """Print raw transcribed tables."""

    print("RAW_WIDE_BINS")
    print("=" * 100)

    for bin_ in RAW_WIDE_BINS:
        print()
        print(
            f"{bin_.source_table}  "
            f"theta={bin_.theta_center} deg "
            f"({bin_.theta_min}-{bin_.theta_max} deg)"
        )

        print(
            f"{'p(GeV/c)':>10} "
            f"{'p_min':>10} "
            f"{'p_max':>10} "
            f"{'N':>8} "
            f"{'Intensity':>15} "
            f"{'Stat err':>15}"
        )

        for pmin, pmax, p, n, i, e in zip(
            bin_.momentum_min,
            bin_.momentum_max,
            bin_.momentum,
            bin_.measured_number,
            bin_.intensity,
            bin_.stat_error,
        ):
            print(
                f"{p:10.2f} "
                f"{pmin:10.2f} "
                f"{pmax:10.2f} "
                f"{str(n):>8} "
                f"{str(i):>15} "
                f"{str(e):>15}"
            )


    print()
    print("RAW_FINE_SCAN")
    print("=" * 100)

    for row in RAW_FINE_SCAN:
        print()
        print(
            f"Table 2  theta={row.theta_center} deg "
            f"({row.theta_min}-{row.theta_max} deg)"
        )

        print(
            f"{'p(GeV/c)':>10} "
            f"{'N':>8} "
            f"{'Intensity':>15} "
            f"{'Stat err':>15}"
        )

        for p, n, i, e in zip(
            row.momentum,
            row.measured_number,
            row.intensity,
            row.stat_error,
        ):
            print(
                f"{p:10.2f} "
                f"{n:8} "
                f"{i:15.5e} "
                f"{e:15.5e}"
            )


def print_transformed_data():
    """Print flattened database rows from transform()."""

    data = transform(include_80deg=True, dedupe=True)

    print("TRANSFORMED OKAYAMA DATA")
    print("=" * 100)

    print(
        f"{'theta':>8} "
        f"{'p':>10} "
        f"{'p_min':>10} "
        f"{'p_max':>10} "
        f"{'Intensity':>15} "
        f"{'Stat err':>15} "
        f"{'N':>8} "
        f"{'source':>12}"
    )

    for r in data:
        print(
            f"{r['theta_center']:8.1f} "
            f"{r['momentum']:10.2f} "
            f"{str(r['momentum_min']):>10} "
            f"{str(r['momentum_max']):>10} "
            f"{r['intensity']:15.5e} "
            f"{r['stat_error']:15.5e} "
            f"{str(r['measured_number']):>8} "
            f"{r['source_table']:>12}"
        )


def find_true_duplicates() -> list:
    """
    Compare overlapping measurements between Table 2 and Tables 3-5.
    Rows are matched by (theta_center, momentum). The returned list
    identifies whether each overlap is an exact duplicate based on the
    published intensity value.

    Returns
    -------
    list[dict]
        Diagnostic information for overlapping cells, including the
        intensities, event counts, source table, and duplicate status.
    """
    wide = []
    for bin_ in RAW_WIDE_BINS:
        wide.extend(_wide_bin_rows(bin_))
    fine = []
    for row in RAW_FINE_SCAN:
        fine.extend(_fine_scan_rows(row))

    wide_by_key = {}
    for r in wide:
        wide_by_key.setdefault((r["theta_center"], r["momentum"]), []).append(r)

    report = []
    for r in fine:
        cand = wide_by_key.get((r["theta_center"], r["momentum"]))
        if not cand:
            continue
        for w in cand:
            exact = (w["intensity"] == r["intensity"])
            report.append(dict(
                theta_center=r["theta_center"],
                momentum=r["momentum"],
                fine_scan_intensity=r["intensity"],
                fine_scan_N=r["measured_number"],
                wide_bin_intensity=w["intensity"],
                wide_bin_N=w["measured_number"],
                wide_bin_source_table=w["source_table"],
                exact_duplicate=exact,
            ))
    return report


if __name__ == "__main__":
    all_rows_with_80 = transform(include_80deg=True, dedupe=True)
    all_rows_without_80 = transform(include_80deg=False, dedupe=True)
    all_rows_with_80_nodedupe = transform(include_80deg=True, dedupe=False)

    print("OKAYAMA (Tsuji et al. 1998) row counts")
    print("-" * 50)
    print(f"  including 80 deg bin, deduped:     {len(all_rows_with_80)}")
    print(f"  excluding 80 deg bin, deduped:     {len(all_rows_without_80)}")
    print(f"  including 80 deg bin, NOT deduped: {len(all_rows_with_80_nodedupe)}")
    print(
        f"  rows removed by dedup:             "
        f"{len(all_rows_with_80_nodedupe) - len(all_rows_with_80)}"
    )
    print()

    #print_raw_tables()
    #print_transformed_data()
