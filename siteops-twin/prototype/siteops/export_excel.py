"""Excel version of the demo (no Python needed to open it):  python -m siteops.export_excel -> ../dist/SiteOps_Twin_Demo.xlsx

Status and cap are LIVE Excel formulas, so a commercial reviewer can see (and change) the rule:
  cap = M + U + T;  status = MATCHED / WITHIN_TOLERANCE / DISCREPANCY / UNVERIFIABLE (D-063, D-064).
All data is SYNTHETIC.
"""
from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient
from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

DIST = Path(__file__).resolve().parent.parent.parent / "dist"
HEAD = PatternFill("solid", fgColor="1F3A5F")
FILLS = {"MATCHED": "D9F2E6", "WITHIN_TOLERANCE": "DCEBFA", "DISCREPANCY": "FBE0D2", "UNVERIFIABLE": "E6E6E6",
         "OVERCLAIM": "FBE0D2", "NO_SIGNAL": "E6E6E6", "NO_DATA": "E6E6E6", "HIGH": "FBE0D2", "MED": "FFF2CC"}


def table(ws, headers, rows, widths=None):
    ws.append(headers)
    for c in ws[1]:
        c.font, c.fill, c.alignment = Font(bold=True, color="FFFFFF"), HEAD, Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{ws.max_row}"
    for i, h in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(h, max(11, min(len(h) + 2, 40)))


def colour_col(ws, col, values):
    rng = f"{col}2:{col}{ws.max_row}"
    for v in values:
        ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=[f'"{v}"'], fill=PatternFill("solid", fgColor=FILLS[v])))


def build(out=DIST / "SiteOps_Twin_Demo.xlsx", db_path=None):
    from .api import create_app
    c = TestClient(create_app(db_path))
    g = lambda p, **k: c.get(p, params=k).json()  # noqa: E731
    meta = g("/api/meta")
    last = meta["date_max"]
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    for line in [
        ["SiteOps Twin: MVP demo workbook (SYNTHETIC DATA)"], [""],
        ["Synthetic spread SYN-SPREAD-01, 25 km, data to " + last + ". No real project, company, person or contract value."],
        ["Sheets: Reconciliation (live status/cap formulas) · Alerts · Scorecard · Presence · Equipment_Hours · Certificate · Rules"],
        ["Change a tolerance or a claimed quantity in 'Reconciliation' and the status and cap recalculate."],
        ["For the interactive dashboard, open SiteOps_Twin_Dashboard.html in Edge or Chrome (no installation)."]]:
        ws.append(line)
    ws["A1"].font = Font(bold=True, size=14)
    ws.column_dimensions["A"].width = 120

    rec = g("/api/reconciliation", date=last)["rows"]
    ws = wb.create_sheet("Reconciliation")
    H = ["Section", "Activity", "Subcontractor", "Unit", "Planned", "Reported", "Measured M", "U (95%)", "Tolerance T",
         "Claimed (cum)", "Claimed at measurement C", "Pending verification", "Certified", "Invoiced", "Cap = M+U+T",
         "Diff C-M", "Status (formula)", "Source", "Last measurement", "Rate", "Claimed value", "Certifiable value", "Alerts"]
    rows = []
    for i, r in enumerate(rec, start=2):
        rows.append([r["section_id"], r["activity_code"], r["subcontractor_id"], r["unit"], r["planned"], r["reported"],
                     r["measured"], r["u"], r["tol"], r["claimed"], r["claimed_at_measurement"], r["pending"], r["certified"],
                     r["invoiced"], f'=IF(G{i}="","",G{i}+H{i}+I{i})', f'=IF(G{i}="","",K{i}-G{i})',
                     f'=IF(J{i}=0,"",IF(G{i}="","UNVERIFIABLE",IF(ROUND(ABS(K{i}-G{i}),2)<=H{i},"MATCHED",'
                     f'IF(ROUND(ABS(K{i}-G{i}),2)<=H{i}+I{i},"WITHIN_TOLERANCE","DISCREPANCY"))))',
                     r["measurement_source"], r["last_flight"], r["rate"], f"=J{i}*T{i}",
                     f'=IF(G{i}="",0,MIN(K{i},O{i}))*T{i}', ", ".join(r["alerts"])])
    table(ws, H, rows, {"Status (formula)": 20, "Alerts": 22})
    colour_col(ws, "Q", ["MATCHED", "WITHIN_TOLERANCE", "DISCREPANCY", "UNVERIFIABLE"])
    for col in "EFGHIJKLMNOP":
        for cell in ws[col][1:]:
            cell.number_format = "#,##0.0"
    for col in "UV":
        for cell in ws[col][1:]:
            cell.number_format = "#,##0"
    n = ws.max_row
    ws.append([])
    ws.append(["TOTAL"] + [""] * 19 + [f"=SUM(U2:U{n})", f"=SUM(V2:V{n})"])
    ws.cell(ws.max_row, 1).font = Font(bold=True)

    al = g("/api/alerts", date=last)["alerts"]
    ws = wb.create_sheet("Alerts")
    table(ws, ["Rule", "Severity", "Title", "Work date", "Section", "Front", "Activity", "Subcontractor", "Crew", "Equipment", "Explanation", "Status"],
          [[a["rule_id"], a["severity"], a["title"], a["work_date"], a["section_id"], a["front_id"], a["activity_code"],
            a["subcontractor_id"], a["crew_id"], a["equipment_id"], a["explanation"], a["status"]] for a in al],
          {"Title": 38, "Explanation": 80})
    colour_col(ws, "B", ["HIGH", "MED"])

    sc = g("/api/scorecard", date=last)["rows"]
    ws = wb.create_sheet("Scorecard")
    rules = sorted({k for r in sc for k in r["alerts_by_rule"]})
    table(ws, ["Subcontractor", "Claimed value", "Certifiable value", "Over-claim %", "Rows in discrepancy",
               "Headcount over-claim days", "Equipment over-claim h", "Reports on time %"] + rules,
          [[r["subcontractor_id"], r["claimed_value"], r["certifiable_value"], r["overclaim_pct"], r["rows_discrepancy"],
            r["headcount_overclaim_days"], r["equipment_overclaim_h"], r["reports_on_time_pct"]]
           + [r["alerts_by_rule"].get(k, 0) for k in rules] for r in sc])
    for col, fmt in (("B", "#,##0"), ("C", "#,##0"), ("D", "0.0%"), ("H", "0%")):
        for cell in ws[col][1:]:
            cell.number_format = fmt

    dates = sorted({r["report_date"] for r in g("/api/field-reports")["reports"]})
    pres, eq = [], []
    for d in dates:
        p = g("/api/presence", date=d)
        pres += [[d, f["front_id"], f["crew_id"], f["subcontractor_id"], f["headcount_claimed"], f["checkin"], f["manifest"],
                  f["camera_max"], f["badge_zone_count"], f["status"]] for f in p["fronts"]]
        eq += [[d, e["equipment_id"], e["type"], e["subcontractor_id"], e["hours_claimed"], e["engine_h"], e["working_h"], e["status"]]
               for e in p["equipment"]]
    ws = wb.create_sheet("Presence")
    table(ws, ["Date", "Front", "Crew", "Subcontractor", "Headcount claimed", "Check-in", "Bus manifest", "Camera max",
               "Badge zone count", "Status"], pres)
    colour_col(ws, "J", ["OVERCLAIM", "NO_SIGNAL"])
    ws = wb.create_sheet("Equipment_Hours")
    table(ws, ["Date", "Equipment", "Type", "Subcontractor", "Hours claimed", "Engine h (telematics)", "Working h", "Status"], eq)
    colour_col(ws, "H", ["OVERCLAIM", "NO_DATA"])

    ws = wb.create_sheet("Certificate")
    lines = []
    for s in meta["subcontractors"]:
        cert = g(f"/api/certificate/{s['subcontractor_id']}", date=last)
        lines += [[s["subcontractor_id"], l["boq_item_id"], l["activity_code"], l["section_id"], l["unit"], l["cum_certified"],
                   l["prev_certified"], l["this_period"], l["rate"], l["amount"]] for l in cert["lines"]]
    table(ws, ["Subcontractor", "BoQ item", "Activity", "Section", "Unit", "Cum. certified", "Previous", "This period", "Rate", "Amount"], lines)

    dr = g("/api/daily-report", date=last)
    ws = wb.create_sheet("Bautagesbericht")
    table(ws, ["Tätigkeit", "Activity", "Unit", "Total", "Plan sheets today", "Cum. previous", "This period", "Cumulative", "%",
               "CHECK measured cum.", "CHECK claimed cum.", "CHECK source", "CHECK worst status", "CHECK alerts"],
          [[x["name_de"], x["name"], x["unit"], x["total"], x["sheets_today"], x["cum_prev"], x["this_period"], x["cum"], x["pct"],
            x["measured_cum"], x["claimed_cum"], x["verification_source"], x["worst_status"], ", ".join(x["open_alerts"])]
           for x in dr["detail"]], {"Tätigkeit": 34})
    for cell in ws["I"][1:]:
        cell.number_format = "0.0%"
    colour_col(ws, "M", ["MATCHED", "WITHIN_TOLERANCE", "DISCREPANCY", "UNVERIFIABLE"])
    r0 = ws.max_row + 2
    ws.cell(r0, 1, "Man-hours today (reported vs sensed)").font = Font(bold=True)
    for j, h in enumerate(["Group", "Cum. previous", "Today total", "Cumulative", "CHECK sensed today", "CHECK unverified h"], 1):
        ws.cell(r0 + 1, j, h).font = Font(bold=True)
    for i, x in enumerate(dr["personnel"], r0 + 2):
        for j, v in enumerate([x["group"], x["cum_prev"], x["today_total"], x["cum"], x["sensed_today"], x["unverified_today"]], 1):
            ws.cell(i, j, v)
    r1 = ws.max_row + 2
    ws.cell(r1, 1, "Equipment hours today: calculated (days assigned) vs measured (telematics)").font = Font(bold=True)
    for j, h in enumerate(["Owner", "Today calc.", "CHECK measured engine h", "CHECK no telematics h", "CHECK calc − measured"], 1):
        ws.cell(r1 + 1, j, h).font = Font(bold=True)
    for i, x in enumerate(dr["equipment"], r1 + 2):
        for j, v in enumerate([x["owner"], x["today_calc"], x["today_measured_engine_h"], x["today_without_telematics_h"], x["calc_minus_measured_h"]], 1):
            ws.cell(i, j, v)

    ws = wb.create_sheet("Rules")
    table(ws, ["Item", "Rule"], [
        ["Status (D-063)", "|C − M| ≤ U → MATCHED; ≤ U + T → WITHIN_TOLERANCE; above → DISCREPANCY; no measurement → UNVERIFIABLE"],
        ["U", "2 × σ of the independent measurement (≈95%)"],
        ["T", "max(absolute, % × M): m 1% / 2 m; m2 2% / 20 m2; nr 0.5% / 3 joints (placeholders until contract values, Q-063)"],
        ["Cap (D-064)", "M + U + T. Certifying above it needs a reason code and a comment; never automatic"],
        ["Measurement time (D-041)", "Claims are compared only up to the last measurement date; later lines are 'pending verification'"],
        ["Alerts", "AL-01…AL-13; see the Alerts sheet 'Explanation' column for why each fired"],
    ], {"Item": 26, "Rule": 110})
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return out


if __name__ == "__main__":
    p = build()
    print(p, f"{p.stat().st_size / 1e6:.2f} MB")
