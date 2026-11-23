# Handover: P0 / solution-architect → data-engineer, gis-engineer, ux-designer, full-stack-developer, quality-reviewer

- **Date:** 2026-11-23
- **Task / backlog IDs:** T-005

## 1. What was produced
| File | Status | Notes |
|---|---|---|
| `04_to_be_architecture/conceptual_architecture.md` | Draft | Layered diagram, components, objectives → epics traceability, standards table, offline-first, time/georef principles, deployment options, daily-cycle sequence, ADR-001…009 |
| `04_to_be_architecture/mvp_scope.md` | Draft, waiting for D-005 | MVP vs roadmap (E1–E10, R1–R9), boundaries, NFR-01…12, demo scenario, confirmation checklist C1–C10 |

## 2. Key decisions taken (proposed rows for `DECISIONS_LOG.md`)
| ID | Date | Decision | Rationale | Owner | Status |
|---|---|---|---|---|---|
| D-040 | 2026-11-23 | Target deployment is hybrid (site edge store-and-forward + company cloud/DC). The prototype runs as a single local instance | Resilient on remote ROW; central audit and backup; simple to build for the thesis | solution-architect | Proposed |
| D-041 | 2026-11-23 | Compare drone measurements with cumulative reported/claimed quantity at `flight_time` (± window), not with the daily total | Avoids false discrepancies from work done after the flight | solution-architect; data-engineer | Proposed |
| D-042 | 2026-11-23 | Invoiced state imported from `[ERP_SYSTEM]` by read-only CSV in the MVP | Closes the six-state chain without ERP integration | solution-architect; commercial-analyst | Proposed |
| D-043 | 2026-11-23 | Roles: Field, Subcontractor, Survey, QS, Commercial, PM, Admin, Auditor. Subcontractors see only their own data | Least privilege; dispute neutrality | solution-architect | Proposed |

## 3. Assumptions introduced (proposed rows for `ASSUMPTIONS_LOG.md`)
| ID | Assumption | Source / basis | Impact if wrong | Validation method | Owner | Due | Status |
|---|---|---|---|---|---|---|---|
| A-040 | MVP activity tracking is event-level (report/telematics events), not minute-level | Feasibility within the MVP | Objective 3 only partially met | User confirmation (C2) | solution-architect | P4 | Open |
| A-041 | Generic formats (CSV + GeoPackage + COG + LandXML) with per-vendor adapters cover `[DRONE_SW]` exports | Common photogrammetry outputs | Adapter effort grows | Vendor docs (Q-005) | solution-architect | P3 | Open |
| A-042 | MVP effort is about 14–18 developer-weeks | T-shirt estimate | P6 slips or scope is cut | Re-estimate after P4 | solution-architect | P4 | Open |
| A-043 | AL-05 default threshold: productivity drop of 25% or more against the 5-day rolling median | Initial judgement | Too many or too few alerts | Calibrate on synthetic data, then pilot data | data-scientist | P6 | Open |

## 4. Open questions (proposed rows for `OPEN_QUESTIONS.md`)
| ID | Question | For | Needed by | Blocking | Status |
|---|---|---|---|---|---|
| Q-040 | Is the hybrid deployment (site edge + company cloud) acceptable to IT and the client (data residency)? | IT | P4 | | Open |
| Q-041 | What is the production-day cutoff for night shifts (e.g. 04:00 local)? Do any spreads work double shifts? | Site Manager | P4 | | Open |
| Q-042 | At what time of day are drone flights made? Is it before or after the shift ends? (affects D-041 and A-013) | Survey team | P4 | | Open |
| Q-043 | Is Streamlit acceptable for the thesis demo instead of FastAPI + web map, if time is short? | User | D-005 | | Open |

## 5. Risks (proposed rows for `RISK_REGISTER.md`)
| ID | Risk | Category | L | I | Score | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| R-40 | MVP scope (14–18 dev-weeks) exceeds the P6 window | Delivery | 4 | 3 | 12 | Cut order in `mvp_scope.md` §2; Streamlit fallback (Q-043) | solution-architect | Open |
| R-41 | Offline sync conflicts produce duplicate or inconsistent records | Data quality | 3 | 3 | 9 | Client UUIDs, append-only versions, DQ flags, no silent merge | data-engineer | Open |

## 6. What the next agent must know
1. **data-engineer.** Records are append-only per quantity state, with `version`, `source`, `provenance`, `superseded_by`, `dq_flag`, UTC timestamps plus `site_tz` and `production_date`. KP from–to on every quantity record.
2. **gis-engineer.** Every Measured qty needs `method`, `accuracy_rmse`, `uncertainty_abs` and footprint geometry. Comparison is at `flight_time` (D-041).
3. **ux-designer.** The screens are the KP strip + map, daily production, the reconciliation workbench (with ortho, footprint and evidence side by side), the scorecard and the timeline. The mobile form must meet NFR-01 and NFR-04.
4. **full-stack-developer.** Do not start until the user ticks C1–C10 (D-005).

## 7. Known weaknesses / not done
- No ERD or data dictionary yet (P4, data-engineer).
- The security control mapping to ISO 27001 / IEC 62443 is only principles so far (P4).
- The effort estimate is unvalidated.
- The C4 container/deployment diagrams are not drawn (P4).
