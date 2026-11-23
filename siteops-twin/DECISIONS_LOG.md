# DECISIONS_LOG

Status values: **Made** (taken within agent authority), **Proposed** (needs the user), **Approved**, **Rejected**.

| ID | Date | Decision | Rationale | Owner | Status |
|---|---|---|---|---|---|
| D-001 | 2026-11-23 | Keep the project self-contained in `siteops-twin/` inside the existing repository | Avoids disturbing existing content. Can be split into its own repository later | project-manager | Made |
| D-002 | 2026-11-23 | Adopt the research framing (5 sub-RQs, operationalised H1–H4, decision rules) | Makes the hypotheses testable within one pilot | research-lead | **Proposed** |
| D-003 | 2026-11-23 | Methodology: Design Science Research (Peffers et al. process) with an embedded action-research pilot | Fits artefact building plus field evaluation | research-lead | Proposed |
| D-004 | 2026-11-23 | Location key = chainage/KP on the as-built alignment. Quantities are aggregated to sections `[SPREAD_ID]-S##` (default 1 km, Q-011) | Pipeline contracts and progress are measured linearly. A KP key joins drone, field and commercial data | gis-engineer; data-engineer | Proposed |
| D-005 | 2026-11-23 | **Code gate.** No platform code until the user confirms the MVP scope in `04_to_be_architecture/mvp_scope.md` | User instruction | project-manager | **Proposed (pending user)** |
| D-006 | 2026-11-23 | Personnel tracking in the MVP is crew/zone level and consent-based, with no individual location history shown to commercial users | Privacy and labour-law risk (R-03). Proportionality | research-lead; solution-architect | **Revised by D-069** |
| D-007 | 2026-11-23 | Complement `[DRONE_SW]`: ingest its exports (orthophoto/DSM/volume reports) rather than re-process imagery | User constraint. Lower cost and risk | solution-architect | Made |
| D-008 | 2026-11-23 | Six-state quantity model: Planned → Reported (field) → Measured (independent) → Claimed (subcontractor) → Certified → Invoiced | Needed to compare all quantity states in one model (state count corrected at P0 QA) | commercial-analyst; data-engineer | Proposed |
| D-009 | 2026-11-23 | MVP stack (indicative): Python + PostgreSQL/PostGIS (SQLite/SpatiaLite for the demo), FastAPI, web map (MapLibre/Leaflet), offline-capable form (PWA or ODK-compatible) | Open, low cost, reproducible for the thesis | solution-architect | Proposed |
| D-010 | 2026-11-23 | Citation style APA 7, unless the supervisor prefers IEEE | Common in construction management venues | academic-writer | Proposed |
| D-011 | 2026-11-23 | Adopt **IPLOCA** as the primary industry-practice reference (*Onshore Pipelines: The Road to Success*, Novel Construction Initiative). It grounds the process, the activity taxonomy, measurement practice and field requirements. It is not used as evidence for H1–H4 effect sizes | User instruction (2026-11-23). Practice-grounded design | literature-reviewer; field-operations-specialist | **Approved (user)** |
| D-020 | 2026-11-23 | SLR date range 2010–2026, with seminal works exempt. English, plus Italian for POLIMI sources | Covers the UAV/DT era | literature-reviewer | Proposed |
| D-021 | 2026-11-23 | Google Scholar limited to the first 200 results per string, reported separately in PRISMA | Scholar ranking is not reproducible | literature-reviewer | Proposed |
| D-030 | 2026-11-23 | Step IDs AS-01 to AS-26 are kept as BPMN element IDs in P3 | Traceability from step to pain point to KPI | process-analyst | Proposed |
| D-031 | 2026-11-23 | One generic as-is map. Variants are mapped in P3 only if they differ materially | Keep Phase 0 lean | process-analyst | Proposed |
| D-040 | 2026-11-23 | Target deployment is hybrid (site edge store-and-forward plus company cloud/DC). The prototype runs as a single local instance | Resilience on a remote ROW; simple for the thesis | solution-architect | Proposed |
| D-041 | 2026-11-23 | Compare drone measurements with the *cumulative* reported/claimed quantity at flight time (± window), not with the daily total | Avoids false discrepancies from work done after the flight | solution-architect | Proposed |
| D-042 | 2026-11-23 | The Invoiced state is imported from `[ERP_SYSTEM]` by read-only CSV in the MVP | Closes the six-state chain without ERP integration | solution-architect; commercial-analyst | Proposed |
| D-043 | 2026-11-23 | Eight roles: Field, Subcontractor, Survey, QS, Commercial, PM, Admin, Auditor. Subcontractors see only their own data | Least privilege; neutrality in disputes | solution-architect | Proposed |
| D-050 | 2026-11-23 | ~~Bands: MATCHED ≤ 0.5·band~~. **Superseded by D-063** at P0 QA (conflicting rules) | One rule only | gis-engineer | Superseded |
| D-051 | 2026-11-23 | Default volume uncertainty uses the correlated-error model σV ≈ A·σΔz. The uncorrelated estimate is shown only as a lower bound | Conservative and honest uncertainty | gis-engineer | Proposed |
| D-052 | 2026-11-23 | UAV verification in the MVP covers CLR, GRD, STR, TRN (length), LOW (time-window), BKF, RST. WLD, NDT, FJC, HDD, tie-ins and HYD are verified against logs or records | Measurability matrix | gis-engineer | Proposed |
| D-053 | 2026-11-23 | Sections are half-open KP intervals. Quantities that span sections are split pro rata | Unambiguous aggregation | gis-engineer | Proposed |
| D-054 | 2026-11-23 | Synthetic seed `20270104`. All synthetic files are prefixed `SYNTHETIC_` and carry a header | Reproducibility and labelling | data-engineer | Proposed |
| D-055 | 2026-11-23 | Reconciliation grain: activity × section × work_date × subcontractor | RQ2 | data-engineer | Proposed |
| D-056 | 2026-11-23 | Records are append-only and versioned; audit events carry before/after hashes | Auditability | data-engineer | Proposed |
| D-057 | 2026-11-23 | Report and claim lines link to sections spatially by KP interval, not by a foreign key | Allows pro rata split | data-engineer | Proposed |
| D-060 | 2026-11-23 | Status is shown as colour + icon + text, using the Okabe–Ito palette | Colour-blind safety; sunlight | ux-designer | Proposed |
| D-061 | 2026-11-23 | Desktop views are exception-first | Supports H2 | ux-designer | Proposed |
| D-062 | 2026-11-23 | Mobile report in 3 screens or fewer, prefilled from yesterday, with GPS-assisted KP | ≤ 5 min target | ux-designer | Proposed |
| D-063 | 2026-11-23 | **Single reconciliation rule:** \|C−M\| ≤ U → MATCHED; ≤ U+T → WITHIN_TOLERANCE; above → DISCREPANCY; no valid M → UNVERIFIABLE. U = 95% measurement uncertainty; T = contract tolerance | Combines measurement uncertainty with the contractual tolerance | commercial-analyst | Proposed |
| D-064 | 2026-11-23 | Certifiable cap without override = M + U + T. Above the cap needs a reason code; above `[OVERRIDE_CM_VALUE]` also needs CM approval. Never auto-certified | Overpayment control; segregation of duties | commercial-analyst | Proposed |
| D-065 | 2026-11-23 | Certificates are on cumulative-to-date quantities; period = change in cumulative. Closed periods are not re-certified | Standard interim-valuation practice | commercial-analyst | Proposed |
| D-066 | 2026-11-23 | Out of the MVP: retention, advances, escalation, variations (flag only), back-charges, tax, currency | Focus on quantities | commercial-analyst | Proposed |
| D-067 | 2026-11-23 | P0 QA harmonisation: AL-05 default threshold = 25% (A-043) across all files | Spec said 40%, backlog example fired at −35% | quality-reviewer | Made |
| D-068 | 2026-11-23 | P0 quality gate passed, with minor items carried forward (see `qa/phase_0_quality_review.md`) | Phase-gate rule | quality-reviewer | Made |
| D-069 | 2026-11-23 | Add a **tiered field-sensing layer** (E11) beyond the drone: T1 muster check-in, T2 vehicle GPS/manifest, T3 plant trackers (MVP); T4 count-only AI cameras at 2–3 fronts (pilot); T5 badges optional and HSE-led; T7 biometrics excluded. Commercial users see aggregates only. Identifiable data stays with HR/HSE | User instruction: the drone is insufficient for manpower, equipment and fragmented locations | solution-architect; research-lead | **Proposed (user to confirm tiers, C11)** |
| D-070 | 2026-11-23 | Add hypothesis **H5** (presence sensing reduces claimed vs verified manpower and equipment-hour discrepancy) | Evaluates the new sensing layer | research-lead | Proposed |
