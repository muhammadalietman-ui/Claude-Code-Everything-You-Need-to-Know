"""API contract tests (prototype/API_CONTRACT.md)."""
import uuid


def test_meta_and_geometry(client):
    m = client.get("/api/meta").json()
    assert m["spread"]["synthetic"] is True and len(m["sections"]) == 25 and m["equipment"]
    g = client.get("/api/geometry").json()
    kinds = {f["properties"]["kind"] for f in g["features"]}
    assert kinds == {"centreline", "section", "front"}


def test_overview_kpis(client):
    o = client.get("/api/overview").json()
    assert o["kpis"]["claimed_value"] >= o["kpis"]["certifiable_value"] > 0
    assert len(o["sections"]) == 25


def test_reconciliation_filters(client):
    rows = client.get("/api/reconciliation", params={"status": "DISCREPANCY"}).json()["rows"]
    assert rows and all(r["status"] == "DISCREPANCY" for r in rows)


def test_subcontractor_rbac(client):
    h = {"X-Role": "SC", "X-Subcontractor": "SYN-SUB-A"}
    rows = client.get("/api/reconciliation", headers=h).json()["rows"]
    assert rows and {r["subcontractor_id"] for r in rows} == {"SYN-SUB-A"}
    assert client.get("/api/certificate/SYN-SUB-B", headers=h).status_code == 403
    assert client.get("/api/audit", headers=h).status_code == 403
    assert client.get("/api/reconciliation", headers={"X-Role": "SC"}).status_code == 400


def test_certify_cap_and_override(client):
    row = client.get("/api/reconciliation", params={"section": "S07", "activity": "TRN"}).json()["rows"][0]
    above = row["cap"] + 50
    r = client.post("/api/certify", json={"key": row["key"], "qty_certified": above}, headers={"X-Role": "QS"})
    assert r.status_code == 409 and r.json()["error"] == "ABOVE_CAP"
    assert client.post("/api/certify", json={"key": row["key"], "qty_certified": above},
                       headers={"X-Role": "FM"}).status_code == 403
    r = client.post("/api/certify", json={"key": row["key"], "qty_certified": above, "reason_code": "JOINT_MEASUREMENT"},
                    headers={"X-Role": "QS"})
    assert r.status_code == 422  # comment required
    r = client.post("/api/certify", json={"key": row["key"], "qty_certified": row["cap"]}, headers={"X-Role": "QS"})
    assert r.status_code == 200 and r.json()["certified"] == row["cap"]
    ev = client.get("/api/audit", params={"entity": "certification"}).json()["events"]
    assert ev and ev[0]["action"] == "CERTIFY" and ev[0]["after_hash"]


def test_field_report_idempotent_and_validated(client):
    body = {"client_uuid": str(uuid.uuid4()), "report_date": "2027-03-13", "crew_id": "SYN-CRW-06", "front_id": "FR-20",
            "lines": [{"activity_code": "TRN", "kp_from_m": 19000, "kp_to_m": 19100, "qty": 100, "hours_worked": 10,
                       "headcount": 15, "equipment_ids": []}]}
    r1 = client.post("/api/field-reports", json=body, headers={"X-Role": "FM"})
    r2 = client.post("/api/field-reports", json=body, headers={"X-Role": "FM"})
    assert r1.status_code == 201 and r2.status_code == 200 and r2.json()["duplicate"] is True
    bad = dict(body, client_uuid=str(uuid.uuid4()))
    bad["lines"] = [dict(body["lines"][0], kp_to_m=18000)]
    assert client.post("/api/field-reports", json=bad, headers={"X-Role": "FM"}).status_code == 422
    assert client.post("/api/field-reports", json=dict(body, client_uuid="x2"), headers={"X-Role": "SC", "X-Subcontractor": "SYN-SUB-B"}).status_code == 403


def test_alert_status_flow(client):
    a = client.get("/api/alerts", params={"rule": "AL-09"}).json()["alerts"][0]
    r = client.post(f"/api/alerts/{a['alert_id']}/status", json={"status": "ACK", "comment": "checking manifest"},
                    headers={"X-Role": "CM"})
    assert r.status_code == 200 and r.json()["status"] == "ACK"


def test_presence_and_scorecard(client):
    p = client.get("/api/presence", params={"date": "2027-01-21"}).json()
    assert any(f["status"] == "OVERCLAIM" for f in p["fronts"]) and "privacy_note" in p
    s = client.get("/api/scorecard").json()["rows"]
    assert {r["subcontractor_id"] for r in s} == {"SYN-SUB-A", "SYN-SUB-B", "SYN-SUB-C", "SYN-SUB-D"}


def test_certificate_csv(client):
    r = client.get("/api/certificate/SYN-SUB-B.csv")
    assert r.status_code == 200 and r.text.startswith("# SYNTHETIC")
    j = client.get("/api/certificate/SYN-SUB-B").json()
    assert j["lines"] and abs(j["total_this_period"] - sum(l["amount"] for l in j["lines"])) < 0.01


def test_static_dashboard_served(client):
    assert client.get("/").status_code == 200
    assert client.get("/field.html").status_code == 200


def test_daily_report_structure_and_arithmetic(client):
    r = client.get("/api/daily-report").json()
    assert r["report_no"] > 0 and r["detail"] and r["personnel"] and r["equipment"]
    for x in r["detail"]:
        assert abs(x["cum"] - (x["cum_prev"] + x["this_period"])) < 0.2
    for x in r["personnel"]:
        assert x["today_total"] == x["today_local"] + x["today_external"]
    assert client.get("/api/daily-report", headers={"X-Role": "SC", "X-Subcontractor": "SYN-SUB-A"}).status_code == 403


def test_calculated_equipment_hours_exceed_measured_on_stop_days(client):
    """Practice: client reports calculate equipment hours from days assigned, so weather-stop days still accrue hours."""
    from siteops.engine import Data
    st = client.app.state.siteops
    d = st.data()
    stop = [w for w, v in d.weather.items() if v["condition"] == "STOPPED"]
    calc_on_stop = sum(r["calc_hours"] for r in d.eq_calc if r["work_date"] in stop)
    measured_on_stop = sum(t["engine_h"] for (e, w), t in d.telematics.items() if w in stop)
    assert calc_on_stop > 0 and measured_on_stop == 0
