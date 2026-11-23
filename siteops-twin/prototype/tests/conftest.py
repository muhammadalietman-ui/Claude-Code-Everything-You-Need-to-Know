import os

import pytest

os.environ.setdefault("SITEOPS_ROUTE", "/nonexistent/route.json")  # tests always use the synthetic geometry
from fastapi.testclient import TestClient

from siteops.cli import build
from siteops.engine import Data, alerts, reconcile


@pytest.fixture(scope="session")
def built(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("siteops")
    db = tmp / "test.db"
    conn = build(db_path=db, out_dir=tmp / "synthetic")
    return db, conn


@pytest.fixture(scope="session")
def computed(built):
    _, conn = built
    d = Data(conn)
    last = d.dates[-1]
    rec = reconcile(d, last)
    al = alerts(d, last, rec)
    gt = [dict(r) for r in conn.execute("SELECT * FROM anomaly_ground_truth")]
    return d, rec, al, gt


@pytest.fixture()
def client(built, tmp_path):
    import shutil
    from siteops.api import create_app
    db = tmp_path / "api.db"
    shutil.copy(built[0], db)
    return TestClient(create_app(db))
