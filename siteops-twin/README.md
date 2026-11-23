# SiteOps Twin

**An Interactive Digital Twin for Daily Production, Personnel/Equipment Tracking, and Subcontractor Quantity Verification in Oil & Gas Pipeline Construction**

Master's research project in collaboration with Politecnico di Milano (POLIMI).
Status: **Phase 0: Research and solution structure (for review)**

> **Confidentiality.** This repository contains no real company names, coordinates, personnel identities or proprietary data. Placeholders are used throughout: `[PROJECT_CODE]`, `[SITE_ID]`, `[SPREAD_ID]`, `[CONTRACTOR_A]`, `[SUBCONTRACTOR_B]`, `[DRONE_SW]`, `[ERP_SYSTEM]`. Any data under `data/synthetic/` is **synthetic demo data** and is labelled as such.

## Repository map

| Folder | Content | Phase |
|---|---|---|
| `agents/` | 14 specialist agent briefs, execution rules, handover template | 0 |
| `handovers/` | Agent-to-agent handover notes (`<phase>_<agent>.md`) | rolling |
| `qa/` | Quality-reviewer phase-gate reviews | rolling |
| `00_project_management/` | Master plan (MD + CSV), project task backlog | 0 |
| `01_governance/` | Charter, stakeholder map, RACI, data-governance, privacy, cybersecurity and ethics plan, pilot-site criteria | 1 |
| `02_literature_review/` | PRISMA protocol, search strings, screening log, reference matrix, gap analysis | 0 (protocol) → 2 |
| `03_as_is_analysis/` | As-is process map, data-flow diagram, pain points, root causes, KPI baseline | 0 (draft) → 3 |
| `04_to_be_architecture/` | Conceptual architecture, quantity measurability matrix, MVP scope, later the data dictionary, ERD and wireframes | 0 (concept) → 4 |
| `05_methodology/` | Research framing (RQs, hypotheses, scope, success criteria); later DSR design, protocols, metrics | 0 → 5 |
| `06_pilot_testing/` | Pilot plan, parallel-measurement protocol, UAT, checklists | 6 |
| `07_business_case/` | Cost-benefit model, ROI, NPV, sensitivity analysis, roadmap | 7 |
| `08_thesis/` | Thesis outline and chapter drafts | 8 |
| `09_paper/` | Journal and conference paper plan | 9 |
| `data/templates/` | Machine-readable templates (CSV, JSON) | rolling |
| `data/synthetic/` | Labelled synthetic demo data for the prototype | 6 |
| `prototype/` | MVP dashboard (**not started: code gate D-005**) | 6 |
| `docs/` | Shareable outputs, such as the executive brief | rolling |
| `phase_reports/` | End-of-phase close-out reports | rolling |

## Root control files
[`PROJECT_STATUS.md`](PROJECT_STATUS.md) · [`DECISIONS_LOG.md`](DECISIONS_LOG.md) · [`ASSUMPTIONS_LOG.md`](ASSUMPTIONS_LOG.md) · [`RISK_REGISTER.md`](RISK_REGISTER.md) · [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md)

## Phase 0 / first-iteration deliverables
1. Repository structure (this file) and [agent roster](agents/README.md)
2. Master plan: [Markdown](00_project_management/master_plan.md), [CSV](00_project_management/master_plan.csv) and [task backlog](00_project_management/backlog.csv)
3. [Research questions, hypotheses, scope, success criteria](05_methodology/research_framing.md)
4. [Literature-review protocol](02_literature_review/protocol.md) and [search strings](02_literature_review/search_strings.md)
5. [As-is process map](03_as_is_analysis/as_is_process_map.md) and [data-flow diagram](03_as_is_analysis/as_is_data_flow.md)
6. [Conceptual architecture](04_to_be_architecture/conceptual_architecture.md) and [MVP scope](04_to_be_architecture/mvp_scope.md)
7. [MVP backlog with user stories and acceptance criteria](04_to_be_architecture/ux/mvp_backlog.md)
8. [Synthetic dataset specification](04_to_be_architecture/data_model/synthetic_dataset_spec.md) and [quantity measurability matrix](04_to_be_architecture/geospatial/quantity_measurability_matrix.md)
9. [Dashboard wireframe description](04_to_be_architecture/ux/dashboard_wireframes.md)
10. [One-page executive brief](docs/executive_brief.md)
11. [Quality review](qa/phase_0_quality_review.md) and [Phase 0 close-out](phase_reports/phase_0_closeout.md)

## Conventions

- **F / A / R tagging.** Statements are tagged **[F]** for fact (sourced or observed), **[A]** for assumption (logged in `assumptions_log.csv`) and **[R]** for recommendation.
- **Location referencing.** All quantities are referenced to **chainage / kilometre point (KP)** along the pipeline alignment, using `KP 012+350` format (km + m), and grouped into **sections** (`[SPREAD_ID]-S##`).
- **Diagrams** are in Mermaid so they render on GitHub and stay version-controlled.
- **Citation style:** APA 7 (IEEE alternative to be confirmed with the supervisor).
