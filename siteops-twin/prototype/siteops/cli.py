"""Command line: build the synthetic demo database, or load a reference project.

    python -m siteops.cli build                # synthetic SYN-SPREAD-01 -> data/synthetic + siteops_demo.db
    python -m siteops.cli load <dir> [prefix]  # load reference-project CSVs (same columns) into a new DB
    python -m siteops.cli check                # print alert counts vs seeded ground truth
"""
from __future__ import annotations

import sys
from pathlib import Path

from . import config as C
from .db import DEFAULT_DB
from .engine import Data, alerts, certify_history, reconcile
from .generate import generate
from .loader import fresh_db, load_dir, write_csvs

ROOT = Path(__file__).resolve().parent.parent
SYN_DIR = ROOT.parent / "data" / "synthetic"


def build(db_path=DEFAULT_DB, seed=C.SEED, out_dir=SYN_DIR):
    tables = generate(seed)
    write_csvs(tables, out_dir, seed)
    conn = fresh_db(db_path)
    load_dir(conn, out_dir)
    certify_history(conn, Data(conn))
    return conn


def check(conn):
    data = Data(conn)
    last = data.dates[-1]
    al = alerts(data, last, reconcile(data, last))
    gt = [dict(r) for r in conn.execute("SELECT * FROM anomaly_ground_truth")]
    from collections import Counter
    print("alerts by rule:", dict(sorted(Counter(a["rule_id"] for a in al.values()).items())))
    print("seeded by rule:", dict(sorted(Counter(g["rule_id"] for g in gt).items())))


def main(argv=None):
    argv = argv or sys.argv[1:]
    cmd = argv[0] if argv else "build"
    if cmd == "build":
        conn = build()
        check(conn)
        print(f"Built {DEFAULT_DB}")
    elif cmd == "load":
        src, prefix = Path(argv[1]), (argv[2] if len(argv) > 2 else "")
        conn = fresh_db(DEFAULT_DB)
        print(load_dir(conn, src, prefix))
    elif cmd == "check":
        from .db import connect
        check(connect())
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
