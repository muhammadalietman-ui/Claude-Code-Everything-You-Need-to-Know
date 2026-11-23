"""CSV <-> SQLite loader. The same loader ingests the user's reference-project CSVs (same column names)."""
from __future__ import annotations

import csv
from pathlib import Path

from .db import TABLES, connect, table_columns

HEADER = "# SYNTHETIC DATA - SiteOps Twin demo - not a real project - seed {seed}\n"


def write_csvs(tables: dict[str, list[dict]], out_dir: Path, seed: int, prefix="SYNTHETIC_"):
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, recs in tables.items():
        if not recs:
            continue
        p = out_dir / f"{prefix}{name}.csv"
        with p.open("w", newline="", encoding="utf-8") as f:
            f.write(HEADER.format(seed=seed))
            w = csv.DictWriter(f, fieldnames=list(recs[0].keys()))
            w.writeheader()
            w.writerows(recs)


def read_csv(p: Path) -> list[dict]:
    with p.open(encoding="utf-8") as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    return list(csv.DictReader(lines))


def load_dir(conn, data_dir: Path, prefix="SYNTHETIC_"):
    """Load <prefix><table>.csv files. Empty strings become NULL; unknown columns are rejected."""
    loaded = {}
    for table in TABLES:
        p = data_dir / f"{prefix}{table}.csv"
        if not p.exists():
            continue
        recs = read_csv(p)
        cols = table_columns(conn, table)
        if recs:
            unknown = set(recs[0]) - set(cols)
            if unknown:
                raise ValueError(f"{p.name}: unknown columns {sorted(unknown)}")
            keys = list(recs[0].keys())
            conn.executemany(f"INSERT INTO {table}({','.join(keys)}) VALUES({','.join('?' * len(keys))})",
                             [[None if r[k] == "" else r[k] for k in keys] for r in recs])
        loaded[table] = len(recs)
    conn.commit()
    return loaded


def fresh_db(path):
    path = Path(path)
    if path.exists():
        path.unlink()
    return connect(path)
