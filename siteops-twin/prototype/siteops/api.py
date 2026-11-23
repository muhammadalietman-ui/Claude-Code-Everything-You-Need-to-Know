"""FastAPI backend implementing prototype/API_CONTRACT.md (demo, SYNTHETIC data only).

Run:  .venv/bin/uvicorn siteops.api:app --reload      then open http://localhost:8000/
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import os
import threading
import uuid
from pathlib import Path

from fastapi import Body, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from . import config as C
from .db import DEFAULT_DB, connect
from .engine import Data, alerts, reconcile, section_shares, to_metres
from .generate import centreline
from .reporting import daily_report

WEB = Path(__file__).resolve().parent.parent / "web"
ROLES = ["CM", "QS", "SM", "FM", "SV", "SC", "ADM", "AUD"]
REASONS = {"JOINT_MEASUREMENT", "SURVEY_RECHECK", "CONTRACT_RULE", "OTHER"}


class State:
    def __init__(self, db_path):
        self.lock = threading.RLock()
        self.conn = connect(db_path)
        self.version = 0
        self.cache: dict = {}

    def bump(self):
        self.version += 1
        self.cache.clear()

    def data(self) -> Data:
        k = ("data", self.version)
        if k not in self.cache:
            self.cache[k] = Data(self.conn)
        return self.cache[k]

    def computed(self, date):
        k = ("rec", self.version, date)
        if k not in self.cache:
            d = self.data()
            rec = reconcile(d, date)
            al = alerts(d, date, rec)
            rec = reconcile(d, date, al)
            self.cache[k] = (rec, al)
        return self.cache[k]


def create_app(db_path=None) -> FastAPI:
    db_path = db_path or os.environ.get("SITEOPS_DB", DEFAULT_DB)
    if not Path(db_path).exists():
        from .cli import build
        build(db_path)
    st = State(db_path)
    app = FastAPI(title="SiteOps Twin MVP (SYNTHETIC demo)", version="0.1.0")
    app.state.siteops = st

    def ctx(role, sub):
        role = (role or "CM").upper()
        if role not in ROLES:
            raise HTTPException(400, f"unknown role {role}")
        if role == "SC" and not sub:
            raise HTTPException(400, "X-Subcontractor header required for role SC")
        return role, sub

    def pick_date(date):
        d = st.data()
        last = d.dates[-1]
        if not date:
            return last
        try:
            dt.date.fromisoformat(date)
        except ValueError:
            raise HTTPException(422, "date must be YYYY-MM-DD")
        return date

    def scope(items, role, sub, field="subcontractor_id"):
        return [i for i in items if role != "SC" or i.get(field) == sub]

    def audit(actor, entity, entity_id, action, detail, before=None, after=None):
        h = lambda o: hashlib.sha256(json.dumps(o, sort_keys=True, default=str).encode()).hexdigest()[:16] if o is not None else None  # noqa: E731
        st.conn.execute("INSERT INTO audit_event(ts,actor_role,entity,entity_id,action,detail,before_hash,after_hash) "
                        "VALUES(?,?,?,?,?,?,?,?)", (dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), actor,
                                                    entity, entity_id, action, detail, h(before), h(after)))

    # ------------------------------------------------------------------ meta / geometry
    @app.get("/api/meta")
    def meta():
        d = st.data()
        sp = dict(st.conn.execute("SELECT * FROM spread").fetchone())
        return {"spread": {"spread_id": sp["spread_id"], "kp_start_m": sp["kp_start_m"], "kp_end_m": sp["kp_end_m"],
                           "site_tz": sp["site_tz"], "synthetic": bool(sp["is_synthetic"])},
                "date_min": d.dates[0], "date_max": d.dates[-1], "default_date": d.dates[-1],
                "sections": [{k: s[k] for k in ("section_id", "kp_from_m", "kp_to_m")} for s in d.sections],
                "activities": [{"activity_code": a["activity_code"], "name": a["name"], "name_de": a.get("name_de"), "unit": a["unit"],
                                "sequence_no": a["sequence_no"], "verification_source": a["verification_source"]}
                               for a in sorted(d.acts.values(), key=lambda a: a["sequence_no"])],
                "subcontractors": [dict(r) for r in st.conn.execute("SELECT * FROM subcontractor")],
                "crews": list(d.crews.values()),
                "equipment": [{k: e[k] for k in ("equipment_id", "type", "owner", "crew_id")} for e in d.equipment.values()],
                "fronts": list(d.fronts.values()),
                "plan_sheets": d.sheets,
                "config": {"tol_pct": C.TOL_PCT, "tol_abs": C.TOL_ABS, "al05_drop": C.AL05_DROP, "tol_head": C.TOL_HEAD,
                           "tol_eq_h": C.TOL_EQ_H, "currency": C.CURRENCY},
                "roles": ROLES}

    route_file = Path(os.environ.get("SITEOPS_ROUTE", Path(__file__).resolve().parent.parent.parent / "data" / "private" / "route.json"))

    def real_geometry(d):
        """Synthetic sections/fronts positioned proportionally along a real route (lon/lat). Display only."""
        r = json.loads(route_file.read_text(encoding="utf-8"))
        pts, kps, L = r["points"], r["kp"], r["length_m"]
        scale = L / C.KP_END_M

        def at(k):  # interpolate lon/lat at real chainage k
            k = min(max(k, 0.0), kps[-1])
            for i in range(1, len(kps)):
                if kps[i] >= k:
                    t = 0.0 if kps[i] == kps[i - 1] else (k - kps[i - 1]) / (kps[i] - kps[i - 1])
                    return [pts[i - 1][0] + t * (pts[i][0] - pts[i - 1][0]), pts[i - 1][1] + t * (pts[i][1] - pts[i - 1][1])]
            return pts[-1]

        def piece(k0, k1):
            a, b = k0 * scale, k1 * scale
            return [at(a)] + [p for p, k in zip(pts, kps) if a < k < b] + [at(b)]
        feats = [{"type": "Feature", "properties": {"kind": "centreline"}, "geometry": {"type": "LineString", "coordinates": pts}}]
        for s in d.sections:
            feats.append({"type": "Feature", "properties": {"kind": "section", **{k: s[k] for k in ("section_id", "kp_from_m", "kp_to_m")}},
                          "geometry": {"type": "LineString", "coordinates": piece(s["kp_from_m"], s["kp_to_m"])}})
        for f in d.fronts.values():
            feats.append({"type": "Feature", "properties": {"kind": "front", "front_id": f["front_id"], "type": f["type"], "name": f["name"]},
                          "geometry": {"type": "Point", "coordinates": at((f["kp_from_m"] + f["kp_to_m"]) / 2 * scale)}})
        for p in r.get("pois", []):
            feats.append({"type": "Feature", "properties": {"kind": "poi", "name": p["name"]},
                          "geometry": {"type": "Point", "coordinates": [p["lon"], p["lat"]]}})
        return {"type": "FeatureCollection", "crs": "EPSG:4326", "title": r.get("title"), "route_length_m": L,
                "crs_note": "Real route geometry (private); quantities and statuses are SYNTHETIC", "features": feats}

    @app.get("/api/geometry")
    def geometry():
        d = st.data()
        if route_file.exists():
            return real_geometry(d)
        pts = centreline()
        step = C.KP_END_M / (len(pts) - 1)
        at = lambda kp: pts[min(int(round(kp / step)), len(pts) - 1)]  # noqa: E731
        feats = [{"type": "Feature", "properties": {"kind": "centreline"},
                  "geometry": {"type": "LineString", "coordinates": [list(p) for p in pts]}}]
        for s in d.sections:
            i0, i1 = int(s["kp_from_m"] / step), int(s["kp_to_m"] / step)
            feats.append({"type": "Feature", "properties": {"kind": "section", **{k: s[k] for k in ("section_id", "kp_from_m", "kp_to_m")}},
                          "geometry": {"type": "LineString", "coordinates": [list(p) for p in pts[i0:i1 + 1]]}})
        for f in d.fronts.values():
            feats.append({"type": "Feature", "properties": {"kind": "front", "front_id": f["front_id"], "type": f["type"],
                                                            "name": f["name"]},
                          "geometry": {"type": "Point", "coordinates": list(at((f["kp_from_m"] + f["kp_to_m"]) / 2))}})
        return {"type": "FeatureCollection", "crs_note": "Local synthetic CRS in metres (not lat/lon)", "features": feats}

    # ------------------------------------------------------------------ overview
    @app.get("/api/overview")
    def overview(date: str | None = None, x_role: str | None = Header(None), x_subcontractor: str | None = Header(None)):
        role, sub = ctx(x_role, x_subcontractor)
        date = pick_date(date)
        d = st.data()
        rec, al = st.computed(date)
        rec = scope(rec, role, sub)
        als = scope(list(al.values()), role, sub)
        claimed_v = sum(r["claimed"] * r["rate"] for r in rec)
        cert_v = sum(r["certifiable"] * r["rate"] for r in rec)
        by_status = {s: 0 for s in ("MATCHED", "WITHIN_TOLERANCE", "DISCREPANCY", "UNVERIFIABLE")}
        for r in rec:
            if r["claimed"] > 0:
                by_status[r["status"]] += 1
        open_al = {"HIGH": 0, "MED": 0, "LOW": 0}
        for a in als:
            if a["status"] != "CLOSED":
                open_al[a["severity"]] += 1
        rc_today = [x for x in d.resource_claims if x["work_date"] == date]
        reports_today = {r["crew_id"] for r in d.reports.values() if r["report_date"] == date}
        pres = {(p["crew_id"]): p for p in d.presence if p["work_date"] == date}
        order = ["MATCHED", "WITHIN_TOLERANCE", "UNVERIFIABLE", "DISCREPANCY"]
        sections = []
        for s in d.sections:
            srows = [r for r in rec if r["section_id"] == s["section_id"] and r["claimed"] > 0]
            worst = max((r["status"] for r in srows), key=order.index, default=None)
            prog = {}
            for code in d.acts:
                pl = d.planned.get((s["section_id"], code), 0)
                rp = sum(r["reported"] for r in rec if r["section_id"] == s["section_id"] and r["activity_code"] == code)
                prog[code] = round(min(rp / pl, 1.0), 3) if pl else 0.0
            sections.append({"section_id": s["section_id"], "kp_from_m": s["kp_from_m"], "kp_to_m": s["kp_to_m"],
                             "worst_status": worst,
                             "open_alerts": sum(1 for a in als if a["section_id"] == s["section_id"] and a["status"] != "CLOSED"),
                             "progress": prog})
        rc_scoped = scope(rc_today, role, sub)
        return {"date": date, "currency": C.CURRENCY, "synthetic": True,
                "kpis": {"claimed_value": round(claimed_v, 2), "certifiable_value": round(cert_v, 2),
                         "at_risk_value": round(claimed_v - cert_v, 2), "rows_by_status": by_status, "open_alerts": open_al,
                         "reports_received": len({x["crew_id"] for x in rc_scoped} & reports_today),
                         "reports_expected": len({x["crew_id"] for x in rc_scoped}),
                         "headcount_claimed": sum(x["headcount_claimed"] for x in rc_scoped),
                         "headcount_sensed": sum(max(pres[x["crew_id"]]["checkin_count"] or 0, pres[x["crew_id"]]["manifest_count"] or 0)
                                                 for x in rc_scoped if x["crew_id"] in pres)},
                "sections": sections}

    # ------------------------------------------------------------------ reconciliation / sections
    @app.get("/api/reconciliation")
    def reconciliation(date: str | None = None, subcontractor: str | None = None, status: str | None = None,
                       activity: str | None = None, section: str | None = None,
                       x_role: str | None = Header(None), x_subcontractor: str | None = Header(None)):
        role, sub = ctx(x_role, x_subcontractor)
        rec, _ = st.computed(pick_date(date))
        out = [r for r in scope(rec, role, sub)
               if (not subcontractor or r["subcontractor_id"] == subcontractor) and (not status or r["status"] == status)
               and (not activity or r["activity_code"] == activity) and (not section or r["section_id"] == section)]
        return {"rows": out}

    @app.get("/api/sections/{section_id}")
    def section_detail(section_id: str, date: str | None = None, x_role: str | None = Header(None),
                       x_subcontractor: str | None = Header(None)):
        role, sub = ctx(x_role, x_subcontractor)
        date = pick_date(date)
        d = st.data()
        if section_id not in d.sec_by_id:
            raise HTTPException(404, "unknown section")
        rec, al = st.computed(date)
        flights = [f for f in d.flights if f["flight_date"] <= date][-10:]
        fl_date = {f["flight_id"]: f["flight_date"] for f in d.flights}
        latest = {}
        for m in d.measurements:
            if m["section_id"] == section_id and m["measure_date"] <= date:
                latest[m["activity_code"]] = m
        meas = [{"measurement_id": m["measurement_id"], "activity_code": m["activity_code"], "method": m["method"],
                 "source": m["source"], "qty": m["qty_cum"], "unit": m["unit"], "sigma": m["sigma"],
                 "flight_date": fl_date.get(m["flight_id"], m["measure_date"]),
                 "kp_from_m": d.sec_by_id[section_id]["kp_from_m"], "kp_to_m": d.sec_by_id[section_id]["kp_to_m"]}
                for m in latest.values()]
        keys = {r["key"] for r in rec if r["section_id"] == section_id}
        aud = [dict(r) for r in st.conn.execute("SELECT * FROM audit_event ORDER BY event_id DESC LIMIT 500")]
        return {"section": {k: d.sec_by_id[section_id][k] for k in ("section_id", "kp_from_m", "kp_to_m")},
                "rows": scope([r for r in rec if r["section_id"] == section_id], role, sub),
                "flights": [{k: f[k] for k in ("flight_id", "flight_date", "gsd_cm", "rmse_z_m", "n_checkpoints")} for f in flights],
                "measurements": meas,
                "alerts": scope([a for a in al.values() if a["section_id"] == section_id], role, sub),
                "audit": [a for a in aud if a["entity_id"] in keys or section_id in (a["detail"] or "")]}

    # ------------------------------------------------------------------ production
    @app.get("/api/production")
    def production(date: str | None = None, x_role: str | None = Header(None), x_subcontractor: str | None = Header(None)):
        role, sub = ctx(x_role, x_subcontractor)
        date = pick_date(date)
        d = st.data()
        _, al = st.computed(date)
        al05 = {a["crew_id"]: a for a in al.values() if a["rule_id"] == "AL-05" and a["work_date"] == date}
        by_crew: dict = {}
        for ln in d.report_lines:
            if ln["report_date"] and ln["report_date"] <= date:
                by_crew.setdefault(ln["crew_id"], {}).setdefault(ln["report_date"], []).append(ln)
        rc_today = {x["crew_id"]: x for x in d.resource_claims if x["work_date"] == date}
        out = []
        for crew, c in sorted(d.crews.items()):
            days = by_crew.get(crew, {})
            today = days.get(date)
            hist = [(dd, ls) for dd, ls in sorted(days.items()) if dd < date and not any(l["downtime_reason"] for l in ls)][-5:]

            def prod(ls):
                h = max(l["hours_worked"] or 0 for l in ls)
                return sum(to_metres(d, c["activity_code"], l["qty"]) for l in ls) / h if h else 0.0
            med = sorted(prod(ls) for _, ls in hist)[len(hist) // 2] if hist else None
            if not today and crew not in rc_today:
                continue
            qty = sum(l["qty"] for l in today) if today else 0.0
            hours = max(l["hours_worked"] or 0 for l in today) if today else 0.0
            p = prod(today) if today else None
            out.append({"crew_id": crew, "subcontractor_id": c["subcontractor_id"], "activity_code": c["activity_code"],
                        "unit": d.acts[c["activity_code"]]["unit"], "qty": round(qty, 1), "hours": hours,
                        "headcount": max((l["headcount"] or 0 for l in today), default=0) if today else 0,
                        "productivity": None if p is None else round(p, 2), "productivity_unit": "m/h",
                        "median5": None if med is None else round(med, 2),
                        "delta_pct": None if (p is None or not med) else round(p / med - 1, 3),
                        "weather": d.weather.get(date, {}).get("condition", "WORKABLE"),
                        "downtime_reason": next((l["downtime_reason"] for l in today or [] if l["downtime_reason"]), None),
                        "report_received": bool(today), "al05": crew in al05,
                        "kp_from_m": min((l["kp_from_m"] for l in today), default=None) if today else None,
                        "kp_to_m": max((l["kp_to_m"] for l in today), default=None) if today else None})
        return {"date": date, "rows": scope(out, role, sub)}

    # ------------------------------------------------------------------ alerts
    @app.get("/api/alerts")
    def list_alerts(date: str | None = None, status: str | None = None, rule: str | None = None,
                    severity: str | None = None, subcontractor: str | None = None,
                    x_role: str | None = Header(None), x_subcontractor: str | None = Header(None)):
        role, sub = ctx(x_role, x_subcontractor)
        _, al = st.computed(pick_date(date))
        sev = {"HIGH": 0, "MED": 1, "LOW": 2}
        out = [a for a in scope(list(al.values()), role, sub)
               if (not status or a["status"] == status) and (not rule or a["rule_id"] == rule)
               and (not severity or a["severity"] == severity) and (not subcontractor or a["subcontractor_id"] == subcontractor)]
        out.sort(key=lambda a: (a["status"] == "CLOSED", sev[a["severity"]], a["work_date"] or ""), reverse=False)
        return {"alerts": out}

    @app.post("/api/alerts/{alert_id}/status")
    def alert_status(alert_id: str, body: dict = Body(...), date: str | None = None,
                     x_role: str | None = Header(None), x_subcontractor: str | None = Header(None)):
        role, _ = ctx(x_role, x_subcontractor)
        if role in ("SC", "AUD", "FM"):
            raise HTTPException(403, "role not allowed to change alert status")
        status = body.get("status")
        if status not in ("ACK", "CLOSED", "OPEN"):
            raise HTTPException(422, "status must be ACK, CLOSED or OPEN")
        with st.lock:
            _, al = st.computed(pick_date(date))
            if alert_id not in al:
                raise HTTPException(404, "unknown alert")
            before = al[alert_id]["status"]
            st.conn.execute("INSERT OR REPLACE INTO alert_state VALUES(?,?,?,?,?)",
                            (alert_id, status, body.get("comment"), dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), role))
            audit(role, "alert", alert_id, f"STATUS_{status}", f"{al[alert_id]['rule_id']} {before}->{status}: {body.get('comment') or ''}",
                  before, status)
            st.conn.commit()
            st.bump()
            _, al = st.computed(pick_date(date))
            return al[alert_id]

    # ------------------------------------------------------------------ scorecard / presence
    @app.get("/api/scorecard")
    def scorecard(date: str | None = None, x_role: str | None = Header(None), x_subcontractor: str | None = Header(None)):
        role, sub = ctx(x_role, x_subcontractor)
        date = pick_date(date)
        d = st.data()
        rec, al = st.computed(date)
        rows = []
        for s in [r["subcontractor_id"] for r in st.conn.execute("SELECT subcontractor_id FROM subcontractor")]:
            sr = [r for r in rec if r["subcontractor_id"] == s]
            cv = sum(r["claimed"] * r["rate"] for r in sr)
            ce = sum(r["certifiable"] * r["rate"] for r in sr)
            sa = [a for a in al.values() if a["subcontractor_id"] == s]
            by_rule = {}
            for a in sa:
                by_rule[a["rule_id"]] = by_rule.get(a["rule_id"], 0) + 1
            eq_over = 0.0
            for ec in d.equipment_claims:
                if ec["subcontractor_id"] == s and ec["work_date"] <= date:
                    t = d.telematics.get((ec["equipment_id"], ec["work_date"]))
                    if t and ec["hours_claimed"] > t["engine_h"] + C.TOL_EQ_H:
                        eq_over += ec["hours_claimed"] - t["engine_h"]
            crews = [c for c, v in d.crews.items() if v["subcontractor_id"] == s]
            rep = [r for r in d.reports.values() if r["crew_id"] in crews and r["report_date"] <= date]
            on_time = [r for r in rep if (r["submitted_at"] or "")[11:13] < "20"]
            rows.append({"subcontractor_id": s, "claimed_value": round(cv, 2), "certifiable_value": round(ce, 2),
                         "overclaim_pct": round((cv - ce) / ce, 4) if ce else None,
                         "rows_discrepancy": sum(1 for r in sr if r["status"] == "DISCREPANCY"),
                         "alerts_by_rule": by_rule, "headcount_overclaim_days": by_rule.get("AL-09", 0),
                         "equipment_overclaim_h": round(eq_over, 1),
                         "reports_on_time_pct": round(len(on_time) / len(rep), 3) if rep else None})
        return {"date": date, "currency": C.CURRENCY, "rows": scope(rows, role, sub)}

    @app.get("/api/presence")
    def presence(date: str | None = None, x_role: str | None = Header(None), x_subcontractor: str | None = Header(None)):
        role, sub = ctx(x_role, x_subcontractor)
        date = pick_date(date)
        d = st.data()
        pres = {p["crew_id"]: p for p in d.presence if p["work_date"] == date}
        fronts = []
        for rc in [x for x in d.resource_claims if x["work_date"] == date]:
            p = pres.get(rc["crew_id"])
            sensed = max(p["checkin_count"] or 0, p["manifest_count"] or 0) if p else None
            stt = "NO_SIGNAL" if p is None else ("OVERCLAIM" if rc["headcount_claimed"] > sensed + C.TOL_HEAD else "OK")
            fronts.append({"front_id": rc["front_id"], "crew_id": rc["crew_id"], "subcontractor_id": rc["subcontractor_id"],
                           "headcount_claimed": rc["headcount_claimed"], "checkin": p and p["checkin_count"],
                           "manifest": p and p["manifest_count"], "camera_max": p and p["camera_max"],
                           "badge_zone_count": p and p["badge_zone_count"], "status": stt})
        eq = []
        for ec in [x for x in d.equipment_claims if x["work_date"] == date]:
            t = d.telematics.get((ec["equipment_id"], date))
            e = d.equipment.get(ec["equipment_id"], {})
            stt = "NO_DATA" if not t else ("OVERCLAIM" if ec["hours_claimed"] > t["engine_h"] + C.TOL_EQ_H else "OK")
            eq.append({"equipment_id": ec["equipment_id"], "type": e.get("type"), "subcontractor_id": ec["subcontractor_id"],
                       "hours_claimed": ec["hours_claimed"], "engine_h": t and t["engine_h"], "working_h": t and t["working_h"],
                       "telematics": "OK" if t else "NO_DATA", "status": stt})
        return {"date": date, "fronts": scope(fronts, role, sub), "equipment": scope(eq, role, sub),
                "privacy_note": "Aggregated counts only. Identifiable presence data is restricted to HR/HSE "
                                "(pseudonymised badge IDs; no individual tracks; no biometrics)."}

    # ------------------------------------------------------------------ field reports (mobile)
    @app.post("/api/field-reports", status_code=201)
    def post_report(body: dict = Body(...), x_role: str | None = Header(None), x_subcontractor: str | None = Header(None)):
        role, _ = ctx(x_role, x_subcontractor)
        if role not in ("FM", "SM", "ADM", "CM"):
            raise HTTPException(403, "role not allowed to submit field reports")
        d = st.data()
        cu = body.get("client_uuid")
        if not cu:
            raise HTTPException(422, "client_uuid required")
        with st.lock:
            ex = st.conn.execute("SELECT report_id FROM field_report WHERE client_uuid=?", (cu,)).fetchone()
            if ex:
                return JSONResponse({"report_id": ex[0], "status": "RECEIVED", "duplicate": True}, status_code=200)
            if body.get("crew_id") not in d.crews:
                raise HTTPException(422, "unknown crew_id")
            try:
                dt.date.fromisoformat(body.get("report_date", ""))
            except ValueError:
                raise HTTPException(422, "report_date must be YYYY-MM-DD")
            lines = body.get("lines") or []
            if not lines:
                raise HTTPException(422, "at least one line required")
            for ln in lines:
                if ln.get("activity_code") not in d.acts:
                    raise HTTPException(422, f"unknown activity_code {ln.get('activity_code')}")
                if ln.get("kp_from_m") is None or ln.get("kp_to_m") is None or float(ln["kp_to_m"]) <= float(ln["kp_from_m"]):
                    raise HTTPException(422, "kp_to_m must be greater than kp_from_m")
                if float(ln.get("qty", -1)) < 0:
                    raise HTTPException(422, "qty must be >= 0")
            rid = "FR-" + uuid.uuid4().hex[:8].upper()
            st.conn.execute("INSERT INTO field_report VALUES(?,?,?,?,?,?,?,?)",
                            (rid, cu, body["report_date"], body["crew_id"], body.get("front_id"),
                             body.get("submitted_at") or dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), "MOBILE", 1))
            photos = ";".join(p.get("name", "") for p in body.get("photos") or [])
            for n, ln in enumerate(lines):
                st.conn.execute("INSERT INTO field_report_line VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                (f"{rid}-{n + 1}", rid, ln["activity_code"], float(ln["kp_from_m"]), float(ln["kp_to_m"]),
                                 float(ln["qty"]), ln.get("unit") or d.acts[ln["activity_code"]]["unit"],
                                 float(ln.get("hours_worked") or 0), int(ln.get("headcount") or 0),
                                 ";".join(ln.get("equipment_ids") or []), float(ln.get("downtime_h") or 0),
                                 ln.get("downtime_reason"), photos))
            audit(role, "field_report", rid, "CREATE", f"{body['crew_id']} {body['report_date']} {len(lines)} line(s)", None, body)
            st.conn.commit()
            st.bump()
        return {"report_id": rid, "status": "RECEIVED", "duplicate": False}

    @app.get("/api/field-reports")
    def get_reports(date: str | None = None, crew: str | None = None, x_role: str | None = Header(None),
                    x_subcontractor: str | None = Header(None)):
        role, sub = ctx(x_role, x_subcontractor)
        d = st.data()
        out = []
        for r in d.reports.values():
            if (date and r["report_date"] != date) or (crew and r["crew_id"] != crew):
                continue
            rr = dict(r)
            rr["subcontractor_id"] = d.crews.get(r["crew_id"], {}).get("subcontractor_id")
            rr["lines"] = [ln for ln in d.report_lines if ln["report_id"] == r["report_id"]]
            out.append(rr)
        out.sort(key=lambda r: (r["report_date"], r["crew_id"]))
        return {"reports": scope(out, role, sub)[-500:]}

    # ------------------------------------------------------------------ certification
    @app.post("/api/certify")
    def certify(body: dict = Body(...), date: str | None = None, x_role: str | None = Header(None),
                x_subcontractor: str | None = Header(None)):
        role, _ = ctx(x_role, x_subcontractor)
        if role not in ("QS", "CM"):
            raise HTTPException(403, "only QS or CM may certify")
        date = pick_date(date)
        with st.lock:
            rec, _ = st.computed(date)
            row = next((r for r in rec if r["key"] == body.get("key")), None)
            if not row:
                raise HTTPException(404, "unknown reconciliation key")
            try:
                q = float(body.get("qty_certified"))
            except (TypeError, ValueError):
                raise HTTPException(422, "qty_certified must be a number")
            if q < 0:
                raise HTTPException(422, "qty_certified must be >= 0")
            reason = body.get("reason_code")
            if q > row["cap"] + 1e-6:
                if not reason:
                    return JSONResponse({"error": "ABOVE_CAP", "cap": row["cap"], "status": row["status"]}, status_code=409)
                if reason not in REASONS:
                    raise HTTPException(422, f"reason_code must be one of {sorted(REASONS)}")
                if not (body.get("comment") or "").strip():
                    raise HTTPException(422, "comment required for an override above cap")
            cid = "CERT-" + uuid.uuid4().hex[:8].upper()
            st.conn.execute("INSERT INTO certification_line VALUES(?,?,?,?,?,?,?)",
                            (cid, row["key"], date, q, role, reason, body.get("comment")))
            audit(role, "certification", row["key"], "CERTIFY_OVERRIDE" if reason else "CERTIFY",
                  f"{row['section_id']} {row['activity_code']}: {row['certified']} -> {q} {row['unit']} (cap {row['cap']})"
                  + (f" reason {reason}" if reason else ""), {"certified": row["certified"]}, {"certified": q})
            st.conn.commit()
            st.bump()
            rec, _ = st.computed(date)
            return next(r for r in rec if r["key"] == row["key"])

    def certificate_data(subcontractor_id, date, role, sub):
        if role == "SC" and subcontractor_id != sub:
            raise HTTPException(403, "subcontractors can only see their own certificate")
        date = pick_date(date)
        d = st.data()
        rec, _ = st.computed(date)
        prev_cert = {}
        for c in sorted(d.certs, key=lambda c: c["cert_date"]):
            if c["cert_date"] < date:
                prev_cert[c["rec_key"]] = c["cum_certified"]
        lines = []
        for r in rec:
            if r["subcontractor_id"] != subcontractor_id or r["certified"] <= 0:
                continue
            prev = prev_cert.get(r["key"], 0.0)
            this = round(r["certified"] - prev, 1)
            boq = next((b["boq_item_id"] for b in d.boq.values() if b["subcontractor_id"] == subcontractor_id
                        and b["activity_code"] == r["activity_code"]), None)
            lines.append({"key": r["key"], "boq_item_id": boq, "activity_code": r["activity_code"], "section_id": r["section_id"],
                          "unit": r["unit"], "cum_certified": r["certified"], "prev_certified": prev, "this_period": this,
                          "rate": r["rate"], "amount": round(this * r["rate"], 2)})
        return {"subcontractor_id": subcontractor_id, "period_to": date, "lines": lines,
                "total_this_period": round(sum(l["amount"] for l in lines), 2), "currency": C.CURRENCY,
                "note": "SYNTHETIC certificate draft. Retention, advances, variations and tax are out of MVP scope (D-066)."}

    @app.get("/api/certificate/{subcontractor_id}.csv", response_class=PlainTextResponse)
    def certificate_csv(subcontractor_id: str, date: str | None = None, x_role: str | None = Header(None),
                        x_subcontractor: str | None = Header(None)):
        role, sub = ctx(x_role, x_subcontractor)
        c = certificate_data(subcontractor_id, date, role, sub)
        buf = io.StringIO()
        buf.write(f"# SYNTHETIC certificate draft {subcontractor_id} period_to {c['period_to']}\n")
        w = csv.DictWriter(buf, fieldnames=["key", "boq_item_id", "activity_code", "section_id", "unit", "cum_certified",
                                            "prev_certified", "this_period", "rate", "amount"])
        w.writeheader()
        w.writerows(c["lines"])
        return PlainTextResponse(buf.getvalue(), media_type="text/csv",
                                 headers={"Content-Disposition": f'attachment; filename="SYNTHETIC_certificate_{subcontractor_id}_{c["period_to"]}.csv"'})

    @app.get("/api/certificate/{subcontractor_id}")
    def certificate(subcontractor_id: str, date: str | None = None, x_role: str | None = Header(None),
                    x_subcontractor: str | None = Header(None)):
        role, sub = ctx(x_role, x_subcontractor)
        return certificate_data(subcontractor_id, date, role, sub)

    @app.get("/api/audit")
    def audit_log(entity: str | None = None, entity_id: str | None = None, x_role: str | None = Header(None),
                  x_subcontractor: str | None = Header(None)):
        role, _ = ctx(x_role, x_subcontractor)
        if role == "SC":
            raise HTTPException(403, "audit log not available to subcontractors")
        q, a = "SELECT * FROM audit_event WHERE 1=1", []
        if entity:
            q, a = q + " AND entity=?", a + [entity]
        if entity_id:
            q, a = q + " AND entity_id=?", a + [entity_id]
        return {"events": [dict(r) for r in st.conn.execute(q + " ORDER BY event_id DESC LIMIT 500", a)]}

    @app.get("/api/daily-report")
    def get_daily_report(date: str | None = None, x_role: str | None = Header(None), x_subcontractor: str | None = Header(None)):
        role, _ = ctx(x_role, x_subcontractor)
        if role == "SC":
            raise HTTPException(403, "the client daily report is an internal/client document")
        date = pick_date(date)
        rec, al = st.computed(date)
        return daily_report(st.data(), date, rec, al)

    @app.get("/api/health")
    def health():
        return {"ok": True, "synthetic": True, "version": st.version}

    if WEB.exists():
        app.mount("/", StaticFiles(directory=str(WEB), html=True), name="web")
    return app


app = create_app()
