"""Shared Excel house style for all DE035 tools (one sheet, grey ribbon, borders, 40/30 heights)."""
import datetime as dt
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter as L
from openpyxl.formatting.rule import FormulaRule

BLACK, DOT = "000000", "BFBFBF"
FILLS = {"blue": "DDEBF7", "green": "C6EFCE", "red": "FFC7CE"}
PAL = {"good": ("C6EFCE", "006100"), "bad": ("FFC7CE", "9C0006"), "warn": ("FFEB9C", "9C5700"), "info": ("DDEBF7", "1F4E78")}

def _b(l="thin", r="thin", t=None, b=None):
    S = lambda s, c=BLACK: Side(style=s, color=c) if s else Side()
    return Border(left=S(l), right=S(r), top=S(t, DOT if t == "dotted" else BLACK), bottom=S(b, DOT if b == "dotted" else BLACK))

def style_table(ws, highlights=None, date_cols=(), num_cols=(), qty_cols=(), int_cols=(), total_row=None, freeze="B2", text_rows_auto=True):
    highlights = highlights or {}
    last, c2 = ws.max_row, ws.max_column
    ws.sheet_view.showGridLines = False; ws.freeze_panes = freeze; ws.sheet_properties.tabColor = "2E75B6"
    ws.auto_filter.ref = f"A1:{L(c2)}{last - (1 if total_row else 0)}"; ws.print_title_rows = "1:1"
    ws.page_setup.orientation = "landscape"; ws.page_setup.paperSize = 9; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    for r in range(1, last + 1):
        hdr, tot = r == 1, r == total_row
        ws.row_dimensions[r].height = 40 if hdr else 30
        kind = highlights.get(r)
        for c in range(1, c2 + 1):
            x = ws.cell(r, c); l = "medium" if c == 1 else "thin"; rr = "medium" if c == c2 else "thin"
            if hdr or tot:
                x.border = _b(l, rr, "medium", "medium"); x.fill = PatternFill("solid", fgColor="BFBFBF")
                x.font = Font(name="Calibri", size=10, bold=True)
                x.alignment = Alignment(horizontal="center" if hdr else ("right" if c in num_cols + qty_cols + int_cols else "left"), vertical="center", wrap_text=True)
            else:
                x.border = _b(l, rr, "dotted" if r > 2 else None, "medium" if r == last else "dotted")
                fill = FILLS.get(kind); x.fill = PatternFill("solid", fgColor=fill) if fill else PatternFill()
                x.font = Font(name="Calibri", size=9, color="FF0000" if kind == "flag" else BLACK)
                v = x.value
                isdate = c in date_cols or isinstance(v, (dt.date, dt.datetime))
                isnum = c in num_cols + qty_cols + int_cols
                x.alignment = Alignment(horizontal="center" if isdate else "right" if isnum else "left", vertical="center", wrap_text=True)
                if isdate: x.number_format = "dd\\.mm\\.yyyy"
                elif c in qty_cols: x.number_format = "#,##0.00;[Red]\\-#,##0.00;\\-"
                elif c in int_cols: x.number_format = "#,##0;[Red]\\-#,##0;\\-"
                elif c in num_cols: x.number_format = "#,##0.00;[Red]\\-#,##0.00;\\-"
    for c in range(1, c2 + 1):
        n = 0
        for r in range(1, last + 1):
            v = ws.cell(r, c).value
            if v is None: continue
            s = v.strftime("%d.%m.%Y") if isinstance(v, (dt.date, dt.datetime)) else str(v)
            if s.startswith("="): s = "0" * 10
            n = max(n, max(len(t) for t in s.split("\n")) * (1.15 if r == 1 else 1))
        ws.column_dimensions[L(c)].width = min(max(n + 3, 10), 70)
    if text_rows_auto:  # grow rows holding wrapped text so nothing is clipped (min 30)
        import math
        for r in range(2, last + 1):
            lines = 1
            for c in range(1, c2 + 1):
                v = ws.cell(r, c).value
                if isinstance(v, str) and not v.startswith("="):
                    w = max(ws.column_dimensions[L(c)].width - 2, 1)
                    lines = max(lines, sum(math.ceil(max(len(p), 1) * 1.1 / w) for p in v.split("\n")))
            ws.row_dimensions[r].height = max(30, lines * 12 + 6)

def cf(ws, rng, formula, tone):
    f, fo = PAL[tone]
    ws.conditional_formatting.add(rng, FormulaRule(formula=[formula], fill=PatternFill("solid", fgColor=f), font=Font(color=fo, bold=True)))
