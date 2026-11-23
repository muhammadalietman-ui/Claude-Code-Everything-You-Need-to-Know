"""Synthetic dataset generator for SYN-SPREAD-01 (spec: 04_to_be_architecture/data_model/synthetic_dataset_spec.md).

Everything produced here is SYNTHETIC: no real project, company, person, location or contract value.
Each of the alert rules AL-01..AL-13 gets at least one deliberately seeded anomaly, recorded in
`anomaly_ground_truth`, so the engine can be tested against a known answer.
"""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

from . import config as C

ACTIVITIES = [
    # code, name, unit, seq, uav_observability, verification, subcontractor, crew, nominal rate (unit/day), crew size, lag days
    ("CLR", "ROW clearing & topsoil strip", "m", 1, "Yes", "UAV", "SYN-SUB-A", "SYN-CRW-01", 900, 12, 0),
    ("GRD", "Grading", "m", 2, "Yes", "UAV", "SYN-SUB-A", "SYN-CRW-02", 850, 10, 3),
    ("STR", "Stringing", "m", 3, "Yes", "UAV", "SYN-SUB-C", "SYN-CRW-03", 800, 9, 6),
    ("WLD", "Mainline welding", "nr", 4, "No", "LOG", "SYN-SUB-C", "SYN-CRW-04", 45, 24, 9),
    ("FJC", "Field joint coating", "nr", 5, "No", "LOG", "SYN-SUB-C", "SYN-CRW-05", 44, 10, 12),
    ("TRN", "Trenching", "m", 6, "Partial", "UAV", "SYN-SUB-B", "SYN-CRW-06", 520, 16, 12),
    ("LOW", "Lowering-in", "m", 7, "Time-window", "ASBUILT", "SYN-SUB-D", "SYN-CRW-07", 500, 14, 16),
    ("BKF", "Padding & backfill", "m", 8, "Yes", "UAV", "SYN-SUB-B", "SYN-CRW-08", 480, 12, 19),
    ("RST", "Clean-up & reinstatement", "m2", 9, "Yes", "UAV", "SYN-SUB-A", "SYN-CRW-09", 13500, 10, 24),
]
PRED = {"GRD": "CLR", "STR": "GRD", "WLD": "STR", "FJC": "WLD", "TRN": "GRD", "LOW": "FJC", "BKF": "LOW", "RST": "BKF"}
EXTRA_PRED = {"LOW": "TRN"}
RATES = {"CLR": 2.0, "GRD": 3.0, "STR": 1.5, "WLD": 180.0, "FJC": 60.0, "TRN": 25.0, "LOW": 15.0, "BKF": 12.0, "RST": 0.8}
SUBS = {
    "SYN-SUB-A": "Clearing, grading, reinstatement",
    "SYN-SUB-B": "Trenching, padding and backfill",
    "SYN-SUB-C": "Stringing, welding, coating",
    "SYN-SUB-D": "Lowering-in and crossings",
}
EQUIP_TYPES = {
    "CLR": ["Dozer", "Excavator", "Mulcher"], "GRD": ["Grader", "Dozer", "Excavator"], "STR": ["Pipe carrier", "Side boom"],
    "WLD": ["Welding tractor", "Welding tractor", "Side boom", "Side boom"], "FJC": ["Coating rig", "Compressor"],
    "TRN": ["Excavator", "Excavator", "Excavator"], "LOW": ["Side boom", "Side boom", "Side boom"],
    "BKF": ["Padding machine", "Excavator", "Dozer"], "RST": ["Dozer", "Tractor & harrow"],
}
BUFFER_M = 300.0
CAMERA_FRONTS = {"FR-05", "FR-12", "FR-18"}


def kp_to_m(code: str, qty: float) -> float:
    unit = next(a[2] for a in ACTIVITIES if a[0] == code)
    return qty * C.JOINT_LEN_M if unit == "nr" else qty / C.ROW_WIDTH_M if unit == "m2" else qty


def m_to_qty(code: str, metres: float) -> float:
    unit = next(a[2] for a in ACTIVITIES if a[0] == code)
    return metres / C.JOINT_LEN_M if unit == "nr" else metres * C.ROW_WIDTH_M if unit == "m2" else metres


def section_of(kp: float) -> str:
    return f"S{min(int(kp // C.SECTION_LEN_M) + 1, C.KP_END_M // C.SECTION_LEN_M):02d}"


def front_of(kp: float) -> str:
    return "FR-" + section_of(kp)[1:]


def working_days() -> list[str]:
    d = dt.date.fromisoformat(C.START_DATE)
    out = []
    while len(out) < C.N_WORKING_DAYS:
        if d.weekday() < 6:  # Mon-Sat
            out.append(d.isoformat())
        d += dt.timedelta(days=1)
    return out


def centreline(step=100.0):
    """Synthetic alignment in a local CRS (metres). KP = arc length, so the shape is not a real route."""
    pts, x, y = [(0.0, 0.0)], 0.0, 0.0
    s = 0.0
    while s < C.KP_END_M:
        theta = 0.35 * math.sin(s / 5200.0) + 0.15 * math.sin(s / 1700.0)
        x += math.cos(theta) * step
        y += math.sin(theta) * step
        s += step
        pts.append((round(x, 2), round(y, 2)))
    return pts


def generate(seed: int = C.SEED) -> dict[str, list[dict]]:
    rng = np.random.default_rng(seed)
    days = working_days()
    T: dict[str, list[dict]] = {k: [] for k in [
        "spread", "section", "activity_type", "subcontractor", "crew", "equipment", "boq_item", "planned_quantity",
        "work_front", "field_report", "field_report_line", "subcontractor_claim", "subcontractor_claim_line",
        "resource_claim", "equipment_claim", "standby_claim", "drone_flight", "measurement", "telematics_daily",
        "presence_daily", "badge_event", "vehicle_trip", "weather_obs", "anomaly_ground_truth"]}
    gt = T["anomaly_ground_truth"]

    def truth(rule, entity, entity_id, date, desc):
        gt.append({"anomaly_id": f"GT-{len(gt) + 1:03d}", "rule_id": rule, "entity": entity, "entity_id": entity_id,
                   "work_date": date, "description": desc})

    # ---------- master data ----------
    T["spread"].append({"spread_id": C.SPREAD_ID, "name": "Synthetic 24-inch onshore spread", "site_tz": C.SITE_TZ,
                        "crs_code": "SYN-LOCAL", "kp_start_m": 0, "kp_end_m": C.KP_END_M, "is_synthetic": 1})
    n_sec = C.KP_END_M // C.SECTION_LEN_M
    for i in range(n_sec):
        sid = f"S{i + 1:02d}"
        T["section"].append({"section_id": sid, "spread_id": C.SPREAD_ID, "kp_from_m": i * 1000, "kp_to_m": (i + 1) * 1000})
        T["work_front"].append({"front_id": f"FR-{i + 1:02d}", "type": "MAINLINE", "name": f"Front {i + 1:02d}",
                                "kp_from_m": i * 1000, "kp_to_m": (i + 1) * 1000})
    for sub, scope in SUBS.items():
        T["subcontractor"].append({"subcontractor_id": sub, "scope": scope})
    eq_n = 0
    crew_members: dict[str, list[str]] = {}
    for code, name, unit, seq, obs, ver, sub, crew, rate, size, lag in ACTIVITIES:
        T["activity_type"].append({"activity_code": code, "name": name, "unit": unit, "sequence_no": seq,
                                   "uav_observability": obs, "verification_source": ver})
        T["crew"].append({"crew_id": crew, "subcontractor_id": sub, "activity_code": code, "nominal_size": size})
        crew_members[crew] = [f"B-{1000 + seq * 100 + k}" for k in range(size)]  # pseudonymised badge IDs
        for etype in EQUIP_TYPES[code]:
            eq_n += 1
            T["equipment"].append({"equipment_id": f"SYN-EQ-{eq_n:03d}", "type": etype, "owner": sub, "crew_id": crew,
                                   "telematics_enabled": int(rng.random() < 0.8 or etype == "Excavator")})
        total = m_to_qty(code, C.KP_END_M)
        contract = total * (0.98 if code == "CLR" else 1.0)  # seeded: CLR BoQ under-sized -> AL-04
        T["boq_item"].append({"boq_item_id": f"BOQ-{sub[-1]}-{code}", "subcontractor_id": sub, "activity_code": code,
                              "unit": unit, "unit_rate": RATES[code], "contract_qty": round(contract, 1)})
        for s in T["section"]:
            T["planned_quantity"].append({"section_id": s["section_id"], "activity_code": code,
                                          "planned_qty": round(m_to_qty(code, 1000), 1), "unit": unit})
    act = {a[0]: a for a in ACTIVITIES}
    eq_by_crew: dict[str, list[dict]] = {}
    for e in T["equipment"]:
        eq_by_crew.setdefault(e["crew_id"], []).append(e)

    # ---------- weather ----------
    stop_days = set(rng.choice(range(5, len(days)), 4, replace=False).tolist())
    half_days = set(rng.choice([i for i in range(5, len(days)) if i not in stop_days], 6, replace=False).tolist())
    weather_factor = {}
    for i, d in enumerate(days):
        if i in stop_days:
            cond, wind, precip, f = "STOPPED", float(rng.uniform(17, 24)), float(rng.uniform(25, 40)), 0.0
        elif i in half_days:
            cond, wind, precip, f = "RESTRICTED", float(rng.uniform(11, 15)), float(rng.uniform(8, 18)), 0.5
        else:
            cond, wind, precip, f = "WORKABLE", float(rng.uniform(2, 9)), float(rng.uniform(0, 4)), 1.0
        weather_factor[d] = f
        T["weather_obs"].append({"work_date": d, "wind_ms": round(wind, 1), "precip_mm": round(precip, 1), "condition": cond})

    # Seeded productivity drops (AL-05): crew, day index, factor
    drops = {("SYN-CRW-04", 30): 0.55, ("SYN-CRW-04", 31): 0.6, ("SYN-CRW-06", 41): 0.5}
    drops = {k: v for k, v in drops.items() if k[1] not in stop_days and k[1] not in half_days}
    for (crew, i), _ in drops.items():
        truth("AL-05", "crew", crew, days[i], "Seeded productivity drop without weather cause")

    # ---------- daily production (true progress) ----------
    pos = {a[0]: 0.0 for a in ACTIVITIES}
    daily_true: list[dict] = []  # true work pieces
    no_fly = set(rng.choice(range(3, len(days)), 5, replace=False).tolist()) | stop_days
    for i, d in enumerate(days):
        for code, name, unit, seq, obs, ver, sub, crew, rate, size, lag in ACTIVITIES:
            if i < lag or pos[code] >= C.KP_END_M:
                continue
            # lognormal sigma 0.08: sigma 0.12 gave ~1.3 % AL-05 false positives at a 25 % threshold
            mult = float(rng.lognormal(0, 0.08)) * weather_factor[d] * drops.get((crew, i), 1.0)
            cap_m = C.KP_END_M - pos[code]
            constrained = False
            for p in [PRED.get(code), EXTRA_PRED.get(code)]:
                if p:
                    lim = (pos[p] if pos[p] >= C.KP_END_M else pos[p] - BUFFER_M) - pos[code]
                    if lim < cap_m:
                        cap_m = max(lim, 0.0)
            want_m = kp_to_m(code, rate * mult)
            if want_m > cap_m:
                constrained = True
            adv = max(min(want_m, cap_m), 0.0)
            hours = 10.0 * (weather_factor[d] if weather_factor[d] > 0 else 0)
            if hours == 0:
                continue
            if adv < 1.0 and not constrained:
                continue
            kp_from, kp_to = pos[code], pos[code] + adv
            pos[code] = kp_to
            daily_true.append({"i": i, "date": d, "code": code, "sub": sub, "crew": crew, "kp_from": kp_from,
                               "kp_to": kp_to, "hours": hours, "size": size, "constrained": constrained,
                               "weather": weather_factor[d]})

    # ---------- field reports (one per crew per day), split by section ----------
    rep_n = line_n = 0
    missing_reports = {("SYN-CRW-06", 22), ("SYN-CRW-06", 37)}
    for w in daily_true:
        crew, i = w["crew"], w["i"]
        headcount = int(w["size"] - (rng.random() < 0.3))
        w["headcount"] = headcount
        w["front"] = front_of((w["kp_from"] + w["kp_to"]) / 2)
        if (crew, i) in missing_reports:
            truth("AL-02", "crew", crew, w["date"], "Seeded missing field daily report")
            continue
        rep_n += 1
        rid = f"FRP-{rep_n:05d}"
        T["field_report"].append({"report_id": rid, "client_uuid": f"syn-{rid}", "report_date": w["date"], "crew_id": crew,
                                  "front_id": w["front"], "submitted_at": f"{w['date']}T17:{int(rng.integers(0, 59)):02d}:00Z",
                                  "source_system": "SYNTHETIC", "record_version": 1})
        eqs = [e["equipment_id"] for e in eq_by_crew[crew]]
        reason = "WAITING_FRONT" if w["constrained"] else ("WEATHER" if w["weather"] < 1 else None)
        for kf, kt in split_by_section(w["kp_from"], w["kp_to"]):
            line_n += 1
            qty = m_to_qty(w["code"], kt - kf) * float(1 + rng.normal(0, 0.003))
            T["field_report_line"].append({
                "line_id": f"FRL-{line_n:06d}", "report_id": rid, "activity_code": w["code"], "kp_from_m": round(kf, 1),
                "kp_to_m": round(kt, 1), "qty": round(qty, 1), "unit": act[w["code"]][2], "hours_worked": w["hours"],
                "headcount": headcount, "equipment_ids": ";".join(eqs), "downtime_h": 10 - w["hours"],
                "downtime_reason": reason, "photo_refs": f"SYN-PHOTO-{rid}-{line_n}.jpg"})
        if (kt - kf) <= 0:
            pass

    # ---------- independent measurements ----------
    true_cum: dict[tuple[str, str], list[tuple[str, float]]] = {}
    cum = {}
    by_day: dict[str, list[dict]] = {}
    for w in daily_true:
        by_day.setdefault(w["date"], []).append(w)
    flight_ok = {}
    for i, d in enumerate(days):
        for w in by_day.get(d, []):
            for kf, kt in split_by_section(w["kp_from"], w["kp_to"]):
                key = (section_of(kf + 0.01), w["code"])
                cum[key] = cum.get(key, 0.0) + (kt - kf)
        snap = dict(cum)
        flight_ok[d] = i not in no_fly
        if flight_ok[d]:
            fid = f"SYN-FLT-{d.replace('-', '')}"
            T["drone_flight"].append({"flight_id": fid, "flight_date": d, "kp_cover_from_m": 0, "kp_cover_to_m": C.KP_END_M,
                                      "gsd_cm": round(float(rng.uniform(2.0, 3.0)), 2),
                                      "rmse_xy_m": round(float(rng.uniform(0.02, 0.04)), 3),
                                      "rmse_z_m": round(float(rng.uniform(0.03, 0.05)), 3),
                                      "n_gcp": int(rng.integers(8, 14)), "n_checkpoints": int(rng.integers(5, 9))})
        for (sid, code), metres in snap.items():
            ver = act[code][5]
            if ver == "UAV" and flight_ok[d]:
                if code == "RST" and sid == "S03":
                    continue  # seeded: reinstatement not processed for S03 -> AL-06
                sigma_m = 0.002 * metres + 0.5
                meas_m = metres + float(rng.normal(0, sigma_m))
                add_meas(T, "UAV", fid, d, code, sid, "LENGTH_DIGITISE" if act[code][2] == "m" else "AREA",
                         m_to_qty(code, meas_m), m_to_qty(code, sigma_m), act[code][2])
            elif ver == "LOG":
                add_meas(T, "QA_LOG", None, d, code, sid, "WELD_LOG" if code == "WLD" else "COATING_LOG",
                         round(m_to_qty(code, metres)), 0.0, act[code][2])
            elif ver == "ASBUILT":
                add_meas(T, "ASBUILT_SURVEY", None, d, code, sid, "TOP_OF_PIPE_GNSS", metres + float(rng.normal(0, 0.3)),
                         0.3, "m")
    # keep only the latest measurement per (section, activity, date) chain: the engine takes latest <= date

    # ---------- subcontractor quantity claims (weekly, line per section per work day) ----------
    bias = {"SYN-SUB-A": 0.0, "SYN-SUB-B": 0.0, "SYN-SUB-C": 0.0, "SYN-SUB-D": 0.0}
    inflate = {("S07", "TRN"): 0.12, ("S12", "BKF"): 0.09}
    for (sid, code), _ in inflate.items():
        truth("AL-01", "reconciliation", f"{sid}|{code}|{act[code][6]}", None, "Seeded over-claim vs independent measurement")
    weeks = week_periods(days)
    claim_n = cl_n = 0
    claims_by_week = {}
    for wk_from, wk_to in weeks:
        for sub in SUBS:
            claim_n += 1
            cid = f"CLM-{sub[-1]}-{claim_n:04d}"
            claims_by_week[(sub, wk_to)] = cid
            T["subcontractor_claim"].append({"claim_id": cid, "subcontractor_id": sub, "period_from": wk_from,
                                             "period_to": wk_to, "submitted_at": f"{wk_to}T18:00:00Z", "status": "SUBMITTED"})
    week_of = {d: wk_to for wk_from, wk_to in weeks for d in days if wk_from <= d <= wk_to}

    def add_claim(sub, code, sid, kf, kt, date, qty):
        nonlocal cl_n
        cl_n += 1
        T["subcontractor_claim_line"].append({
            "claim_line_id": f"CL-{cl_n:06d}", "claim_id": claims_by_week[(sub, week_of[date])],
            "boq_item_id": f"BOQ-{sub[-1]}-{code}", "activity_code": code, "section_id": sid, "kp_from_m": round(kf, 1),
            "kp_to_m": round(kt, 1), "work_date": date, "qty_claimed": round(qty, 1), "unit": act[code][2]})
        return T["subcontractor_claim_line"][-1]

    dup_done = overlap_done = False
    for w in daily_true:
        for kf, kt in split_by_section(w["kp_from"], w["kp_to"]):
            sid = section_of(kf + 0.01)
            q = m_to_qty(w["code"], kt - kf) * float(1 + rng.normal(bias[w["sub"]], 0.004))
            q *= 1 + inflate.get((sid, w["code"]), 0.0)
            line = add_claim(w["sub"], w["code"], sid, kf, kt, w["date"], q)
            if not dup_done and w["code"] == "WLD" and w["i"] >= 25 and kt - kf > 300:
                nxt = next(d for d in days if d > week_of[w["date"]])
                add_claim(w["sub"], w["code"], sid, kf, kt, nxt, q)  # same KP range claimed again next week
                truth("AL-03", "claim_line", line["claim_line_id"], w["date"], "Seeded duplicate claim of the same KP range")
                dup_done = True
            if not overlap_done and w["code"] == "BKF" and w["i"] >= 35 and kt - kf > 300:
                add_claim(w["sub"], w["code"], sid, kf + 50, kf + 250, w["date"], m_to_qty("BKF", 200))
                truth("AL-03", "claim_line", line["claim_line_id"], w["date"], "Seeded overlapping backfill claim (200 m)")
                overlap_done = True
    # AL-08 seeded out-of-sequence: lowering-in claimed where no trench exists yet
    d_oos = days[34]
    trn_pos_then = max([w["kp_to"] for w in daily_true if w["code"] == "TRN" and w["i"] <= 34] or [0])
    kp_oos = (int(trn_pos_then // 1000) + 3) * 1000.0
    add_claim("SYN-SUB-D", "LOW", section_of(kp_oos + 1), kp_oos, kp_oos + 300, d_oos, 300.0)
    truth("AL-08", "reconciliation", f"{section_of(kp_oos + 1)}|LOW|SYN-SUB-D", d_oos,
          "Seeded lowering-in claimed ahead of trenching")
    truth("AL-04", "boq_item", "BOQ-A-CLR", None, "Seeded BoQ quantity exceeded by cumulative claims")
    truth("AL-06", "reconciliation", "S03|RST|SYN-SUB-A", None, "Seeded reinstatement claimed with no measurement")

    # ---------- field sensing: presence, vehicles, badges, cameras, telematics, resource claims ----------
    rc_n = ec_n = vt_n = 0
    head_inflate = {("SYN-CRW-06", i) for i in (15, 16, 17, 26)}
    no_presence = ("SYN-CRW-09", 40)
    eq_overclaim = {(e, i) for e in ["SYN-EQ-016"] for i in (28, 29, 33)}   # AL-11
    eq_idle = {(e, i) for e in ["SYN-EQ-017"] for i in (20, 21, 44)}       # AL-07
    for w in daily_true:
        crew, i, d, sub, front = w["crew"], w["i"], w["date"], w["sub"], w["front"]
        hc = w["headcount"]
        claimed_hc = hc + (8 if (crew, i) in head_inflate else 0)
        if (crew, i) in head_inflate:
            truth("AL-09", "resource_claim", crew, d, "Seeded headcount over-claim (+8)")
        rc_n += 1
        T["resource_claim"].append({"rc_id": f"RC-{rc_n:05d}", "subcontractor_id": sub, "crew_id": crew, "front_id": front,
                                    "work_date": d, "headcount_claimed": claimed_hc, "hours_claimed": w["hours"]})
        if (crew, i) == no_presence:
            truth("AL-12", "front", front, d, "Seeded work reported/claimed at a front with no presence signal")
        else:
            manifest = hc + int(rng.integers(-1, 2))
            cam = int(round(hc * rng.uniform(0.8, 0.95))) if front in CAMERA_FRONTS else None
            members = crew_members[crew][:hc]
            badged = [b for b in members if rng.random() < 0.7]
            T["presence_daily"].append({"work_date": d, "front_id": front, "crew_id": crew, "checkin_count": hc,
                                        "manifest_count": manifest, "camera_max": cam, "badge_zone_count": len(badged)})
            vt_n += 1
            T["vehicle_trip"].append({"trip_id": f"VT-{vt_n:05d}", "vehicle_id": f"SYN-BUS-{crew[-2:]}", "crew_id": crew,
                                      "work_date": d, "front_id": front, "arrive_ts": f"{d}T06:{int(rng.integers(10, 50)):02d}:00Z",
                                      "pax": manifest})
            for b in badged:
                T["badge_event"].append({"badge_pid": b, "front_id": front, "ts": f"{d}T06:{int(rng.integers(30, 59)):02d}:00Z"})
        for e in eq_by_crew[crew]:
            eid = e["equipment_id"]
            hours_claimed = w["hours"]
            if e["telematics_enabled"]:
                engine = w["hours"] * float(rng.uniform(0.93, 1.02))
                if (eid, i) in eq_overclaim:
                    engine = w["hours"] * 0.45
                    truth("AL-11", "equipment", eid, d, "Seeded equipment hire hours not supported by telematics")
                working = engine * 0.86
                if (eid, i) in eq_idle:
                    working = w["hours"] * 0.2
                    engine = working + 0.5
                    hours_claimed = engine  # claimed hours honest, but reported as working the full shift
                    truth("AL-07", "equipment", eid, d, "Seeded equipment reported working, telematics idle")
                T["telematics_daily"].append({"equipment_id": eid, "work_date": d, "engine_h": round(engine, 2),
                                              "idle_h": round(engine - working, 2), "working_h": round(working, 2),
                                              "last_kp_m": round(w["kp_to"], 0), "data_status": "OK"})
            ec_n += 1
            T["equipment_claim"].append({"ec_id": f"EC-{ec_n:05d}", "subcontractor_id": sub, "equipment_id": eid,
                                         "work_date": d, "hours_claimed": round(hours_claimed, 2)})
    # AL-10 seeded impossible presence: a welding badge also appears at a far front 15 minutes later
    d10 = days[27]
    wl = next(w for w in daily_true if w["crew"] == "SYN-CRW-04" and w["i"] == 27)
    far = front_of(min(wl["kp_from"] + 14_000, C.KP_END_M - 1) if wl["kp_from"] < 11_000 else wl["kp_from"] - 14_000)
    pid = crew_members["SYN-CRW-04"][0]
    T["badge_event"].append({"badge_pid": pid, "front_id": wl["front"], "ts": f"{d10}T07:00:00Z"})
    T["badge_event"].append({"badge_pid": pid, "front_id": far, "ts": f"{d10}T07:05:00Z"})
    truth("AL-10", "badge", pid, d10, "Seeded impossible presence at two fronts 14 km apart within 5 minutes")
    # Standby claims: legitimate on STOPPED days, one seeded on a workable day (AL-13)
    sb_n = 0
    for i, d in enumerate(days):
        if i in stop_days:
            sb_n += 1
            T["standby_claim"].append({"sb_id": f"SB-{sb_n:04d}", "subcontractor_id": "SYN-SUB-B", "crew_id": "SYN-CRW-06",
                                       "work_date": d, "reason": "WEATHER", "hours": 10})
    workable = [d for i, d in enumerate(days) if i not in stop_days and i not in half_days and i > 20]
    sb_n += 1
    T["standby_claim"].append({"sb_id": f"SB-{sb_n:04d}", "subcontractor_id": "SYN-SUB-B", "crew_id": "SYN-CRW-08",
                               "work_date": workable[5], "reason": "WEATHER", "hours": 10})
    truth("AL-13", "standby_claim", f"SB-{sb_n:04d}", workable[5], "Seeded weather standby on a workable day")
    return T


def add_meas(T, source, flight_id, date, code, sid, method, qty, sigma, unit):
    T["measurement"].append({"measurement_id": f"M-{len(T['measurement']) + 1:06d}", "source": source, "flight_id": flight_id,
                             "measure_date": date, "activity_code": code, "section_id": sid, "method": method,
                             "kp_from_m": None, "kp_to_m": None, "qty_cum": round(qty, 2), "unit": unit,
                             "sigma": round(sigma, 3), "quality_flag": "OK"})


def split_by_section(kf: float, kt: float):
    """Split a KP interval at section boundaries (half-open intervals, D-053)."""
    out, a = [], kf
    while a < kt - 1e-9:
        b = min((math.floor(a / C.SECTION_LEN_M) + 1) * C.SECTION_LEN_M, kt)
        out.append((a, b))
        a = b
    return out


def week_periods(days: list[str]):
    out, cur = [], []
    for d in days:
        cur.append(d)
        if dt.date.fromisoformat(d).weekday() == 5:
            out.append((cur[0], cur[-1]))
            cur = []
    if cur:
        out.append((cur[0], cur[-1]))
    return out
