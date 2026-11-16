"""Cumulative Issue & TQ Register: merges 09_Issue_Log/issues_batch*.json into one house-style sheet.
Status/remarks typed in the existing xlsx are preserved by issue ID."""
import json, sys
from pathlib import Path
import openpyxl
sys.path.insert(0, str(Path(__file__).parent)); from house_style import style_table, cf
ROOT = Path(__file__).resolve().parents[1]; LOG = ROOT / "09_Issue_Log"; OUT = LOG / "DE035_Issue_TQ_Register.xlsx"
H = ["ID", "Batch", "Source doc (Reg. ID)", "Location (sheet / page)", "Gap type", "Category", "Description (fact)", "Lot 2 impact",
     "Lead dept", "Support depts", "Proposed action", "Closure evidence", "Approver", "Priority", "Need date (from schedule)", "Status", "Remarks"]
keep = {}
if OUT.exists():
    for r in openpyxl.load_workbook(OUT).active.iter_rows(min_row=2, values_only=True):
        if r[0]: keep[r[0]] = (r[14], r[15], r[16])
wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Issue & TQ Register"; ws.append(H)
for f in sorted(LOG.glob("issues_batch*.json")):
    for it in json.load(open(f)):
        nd, st, rm = keep.get(it[0], (None, "Open", None))
        ws.append(it + [nd, st, rm])
style_table(ws, date_cols=(15,), freeze="B2")
n = ws.max_row
cf(ws, f"N2:N{n}", 'N2="High"', "bad"); cf(ws, f"N2:N{n}", 'N2="Medium"', "warn")
cf(ws, f"P2:P{n}", 'P2="Closed"', "good")
wb.save(OUT); print(n - 1, "issues ->", OUT.relative_to(ROOT))
