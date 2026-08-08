"""
(Allkofer, O.C., Bella, G., Dau, W.D., Jokisch, H., Klemke, G., Oren, Y.,
Uhr, R. "Cosmic ray muon spectra at sea-level up to 10 TeV," Nucl. Phys. B
259 (1985) 1-18.)

SOURCE SECTIONS USED (page numbers refer to Nucl. Phys. B 259 (1985) 1-18):
----------------------------------------------------------------------
  - Table 1, p.3            : spectrometer parameters (viewing direction,
                               azimuth, open angle, magnetic field).
  - Table 2, p.11            : "The measured corrected muon fluxes
                               N(p_mu, theta)" -- base spectrum for the
                               full 78.15-90 deg aperture, plus 8
                               multiplicative angular scale factors, plus
                               point-to-point (statistical) errors in %.
  - Sec. 5.1 "ERRORS", p.12-13 : point-to-point (statistical) error
                               definition; B-field-calibration systematic
                               (momentum dependent); absolute-normalization
                               systematic (3.1%, => 4.5% total at 1 TeV/c);
                               low-momentum multiple-scattering / dE/dx
                               correction-uncertainty (momentum dependent,
                               <60 GeV/c only).
  - Fig. 4, p.12             : confirms the 8 bin-center labels
                               (79, 81, 83, 85, 86.5, 87.5, 88.5, 89.5 deg)
                               used as human-readable names for the 8
                               Table 2 angular columns.

Table 2, p.11
----------------------------------------------------------------------
Table 2 has 26 momentum rows (I = 1..26) x 9 intensity/scale columns x 2
lines (value + error %)

Table 2's footnote (p.11) states explicitly: column 3, first line of each
momentum-bin pair, is "the differential intensity in the total zenith
range 78.15 < theta < 90" in units of (GeV/c)^-1 s^-1 sr^-1 cm^-2.
The following 8 columns are dimensionless multiplicative scale factors,
one per zenith bin, to be applied to that same base N(p) to get the intensity
for that particular zenith bin.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# 1. RAW_BASE_SPECTRUM  (Table 2, p.11, column headed "78.15 deg - 90 deg")
# ---------------------------------------------------------------------------
# Quantity tabulated: N(p) = differential muon intensity for the FULL
# 78.15-90 deg aperture.
# Units as printed: (GeV/c)^-1 s^-1 sr^-1 cm^-2  (see discussion above).
# momentum_low/high are the bin edges (GeV/c), exactly as printed.
# stat_error_pct is the "point-to-point" statistical error in %, printed on
# the line directly below each intensity value (Table 2 footnote, p.11).
#
# Each entry: (row_index_I, p_low, p_high, intensity, stat_error_pct)

RAW_BASE_SPECTRUM = [
    (1, 10.8, 12.6, 1.37e-06, 0.65),
    (2, 12.6, 15.8, 1.30e-06, 0.50),
    (3, 15.8, 20.0, 1.15e-06, 0.42),
    (4, 20.0, 25.1, 1.08e-06, 0.38),
    (5, 25.1, 31.6, 8.76e-07, 0.35),
    (6, 31.6, 39.8, 6.99e-07, 0.34),
    (7, 39.8, 50.1, 5.34e-07, 0.33),
    (8, 50.1, 63.1, 3.90e-07, 0.34),
    (9, 63.1, 79.4, 2.72e-07, 0.35),
    (10, 79.4, 100.0, 1.84e-07, 0.38),
    (11, 100.0, 125.9, 1.19e-07, 0.41),
    (12, 125.9, 158.5, 7.44e-08, 0.46),
    (13, 158.5, 199.5, 4.45e-08, 0.53),
    (14, 199.5, 251.2, 2.62e-08, 0.61),
    (15, 251.2, 316.2, 1.50e-08, 0.75),
    (16, 316.2, 398.1, 8.16e-09, 0.87),
    (17, 398.1, 501.2, 4.31e-09, 1.06),
    (18, 501.2, 631.0, 2.20e-09, 1.32),
    (19, 631.0, 793.4, 1.12e-09, 1.64),
    (20, 793.4, 1000.0, 5.67e-10, 2.05),
    (21, 1000.0, 1258.9, 2.63e-10, 2.67),
    (22, 1258.9, 1584.9, 1.18e-10, 3.54),
    (23, 1584.9, 2511.9, 3.90e-11, 3.66),
    (24, 2511.9, 3981.1, 9.31e-12, 5.61),
    (25, 3981.1, 6309.6, 2.14e-12, 8.27),
    (26, 6309.6, 10000.0, 4.69e-13, 11.47),
]

# ---------------------------------------------------------------------------
# 2. RAW_SCALE_FACTORS  (Table 2, p.11, the 8 columns to the right of the
#    base spectrum). Each is a dimensionless multiplier: intensity(theta) =
#    base_intensity(p) * scale_factor(theta_bin, p).
# ---------------------------------------------------------------------------
# Bin definitions per Sec. 3.3 (p.6): "The muons were binned according to
# their zenith-angle theta (west: 78.15-80; 80-82; 82-84; 84-86; 86-87;
# 87-88; 88-89; 89-90; east: 88-89)". The 8 columns of Table 2 are the
# WEST-viewed bins listed there;

ANGULAR_BINS = [
    {"key": "78-80", "label": "79.0", "theta_min": 78.15, "theta_max": 80.0},
    {"key": "80-82", "label": "81.0", "theta_min": 80.0, "theta_max": 82.0},
    {"key": "82-84", "label": "83.0", "theta_min": 82.0, "theta_max": 84.0},
    {"key": "84-86", "label": "85.0", "theta_min": 84.0, "theta_max": 86.0},
    {"key": "86-87", "label": "86.5", "theta_min": 86.0, "theta_max": 87.0},
    {"key": "87-88", "label": "87.5", "theta_min": 87.0, "theta_max": 88.0},
    {"key": "88-89", "label": "88.5", "theta_min": 88.0, "theta_max": 89.0},
    {"key": "89-90", "label": "89.5", "theta_min": 89.0, "theta_max": 90.0},
]

# RAW_SCALE_FACTORS[row_index_I][column_key] = (scale_factor, error_percent)
# error_percent is the "point-to-point" statistical error on the derived
# angular-bin intensity (base*scale), printed on the line directly

RAW_SCALE_FACTORS = {
    1: {"78-80": (6.09, 1.01), "80-82": (3.35, 1.14), "82-84": (2.03, 1.64), "84-86": (0.97, 2.65),
        "86-87": (0.45, 4.68), "87-88": (0.24, 5.40), "88-89": (0.13, 6.18), "89-90": (0.07, 7.17)},
    2: {"78-80": (4.98, 0.88), "80-82": (3.00, 0.91), "82-84": (1.87, 1.13), "84-86": (0.99, 1.50),
        "86-87": (0.51, 2.74), "87-88": (0.30, 3.38), "88-89": (0.17, 4.12), "89-90": (0.08, 5.57)},
    3: {"78-80": (4.46, 0.85), "80-82": (3.02, 0.80), "82-84": (1.89, 0.86), "84-86": (1.06, 1.08),
        "86-87": (0.54, 2.07), "87-88": (0.34, 2.60), "88-89": (0.19, 3.47), "89-90": (0.10, 4.78)},
    4: {"78-80": (3.47, 0.87), "80-82": (2.57, 0.74), "82-84": (1.71, 0.72), "84-86": (0.99, 0.89),
        "86-87": (0.55, 1.66), "87-88": (0.37, 2.05), "88-89": (0.20, 2.95), "89-90": (0.10, 4.39)},
    5: {"78-80": (3.04, 0.93), "80-82": (2.31, 0.93), "82-84": (1.61, 0.65), "84-86": (0.94, 0.79),
        "86-87": (0.59, 1.43), "87-88": (0.38, 1.86), "88-89": (0.23, 2.57), "89-90": (0.12, 3.94)},
    6: {"78-80": (2.63, 0.99), "80-82": (2.07, 0.99), "82-84": (1.53, 0.62), "84-86": (0.98, 0.72),
        "86-87": (0.64, 1.30), "87-88": (0.44, 1.67), "88-89": (0.26, 2.37), "89-90": (0.14, 3.57)},
    7: {"78-80": (2.27, 1.07), "80-82": (1.85, 0.70), "82-84": (1.41, 0.61), "84-86": (0.99, 0.68),
        "86-87": (0.68, 1.22), "87-88": (0.47, 1.60), "88-89": (0.30, 2.15), "89-90": (0.18, 3.13)},
    8: {"78-80": (2.04, 1.14), "80-82": (1.70, 0.73), "82-84": (1.37, 0.63), "84-86": (0.98, 0.67),
        "86-87": (0.71, 1.18), "87-88": (0.51, 1.52), "88-89": (0.34, 2.07), "89-90": (0.20, 3.04)},
    9: {"78-80": (1.79, 1.28), "80-82": (1.60, 0.77), "82-84": (1.31, 0.67), "84-86": (0.99, 0.68),
        "86-87": (0.75, 1.20), "87-88": (0.54, 1.51), "88-89": (0.38, 2.02), "89-90": (0.23, 2.97)},
    10: {"78-80": (1.62, 1.43), "80-82": (1.46, 0.86), "82-84": (1.25, 0.72), "84-86": (0.99, 0.73),
         "86-87": (0.75, 1.25), "87-88": (0.60, 1.54), "88-89": (0.43, 2.03), "89-90": (0.27, 2.95)},
    11: {"78-80": (1.42, 1.66), "80-82": (1.35, 0.97), "82-84": (1.21, 0.81), "84-86": (0.97, 0.79),
         "86-87": (0.78, 1.34), "87-88": (0.64, 1.62), "88-89": (0.47, 2.14), "89-90": (0.34, 2.91)},
    12: {"78-80": (1.34, 1.91), "80-82": (1.26, 1.12), "82-84": (1.15, 0.92), "84-86": (0.97, 0.88),
         "86-87": (0.82, 1.46), "87-88": (0.70, 1.74), "88-89": (0.54, 2.22), "89-90": (0.37, 3.11)},
    13: {"78-80": (1.18, 2.32), "80-82": (1.20, 1.32), "82-84": (1.11, 1.07), "84-86": (0.98, 1.0),
         "86-87": (0.85, 1.63), "87-88": (0.72, 1.96), "88-89": (0.60, 2.40), "89-90": (0.44, 3.25)},
    14: {"78-80": (1.13, 2.75), "80-82": (1.16, 1.54), "82-84": (1.07, 1.26), "84-86": (0.98, 1.16),
         "86-87": (0.88, 1.87), "87-88": (0.75, 2.21), "88-89": (0.63, 2.71), "89-90": (0.48, 3.61)},
    15: {"78-80": (1.11, 3.27), "80-82": (1.07, 1.88), "82-84": (1.04, 1.50), "84-86": (0.98, 1.36),
         "86-87": (0.91, 2.14), "87-88": (0.81, 2.49), "88-89": (0.68, 3.06), "89-90": (0.54, 3.99)},
    16: {"78-80": (1.06, 4.04), "80-82": (1.01, 2.34), "82-84": (1.04, 1.81), "84-86": (1.00, 1.62),
         "86-87": (0.88, 2.62), "87-88": (0.84, 2.95), "88-89": (0.77, 3.45), "89-90": (0.58, 4.62)},
    17: {"78-80": (0.88, 5.41), "80-82": (1.00, 2.88), "82-84": (1.00, 2.25), "84-86": (0.98, 2.00),
         "86-87": (0.93, 3.11), "87-88": (0.94, 3.42), "88-89": (0.81, 4.15), "89-90": (0.68, 5.26)},
    18: {"78-80": (0.92, 6.60), "80-82": (0.92, 3.74), "82-84": (1.02, 2.77), "84-86": (1.00, 2.45),
         "86-87": (0.91, 3.92), "87-88": (0.93, 4.27), "88-89": (0.78, 5.23), "89-90": (0.80, 5.97)},
    19: {"78-80": (0.96, 8.07), "80-82": (0.95, 4.58), "82-84": (0.97, 3.54), "84-86": (1.00, 3.07),
         "86-87": (0.90, 4.91), "87-88": (0.93, 5.31), "88-89": (0.84, 6.27), "89-90": (0.82, 7.37)},
    20: {"78-80": (0.86, 10.61), "80-82": (0.93, 5.79), "82-84": (1.05, 4.26), "84-86": (0.98, 3.86),
         "86-87": (0.93, 6.03), "87-88": (0.91, 6.72), "88-89": (0.79, 8.10), "89-90": (0.84, 9.08)},
    21: {"78-80": (1.02, 12.71), "80-82": (1.02, 7.27), "82-84": (0.88, 6.06), "84-86": (0.96, 5.12),
         "86-87": (0.99, 7.62), "87-88": (0.95, 8.57), "88-89": (0.92, 9.79), "89-90": (0.95, 11.20)},
    22: {"78-80": (1.04, 16.67), "80-82": (0.84, 10.54), "82-84": (0.94, 7.77), "84-86": (1.01, 6.59),
         "86-87": (0.88, 10.77), "87-88": (1.02, 11.00), "88-89": (1.14, 11.63), "89-90": (0.77, 16.43)},
    23: {"78-80": (0.58, 22.93), "80-82": (0.81, 11.04), "82-84": (0.84, 8.50), "84-86": (1.03, 6.72),
         "86-87": (1.13, 9.79), "87-88": (1.13, 10.79), "88-89": (0.99, 12.91), "89-90": (0.85, 16.23)},
    24: {"78-80": (0.50, 37.82), "80-82": (1.00, 15.30), "82-84": (0.91, 12.49), "84-86": (0.93, 10.92),
         "86-87": (1.00, 16.06), "87-88": (1.15, 16.45), "88-89": (0.98, 19.96), "89-90": (1.02, 22.91)},
    25: {"78-80": (0.78, 44.72), "80-82": (0.86, 24.32), "82-84": (0.71, 20.78), "84-86": (1.35, 13.36),
         "86-87": (0.73, 27.64), "87-88": (0.82, 28.97), "88-89": (0.61, 37.69), "89-90": (1.53, 27.74)},
    26: {"78-80": (1.19, 50.00), "80-82": (1.06, 30.18), "82-84": (0.77, 27.62), "84-86": (0.88, 22.91),
         "86-87": (1.51, 26.76), "87-88": (0.79, 40.81), "88-89": (1.00, 40.85), "89-90": (0.68, 57.81)},
}

# ---------------------------------------------------------------------------
# 3. RAW_SYSTEMATICS  (Sec. 5.1 "ERRORS", p.12-13, and Table 1 / p.4)
# ---------------------------------------------------------------------------
# These are explicitly not part of the "point-to-point" statistical errors
# tabulated in Table 2. The paper is careful to separate them (p.12:
# "The errors quoted in table 2 and the following figures are
# point-to-point errors which are due to statistical fluctuations."),
# and this module keeps them separate too.

# 3.1. Absolute normalization uncertainty (p.12): "From the normalization
# procedure for the top and bottom telescopes of the spectrometer for
# positive and negative magnetic field strengths corrections for the
# absolute flux can be obtained with 3.1% [uncertainty]".
NORMALIZATION_UNCERTAINTY_PCT = 3.1

# 3.2. Magnetic-field calibration uncertainty (p.12): "An uncertainty in
# the magnetic field B of 1% leads to momentum dependent errors in the
# spectrum: 1.3% at 50 GeV/c; 1.9% at 100 GeV/c; and 3.3% at 1 TeV/c."
# Combined with the 3.1% normalization term in quadrature the paper
# quotes "a total error of 4.5% at 1 TeV/c":
# sqrt(3.3^2 + 3.1^2) = 4.53% ~ 4.5%
BFIELD_UNCERTAINTY_ANCHORS_GEV = [
    (50.0, 1.3),
    (100.0, 1.9),
    (1000.0, 3.3),
]

# 3.3. Low-momentum multiple-scattering / dE/dx correction uncertainty
# (p.12-13): "Below p_mu = 60 GeV/c the error increased because of
# multiple scattering and energy losses dE/dx. The estimate of this error
# is 1% at p_mu = 45 GeV/c, 5% at p_mu = 20 GeV/c, and 20% at
# p_mu = 10 GeV/c."
MULTIPLE_SCATTERING_UNCERTAINTY_ANCHORS_GEV = [
    (10.0, 20.0),
    (20.0, 5.0),
    (45.0, 1.0),
    # The paper does not quote a number above 45 GeV/c, only the
    # qualitative statement that the error "increased below p=60 GeV/c"
    (60.0, 0.0),  # not printed in the paper as a numeric value
]

# 3.4. Azimuth / viewing-direction caveat (Table 1 p.3, "Trigger system"
# p.4, and Sec. 3.3 p.6).
# The DEIS spectrometer axis points "nearly to the west" (p.2); Table 1
# (p.3) lists the pointing direction as "85 deg zenith; 266 deg azimuth"
# with an open angle of "+/-8 deg zenith; +/-22 deg azimuth".
AZIMUTH_NOTE = (
    "DEIS spectrometer points west (Table 1, p.3: 85° zenith, 266° azimuth, "
    "±8° zenith × ±22° azimuth aperture; p.2 gives 86° azimuth using the "
    "opposite direction convention). All 8 Table 2 bins are west-viewed. "
    "TOF identifies ~95% west and ~4% east events (p.4). A separate east "
    "88–89° bin is used only as a cross-check (Sec. 3.3, p.6) and is not "
    "included in Table 2."
)


# ---------------------------------------------------------------------------
# 3.5. Helper: turn the momentum-anchored uncertainty tables above into a
# usable per-point percentage via log-log linear interpolation.
# ---------------------------------------------------------------------------
def _interp_pct(anchors, p):
    """Interpolate a percentage error vs. momentum from (p_GeV, pct) anchor
    points, linear in log10(p). Outside the quoted range the value is HELD
    FLAT at the nearest anchor -- the paper only states numbers at these
    anchor points, so we do not extrapolate beyond them (a documented,
    conservative choice, not a value from the paper)."""
    import math

    pts = sorted(anchors)
    if p <= pts[0][0]:
        return pts[0][1]
    if p >= pts[-1][0]:
        return pts[-1][1]
    for (p0, v0), (p1, v1) in zip(pts, pts[1:]):
        if p0 <= p <= p1:
            if p0 == p1 or v0 == v1:
                return v0
            lx0, lx1, lp = math.log10(p0), math.log10(p1), math.log10(p)
            frac = (lp - lx0) / (lx1 - lx0)
            return v0 + frac * (v1 - v0)
    return pts[-1][1]


def systematic_error_pct(momentum: float) -> dict:
    """Combine DEIS's three documented systematic components (Sec. 5.1,
    p.12-13) into one momentum-dependent percentage, in quadrature -- this is
    exactly how the paper itself combines the normalization and B-field terms
    ("sqrt(3.3^2 + 3.1^2) = 4.53% ~ 4.5% at 1 TeV/c", see the comment above
    BFIELD_UNCERTAINTY_ANCHORS_GEV). The multiple-scattering / dE/dx term is
    added in quadrature too, since the paper describes all three as
    independent error sources; it is only non-zero below 60 GeV/c.

    Returns a dict with each component and the combined total, so the
    breakdown stays visible downstream rather than only the final number.
    """
    norm_pct = NORMALIZATION_UNCERTAINTY_PCT
    bfield_pct = _interp_pct(BFIELD_UNCERTAINTY_ANCHORS_GEV, momentum)
    ms_pct = (
        _interp_pct(MULTIPLE_SCATTERING_UNCERTAINTY_ANCHORS_GEV, momentum)
        if momentum < 60.0
        else 0.0
    )
    total_pct = (norm_pct**2 + bfield_pct**2 + ms_pct**2) ** 0.5
    return {
        "normalization_pct": norm_pct,
        "bfield_calibration_pct": round(bfield_pct, 3),
        "multiple_scattering_pct": round(ms_pct, 3),
        "combined_pct": round(total_pct, 3),
    }


# ---------------------------------------------------------------------------
# 4. transform() - turns RAW numbers into unified-format rows.
# ---------------------------------------------------------------------------
def transform() -> list[dict]:
    """Convert the raw DEIS Table 2 values into the common data format.

        1. The momentum value is taken as the arithmetic mean of the published
        momentum-bin edges.

        2. The intensity for each angular bin is calculated as:
                intensity = base_intensity × scale_factor

        3. The statistical uncertainty is taken directly from the percentage
        reported in Table 2 (point-to-point error, Sec. 5.1 p.12):
                stat_error = intensity × error_percent / 100

        4. The systematic uncertainty (Sec. 5.1 "ERRORS", p.12-13) is the
        quadrature combination of the three components the paper documents
        separately -- absolute normalization (3.1%), B-field calibration
        (momentum-dependent, 1.3-3.3%), and, below 60 GeV/c, the low-momentum
        multiple-scattering / dE/dx correction uncertainty (momentum-dependent,
        up to 20% at 10 GeV/c):
                sys_error = intensity × systematic_error_pct(p)["combined_pct"] / 100
        Previously the three components were tabulated above but never combined
        into sys_error, so only the ~0.8-1% statistical bar reached the plot --
        the exact issue raised in reviewer comment 6. Fixed here.

        total_error (= sqrt(stat^2 + sys^2)) is computed centrally in
        build_database.py, not here, so all datasets use one rule.
    """
    rows: list[dict] = []

    for row_index, p_low, p_high, base_intensity, base_stat_pct in RAW_BASE_SPECTRUM:
        momentum_center = (p_low + p_high) / 2.0  # arithmetic mean

        for abin in ANGULAR_BINS:
            key = abin["key"]
            scale_factor, err_pct = RAW_SCALE_FACTORS[row_index][key]
            theta_min, theta_max = abin["theta_min"], abin["theta_max"]
            theta_center = (theta_min + theta_max) / 2.0

            azimuth_note = AZIMUTH_NOTE
            if key == "88-89":
                azimuth_note += (
                    " This particular bin (88-89 deg) is the one for which the "
                    "paper also reports a separate East-viewed measurement "
                    "(Sec. 3.3, p.6) as a cross-check -- not included here."
                )

            if scale_factor is None:
                # Raw data gap
                rows.append({
                    "experiment": "DEIS",
                    "reference": "Allkofer et al. 1985",
                    "theta_center": theta_center,
                    "theta_min": theta_min,
                    "theta_max": theta_max,
                    "azimuth": "west (nominal; see notes)",
                    "altitude_m": 0,
                    "momentum": momentum_center,
                    "momentum_min": p_low,
                    "momentum_max": p_high,
                    "intensity": None,
                    "stat_error": None,
                    "sys_error": None,
                    "sys_components_pct": None,
                    "error_note": (
                        "No value: Table 2 scale factor for this (angle, momentum) "
                        "bin (row I={}, column {}) is missing "
                        "RAW_SCALE_FACTORS.".format(row_index, key)
                    ),
                    "source_table": "Table 2, Allkofer et al. 1985",
                    "notes": azimuth_note,
                })
                continue

            intensity = base_intensity * scale_factor  # see docstring point 2
            stat_error = None if err_pct is None else intensity * (err_pct / 100.0)  # docstring point 3

            # docstring point 4: combine the three documented systematics
            sys_breakdown = systematic_error_pct(momentum_center)
            sys_error = intensity * (sys_breakdown["combined_pct"] / 100.0)

            error_note = (
                "stat = Table 2 point-to-point % (Sec. 5.1). "
                "sys = norm {:.1f}% + B-field {:.2f}% + mult-scatt {:.2f}% "
                "(<60 GeV/c) in quadrature = {:.2f}% (Sec. 5.1)."
            ).format(
                sys_breakdown["normalization_pct"],
                sys_breakdown["bfield_calibration_pct"],
                sys_breakdown["multiple_scattering_pct"],
                sys_breakdown["combined_pct"],
            )

            rows.append({
                "experiment": "DEIS",
                "reference": "Allkofer et al. 1985",
                "theta_center": theta_center,
                "theta_min": theta_min,
                "theta_max": theta_max,
                "azimuth": "west",
                "altitude_m": 0,
                "momentum": momentum_center,
                "momentum_min": p_low,
                "momentum_max": p_high,
                "intensity": intensity,
                "stat_error": stat_error,
                "sys_error": sys_error,
                "sys_components_pct": sys_breakdown,
                "error_note": error_note,
                "source_table": "Table 2, Allkofer et al. 1985",
                "notes": azimuth_note,
            })

    return rows

def print_rawdata():
    # Print the values exactly as stored from the original paper.
    print("RAW BASE SPECTRUM")
    for row in RAW_BASE_SPECTRUM:
        print(row)
    print("\nRAW SCALE FACTORS")
    for row_index, data in RAW_SCALE_FACTORS.items():
        print(row_index, data)


def print_transformed():
    # Print the main quantities for each transformed measurement.
    rows = transform()
    for row in rows:
        print(
            f"theta={row['theta_center']:5.1f}  "
            f"p={row['momentum']:8.2f}  "
            f"I={row['intensity']:.4e}  "
            f"stat={row['stat_error']}"
        )


if __name__ == "__main__":
    all_rows = transform()
    n_total = len(all_rows)
    n_with_data = sum(1 for r in all_rows if r["intensity"] is not None)
    n_gaps = n_total - n_with_data

    print("DEIS transform(): {} rows total".format(
        n_total))

    #print_rawdata()
    #print_transformed()