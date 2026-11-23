# Contractor-to-Client Daily Report (Bautagesbericht): Structure Analysis (RPT-0)

Owners: process-analyst and commercial-analyst. Date: 2026-11-23. Source: one real daily report supplied by the user (a near-complete onshore gas pipeline lot in Germany). **Anonymised:** the source file is kept outside the repository. No company, client, project, road or person names and no project figures are reproduced here.

## 1. Structure [F]

| § | Section | Content | Granularity |
|---|---|---|---|
| Header | Project/lot, report date + weekday, sequential report number | n/a | Project / lot |
| 1 | Weather | Today + forecast for the next working day (icon, max/min °C) | Project |
| 2 | Personnel (*Personalübersicht*) | **Man-hours** (not headcount): cumulative to previous period, today (local / external / total), cumulative. Split into JV direct, JV indirect and subcontractors. Daily bar chart + cumulative S-curve | Company type × origin |
| 3 | Equipment (*Geräte/Maschinen*) | Machine-hours and vehicle-hours: cumulative, today, cumulative + today, for the JV and subcontractors. **Footnote: hours are calculated from the number of days each unit is assigned to the project** | Owner × category |
| 4 | Activity summary | Free text: work completed today; planned for the next days | Project, with plan-sheet ranges in the text |
| 5 | Special events | HSE, QA/QC, safety (free text) | Project |
| 6 | Detailed activity report | Activity hierarchy (route preparation, drainage, stringing and bending, welding and NDT, field-joint coating, trenching incl. open cuts and crossings, bedding, lowering-in and tie-in welding, backfill incl. cable ducts, cathodic protection, reinstatement and cleaning, pre-commissioning incl. pressure test); unit, total, **construction-plan sheet numbers**, previous cumulative, this period, cumulative, % | Activity × plan-sheet range |
| 6b | Pipe yards | Topsoil (m²), gravel layer (m²), temporary fencing (lm), site container (pc) | Yard |
| 6c | Valve stations | **Lump-sum (psch) items** with stage progress (preparation, civil, mechanical, completion) in % | Station × stage |
| 6d | Welding procedure summary | Welds executed, repairs and repair rate per WPS (cumulative) | WPS |
| 6e | Crossings | Auger bores, pipe ramming, direct piping, HDD: length, start/target pit %, casing (dummy) pipe and product pipe (previous, period, cumulative, %), remark (road/rail crossed) | Crossing object |

## 2. Findings for SiteOps Twin

| # | Finding | Evidence type | Design response | Status |
|---|---|---|---|---|
| F1 | **Location is referenced by construction-plan sheet number**, not KP | [F] | `plan_sheet` table (sheet ↔ KP range); sheet ranges shown in reports and rows. Likely the user's "corner" (Q-011, A-034) | ✅ Built (demo sheets BP101…) |
| F2 | Manpower is reported as **man-hours by company type and origin**, not headcount per crew | [F] | `manpower_daily` (reported vs sensed man-hours); S9 shows "unverified hours" for subcontractors | ✅ Built |
| F3 | **Equipment hours are calculated from days assigned, not measured.** Weather-stop and idle days still accrue hours | [F] (footnote) | `equipment_calc_daily` vs telematics engine hours; "calc − measured" column in S9. A strong argument for T3 telematics (H5) | ✅ Built + test |
| F4 | The **narrative and the quantity table can disagree** (text reports coating completed; the period quantity shows 0) | [F] (one instance in RPT-0) | New rule **AL-14** (text vs quantity) | ✅ Built + seeded test |
| F5 | Totals differ between activities (route length vs pipe length incl. bends) | [F] | Keep an explicit `total` per activity; never compare across activities without unit/basis conversion | Design rule |
| F6 | Lump-sum items are progressed by **% stage completion** | [F] | Roadmap: `milestone` measurement type (stage weights, evidence = photo / inspection record), verified by sign-off rather than drone | Backlog T-507 |
| F7 | Crossings are **discrete objects** with sub-components (pits, casing, product pipe) | [F] | Roadmap: `crossing` entity with component progress; HDD/drilling logs as independent evidence | Backlog T-508 |
| F8 | QA KPI (weld repair rate per WPS) appears in the client report | [F] | Use the weld log as the LOG source (already) plus a repair-rate KPI | Backlog |
| F9 | The report is project-level. It does not show crew-level or claim-level reconciliation | [F] | S9 = the same report **plus** check columns (measured, claimed, status, alerts) | ✅ Built |
| F10 | "Drohne" in the project title is a place name, not a drone reference | [F] | Avoid confusion in the thesis | Note |

## 3. Questions raised
- Q-076: Which plan-sheet numbering and sheet ↔ KP table does the project use? Can an anonymised sheet index be shared?
- Q-077: Are subcontractor man-hours in the client report taken from subcontractor timesheets, or from the JV's own attendance records?
- Q-078: For lump-sum items (valve stations), what are the stage weights and who certifies the %?
