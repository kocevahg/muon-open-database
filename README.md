# Atmospheric Muon Differential Spectra Database

An open, source-verified database of atmospheric muon differential momentum
spectra compiled from nine historical cosmic-ray experiments, together with
the pipeline that builds it and a desktop app for exploring it.

Companion code for the paper *An open database of the energy and angular distribution of atmospheric muons, with emphasis on large zenith angles*, submitted to *Astroparticle
Physics*.

## Repository layout

```
.
├── raw_deis.py                  # per-experiment transcription + transform()
├── raw_amh.py
├── raw_okayama.py
├── raw_kieldesy.py
├── raw_mutron.py
├── raw_l3c.py
├── raw_depascale.py
├── raw_kellogg.py
├── raw_nottingham.py
├── build_database.py            # runs all nine transform()s, writes the databases
├── muon_spectrum_visualization.py   # PyQt6 desktop viewer
├── overlap_analysis.py          # cross-dataset chi2/ratio comparisons
├── coverage_plot.py             # angle-vs-momentum coverage scatter plot
└── README.md
```

### `raw_<experiment>.py`

One module per experiment. Each contains:

- **`RAW_TABLE*`** — the data exactly as printed in the source paper's
  table(s), in the paper's own units, with no conversion or combination.
  Every value is annotated with its source table and page number.
- **`transform()`** — converts the raw table into the database's common
  schema: momentum in GeV/c, intensity in cm⁻² s⁻¹ sr⁻¹ (GeV/c)⁻¹, with
  statistical and systematic uncertainties kept separate.


### `build_database.py`

Calls each experiment module's `transform()`, collects the rows, and writes
out two SQLite databases plus CSV exports (standard-library only -
`sqlite3` and `csv`):

- **`muon_data.db` / `muon_data.csv`** - the processed database: one row per
  (experiment, angle, momentum) measurement, in common units, with a
  `total_error = sqrt(stat_error² + sys_error²)` column computed centrally.
  A `data_dictionary` table describing every column is embedded in the
  `.db` file itself. A `UNIQUE` constraint prevents duplicate rows.
- **`muon_data_raw.db` / `muon_data_raw.csv`** - a literal dump of every
  `RAW_*` table, before any unit conversion, for checking the pipeline
  against the original papers.
- **`sources.csv`** - one row per experiment with its reference, row count,
  and a short description.

```bash
python build_database.py
```

Safe to re-run - existing databases are deleted and rebuilt from scratch
each time.

### `muon_spectrum_visualization.py`

A PyQt6 desktop app for browsing the database interactively: a hierarchical
experiment -> angle tree for selecting which spectra to plot, a log-log
matplotlib canvas, and a choice of statistical / systematic / total error
bars.

```bash
pip install PyQt6 matplotlib numpy
python muon_spectrum_visualization.py
```

### `overlap_analysis.py`

For every pair of experiments that overlap in both zenith angle and
momentum, this script auto-detects the best-matched overlap region,
interpolates in log-log space, and reports a χ²/ndf and intensity ratio -
a quantitative check of agreement or discrepancy between independent
measurements.

```bash
python overlap_analysis.py
```

Writes `overlap_ratios.png` / `.svg` (ratio plots with 1σ bands) and
`overlap_summary.csv` (χ²/ndf and mean ratio per comparison pair).

### `coverage_plot.py`

Produces a scatter plot of zenith angle vs. momentum for every measurement
in the database, showing which (angle, momentum) regions each experiment
covers.

```bash
python coverage_plot.py
```

## Requirements

- Python 3.9+
- Standard library only for `build_database.py`
- `numpy`, `matplotlib` for analysis and plotting scripts
- `PyQt6` additionally for `muon_spectrum_visualization.py`
- `pandas` for `coverage_plot.py`

```bash
pip install numpy matplotlib pandas PyQt6
```

## Quick start

```bash
python build_database.py                 # builds muon_data.db
python muon_spectrum_visualization.py     # explore it interactively
python overlap_analysis.py                # cross-dataset consistency checks
python coverage_plot.py                   # angle/momentum coverage map
```

## Citation

If you use this database, please cite:

> Khirstina Kotseva, Sergey Gorbunov, "An open database of the energy and angular distribution of atmospheric muons, with emphasis on large zenith angles", *Astroparticle Physics* (in review)

## License

[Add a license, e.g. MIT]
