"""
SUMMARY
------------------------------------------
Each raw_<exp>.py file is a hand-transcription of one paper's data table,
plus a transform() function that turns it into a common format. This
script only calls those nine transform() functions, collects what they return,
and writes the result out as a database.
It writes out TWO databases, because a peer reviewer specifically asked
for both:

  * muon_data.db / muon_data.csv - the "processed" data: one row
    per measurement, already converted to common units (GeV/c, and
    intensity per GeV/c per cm^2 per second per steradian).
    This is what the plotting/analysis tool reads.

  * muon_data_raw.db / muon_data_raw.csv - the "as-printed" data: the
    numbers exactly as they appear in each paper's own table, before any
    unit conversion or combination. This exists so a reader can check the
    database against the original publication without having to trust
    the conversion step.

OUTPUTS
------------------------------------------
1. muon_data.db / muon_data.csv
       The unified, converted database. Table `muon_data`, one row per
       (experiment, angle bin, momentum bin) measurement. Momentum is in
       GeV/c; intensity is in (GeV/c)^-1 cm^-2 s^-1 sr^-1. A second table,
       `data_dictionary`, is written into the same .db file and explains
       every column in English.
2. muon_data_raw.db / muon_data_raw.csv
       A generic, literal dump of every RAW_* table defined in each
       raw_<exp>.py module, exactly as transcribed from the source paper,
       BEFORE any unit conversion or combination. Because each
       experiment's raw table has a different shape, this dump does not
       force a single flat schema onto data the original authors did not
       tabulate uniformly -- instead every record's fields are written out
       as plain "label: value" lines.
3. sources.csv
       One row per experiment: reference, row count, and a short
       description.

USAGE
-----
    python build_database.py

dependencies - only the standard library (sqlite3, csv).
Safe to re-run: existing muon_data.db / muon_data_raw.db are deleted and
rebuilt from scratch each time.
"""

from __future__ import annotations

import csv
import dataclasses
import importlib
import os
import sqlite3
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

# Module name -> transform() kwargs. Kwargs are each module's own
# documented defaults except where noted.
EXPERIMENT_MODULES = {
    "raw_deis":        dict(kwargs={}),
    "raw_mutron":      dict(kwargs={}),
    "raw_amh":         dict(kwargs={}),   # default momentum_range=(20,50), the authors own recommended range
    "raw_kieldesy":    dict(kwargs={}),
    "raw_okayama":     dict(kwargs={}),   # default include_80deg=True
    "raw_depascale":   dict(kwargs={}),
    "raw_kellogg":     dict(kwargs={}),
    "raw_l3c":         dict(kwargs={}),
    "raw_nottingham":  dict(kwargs={}),
}


CORE_COLUMNS = [
    "experiment", "reference", "source_table",
    "theta_center", "theta_min", "theta_max",
    "azimuth", "altitude_m",
    "momentum", "momentum_min", "momentum_max",
    "intensity",
    "stat_error", "sys_error", "total_error", "error_note",
    "notes",
]

# English explanation of every column
DATA_DICTIONARY = [
    ("experiment", "Short experiment name."),
    ("reference", "Citation for the source paper."),
    ("source_table", "Which table (and, where relevant, page) of the source paper this row's numbers were read from."),
    ("theta_center", "Zenith angle in degrees (0 = vertical, 90 = horizontal). Paper's reported mean angle where given, else midpoint of theta_min/theta_max."),
    ("theta_min / theta_max", "Zenith-angle bin edges in degrees. NULL where the paper gives only a single angle."),
    ("azimuth", "Horizontal viewing direction (free text)."),
    ("altitude_m", "Observation altitude, meters above sea level."),
    ("momentum", "Muon momentum in GeV/c. Paper's mean/weighted-mean/median where given."),
    ("momentum_min / momentum_max", "Momentum bin edges in GeV/c. NULL where the paper gives only a central momentum."),
    ("intensity", "Differential muon intensity, (GeV/c)^-1 cm^-2 s^-1 sr^-1."),
    ("stat_error", "Statistical (point-to-point) uncertainty on intensity, same units."),
    ("sys_error", "Systematic / normalization uncertainty on intensity, same units, "
                  "quoted as 1 sigma. Kiel-DESY: the +-5% (95% CL) calibration error "
                  "of Jokisch et al. is divided by 1.96 (about 2.55%). NULL where the "
                  "source reports none (AMH, OKAYAMA, Nottingham)."),
    ("total_error", "Combined uncertainty: sqrt(stat^2 + sys^2) where both exist, else "
                    "whichever single component the paper reports. Nottingham stores its "
                    "single published uncertainty here only (stat_error and sys_error are NULL)."),
    ("error_note", "Short note on what this row's errors include."),
    ("notes", "Other caveats: model-dependence, azimuth ambiguity, large-error bins, etc."),
    ("additional_details", "Experiment-specific extras (event counts, De Pascale mu+/mu- split, etc.)."),
]


def _fmt_value(value):
    if value is None:
        return "not available"
    if isinstance(value, float):
        # Keep scientific notation for very small/large numbers
        if value != 0 and (abs(value) < 1e-3 or abs(value) >= 1e6):
            return f"{value:.6g}"
        return f"{value:g}"
    return str(value)


def _to_plain(value):
    """Convert dataclass instances (used by raw_kellogg.py, raw_okayama.py)
    into plain dicts/lists so the readable-text renderer below doesn't
    need to know about any experiment-specific types."""
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {f.name: _to_plain(getattr(value, f.name)) for f in dataclasses.fields(value)}
    if isinstance(value, dict):
        return {k: _to_plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_plain(v) for v in value]
    return value


def render_readable(value, indent=0):
    """Turn any RAW_* constant (dict / list / tuple / dataclass / plain
    value, nested to any depth) into indented, human-readable text.
    """
    value = _to_plain(value)
    pad = "  " * indent
    lines = []
    if isinstance(value, dict):
        for k, v in value.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}{k}:")
                lines.append(render_readable(v, indent + 1))
            else:
                lines.append(f"{pad}{k}: {_fmt_value(v)}")
    elif isinstance(value, list):
        for i, item in enumerate(value):
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}- entry {i + 1}:")
                lines.append(render_readable(item, indent + 1))
            else:
                lines.append(f"{pad}- {_fmt_value(item)}")
    else:
        lines.append(f"{pad}{_fmt_value(value)}")
    return "\n".join(lines)


def render_readable_inline(mapping):
    """Same idea as render_readable(), but for the per-row 'additional_details'
    column in the processed table: one line, semicolon-separated, so it
    stays a single, readable spreadsheet cell. """
    parts = []
    for k, v in mapping.items():
        if isinstance(v, (dict, list, tuple)):
            v = render_readable(v).replace("\n", " / ")
        parts.append(f"{k}: {_fmt_value(v)}")
    return "; ".join(parts) if parts else None


def load_all_rows():
    """Import each raw_<exp> module and call its transform()."""
    all_rows = []
    per_experiment_counts = {}
    load_errors = {}
    modules = {}

    for mod_name, cfg in EXPERIMENT_MODULES.items():
        try:
            mod = importlib.import_module(mod_name)
            modules[mod_name] = mod
        except Exception:
            load_errors[mod_name] = "IMPORT FAILED:\n" + traceback.format_exc()
            continue

        try:
            rows = mod.transform(**cfg["kwargs"])
        except Exception:
            load_errors[mod_name] = "transform() FAILED:\n" + traceback.format_exc()
            continue

        if not rows:
            load_errors[mod_name] = (
                "transform() returned 0 rows -- see the module's own "
                "__main__ output for why (usually: the source "
                "PDF did not contain the numeric table needed)."
            )
            continue

        for r in rows:
            r.setdefault("experiment", mod_name)
            # Papers that report a single undecomposed error (Nottingham) use
            # the key "error"; move it into total_error.
            if "error" in r and r.get("total_error") is None:
                r["total_error"] = r.pop("error")
            # total_error = quadrature sum of whichever components exist.
            if r.get("total_error") is None:
                stat, sys = r.get("stat_error"), r.get("sys_error")
                if stat is not None and sys is not None:
                    r["total_error"] = (stat**2 + sys**2) ** 0.5
                elif stat is not None:
                    r["total_error"] = stat
                elif sys is not None:
                    r["total_error"] = sys
        all_rows.extend(rows)
        per_experiment_counts[mod_name] = len(rows)

    return all_rows, per_experiment_counts, load_errors, modules


def build_processed_database(all_rows, db_path, csv_path):
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE muon_data (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment          TEXT NOT NULL,
            reference           TEXT,
            source_table        TEXT,
            theta_center        REAL,
            theta_min           REAL,
            theta_max           REAL,
            azimuth             TEXT,
            altitude_m          REAL,
            momentum            REAL NOT NULL,
            momentum_min        REAL,
            momentum_max        REAL,
            intensity           REAL,
            stat_error          REAL,
            sys_error           REAL,
            total_error         REAL,
            error_note          TEXT,
            notes               TEXT,
            additional_details  TEXT
        )
    """)
    cur.execute("""
            CREATE UNIQUE INDEX uq_muon_window ON muon_data (
                experiment,
                COALESCE(theta_min, theta_center), COALESCE(theta_max, theta_center),
                COALESCE(momentum_min, momentum),  COALESCE(momentum_max, momentum),
                COALESCE(azimuth, '')
            )
        """)
    # Units and conventions are documented once, here, as plain sentences
    cur.execute("""
        CREATE TABLE data_dictionary (
            column  TEXT PRIMARY KEY,
            meaning TEXT
        )
    """)
    cur.executemany("INSERT INTO data_dictionary VALUES (?, ?)", DATA_DICTIONARY)
    cur.execute("""
        CREATE TABLE data_dictionary_notes (
            note TEXT
        )
    """)
    cur.execute(
        "INSERT INTO data_dictionary_notes VALUES (?)",
        ("A UNIQUE index on (experiment, angular window, momentum window, "
         "azimuth) - prevents the same measurement being stored twice.",),
    )

    n_inserted = 0
    n_duplicate_rejected = 0
    duplicate_examples = []
    for r in all_rows:
        core = {k: r.get(k) for k in CORE_COLUMNS}
        extra = {k: v for k, v in r.items() if k not in CORE_COLUMNS and not k.startswith("_")}
        additional_details = render_readable_inline(extra)
        try:
            cur.execute(
                """INSERT INTO muon_data
                   (experiment, reference, source_table, theta_center, theta_min, theta_max,
                    azimuth, altitude_m, momentum, momentum_min, momentum_max,
                    intensity, stat_error, sys_error, total_error, error_note,
                    notes, additional_details)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    core["experiment"], core["reference"], core["source_table"],
                    core["theta_center"], core["theta_min"], core["theta_max"],
                    core["azimuth"], core["altitude_m"], core["momentum"],
                    core["momentum_min"], core["momentum_max"], core["intensity"],
                    core["stat_error"], core["sys_error"], core["total_error"],
                    core["error_note"], core["notes"], additional_details,
                ),
            )
            n_inserted += 1
        except sqlite3.IntegrityError as e:
            n_duplicate_rejected += 1
            if len(duplicate_examples) < 10:
                duplicate_examples.append((core["experiment"], core["theta_center"], core["momentum"], str(e)))

    conn.commit()

    # CSV export of the same table
    cur.execute("PRAGMA table_info(muon_data)")
    colnames = [c[1] for c in cur.fetchall()]
    cur.execute("SELECT * FROM muon_data ORDER BY experiment, theta_center, momentum")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(colnames)
        w.writerows(cur.fetchall())

    conn.close()
    return n_inserted, n_duplicate_rejected, duplicate_examples


def build_raw_database(modules, db_path, csv_path):
    """Literal dump of every RAW_* module-level constant, exactly as
    transcribed, one row per top-level record of each RAW_* structure (or
    one row for the whole constant, if it isn't a list/dict of records).
    """
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE raw_records (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment   TEXT NOT NULL,
            raw_table    TEXT NOT NULL,
            record_label TEXT,
            raw_values   TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE data_dictionary_notes (
            note TEXT
        )
    """)
    cur.execute(
        "INSERT INTO data_dictionary_notes VALUES (?)",
        ("This table is the 'as printed in the original paper' layer: one "
         "row per record inside a RAW_* table defined in the matching "
         "raw_<experiment>.py file, before any unit conversion or "
         "combination. 'raw_values' is plain text (label: value, one per "
         "line for nested fields) -- it is not JSON and does not need "
         "decoding; open muon_data_raw.csv in any spreadsheet program and "
         "read it directly. For the converted, analysis-ready numbers, "
         "use muon_data.db / muon_data.csv instead.",),
    )

    n_records = 0
    for mod_name, mod in modules.items():
        raw_const_names = sorted(n for n in dir(mod) if n.startswith("RAW_"))
        for const_name in raw_const_names:
            value = _to_plain(getattr(mod, const_name))
            if isinstance(value, dict):
                for k, v in value.items():
                    cur.execute(
                        "INSERT INTO raw_records (experiment, raw_table, record_label, raw_values) VALUES (?,?,?,?)",
                        (mod_name, const_name, str(k), render_readable(v)),
                    )
                    n_records += 1
            elif isinstance(value, list):
                for i, v in enumerate(value):
                    cur.execute(
                        "INSERT INTO raw_records (experiment, raw_table, record_label, raw_values) VALUES (?,?,?,?)",
                        (mod_name, const_name, f"entry {i + 1}", render_readable(v)),
                    )
                    n_records += 1
            else:
                cur.execute(
                    "INSERT INTO raw_records (experiment, raw_table, record_label, raw_values) VALUES (?,?,?,?)",
                    (mod_name, const_name, None, render_readable(value)),
                )
                n_records += 1

    conn.commit()

    cur.execute("SELECT experiment, raw_table, record_label, raw_values FROM raw_records ORDER BY experiment, raw_table, id")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["experiment", "raw_table", "record_label", "raw_values (plain text, not JSON)"])
        w.writerows(cur.fetchall())

    conn.close()
    return n_records


def write_sources_csv(per_experiment_counts, modules, path):
    rows = []
    for mod_name in EXPERIMENT_MODULES:
        mod = modules.get(mod_name)
        doc = (mod.__doc__ or "").strip().splitlines() if mod else []
        first_line = next((l.strip() for l in doc if l.strip()), "")
        rows.append({
            "module": mod_name,
            "n_rows_in_processed_db": per_experiment_counts.get(mod_name, 0),
            "docstring_summary": first_line,
        })
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["module", "n_rows_in_processed_db", "docstring_summary"])
        w.writeheader()
        w.writerows(rows)


def main():
    all_rows, per_experiment_counts, load_errors, modules = load_all_rows()

    print("=" * 70)
    print("MUON SPECTRUM DATABASE BUILD")
    print("=" * 70)
    for mod_name in EXPERIMENT_MODULES:
        if mod_name in per_experiment_counts:
            print(f"  {mod_name:20s} OK  {per_experiment_counts[mod_name]:5d} rows")
        else:
            print(f"  {mod_name:20s} !!  {load_errors.get(mod_name, 'unknown error').splitlines()[0]}")

    if not all_rows:
        print("\nNo rows loaded from any module - aborting database build.")
        return

    n_missing_intensity = sum(1 for r in all_rows if r.get("intensity") is None)

    db_path = os.path.join(HERE, "muon_data.db")
    csv_path = os.path.join(HERE, "muon_data.csv")
    n_inserted, n_dupe_rejected, dupe_examples = build_processed_database(all_rows, db_path, csv_path)

    raw_db_path = os.path.join(HERE, "muon_data_raw.db")
    raw_csv_path = os.path.join(HERE, "muon_data_raw.csv")
    n_raw_records = build_raw_database(modules, raw_db_path, raw_csv_path)

    sources_path = os.path.join(HERE, "sources.csv")
    write_sources_csv(per_experiment_counts, modules, sources_path)

    print("\n" + "-" * 70)
    print(f"Total rows produced by transform()          : {len(all_rows)}")
    print(f"Rows with intensity marked 'not available'  : {n_missing_intensity}")
    print(f"Rows inserted into muon_data.db             : {n_inserted}")
    print(f"Rows rejected as exact duplicates            : {n_dupe_rejected}")
    if dupe_examples:
        print("  Duplicate examples (experiment, theta, momentum):")
        for ex in dupe_examples:
            print(f"    {ex[0]!r} theta={ex[1]} p={ex[2]}")
    print(f"Raw transcription records in muon_data_raw.db: {n_raw_records}")
    print("\nFiles written:")
    for p in (db_path, csv_path, raw_db_path, raw_csv_path, sources_path):
        print(f"  {p}")

    if load_errors:
        print("\n" + "-" * 70)
        print("WARNINGS - these experiments did not fully load, see above:")
        for mod_name, err in load_errors.items():
            print(f"\n[{mod_name}]")
            print(err)


if __name__ == "__main__":
    main()
