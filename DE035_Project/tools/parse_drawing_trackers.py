"""Parse client drawing-progress trackers (TL route longitudinal sections, SL special longitudinal sections)
into house-style registers in 02_Engineering. Read-only on source PDFs. Usage:
  python3 tools/parse_drawing_trackers.py <TL-tracker.pdf> <SL-tracker.pdf>
Lot boundaries are taken from 'Losgrenze ergänzt' sheets (099/100 and 182/183) - confirm with client."""
import re, sys, datetime as dt
from pathlib import Path
import pdfplumber, openpyxl
sys.path.insert(0, str(Path(__file__).parent)); from house_style import style_table, cf

ROOT = Path(__file__).resolve().parents[1]; ENG = ROOT / "02_Engineering"
BASELINE = dt.date(2024, 8, 26)  # final bid submission per WAD update 30.07.2024 - CONFIRM contract baseline

def d(s):
    s = (s or "").strip()
    try: return dt.datetime.strptime(s, "%d.%m.%Y").date()
    except ValueError: return None

def lot(first, last):
    if last <= 99: return "Los 1"
    if first == 99 and last == 100: return "Los 1/2 boundary"
    if first == 182 and last == 183: return "Los 2/3 boundary"
    if first >= 100 and last <= 182: return "Los 2"
    return "Los 3"

def category(t):
    t = t.lower(); out = []
    for k, v in [("düker unter gewässer", "Siphon depth - watercourse"), ("ogE-ltg".lower(), "Depth - OGE line"), ("kanal", "Siphon depth - canal"),
                 ("durchlass", "Siphon depth - culvert"), ("umtrass", "Rerouting"), ("losgrenze", "Lot boundary"), ("wkr", "Bend change"),
                 ("hdd", "HDD"), ("kks", "Cathodic protection (KKS) to add"), ("vorblatt", "Knock-on from previous sheet"), ("ap ", "AP revised"), ("ts-punkt", "Tangent point"), ("ts 1", "Tangent point")]:
        if k in t and v not in out: out.append(v)
    return "; ".join(out)

def tl(path):
    rows = []
    with pdfplumber.open(path) as pdf:
        for pg in pdf.pages:
            for r in pg.extract_tables()[0]:
                if r[1] and r[1].startswith("_BL"): rows.append(r)
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "TL Revision Register"
    H = ["Line", "Tracker no.", "Sheet ref", "Sheet from", "Sheet to", "Rev", "Status", "Lot (indicative)", "Design date (Konstruktion)",
         "Client remarks (as given)", "Change category", "Draft 00 handover", "Draft 01 handover", "Draft 02 handover", "Last draft handover",
         "Release (Freigabe)", "Final issue (o. Entwurf)", "Released?", "Contract baseline date (confirm)", "Revised after baseline?",
         "Days design to final issue", "System flag"]
    ws.append(H); hl = {}; seen = {}
    for i, r in enumerate(rows, 2):
        ref = r[1]; m = re.match(r"_BL_(\d+)\w*?_(\d+)\w*?_TL_Rev(\d+)", ref)
        a, b, rev = int(m.group(1)), int(m.group(2)), m.group(3)
        status = "Superseded" if r[0] in ("-", "") else "Current"
        rem = (r[3] or "").replace("\n", " | ")
        flag = []
        if ref in seen: flag.append(f"Same sheet/rev label as line {seen[ref]} - rev numbering error, TQ")
        seen.setdefault(ref, i - 1)
        if "kks" in rem.lower(): flag.append("KKS (cathodic protection) to be added - verify in later rev")
        if d(r[8]) is None: flag.append("Not released")
        ws.append([i - 1, r[0], ref, a, b, rev, status, lot(a, b), d(r[2]), rem, category(rem), d(r[4]), d(r[5]), d(r[6]), d(r[7]),
                   d(r[8]), d(r[9]), f'=IF(P{i}="","No","Yes")', BASELINE, f'=IF(I{i}>S{i},"Yes","No")', f'=IF(Q{i}="","",Q{i}-I{i})', "; ".join(flag)])
        if flag: hl[i] = "flag"
        elif status == "Current" and lot(a, b).startswith("Los 2"): hl[i] = "blue"
    style_table(ws, hl, date_cols=(9, 12, 13, 14, 15, 16, 17, 19), int_cols=(4, 5, 21), freeze="D2")
    n = ws.max_row
    cf(ws, f"R2:R{n}", 'R2="No"', "bad"); cf(ws, f"T2:T{n}", 'AND(T2="Yes",G2="Current")', "warn")
    ENG.mkdir(exist_ok=True); out = ENG / "DE035_TL_Revision_Register.xlsx"; wb.save(out); return out, len(rows)

def sl(path):
    with pdfplumber.open(path) as pdf: t = pdf.pages[0].extract_tables()[0]
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "SL Crossing Revision Register"
    H = ["Sheet", "Sheet no.", "Lot (indicative)", "Rev 1 reason", "Rev 2 reason", "Rev 3 reason", "Rev 4 reason", "Rev 5 reason",
         "No. of revisions", "Depth change (as given)", "Crossing method changed?", "Rerouting / new sheet?", "Matching TL sheet pair to check", "System flag"]
    ws.append(H); hl = {}
    for i, r in enumerate([x for x in t[1:] if x[0]], 2):
        sheet = r[0].strip(); no = int(re.search(r"(\d+)", sheet).group(1))
        lt = "Los 1" if no <= 99 else "Los 2" if no <= 182 else "Los 3"
        revs = [(x or "").replace("\n", " ") for x in r[1:6]]
        txt = " ".join(revs).lower(); depth = (r[6] or "").replace("\n", " ")
        meth = "Yes" if any(k in txt for k in ("verfahren", "vortrieb", "mt ", "hdd")) else "No"
        new = "Yes" if ("umtrass" in txt or "neu" in depth.lower()) else "No"
        flag = []
        if new == "Yes": flag.append("Rerouting / new crossing sheet - check BOQ quantities and permits")
        if meth == "Yes": flag.append("Method change - check BOQ item, subcontract package and method statement")
        ws.append([sheet, no, lt] + revs + [f'=COUNTA(D{i}:H{i})', depth, meth, new, f"TL sheet pair containing {no:03d}", "; ".join(flag)])
        # COUNTA counts "" written by openpyxl as empty -> blanks are None
        for c in range(4, 9):
            if ws.cell(i, c).value == "": ws.cell(i, c).value = None
        if lt == "Los 2": hl[i] = "blue"
    style_table(ws, hl, int_cols=(2, 9), freeze="B2")
    n = ws.max_row
    cf(ws, f"K2:K{n}", 'K2="Yes"', "warn"); cf(ws, f"L2:L{n}", 'L2="Yes"', "bad")
    out = ENG / "DE035_SL_Crossing_Revision_Register.xlsx"; wb.save(out); return out, ws.max_row - 1

if __name__ == "__main__":
    o1, n1 = tl(sys.argv[1]); o2, n2 = sl(sys.argv[2])
    print(f"TL: {n1} rows -> {o1.relative_to(ROOT)}\nSL: {n2} rows -> {o2.relative_to(ROOT)}")
