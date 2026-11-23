# DECISIONS_LOG

Status values: **Made** (taken within agent authority), **Proposed** (needs the user), **Approved**, **Rejected**.

| ID | Date | Decision | Rationale | Owner | Status |
|---|---|---|---|---|---|
| D-001 | 2026-11-23 | Keep the project self-contained in `siteops-twin/` inside the existing repository | Avoids disturbing existing content. Can be split into its own repository later | project-manager | Made |
| D-002 | 2026-11-23 | Adopt the research framing (5 sub-RQs, operationalised H1–H4, decision rules) | Makes the hypotheses testable within one pilot | research-lead | **Proposed** |
| D-003 | 2026-11-23 | Methodology: Design Science Research (Peffers et al. process) with an embedded action-research pilot | Fits artefact building plus field evaluation | research-lead | Proposed |
| D-004 | 2026-11-23 | Location key = chainage/KP on the as-built alignment. Quantities are aggregated to sections `[SPREAD_ID]-S##` (default 1 km, Q-011) | Pipeline contracts and progress are measured linearly. A KP key joins drone, field and commercial data | gis-engineer; data-engineer | Proposed |
| D-005 | 2026-11-23 | **Code gate.** No platform code until the user confirms the MVP scope in `04_to_be_architecture/mvp_scope.md` | User instruction | project-manager | **Proposed (pending user)** |
| D-006 | 2026-11-23 | Personnel tracking in the MVP is crew/zone level and consent-based, with no individual location history shown to commercial users | Privacy and labour-law risk (R-03). Proportionality | research-lead; solution-architect | Proposed |
| D-007 | 2026-11-23 | Complement `[DRONE_SW]`: ingest its exports (orthophoto/DSM/volume reports) rather than re-process imagery | User constraint. Lower cost and risk | solution-architect | Made |
| D-008 | 2026-11-23 | Five-state quantity model: Planned → Reported (field) → Measured (independent) → Claimed (subcontractor) → Certified → Invoiced | Needed to compare all quantity states in one model | commercial-analyst; data-engineer | Proposed |
| D-009 | 2026-11-23 | MVP stack (indicative): Python + PostgreSQL/PostGIS (SQLite/SpatiaLite for the demo), FastAPI, web map (MapLibre/Leaflet), offline-capable form (PWA or ODK-compatible) | Open, low cost, reproducible for the thesis | solution-architect | Proposed |
| D-010 | 2026-11-23 | Citation style APA 7, unless the supervisor prefers IEEE | Common in construction management venues | academic-writer | Proposed |
