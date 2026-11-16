"""DE035 intake automation - step 1: Document Register.

Scans 00_Inbox and 01_Client_Docs (recursively), extracts text from PDFs/DOCX/XLSX into
01_Client_Docs/_text/ (for search and obligation extraction), and writes
01_Client_Docs/DE035_Document_Register.xlsx in the excel house style (one sheet).

Auto-filled fields are SUGGESTIONS (doc no., revision, title, language, owner dept);
columns marked 'confirm' are for the reviewer. Run:  python3 tools/build_document_register.py
"""
import hashlib, re, subprocess, sys, datetime as dt
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter as L
from openpyxl.formatting.rule import FormulaRule

ROOT = Path(__file__).resolve().parents[1]
SCAN = [ROOT / "00_Inbox", ROOT / "01_Client_Docs"]
TXT = ROOT / "01_Client_Docs" / "_text"
OUT = ROOT / "01_Client_Docs" / "DE035_Document_Register.xlsx"
SKIP = {".gitkeep", ".gitignore"}

# keyword -> (document type, owner department). First match wins; German and English.
RULES = [
    (r"fortschritt|progress|tracker|statusbericht|update|vorstellung|pr(ä|ae)sentation|transmittal", "Status / progress / transmittal information", "D13 Document Control"),
    (r"vertrag|contract|agreement|besondere vertragsbed|bvb|avb|zvb|conditions", "Contract conditions", "D04 Contracts"),
    (r"leistungsverzeichnis|\blv\b|boq|bill of quant|preisblatt|price schedule", "BOQ / price schedule", "D12 Cost"),
    (r"leistungsbeschreibung|scope of work|\bsow\b", "Scope of work", "D04 Contracts"),
    (r"genehmigung|planfeststellung|permit|auflage|bescheid|wasserrecht", "Permit / authority condition", "D09 Permits & Land"),
    (r"eigent(ü|ue)mer|grundst(ü|ue)ck|landowner|flurst(ü|ue)ck|gestattung", "Landowner document", "D09 Permits & Land"),
    (r"umwelt|environment|lbp|artenschutz|boden|soil|ecolog", "Environmental document", "D09 Permits & Land"),
    (r"druckpr(ü|ue)fung|hydro ?test|pressure test|molch|pigging|inbetriebnahme|commission", "Testing / commissioning", "D11 Testing"),
    (r"schwei(ß|ss)|weld|wps|pqr|ndt|zfp|r(ö|oe)ntgen|ultraschall|aut\b", "Welding / NDT", "D07 QA/QC"),
    (r"umh(ü|ue)llung|coating|nachumh|denso|korrosion|cathodic|kks", "Coating / corrosion", "D07 QA/QC"),
    (r"pr(ü|ue)fplan|itp|inspection and test|qualit(ä|ae)t|quality", "Quality requirement", "D07 QA/QC"),
    (r"arbeitsschutz|sicherheit|sige|hse|safety|dguv|gef(ä|ae)hrdung", "HSE requirement", "D08 HSE"),
    (r"hdd|spülbohr|spuelbohr|bohrung|kreuzung|crossing|d(ü|ue)ker|pressung", "Crossing / HDD", "D02 Field Engineering"),
    (r"lageplan|trassenplan|alignment|zeichnung|drawing|l(ä|ae)ngsschnitt|profile|detail", "Drawing", "D02 Field Engineering"),
    (r"spezifikation|specification|spec\b|norm|standard|richtlinie|technische", "Technical specification", "D07 QA/QC"),
    (r"terminplan|bauzeitenplan|schedule|programme|program", "Schedule / programme", "D03 Planning"),
    (r"dokumentation|dossier|mdr|as[- ]?built|bestand", "Documentation / dossier", "D13 Document Control"),
    (r"material|beistell|free[- ]issue|rohr|pipe|bogen|bend|armatur|valve", "Material / client supply", "D06 Materials"),
]
DE_WORDS = re.compile(r"\b(der|die|das|und|nicht|werden|mit|für|auf|ist|sind|bei|durch)\b", re.I)
EN_WORDS = re.compile(r"\b(the|and|shall|with|for|of|be|is|are|by|to)\b", re.I)
REV = re.compile(r"(?:rev(?:ision)?|index|stand)[\s._-]*([A-Z0-9]{1,3})\b", re.I)
DOCNO = re.compile(r"(?<![A-Za-z0-9])([A-Z0-9]{2,}(?:[-_.][A-Z0-9]{2,}){2,})(?![A-Za-z0-9])")

def text_of(p: Path) -> tuple[str, int | None]:
    ext = p.suffix.lower()
    try:
        if ext == ".pdf":
            t = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True, timeout=120).stdout
            info = subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True).stdout
            m = re.search(r"Pages:\s+(\d+)", info)
            return t, int(m.group(1)) if m else None
        if ext == ".docx":
            import docx
            d = docx.Document(str(p))
            return "\n".join(x.text for x in d.paragraphs), None
        if ext in (".xlsx", ".xlsm"):
            wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
            rows = []
            for ws in wb:
                for r in ws.iter_rows(values_only=True):
                    rows.append(" | ".join(str(v) for v in r if v is not None))
            return "\n".join(rows), None
        if ext in (".txt", ".csv", ".md"):
            return p.read_text(errors="ignore"), None
    except Exception as e:  # unreadable file -> flagged in register
        return f"__ERROR__ {e}", None
    return "", None

def guess_title(text: str, name: str) -> str:
    for line in text.splitlines():
        s = " ".join(line.split())
        if 12 <= len(s) <= 120 and sum(ch.isalpha() for ch in s) > len(s) * 0.6:
            return s
    return Path(name).stem.replace("_", " ")

def classify(name: str, text: str):
    for hay in (name.lower(), text[:4000].lower()):  # filename first, then content
        for pat, typ, dept in RULES:
            if re.search(pat, hay):
                return typ, dept
    return "Unclassified - confirm", "CM to assign"

def language(text: str) -> str:
    de, en = len(DE_WORDS.findall(text[:6000])), len(EN_WORDS.findall(text[:6000]))
    if de + en < 10: return "unknown (scan?)"
    return "DE" if de > en * 1.3 else "EN" if en > de * 1.3 else "DE/EN"

def main():
    TXT.mkdir(parents=True, exist_ok=True)
    keep = {}  # manual review columns survive re-runs, keyed by checksum
    if OUT.exists():
        for r in openpyxl.load_workbook(OUT).active.iter_rows(min_row=2, values_only=True):
            if r[11]: keep[r[11]] = list(r[13:17])
    files = sorted(f for d in SCAN if d.exists() for f in d.rglob("*")
                   if f.is_file() and f.name not in SKIP and "_text" not in f.parts and f != OUT and not f.name.startswith("~$"))
    rows, seen = [], {}
    for i, f in enumerate(files, 1):
        h = hashlib.sha1(f.read_bytes()).hexdigest()[:10]
        text, pages = text_of(f)
        err = text.startswith("__ERROR__")
        if text and not err:
            (TXT / (f.stem + "__" + h + ".txt")).write_text(text)
        stem = REV.sub("", f.stem).rstrip("_- .")
        m_no = DOCNO.search(stem) or DOCNO.search(text[:3000] if not err else "")
        m_rev = REV.search(f.stem) or REV.search(text[:3000] if not err else "")
        typ, dept = classify(f.name, "" if err else text)
        flag = ""
        if h in seen: flag = f"Duplicate of {seen[h]}"
        elif err: flag = "Could not read - check file"
        elif len(text.strip()) < 50 and f.suffix.lower() == ".pdf": flag = "No text layer - scanned PDF, OCR needed"
        seen.setdefault(h, f"DOC-{i:03d}")
        rows.append([f"DOC-{i:03d}", str(f.relative_to(ROOT)), m_no.group(1) if m_no else "", m_rev.group(1).upper() if m_rev else "",
                     guess_title("" if err else text, f.name), typ, dept, language("" if err else text), pages,
                     dt.date.fromtimestamp(f.stat().st_mtime), round(f.stat().st_size / 1024, 1), h, flag,
                     *keep.get(h, ["", "To review", "", ""])])
    # superseded candidates: same doc no., lower revision
    by_no = {}
    for r in rows:
        if r[2]: by_no.setdefault(r[2], []).append(r)
    for no, group in by_no.items():
        if len(group) > 1:
            top = max(g[3] for g in group)
            for g in group:
                if g[3] != top and not g[12]: g[12] = f"Possible superseded rev (latest {top})"
    write(rows)
    print(f"{len(rows)} files registered -> {OUT.relative_to(ROOT)}; text in {TXT.relative_to(ROOT)}")

H = ["Reg. ID", "File", "Doc no. (suggested)", "Rev (suggested)", "Title (suggested)", "Document type (suggested)",
     "Owner dept (suggested)", "Language", "Pages", "File date", "Size (KB)", "Checksum", "System flag",
     "Order of precedence (confirm)", "Review status", "Reviewed by", "Remarks / TQ ref"]

def write(rows):
    BLACK, DOT = "000000", "BFBFBF"
    def b(l, r, t=None, bo=None):
        S = lambda s, c=BLACK: Side(style=s, color=c) if s else Side()
        return Border(left=S(l), right=S(r), top=S(t, DOT if t == "dotted" else BLACK), bottom=S(bo, DOT if bo == "dotted" else BLACK))
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Document Register"
    ws.append(H)
    for r in rows: ws.append(r)
    last, c2 = max(ws.max_row, 2), len(H)
    if ws.max_row == 1: ws.append([""] * c2)
    ws.sheet_view.showGridLines = False; ws.freeze_panes = "C2"; ws.sheet_properties.tabColor = "2E75B6"
    ws.auto_filter.ref = f"A1:{L(c2)}{last}"; ws.print_title_rows = "1:1"
    ws.page_setup.orientation = "landscape"; ws.page_setup.paperSize = 9; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    for r in range(1, last + 1):
        hdr = r == 1; ws.row_dimensions[r].height = 40 if hdr else 30
        flagged = not hdr and ws.cell(r, 13).value
        for c in range(1, c2 + 1):
            x = ws.cell(r, c); l = "medium" if c == 1 else "thin"; rr = "medium" if c == c2 else "thin"
            if hdr:
                x.border = b(l, rr, "medium", "medium"); x.fill = PatternFill("solid", fgColor="BFBFBF")
                x.font = Font(name="Calibri", size=10, bold=True); x.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            else:
                x.border = b(l, rr, "dotted" if r > 2 else None, "medium" if r == last else "dotted")
                x.font = Font(name="Calibri", size=9, color="FF0000" if flagged else "000000")
                h = "center" if c == 10 else "right" if c in (9, 11) else "left"
                x.alignment = Alignment(horizontal=h, vertical="center", wrap_text=True)
                if c == 10: x.number_format = "dd\\.mm\\.yyyy"
                if c == 11: x.number_format = "#,##0.0"
    for c in range(1, c2 + 1):
        n = max(len(str(ws.cell(r, c).value or "")) * (1.15 if r == 1 else 1) for r in range(1, last + 1))
        ws.column_dimensions[L(c)].width = min(max(n + 3, 10), 70)
    for txt, fill, font in (("Reviewed", "C6EFCE", "006100"), ("To review", "FFEB9C", "9C5700"), ("Superseded", "FFC7CE", "9C0006")):
        ws.conditional_formatting.add(f"O2:O{last}", FormulaRule(formula=[f'O2="{txt}"'], fill=PatternFill("solid", fgColor=fill), font=Font(color=font, bold=True)))
    wb.save(OUT)

if __name__ == "__main__":
    sys.exit(main())
