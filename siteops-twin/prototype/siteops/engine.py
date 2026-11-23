"""Reconciliation engine (E5) and alert rules AL-01..AL-13 (E6, E11).

Status rule (D-063): |C - M| <= U -> MATCHED; <= U + T -> WITHIN_TOLERANCE; above -> DISCREPANCY;
no valid measurement -> UNVERIFIABLE. U = k * sigma (95 %), T = max(abs, pct * M).
Claims are compared with the measurement at the measurement date (D-041): claim lines with a work
date after the latest measurement are "pending verification" and cannot be certified yet.
Certifiable cap without override (D-064): M + U + T.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import statistics
from collections import defaultdict

from . import config as C

SEVERITY = {"AL-01": "HIGH", "AL-02": "MED", "AL-03": "HIGH", "AL-04": "MED", "AL-05": "MED", "AL-06": "MED",
            "AL-07": "MED", "AL-08": "HIGH", "AL-09": "HIGH", "AL-10": "HIGH", "AL-11": "HIGH", "AL-12": "HIGH",
            "AL-13": "MED"}
TITLES = {"AL-01": "Claimed above measured (beyond tolerance)", "AL-02": "Missing field daily report",
          "AL-03": "Duplicate / overlapping KP claim", "AL-04": "Cumulative claim exceeds BoQ quantity",
          "AL-05": "Productivity drop vs 5-day median", "AL-06": "Claimed with no measurement or evidence",
          "AL-07": "Equipment reported working, telematics idle", "AL-08": "Out-of-sequence progress",
          "AL-09": "Claimed headcount above sensed", "AL-10": "Impossible presence (two fronts)",
          "AL-11": "Equipment hours not supported by telematics", "AL-12": "Front reported active, no presence signal",
          "AL-13": "Weather standby not supported"}


def rows(conn, sql, args=()):
    return [dict(r) for r in conn.execute(sql, args)]


class Data:
    """In-memory snapshot of the database (the demo dataset is small)."""

    def __init__(self, conn):
        q = lambda t: rows(conn, f"SELECT * FROM {t}")  # noqa: E731
        self.sections = q("section")
        self.sec_by_id = {s["section_id"]: s for s in self.sections}
        self.acts = {a["activity_code"]: a for a in q("activity_type")}
        self.crews = {c["crew_id"]: c for c in q("crew")}
        self.equipment = {e["equipment_id"]: e for e in q("equipment")}
        self.boq = {b["boq_item_id"]: b for b in q("boq_item")}
        self.sub_of_act = {}
        for b in self.boq.values():
            self.sub_of_act.setdefault(b["activity_code"], b["subcontractor_id"])
        for c in self.crews.values():
            self.sub_of_act.setdefault(c["activity_code"], c["subcontractor_id"])
        self.rate = {(b["subcontractor_id"], b["activity_code"]): b["unit_rate"] for b in self.boq.values()}
        self.planned = {(p["section_id"], p["activity_code"]): p["planned_qty"] for p in q("planned_quantity")}
        self.fronts = {f["front_id"]: f for f in q("work_front")}
        self.reports = {r["report_id"]: r for r in q("field_report")}
        self.report_lines = q("field_report_line")
        self.claim_lines = q("subcontractor_claim_line")
        self.claims = {c["claim_id"]: c for c in q("subcontractor_claim")}
        self.measurements = q("measurement")
        self.flights = q("drone_flight")
        self.telematics = {(t["equipment_id"], t["work_date"]): t for t in q("telematics_daily")}
        self.presence = q("presence_daily")
        self.badges = q("badge_event")
        self.trips = q("vehicle_trip")
        self.weather = {w["work_date"]: w for w in q("weather_obs")}
        self.resource_claims = q("resource_claim")
        self.equipment_claims = q("equipment_claim")
        self.standby = q("standby_claim")
        self.certs = q("certification_line")
        self.invoices = q("invoice_line")
        self.alert_state = {a["alert_id"]: a for a in q("alert_state")}
        # derived: claim line subcontractor
        for cl in self.claim_lines:
            cl["subcontractor_id"] = self.boq.get(cl["boq_item_id"], {}).get("subcontractor_id") or \
                self.sub_of_act.get(cl["activity_code"])
        for ln in self.report_lines:
            rep = self.reports.get(ln["report_id"], {})
            ln["report_date"] = rep.get("report_date")
            ln["crew_id"] = rep.get("crew_id")
            ln["front_id"] = rep.get("front_id")
        self.dates = sorted({r["report_date"] for r in self.reports.values()} | {w for w in self.weather})


def section_shares(data, kf, kt, section_id=None):
    """Pro rata split of a KP interval over sections (D-053, D-057)."""
    if section_id and (kf is None or kt is None):
        return [(section_id, 1.0)]
    if kf is None or kt is None or kt <= kf:
        return [(section_id, 1.0)] if section_id else []
    out = []
    for s in data.sections:
        ov = min(kt, s["kp_to_m"]) - max(kf, s["kp_from_m"])
        if ov > 0:
            out.append((s["section_id"], ov / (kt - kf)))
    return out


def to_metres(data, code, qty):
    unit = data.acts[code]["unit"]
    return qty * C.JOINT_LEN_M if unit == "nr" else qty / C.ROW_WIDTH_M if unit == "m2" else qty


def classify(claimed, measured, u, tol):
    if measured is None:
        return "UNVERIFIABLE" if claimed > 0 else "MATCHED"
    diff = abs(claimed - measured)
    if diff <= u + 1e-9:
        return "MATCHED"
    if diff <= u + tol + 1e-9:
        return "WITHIN_TOLERANCE"
    return "DISCREPANCY"


def reconcile(data: Data, date: str, with_alerts: dict | None = None) -> list[dict]:
    rep = defaultdict(float)
    claimed_by_date = defaultdict(list)  # key -> [(work_date, qty)]
    for ln in data.report_lines:
        if ln["report_date"] and ln["report_date"] <= date:
            for sid, sh in section_shares(data, ln["kp_from_m"], ln["kp_to_m"]):
                sub = data.crews.get(ln["crew_id"], {}).get("subcontractor_id") or data.sub_of_act.get(ln["activity_code"])
                rep[(sid, ln["activity_code"], sub)] += ln["qty"] * sh
    for cl in data.claim_lines:
        if cl["work_date"] <= date:
            for sid, sh in section_shares(data, cl["kp_from_m"], cl["kp_to_m"], cl["section_id"]):
                claimed_by_date[(sid, cl["activity_code"], cl["subcontractor_id"])].append((cl["work_date"], cl["qty_claimed"] * sh))
    latest_m = {}
    for m in data.measurements:
        if m["measure_date"] <= date:
            k = (m["section_id"], m["activity_code"])
            if k not in latest_m or m["measure_date"] >= latest_m[k]["measure_date"]:
                latest_m[k] = m
    cert, inv = {}, {}
    for c in data.certs:
        if c["cert_date"] <= date and (c["rec_key"] not in cert or c["cert_date"] >= cert[c["rec_key"]]["cert_date"]):
            cert[c["rec_key"]] = c
    for i in data.invoices:
        if i["invoice_date"] <= date and (i["rec_key"] not in inv or i["invoice_date"] >= inv[i["rec_key"]]["invoice_date"]):
            inv[i["rec_key"]] = i
    keys = set(rep) | set(claimed_by_date)
    for (sid, code) in latest_m:
        keys.add((sid, code, data.sub_of_act.get(code)))
    out = []
    for (sid, code, sub) in sorted(keys, key=lambda k: (k[0], data.acts[k[1]]["sequence_no"], k[2] or "")):
        unit = data.acts[code]["unit"]
        claims = claimed_by_date.get((sid, code, sub), [])
        claimed = sum(q for _, q in claims)
        m = latest_m.get((sid, code))
        measured = m["qty_cum"] if m else None
        m_date = m["measure_date"] if m else None
        claimed_at_m = sum(q for d, q in claims if m_date and d <= m_date)
        pending = claimed - claimed_at_m
        u = C.U_K * m["sigma"] if m else 0.0
        tol = max(C.TOL_ABS[unit], C.TOL_PCT[unit] * measured) if m else 0.0
        # Classify on the displayed precision so every status is reproducible from the published figures (audit)
        status = classify(round(claimed_at_m if m else claimed, 1), None if measured is None else round(measured, 1),
                          round(u, 2), round(tol, 2))
        cap = (measured + u + tol) if m else 0.0
        key = f"{sid}|{code}|{sub}"
        unverified_since = min((d for d, _ in claims if not m_date or d > m_date), default=None)
        rate = data.rate.get((sub, code), 0.0)
        row = {
            "key": key, "section_id": sid, "activity_code": code, "subcontractor_id": sub, "unit": unit,
            "planned": round(data.planned.get((sid, code), 0.0), 1), "reported": round(rep.get((sid, code, sub), 0.0), 1),
            "measured": None if measured is None else round(measured, 1), "u": round(u, 2), "tol": round(tol, 2),
            "claimed": round(claimed, 1), "claimed_at_measurement": round(claimed_at_m, 1), "pending": round(pending, 1),
            "certified": round(cert[key]["cum_certified"], 1) if key in cert else 0.0,
            "invoiced": round(inv[key]["cum_invoiced"], 1) if key in inv else 0.0,
            "cap": round(cap, 1), "diff": None if measured is None else round(claimed_at_m - measured, 1),
            "diff_pct": None if not measured else round((claimed_at_m - measured) / measured, 4),
            "status": status, "verification_source": data.acts[code]["verification_source"],
            "measurement_source": m["source"] if m else None, "last_flight": m_date,
            "unverified_since": unverified_since, "rate": rate, "alerts": [],
        }
        row["certifiable"] = round(min(claimed_at_m, cap) if m else 0.0, 1)
        # Certified earlier against an older measurement but now above the cap -> recover in next certificate
        row["over_certified"] = round(max(row["certified"] - cap, 0.0), 1) if m else 0.0
        out.append(row)
    if with_alerts is not None:
        by_key = defaultdict(list)
        for a in with_alerts.values():
            if a.get("rec_key"):
                by_key[a["rec_key"]].append(a["rule_id"])
        for r in out:
            r["alerts"] = sorted(set(by_key.get(r["key"], [])))
    return out


def _aid(rule, entity_id, date):
    return "A-" + hashlib.sha1(f"{rule}|{entity_id}|{date}".encode()).hexdigest()[:8].upper()


def alerts(data: Data, date: str, rec_rows: list[dict] | None = None) -> dict[str, dict]:
    rec_rows = rec_rows if rec_rows is not None else reconcile(data, date)
    out: dict[str, dict] = {}

    def add(rule, entity, entity_id, work_date, explanation, **kw):
        aid = _aid(rule, entity_id, work_date)
        st = data.alert_state.get(aid, {})
        a = {"alert_id": aid, "rule_id": rule, "severity": SEVERITY[rule], "title": TITLES[rule], "work_date": work_date,
             "section_id": kw.get("section_id"), "front_id": kw.get("front_id"), "activity_code": kw.get("activity_code"),
             "subcontractor_id": kw.get("subcontractor_id"), "crew_id": kw.get("crew_id"),
             "equipment_id": kw.get("equipment_id"), "rec_key": kw.get("rec_key"), "entity": entity,
             "entity_id": entity_id, "explanation": explanation, "status": st.get("status", "OPEN"),
             "comment": st.get("comment")}
        out[aid] = a

    dates = [d for d in data.dates if d <= date]
    crew_sub = {c: v["subcontractor_id"] for c, v in data.crews.items()}

    # AL-01 over-claim beyond tolerance; AL-06 unverifiable claims older than grace period
    grace_limit = (dt.date.fromisoformat(date) - dt.timedelta(days=C.AL06_GRACE_DAYS)).isoformat()
    for r in rec_rows:
        ctx = dict(section_id=r["section_id"], activity_code=r["activity_code"], subcontractor_id=r["subcontractor_id"],
                   rec_key=r["key"])
        if r["status"] == "DISCREPANCY" and r["diff"] is not None and r["diff"] > 0:
            add("AL-01", "reconciliation", r["key"], r["last_flight"],
                f"Claimed {r['claimed_at_measurement']} {r['unit']} vs measured {r['measured']} ± {r['u']} "
                f"(tolerance {r['tol']}); cap {r['cap']}", **ctx)
        if r["claimed"] > 0 and r["unverified_since"] and r["unverified_since"] <= grace_limit:
            add("AL-06", "reconciliation", r["key"], r["unverified_since"],
                f"{r['pending'] if r['measured'] is not None else r['claimed']} {r['unit']} claimed since "
                f"{r['unverified_since']} with no independent measurement", **ctx)

    # AL-04 cumulative claimed vs BoQ contract quantity
    cum_boq = defaultdict(float)
    for cl in data.claim_lines:
        if cl["work_date"] <= date:
            cum_boq[cl["boq_item_id"]] += cl["qty_claimed"]
    for bid, q in cum_boq.items():
        b = data.boq.get(bid)
        if b and q > b["contract_qty"] + 1e-6:
            add("AL-04", "boq_item", bid, date, f"Cumulative claimed {q:.1f} {b['unit']} > BoQ {b['contract_qty']}",
                activity_code=b["activity_code"], subcontractor_id=b["subcontractor_id"])

    # AL-03 overlapping claim lines (same activity, KP overlap >= threshold)
    by_act = defaultdict(list)
    for cl in data.claim_lines:
        if cl["work_date"] <= date and cl["kp_from_m"] is not None:
            by_act[cl["activity_code"]].append(cl)
    for code, lines in by_act.items():
        lines.sort(key=lambda x: x["kp_from_m"])
        active = []
        for cl in lines:
            active = [a for a in active if a["kp_to_m"] > cl["kp_from_m"] + C.AL03_MIN_OVERLAP_M]
            for a in active:
                ov = min(a["kp_to_m"], cl["kp_to_m"]) - max(a["kp_from_m"], cl["kp_from_m"])
                if ov >= C.AL03_MIN_OVERLAP_M:
                    sid = cl["section_id"]
                    add("AL-03", "claim_line", a["claim_line_id"], max(a["work_date"], cl["work_date"]),
                        f"{a['claim_line_id']} and {cl['claim_line_id']} overlap by {ov:.0f} m "
                        f"(KP {cl['kp_from_m']:.0f}–{cl['kp_to_m']:.0f})", section_id=sid, activity_code=code,
                        subcontractor_id=cl["subcontractor_id"], rec_key=f"{sid}|{code}|{cl['subcontractor_id']}",
                        claim_lines=[a["claim_line_id"], cl["claim_line_id"]])
                    out[_aid("AL-03", a["claim_line_id"], max(a["work_date"], cl["work_date"]))]["related"] = cl["claim_line_id"]
            active.append(cl)

    # AL-08 out-of-sequence (cumulative claimed successor > predecessor at the claim date)
    claims_sec = defaultdict(list)
    for cl in data.claim_lines:
        if cl["work_date"] <= date:
            claims_sec[(cl["section_id"], cl["activity_code"])].append(cl)
    for sec in data.sections:
        sid = sec["section_id"]
        for pred, succ in C.PRECEDENCE:
            if pred not in data.acts or succ not in data.acts:
                continue
            succ_lines = sorted(claims_sec.get((sid, succ), []), key=lambda x: x["work_date"])
            pred_lines = claims_sec.get((sid, pred), [])
            for d in sorted({cl["work_date"] for cl in succ_lines}):
                cs = sum(to_metres(data, succ, cl["qty_claimed"]) for cl in succ_lines if cl["work_date"] <= d)
                cp = sum(to_metres(data, pred, cl["qty_claimed"]) for cl in pred_lines if cl["work_date"] <= d)
                if cs > cp + C.AL08_TOL_M:
                    sub = data.sub_of_act.get(succ)
                    add("AL-08", "reconciliation", f"{sid}|{succ}|{sub}", d,
                        f"{succ} claimed {cs:.0f} m but {pred} only {cp:.0f} m in {sid} on {d}", section_id=sid,
                        activity_code=succ, subcontractor_id=sub, rec_key=f"{sid}|{succ}|{sub}")
                    break

    # Daily crew-level rules
    reports_by = defaultdict(list)
    for ln in data.report_lines:
        if ln["report_date"] and ln["report_date"] <= date:
            reports_by[(ln["crew_id"], ln["report_date"])].append(ln)
    presence = {(p["crew_id"], p["work_date"]): p for p in data.presence}
    trips = {(t["crew_id"], t["work_date"]) for t in data.trips}
    for rc in data.resource_claims:
        d, crew = rc["work_date"], rc["crew_id"]
        if d > date:
            continue
        p = presence.get((crew, d))
        if (crew, d) not in reports_by:  # AL-02
            add("AL-02", "crew", f"{crew}|{d}", d, f"{crew} claimed/sensed on {d} but no field report received",
                crew_id=crew, subcontractor_id=rc["subcontractor_id"], front_id=rc["front_id"])
        if p is None and (crew, d) not in trips:  # AL-12
            add("AL-12", "front", f"{rc['front_id']}|{d}", d,
                f"{rc['front_id']} reported/claimed active by {crew} but no check-in, vehicle, camera or badge signal",
                crew_id=crew, subcontractor_id=rc["subcontractor_id"], front_id=rc["front_id"])
        elif p is not None:  # AL-09
            sensed = max(p["checkin_count"] or 0, p["manifest_count"] or 0)
            if rc["headcount_claimed"] > sensed + C.TOL_HEAD:
                add("AL-09", "resource_claim", f"{crew}|{d}", d,
                    f"Claimed {rc['headcount_claimed']}; check-in {p['checkin_count']}, manifest {p['manifest_count']}"
                    f"{', camera ' + str(p['camera_max']) if p['camera_max'] is not None else ''} (tolerance {C.TOL_HEAD})",
                    crew_id=crew, subcontractor_id=rc["subcontractor_id"], front_id=rc["front_id"])

    # AL-05 productivity drop (excludes logged downtime and non-workable weather)
    series = defaultdict(list)
    for (crew, d), lines in sorted(reports_by.items(), key=lambda x: x[0][1]):
        code = lines[0]["activity_code"]
        metres = sum(to_metres(data, code, ln["qty"]) for ln in lines)
        hours = max(ln["hours_worked"] or 0 for ln in lines)
        if hours <= 0:
            continue
        excused = any(ln["downtime_reason"] for ln in lines) or \
            data.weather.get(d, {}).get("condition", "WORKABLE") != "WORKABLE"
        series[crew].append((d, metres / hours, excused, lines))
    for crew, ser in series.items():
        for idx, (d, prod, excused, lines) in enumerate(ser):
            prev = [p for _, p, ex, _ in ser[max(0, idx - 8):idx] if not ex][-5:]
            if len(prev) < 3 or excused:
                continue
            med = statistics.median(prev)
            if med > 0 and prod < med * (1 - C.AL05_DROP):
                add("AL-05", "crew", f"{crew}|{d}", d, f"{crew} productivity {prod:.1f} m/h vs 5-day median {med:.1f} "
                    f"({(prod / med - 1) * 100:.0f} %), no downtime or weather logged", crew_id=crew,
                    subcontractor_id=crew_sub.get(crew), activity_code=lines[0]["activity_code"],
                    front_id=lines[0]["front_id"])

    # AL-07 equipment reported working but telematics idle
    for (crew, d), lines in reports_by.items():
        hours = max(ln["hours_worked"] or 0 for ln in lines)
        eqs = {e for ln in lines for e in (ln["equipment_ids"] or "").split(";") if e}
        for e in eqs:
            t = data.telematics.get((e, d))
            if t and t["data_status"] == "OK" and hours > 0 and t["working_h"] < C.AL07_RATIO * hours:
                add("AL-07", "equipment", f"{e}|{d}", d, f"{e} reported {hours:.1f} h working; telematics working "
                    f"{t['working_h']:.1f} h (engine {t['engine_h']:.1f} h)", equipment_id=e, crew_id=crew,
                    subcontractor_id=crew_sub.get(crew))

    # AL-11 equipment hire hours vs telematics engine hours
    for ec in data.equipment_claims:
        if ec["work_date"] > date:
            continue
        t = data.telematics.get((ec["equipment_id"], ec["work_date"]))
        if t and t["data_status"] == "OK" and ec["hours_claimed"] > t["engine_h"] + C.TOL_EQ_H:
            add("AL-11", "equipment", f"{ec['equipment_id']}|{ec['work_date']}", ec["work_date"],
                f"{ec['equipment_id']} claimed {ec['hours_claimed']:.1f} h; engine-on {t['engine_h']:.1f} h",
                equipment_id=ec["equipment_id"], subcontractor_id=ec["subcontractor_id"])

    # AL-10 impossible presence (pseudonymised badge IDs; identities never leave HR/HSE)
    mid = {f: (v["kp_from_m"] + v["kp_to_m"]) / 2 for f, v in data.fronts.items()}
    ev = defaultdict(list)
    for b in data.badges:
        if b["ts"][:10] <= date:
            ev[b["badge_pid"]].append(b)
    for pid, es in ev.items():
        es.sort(key=lambda x: x["ts"])
        for a, b in zip(es, es[1:]):
            if a["front_id"] == b["front_id"] or a["ts"][:10] != b["ts"][:10]:
                continue
            km = abs(mid.get(a["front_id"], 0) - mid.get(b["front_id"], 0)) / 1000
            h = (dt.datetime.fromisoformat(b["ts"].replace("Z", "")) - dt.datetime.fromisoformat(a["ts"].replace("Z", ""))).total_seconds() / 3600
            if km > 1 and (h <= 0 or km / h > C.AL10_MAX_KMH):
                add("AL-10", "badge", f"{pid}|{a['ts'][:10]}", a["ts"][:10],
                    f"Badge {pid} at {a['front_id']} {a['ts'][11:16]} and {b['front_id']} {b['ts'][11:16]} "
                    f"({km:.0f} km apart)", front_id=b["front_id"])

    # AL-13 weather standby claimed on a workable day
    for sb in data.standby:
        if sb["work_date"] > date or sb["reason"] != "WEATHER":
            continue
        w = data.weather.get(sb["work_date"])
        if w and w["wind_ms"] < C.WEATHER_WIND_LIMIT_MS and w["precip_mm"] < C.WEATHER_PRECIP_LIMIT_MM:
            add("AL-13", "standby_claim", sb["sb_id"], sb["work_date"],
                f"Weather standby {sb['hours']} h claimed; site weather wind {w['wind_ms']} m/s, rain {w['precip_mm']} mm "
                f"(limits {C.WEATHER_WIND_LIMIT_MS} m/s / {C.WEATHER_PRECIP_LIMIT_MM} mm)", crew_id=sb["crew_id"],
                subcontractor_id=sb["subcontractor_id"])
    return out


def certify_history(conn, data: Data):
    """Synthetic certification/invoice history: weekly QS certification up to 14 days before the last date."""
    last = data.dates[-1]
    limit = (dt.date.fromisoformat(last) - dt.timedelta(days=14)).isoformat()
    cert_dates = [d for d in data.dates if d <= limit and dt.date.fromisoformat(d).weekday() == 5]
    prev = {}
    n = 0
    for cd in cert_dates:
        for r in reconcile(data, cd):
            if r["claimed"] <= 0:
                continue
            cum = r["certifiable"] if r["status"] != "UNVERIFIABLE" else prev.get(r["key"], 0.0)
            cum = max(cum, prev.get(r["key"], 0.0))
            n += 1
            conn.execute("INSERT INTO certification_line VALUES(?,?,?,?,?,?,?)",
                         (f"CERT-{n:06d}", r["key"], cd, round(cum, 1), "QS", None, "SYNTHETIC history"))
            if r["key"] in prev:
                conn.execute("INSERT INTO invoice_line VALUES(?,?,?,?,?)",
                             (f"INV-{n:06d}", r["key"], cd, prev[r["key"]], f"SYN-INV-{cd}"))
            prev[r["key"]] = round(cum, 1)
    conn.commit()
