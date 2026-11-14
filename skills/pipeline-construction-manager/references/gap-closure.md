# Gap-Closure Operating System

Purpose: make the distance between **what the contract requires** and **what is priced, owned, planned, resourced and evidenced on site** visible, owned and closed — every week, by every department, with proof.

## 1. Definitions
- **Obligation** — anything the contract, SOW, specifications, permits or agreed correspondence requires the JV to deliver, perform, submit, notify, obtain, allow or refrain from. One obligation per line.
- **Execution layer** — one of five conditions an obligation needs to be delivered: **Priced, Owned, Planned, Resourced, Evidenced**.
- **Gap** — an obligation (or a site reality) missing one or more execution layers, or a site activity with no contract basis.
- **Need date** — the date the gap must be closed so the dependent activity, notice or payment is not affected. Taken from the schedule (D03) or the contract time limit (D04).
- **Closure evidence** — the document that proves the gap is closed. Without it, status stays open.

## 2. Five-layer trace (apply to every obligation)
| Layer | Question | Typical evidence | Department check |
|---|---|---|---|
| Priced | Is it in BOQ / lump sum / agreed variation / subcontract price? | BOQ line, subcontract item, variation agreement | D12, D05, D04 |
| Owned | Is there exactly one accountable department and, if outsourced, one contracted party? | RACI row with one A; subcontract scope clause | CM, D04 |
| Planned | Is there a schedule activity with logic and dates? | Activity ID in baseline/look-ahead | D03 |
| Resourced | Are crew, plant, material, subcontractor secured for the need date? | Crew plan, PO, rental, material receipt | D01, D05, D06, D10 |
| Evidenced | Is the compliance record defined and will it be produced? | ITP point, record template, permit, dossier index line | D07, D13, D09 |

Reverse trace (catches unpaid work): for every site activity, subcontract item and PO line, ask "which obligation does this serve?" No answer = potential G3 (cost without entitlement) or a variation to raise.

## 3. Gap taxonomy
| Code | Type | Typical DE035 example | Default lead |
|---|---|---|---|
| G1 | Scope gap — required but in no scope/package | Test or pigging step not in any subcontract | D05 / D04 |
| G2 | Interface gap — between two parties/departments, nobody owns the hand-off | HDD pull-in ↔ pressure test (S-02); DE035/DE042 shared yard | CM |
| G3 | Commercial gap — cost without entitlement, entitlement without notice, invoice/PO mismatch | Retroactive rental PO (S-03); event without notice | D04 / D12 |
| G4 | Back-to-back gap — main-contract obligation not flowed down, or weaker | Permit condition not in subcontract | D04 |
| G5 | Approval/document gap — drawing, procedure, JV or client approval missing at need date | WPS not approved; OGE review overdue | D13 / D14 |
| G6 | Permit/land gap — permit, condition or parcel release missing | Parcel not released; discharge permit | D09 |
| G7 | Resource/capacity gap — crew, welders, NDT, plant short of plan | NDT backlog behind welding | D01 / D10 |
| G8 | Material/supply gap — material or supplier not available by need date | Blocked supplier account (S-04) | D05 / D06 |
| G9 | Readiness gap — an activity about to start without its preconditions | Hydrotest with open NCRs | owning dept |
| G10 | Records/evidence gap — work done but not proven | Handover damage unrecorded; dossier holes | D13 / owning dept |

## 4. Registers — column specifications
Build in Excel per excel-house-style (one worksheet per file unless asked; formula-only; no macros). Status and score columns use formulas, never typed values where a formula can derive them.

### 4.1 Obligation Register
`OBL-ID | Source doc no. | Rev | Clause/section (as given) | Obligation text (short) | Type (deliver/perform/submit/notify/obtain/allow/refrain) | Owner dept (one) | Execution vehicle (own forces / SC package / client supply / third party) | Package/PO ref | BOQ item | Schedule activity ID | Evidence of compliance | Due trigger / date | Priced (Y/N) | Owned (Y/N) | Planned (Y/N) | Resourced (Y/N) | Evidenced (Y/N) | Layers missing (formula: count of N) | Gap ID(s) | Notes / verify flag`

### 4.2 Gap Register
`GAP-ID | Date raised | Raised by dept | Gap type (G1–G10) | Linked OBL-ID / seed ID | Description (fact, not opinion) | Source / evidence of gap | Consequence (1–5) | Need date | Days to need date (formula: need date − TODAY()) | Proximity score (formula: 5 if ≤7 d, 4 if ≤14, 3 if ≤30, 2 if ≤60, else 1) | Priority score (formula: consequence × proximity) | Override flag (time bar / safety → forced top) | Lead dept | Support depts | Closure action | Closure evidence required | Action due | Approver needed (none / PM / PD / JV / OGE) | Status (Open / In progress / Evidence submitted / Closed / Accepted risk) | Date closed | Evidence ref (doc no.) | Ageing days (formula)`

Consequence scale (state it in the file so users score consistently):
5 = safety/integrity, time bar loss, critical path or milestone payment; 4 = near-critical activity or major cost; 3 = cost or delay within float; 2 = administrative with knock-on risk; 1 = housekeeping.

### 4.3 Action Tracker
`ACT-ID | GAP-ID | Department | Action | Owner (role) | Due | Status | Priority (from gap) | Closure evidence | Linked clause / notice`

### 4.4 Heat map (summary)
Department (rows D01–D14) × gap type (G1–G10), count of open gaps via COUNTIFS on the Gap Register; second view by priority band. Shows where the organisation is failing, not just what.

## 5. Ready-to-Start gate (per activity, front, crossing, HDD, tie-in, test section)
Run department by department. Every line is Yes / No / N/A with evidence ref. Output GO, GO with conditions (listed, owner, date), or NO-GO.

| # | Check | Dept | Evidence |
|---|---|---|---|
| 1 | Front / parcel released, entry notice served | D09 | Release map, notice copy |
| 2 | Permits valid for the full duration; conditions flowed down | D09 / D04 | Permit register, subcontract clause |
| 3 | IFC drawings at current revision on site; TQs closed | D02 / D13 | Drawing register, TQ log |
| 4 | Method statement and risk assessment approved | D01 / D08 | Approval transmittal |
| 5 | ITP approved; client notified for hold/witness points | D07 | ITP, notification |
| 6 | Welders/operators qualified; procedures (WPS/PQR) approved | D07 | Qualification register |
| 7 | Material on site, inspected, traceable, allocated | D06 | Receipt register, tally |
| 8 | Subcontract/PO in place covering the full scope incl. interfaces | D05 | PO / subcontract, interface register |
| 9 | Plant on hire under PO, inspected, certified; on-hire record signed | D10 | Rental register, certificate |
| 10 | Foreign utilities located and owner conditions met | D02 / D09 | Locating record, owner consent |
| 11 | PTW, inductions, emergency arrangements in place | D08 | PTW, induction register |
| 12 | Weather/ground/season window confirmed | D03 / D01 | Look-ahead, forecast |
| 13 | Records templates ready (daily report, ITP sheets, as-built) | D13 / D07 | Templates issued |
| 14 | Priced: activity is in BOQ/subcontract or a variation notice is issued | D12 / D04 | BOQ line / notice ref |
| 15 | JV / client approvals required for this activity obtained | D14 | Approval record |

Rule: lines 1, 2, 4, 6 and 11 are **non-waivable** (people, environment, integrity, legality). Other lines can be GO-with-conditions only by CM signature stating the risk accepted and the closure date.

## 6. Weekly cadence (aligned to the procurement SOP rhythm)
| Day | Gap-closure step | Procurement SOP step | Who |
|---|---|---|---|
| Mon | Gap intake: every department submits new gaps and closure evidence; Document Controller logs | MRF intake | All depts → D13 |
| Tue | D03 links each gap to its need date; D04 screens all new gaps for notices/time bars | MRF intake | D03, D04 |
| Wed | Cross-department interface review (G2/G4 focus), 3-week look-ahead readiness gates | Bid evaluation (CBE) | CM chairs; D01–D14 leads |
| Thu | CM decisions; escalation to PM / PD / JV / OGE; POs to close G1/G8 gaps issued | PO issue | CM, D05, D14 |
| Fri | Closure verification (evidence checked, status closed or reopened); weekly gap report issued | Invoice verification (G3 three-way match) | D13, D12, CM |

Weekly gap report (one page): new / closed / overdue by department; top 5 gaps by priority; gaps whose closure date is after need date; decisions needed this week and from whom; ageing trend.

## 7. Closure rules
1. Only the **lead department** can submit closure; only the **CM (or delegate)** can mark Closed after checking the evidence.
2. Evidence must be a controlled document with a reference (letter, minutes, PO, revised drawing, signed record, permit). Emails count only when filed in the correspondence log.
3. "Accepted risk" requires the risk statement, the approver at the right level, and a review date.
4. A gap reopens automatically if the evidence is superseded, the subcontractor disputes it, or the site finds the condition again.
5. Time-bar and safety gaps are reviewed daily, not weekly.

## 8. Gap audit — step-by-step (Gap audit mode)
1. Build the Document Register; confirm order of precedence (D04, D13).
2. Extract obligations per `contract-to-execution.md` into the Obligation Register; assign one owner each.
3. Run the five-layer trace; generate gaps; run the reverse trace on POs/subcontracts/daily reports.
4. Score, link to need dates, override for time bars and safety.
5. Produce heat map, top-10 gap list with closure actions, and the TQ/notice list for D04.
6. Decision note for the PM: what is covered, what is exposed, what needs approval.
