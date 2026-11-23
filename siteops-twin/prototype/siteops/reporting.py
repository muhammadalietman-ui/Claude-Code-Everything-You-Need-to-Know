"""Client daily report (Bautagesbericht) generated from the SiteOps data model.

Mirrors the structure of a real contractor-to-client daily report: weather, man-hours, equipment hours,
narrative, detailed activity progress. It adds what that report cannot show: independent verification of each
activity, sensed vs reported man-hours, and measured (telematics) vs calculated equipment hours.
"""
from __future__ import annotations

from collections import defaultdict

from .engine import Data, sheets_for


def daily_report(data: Data, date: str, rec_rows: list[dict], alerts: dict) -> dict:
    days = [d for d in data.dates if d <= date]
    report_no = len(days)
    nxt = next((d for d in data.dates if d > date), None)
    w = data.weather.get(date, {})
    # 2. Personnel (man-hours)
    mp = defaultdict(lambda: {"cum_prev": 0.0, "local": 0.0, "external": 0.0, "sensed_today": None})
    for r in data.manpower:
        key = r["company_type"] if r["company_type"] != "SUB" else f"SUB|{r['subcontractor_id']}"
        if r["work_date"] < date:
            mp[key]["cum_prev"] += r["manhours_reported"] or 0
        elif r["work_date"] == date:
            mp[key]["local" if r["origin"] == "LOCAL" else "external"] += r["manhours_reported"] or 0
            if r["manhours_sensed"] is not None:
                mp[key]["sensed_today"] = (mp[key]["sensed_today"] or 0) + r["manhours_sensed"]
    personnel = []
    for k in sorted(mp, key=lambda k: (k.startswith("SUB"), k)):
        v = mp[k]
        today = v["local"] + v["external"]
        personnel.append({"group": k.replace("SUB|", ""), "company_type": "SUB" if k.startswith("SUB") else k,
                          "cum_prev": round(v["cum_prev"]), "today_local": round(v["local"]),
                          "today_external": round(v["external"]), "today_total": round(today),
                          "cum": round(v["cum_prev"] + today),
                          "sensed_today": None if v["sensed_today"] is None else round(v["sensed_today"]),
                          "unverified_today": None if v["sensed_today"] is None else round(today - v["sensed_today"])})
    # 3. Equipment hours: calculated (days assigned) vs measured (telematics)
    eq = defaultdict(lambda: {"cum_prev": 0.0, "today_calc": 0.0, "today_measured": 0.0, "today_no_telematics": 0.0})
    for r in data.eq_calc:
        owner = data.equipment.get(r["equipment_id"], {}).get("owner", "?")
        if r["work_date"] < date:
            eq[owner]["cum_prev"] += r["calc_hours"]
        elif r["work_date"] == date:
            eq[owner]["today_calc"] += r["calc_hours"]
            t = data.telematics.get((r["equipment_id"], date))
            if t:
                eq[owner]["today_measured"] += t["engine_h"]
            else:
                eq[owner]["today_no_telematics"] += r["calc_hours"]
    equipment = [{"owner": k, "cum_prev": round(v["cum_prev"]), "today_calc": round(v["today_calc"]),
                  "cum": round(v["cum_prev"] + v["today_calc"]), "today_measured_engine_h": round(v["today_measured"], 1),
                  "today_without_telematics_h": round(v["today_no_telematics"]),
                  "calc_minus_measured_h": round(v["today_calc"] - v["today_no_telematics"] - v["today_measured"], 1)}
                 for k, v in sorted(eq.items())]
    # 4./5. Narrative
    items = [i for i in data.summary if i["work_date"] == date]
    # 6. Detailed activity progress + independent check
    prev, today, sheets_today = defaultdict(float), defaultdict(float), defaultdict(list)
    for ln in data.report_lines:
        if not ln["report_date"] or ln["report_date"] > date:
            continue
        (today if ln["report_date"] == date else prev)[ln["activity_code"]] += ln["qty"] or 0
        if ln["report_date"] == date and ln["kp_from_m"] is not None:
            sheets_today[ln["activity_code"]].append((ln["kp_from_m"], ln["kp_to_m"]))
    planned = defaultdict(float)
    for (sid, code), q in data.planned.items():
        planned[code] += q
    order = ["MATCHED", "WITHIN_TOLERANCE", "UNVERIFIABLE", "DISCREPANCY"]
    detail = []
    for code, a in sorted(data.acts.items(), key=lambda x: x[1]["sequence_no"]):
        rows = [r for r in rec_rows if r["activity_code"] == code]
        cum = prev[code] + today[code]
        kps = sheets_today.get(code)
        detail.append({
            "activity_code": code, "name_de": a.get("name_de") or a["name"], "name": a["name"], "unit": a["unit"],
            "total": round(planned[code], 1), "sheets_today": sheets_for(data, min(k[0] for k in kps), max(k[1] for k in kps)) if kps else None,
            "cum_prev": round(prev[code], 1), "this_period": round(today[code], 1), "cum": round(cum, 1),
            "pct": round(cum / planned[code], 4) if planned[code] else None,
            "measured_cum": round(sum(r["measured"] for r in rows if r["measured"] is not None), 1),
            "claimed_cum": round(sum(r["claimed"] for r in rows), 1),
            "verification_source": a["verification_source"],
            "worst_status": max((r["status"] for r in rows if r["claimed"] > 0), key=order.index, default=None),
            "open_alerts": sorted({x["rule_id"] for x in alerts.values() if x["activity_code"] == code and x["status"] != "CLOSED"})})
    al14 = [x for x in alerts.values() if x["rule_id"] == "AL-14" and x["work_date"] == date]
    return {"report_no": report_no, "date": date, "next_working_day": nxt, "synthetic": True,
            "weather": {"today": w, "next": data.weather.get(nxt) if nxt else None},
            "personnel": personnel, "equipment": equipment,
            "completed": [i["text"] for i in items if i["kind"] == "COMPLETED"],
            "planned": [i["text"] for i in items if i["kind"] == "PLANNED"],
            "hse": [i["text"] for i in items if i["kind"] == "HSE"],
            "detail": detail, "consistency_alerts": al14,
            "notes": ["Equipment hours in the client report are calculated from days assigned (as in current practice); "
                      "the 'measured' column shows telematics engine hours where available.",
                      "Sensed man-hours = check-in headcount x reported hours (subcontractors only)."]}
