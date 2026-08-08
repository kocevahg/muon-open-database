"""
(Judge, R. J. R. and Nash, W. F.
"Measurements on the Muon Flux at Various Zenith Angles,"
Il Nuovo Cimento 35 (1965) 999-1024.)

SOURCE SECTIONS USED (page numbers refer to Il Nuovo Cimento 35 (1965) 999-1024):
----------------------------------------------------------------------
  - Table II, p.1013         : measured differential muon intensities
                               for four zenith-angle/azimuth
                               configurations; momentum-bin interval,
                               mean momentum, differential intensity,
                               and quoted uncertainty for each point.
  - Table I, p.1011          : zenith-angle and azimuth labels used to
                               identify the four measured spectra.
  - Sec. 5 "Experimental
    results", p.1013         : description of the published intensity
                               units and treatment of the quoted
                               uncertainties.

Table II, p.1013
----------------------------------------------------------------------
Table II contains 13 momentum bins for each of four measurement
configurations:

    - 30 deg East
    - 45 deg East
    - 60 deg East
    - 60 deg West

Each entry gives:
    - momentum-bin interval (GeV/c),
    - mean momentum (GeV/c),
    - differential intensity,
    - quoted uncertainty.

The intensities are printed in units of:

    10^5 cm^-2 s^-1 sr^-1 (GeV/c)^-1

and are converted to

    cm^-2 s^-1 sr^-1 (GeV/c)^-1

by applying the published scale factor of 10^-5.

The quoted uncertainties are taken directly from Table II. The paper
does not separate statistical and systematic uncertainties or quote a
single overall normalization uncertainty; therefore only the published
uncertainty is recorded.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# RAW_TABLES
# ---------------------------------------------------------------------------
# Exactly as printed in Table II of Judge & Nash (1965), Il Nuovo Cimento 35,
# p. 1013. The paper's own column-header/caption convention is:
#
#     "The measured differential intensities ... in the units
#      10^5 (s^-1 cm^-2 sr^-1 GeV/c^-1) ... are given in Table II."
#
# i.e. every intensity AND error value below must be multiplied by 1e-5 to
# get physical units of (GeV/c)^-1 cm^-2 s^-1 sr^-1. This is a table-caption
# display multiplier (like a plot axis labelled "/1e5"), not a genuine
# area/time/solid-angle unit conversion -- see module docstring.
#
# Momentum bin edges (GeV/c) are shared across all four spectra (Table II,
# "Momentum group" column) and are listed once as MOMENTUM_BIN_EDGES.

MOMENTUM_BIN_EDGES = [
    (0.7, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 8),
    (8, 10), (10, 14), (14, 20), (20, 26), (26, 36), (36, 50),
]

RAW_TABLES = {
    "30E": {
        "theta_center": 30.0,
        "azimuth": "East",
        # mean momentum per bin (GeV/c), as printed
        "momentum": [0.85, 1.5, 2.5, 3.5, 4.5, 5.5, 6.95, 8.83, 11.81, 16.4, 22.5, 29.9, 41],
        # intensity as printed, in units of 1e5 (s^-1 cm^-2 sr^-1 (GeV/c)^-1)
        "intensity_raw": [200, 156, 89.0, 55.5, 37.0, 25.7, 16.8, 9.70, 5.30, 2.54, 1.27, 0.71, 0.35],
        # +/- error as printed, same x1e5 units
        "error_raw": [14, 7, 4.9, 3.8, 3.1, 2.6, 2.1, 1.60, 1.18, 0.80, 0.58, 0.43, 0.30],
        "source_table": "Table II (Judge & Nash 1965, Il Nuovo Cimento 35, p. 1013), column '30 deg East'",
    },
    "45E": {
        "theta_center": 45.0,
        "azimuth": "East",
        "momentum": [0.85, 1.5, 2.5, 3.5, 4.5, 5.5, 7.0, 8.8, 11.9, 16.9, 23.0, 28.25, 42],
        "intensity_raw": [95.8, 77.2, 51.2, 35.7, 26.2, 18.5, 12.0, 9.15, 4.36, 2.38, 1.32, 0.66, 0.27],
        "error_raw": [7.7, 3.7, 2.9, 2.5, 2.1, 1.8, 1.4, 1.24, 0.86, 0.63, 0.47, 0.34, 0.20],
        "source_table": "Table II (Judge & Nash 1965, Il Nuovo Cimento 35, p. 1013), column '45 deg East'",
    },
    "60E": {
        "theta_center": 60.0,
        "azimuth": "East",
        "momentum": [0.85, 1.5, 2.5, 3.5, 4.5, 5.5, 6.93, 9.0, 11.43, 16.46, 22.6, 30.1, 43],
        "intensity_raw": [27.5, 26.7, 26.6, 18.2, 14.1, 12.2, 7.32, 5.44, 3.16, 1.96, 0.85, 0.47, 0.23],
        "error_raw": [2.9, 1.5, 1.5, 1.2, 1.1, 1.0, 0.78, 0.67, 0.51, 0.40, 0.26, 0.19, 0.15],
        "source_table": "Table II (Judge & Nash 1965, Il Nuovo Cimento 35, p. 1013), column '60 deg East'",
    },
    "60W": {
        "theta_center": 60.0,
        "azimuth": "West",
        "momentum": [0.85, 1.5, 2.5, 3.5, 4.5, 5.5, 6.97, 8.85, 11.87, 16.44, 21.9, 31.5, 43],
        "intensity_raw": [32.4, 35.4, 24.3, 20.2, 12.7, 13.0, 7.70, 4.80, 3.31, 1.34, 0.83, 0.45, 0.29],
        "error_raw": [3.4, 2.1, 1.7, 1.6, 1.2, 1.2, 0.86, 0.67, 0.56, 0.36, 0.28, 0.21, 0.17],
        "source_table": "Table II (Judge & Nash 1965, Il Nuovo Cimento 35, p. 1013), column '60 deg West'",
    },
}

# true_intensity [(GeV/c)^-1 cm^-2 s^-1 sr^-1] = tabulated_value * UNIT_CONVERSION_FACTOR
UNIT_CONVERSION_FACTOR = 1e-5


def transform():
    """
    Turn RAW_TABLES into a flat list of row dicts .
    """
    rows = []

    for key, table in RAW_TABLES.items():
        theta_center = table["theta_center"]
        azimuth = table["azimuth"]
        source_table = table["source_table"]

        momenta = table["momentum"]
        intens_raw = table["intensity_raw"]
        errs_raw = table["error_raw"]

        n = len(momenta)

        for i in range(n):
            p_min, p_max = MOMENTUM_BIN_EDGES[i]

            intensity = intens_raw[i] * UNIT_CONVERSION_FACTOR
            error = errs_raw[i] * UNIT_CONVERSION_FACTOR

            rows.append({
                "experiment": "Nottingham",
                "reference": "Judge and Nash, 1965",
                "theta_center": theta_center,

                "theta_min": None,  # not given in paper
                "theta_max": None,  # not given in paper
                "azimuth": azimuth,
                "altitude_m": 0,
                "momentum": momenta[i],
                "momentum_min": p_min,
                "momentum_max": p_max,
                "intensity": intensity,
                "stat_error": None,
                "sys_error": None,
                "error": error,
                "error_note": (
                    "paper does not decompose statistical vs systematic "
                    "uncertainty; tabulated errors used as-is"
                ),
                "source_table": source_table,
                "notes": (
                        "The paper does not report a separate normalization or systematic "
                        "uncertainty. The manuscript notes that this dataset may be "
                        "systematically lower than other measurements."
                ),
            })

    return rows


def print_raw_data() -> None:
    """Print the raw values transcribed from Table II."""

    print("RAW TABLE (as printed)")
    print(
        f"{'theta':>6} {'azimuth':>8} {'p(GeV/c)':>10} "
        f"{'intensity':>12} {'error':>12}"
    )

    for table in RAW_TABLES.values():
        theta = table["theta_center"]
        azimuth = table["azimuth"]

        for p, intensity, error in zip(
            table["momentum"],
            table["intensity_raw"],
            table["error_raw"],
        ):
            print(
                f"{theta:>6.0f} "
                f"{azimuth:>8} "
                f"{p:>10.2f} "
                f"{intensity:>12.2f} "
                f"{error:>12.2f}"
            )


def print_transformed_data(rows) -> None:
    """Print the transformed dataset."""

    print(f"Total rows: {len(rows)}")
    print()
    print(
        f"{'theta':>6} {'azimuth':>8} {'p(GeV/c)':>10} "
        f"{'intensity':>14} {'error':>14}"
    )

    for row in rows:
        print(
            f"{row['theta_center']:>6} "
            f"{row['azimuth']:>8} "
            f"{row['momentum']:>10.1f} "
            f"{row['intensity']:>14.4e} "
            f"{row['error']:>14.4e}"
        )


if __name__ == "__main__":
    #print_raw_data()
    print()
    #print_transformed_data(transform())
