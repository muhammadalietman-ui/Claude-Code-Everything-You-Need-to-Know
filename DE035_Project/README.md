# DE035 working area: Construction Manager initial job

> **Public repository.** `.gitignore` blocks everything except this README, the folder skeleton and `tools/*.py`.
> Client documents, registers and outputs stay in the session container only and are never pushed.

## How documents come in
1. Upload files (PDF, DOCX, XLSX, ZIP) into `00_Inbox/`, or name the Google Drive folder / Gmail thread to pull from.
2. Run `python3 tools/build_document_register.py`. It extracts text to `01_Client_Docs/_text/` and builds `01_Client_Docs/DE035_Document_Register.xlsx` with suggested doc no., revision, title, type, owner department and language, plus flags for duplicates, scanned PDFs and possibly superseded revisions.
3. The CM confirms the order of precedence and the owner for each document. Files then move from `00_Inbox` to `01_Client_Docs`.

## Initial job: phases and outputs
| Step | Output | Folder | Department |
|---|---|---|---|
| 1 Document intake | Document Register, order of precedence, missing-document list | 01 | D13, D04 |
| 2 Contract decomposition | Obligation Register, notices calendar, TQ list | 01, 09 | D04 + document owners |
| 3 Engineering development | Design Basis memo, crossing and tie-in schedule, test-section plan | 02 | D02, D07, D11 |
| 4 Execution method | Method statement outlines, ITP list, HSE risk register, Ready-to-Start gates | 03 | D01, D07, D08, D09 |
| 5 BOQ / SOW / RACI | BOQ, SOW, RACI traced to Obligation IDs | 04-06 | D12, D04, D05 |
| 6 Schedule | Logic-linked schedule, long-lead items, gap need dates | 07 | D03 |
| 7 Special clauses | Clause schedule linked to Gap IDs | 08 | D04 |
| 8 Gap closure | Gap Register, heat map, weekly report | 10 | CM |

## Automation roadmap (built as we go)
| # | Tool | Status |
|---|---|---|
| A1 | `build_document_register.py`: intake, text extraction, classification, flags | Done |
| A2 | Obligation extractor: finds "shall / hat zu / ist zu / muss" sentences, notices and time limits, and drafts Obligation Register lines with source page | Next, once documents arrive |
| A3 | Standards & editions extractor (EN, DIN, DVGW, API, ISO references) into a conflicts list | Planned |
| A4 | Five-layer trace and Gap Register builder (Obligation ↔ BOQ ↔ RACI ↔ schedule) | Planned |
| A5 | Weekly gap report generator (Friday) | Planned |
| A6 | Department sub-agents: each D01-D14 reviews its own documents in parallel using its charter | Planned |
