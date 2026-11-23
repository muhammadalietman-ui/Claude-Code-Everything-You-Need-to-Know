# Industry-Practice Sources: IPLOCA First

Owners: literature-reviewer and field-operations-specialist. Version 0.1. Added at the user's request (D-011).

> **Why this file exists.** Academic literature on digital twins and UAV surveying rarely describes how a pipeline spread actually works day to day. IPLOCA is the contractor-side reference for onshore pipeline construction practice. It is used here to make the as-is process, the activity taxonomy, the measurement practice and the MVP requirements **practice-grounded**, so that they reflect how spreads are organised and paid, not how an academic model assumes they are.

## 1. IPLOCA sources

| ID | Source | What it is [F] | How we use it | Access | Status |
|---|---|---|---|---|---|
| IP-01 | IPLOCA, *Onshore Pipelines: The Road to Success*. First edition 2009 (two volumes: guidance and appendices). Updated in 2011 and 2013, then a 4th-edition app in 2017; IPLOCA's committee page refers to a 5th edition. | IPLOCA's flagship onshore pipeline guide, produced through the Novel Construction Initiative. It covers project phases, contract baselines, risk analysis and management, best practices, and new trends and innovation, with the aim of improving cost and schedule delivery, environmental footprint and safety. | The reference for spread organisation, the construction sequence, contract baselines and risk practice. It is used to validate the as-is map (AS-xx), the activity catalogue (E1), the measurability matrix and the risk register | **Members-only** (app, through the company's IPLOCA member representative) | VERIFY edition and access (Q-013) |
| IP-02 | IPLOCA Novel Construction Initiative: Spring and Fall sessions (e.g. Lisbon 2024, Palermo 2025) | Working-group outputs on innovation in onshore pipeline construction. The Lisbon 2024 groups covered AI and digital transformation: digitising pipeline activities, 3D control systems, planning and resource scheduling, predictive management, and barriers such as security and trust | Positions SiteOps Twin against the industry's own digital agenda (Ch. 2, Ch. 8). It also provides practitioner-identified barriers for RQ5 | Some session slides are public on iploca.com; the full archive is on the members-only NEST platform | To retrieve |
| IP-03 | IPLOCA Yearbook and Newsletter technical articles | Annual and periodic industry publications | Case examples of digital progress tracking, drone use and spread productivity | Public (issuu) | To screen |
| IP-04 | IPLOCA committee guidance (HSE, Environment, Innovation) | Committee outputs and recommended practices | HSE constraints for devices and drones on the ROW (R-13); environmental reinstatement practice | Varies | To identify. Specific titles are not listed until verified |

## 2. Complementary practice and normative sources

| ID | Source | Use | Status |
|---|---|---|---|
| PR-01 | AACE International recommended practices (progress measurement, earned value, productivity-loss and forensic schedule analysis) | Progress rules of credit, EVM, and claims defensibility (C5, C6) | VERIFY the specific RP numbers |
| PR-02 | FIDIC conditions of contract: measurement and valuation clauses | The measurement principle in subcontracts (commercial-analyst, CTL rules) | VERIFY the edition used by `[CONTRACTOR_A]` |
| PR-03 | API 1104 (welding of pipelines and related facilities) | Why weld and NDT quantities come from the QA/QC record, not the drone (A-014, A-064) | VERIFY edition |
| PR-04 | ASME B31.4 / B31.8; ISO 13623; EN 1594; CSA Z662 (depending on the project code) | Design code context for cover depth, hydrotest sections and as-built requirements | VERIFY applicable code (Q-008) |
| PR-05 | IOGP reports on HSE and digital | Industry HSE and data-governance practice | To identify |

## 3. Practice-grounding rules for all agents [R]
1. **Map to how the spread is organised.** Model the front end (clearing, grading, stringing, bending), the mainline welding/NDT/coating crews, the tie-in crews and the back end (trenching, lowering-in, backfill, clean-up/reinstatement), plus special crews (crossings/HDD, hydrotest). Each group moves at its own rate along the KP.
2. **Measure progress the way spreads already do.** For each activity, use the existing source of daily metres or joints: foreman tallies, the weld log, NDT reports and the as-built survey. The digital twin **reuses existing records**; it does not create a parallel paperwork stream.
3. **Use the as-built survey as an independent witness.** In practice the survey crew picks up top-of-pipe before backfill. This record and the drone flight are the two independent measurements for lowering-in and trench depth (PP-03, R-50).
4. **Respect the commercial ritual.** Joint measurement walks and weekly progress meetings with subcontractors are where quantities are agreed. The platform must produce the evidence pack *for* that meeting, not bypass it.
5. **Field burden budget.** Any new field data entry must replace an existing one or take under 5 minutes per crew per shift (NFR, US-E2).
6. **HSE first.** No new device, flight pattern or ROW access without the site's permit-to-work and HSE review.
7. **Tag practice claims.** A statement like "spreads usually…" is tagged **[A]** unless it is backed by IPLOCA or another IP/PR source, or by a P3 interview.

## 4. Actions
- **T-205.** Confirm whether `[CONTRACTOR_A]` is an IPLOCA member and get *The Road to Success* app through the member representative (Q-013).
- **T-206.** Extract the Road to Success guidance relevant to: spread organisation, contract baselines, progress and measurement, risk, and innovation. Record it as a practice-evidence table in `industry_practice_extract.csv` (columns: ip_id, chapter/section, practice statement, used_in_artefact, artefact_id).
- **T-207.** Retrieve the public Novel Construction session outputs on AI and digital transformation, and code their barriers and enablers against UTAUT constructs for RQ5.
- **T-208.** The field-operations-specialist validates the as-is map and the measurability matrix against IP-01 and against P3 interviews.

## Sources consulted (web, 2026-11-23)
- IPLOCA, "The Road to Success": https://iploca.com/news-media/the-road-to-success
- IPLOCA, Road to Success presentation (2010): https://www.iploca.com/app/uploads/2021/01/100317PresentationofTheRoadtoSuccess.pdf
- IPLOCA, Road to Success regional presentation: https://www.iploca.com/app/uploads/2021/01/07-Roadtosuccess-Truscello.pdf
- IPLOCA Novel Construction Initiative: https://www.iploca.com/committees/innovation/novel-construction-initiative/
- IPLOCA Novel Construction, Lisbon 2024 group outputs: https://www.iploca.com/app/uploads/2024/07/Group-1-Novel-Construction-PPT-Template-Lisbon-2024.pdf
