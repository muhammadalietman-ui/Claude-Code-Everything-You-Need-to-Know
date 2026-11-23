# Phase 0 Close-Out: Research and Solution Structure

Date: 2026-11-23 · Lead: project-manager · QA: pass with conditions (D-068)

## 1. Completed deliverables

| # | First-iteration item | File(s) | Agent |
|---|---|---|---|
| 1 | Complete repository structure, plus 14 agent briefs | `README.md`, `agents/` | project-manager |
| 2 | Master project plan (MD + CSV), plus task backlog | `00_project_management/master_plan.md`, `master_plan.csv`, `backlog.csv` | project-manager |
| 3 | Research questions, hypotheses, scope, success criteria | `05_methodology/research_framing.md` | research-lead |
| 4 | Literature-review protocol, search strings, templates, seed references, gap hypotheses, **IPLOCA practice sources** | `02_literature_review/` | literature-reviewer |
| 5 | As-is process map and data-flow diagram (Mermaid), pain points, KPI baseline template, root-cause preview, **IPLOCA practice alignment** | `03_as_is_analysis/` | process-analyst, field-operations-specialist |
| 6 | Conceptual architecture (Mermaid) and MVP scope, plus **field-sensing layer** | `04_to_be_architecture/conceptual_architecture.md`, `mvp_scope.md`, `field_sensing_layer.md` | solution-architect |
| 7 | MVP backlog: 44 user stories with Gherkin acceptance criteria, control matrix CTL-01…13 | `04_to_be_architecture/ux/mvp_backlog.md`, `.csv` | ux-designer, commercial-analyst |
| 8 | Synthetic dataset specification, quantity measurability matrix, data templates | `04_to_be_architecture/data_model/`, `geospatial/`, `data/templates/` | data-engineer, gis-engineer |
| 9 | Dashboard wireframe description (S1–S7 desktop, M1–M4 mobile) | `04_to_be_architecture/ux/dashboard_wireframes.md` | ux-designer |
| 10 | One-page executive brief | `docs/executive_brief.md` | academic-writer |
| plus | Root logs, quality review, handovers | `PROJECT_STATUS.md`, `*_LOG.md`, `RISK_REGISTER.md`, `OPEN_QUESTIONS.md`, `qa/`, `handovers/` | all |

## 2. Open questions (blocking first)
- **Q-001:** POLIMI programme, supervisor, graduation session.
- **Q-003:** pilot spread and dates, plus a backup.
- **Q-008:** site jurisdiction for labour, privacy and drone law; ethics committee.
- **Q-022:** Scopus/WoS access through POLIMI.
- **Q-072:** sensing tiers acceptable to management; DPO availability.
- Also: Q-011 (what "corner" means), Q-013 (IPLOCA membership), Q-063 (contract tolerances), Q-070 (subcontract basis for presence verification). The full list is in `OPEN_QUESTIONS.md`.

## 3. Decisions required from the user
1. **D-002:** approve the research framing (RQ1–RQ5, H1–H4, decision rules).
2. **D-069 / D-070:** which field-sensing tiers go into the MVP and pilot, and whether H5 is added.
3. **D-005, the code gate:** confirm the MVP scope with checklist C1–C11 in `mvp_scope.md`. Note QA-03: the full MVP plus E11 is about 17–22 developer-weeks against a 10-week P6 window. Options are (a) the cut order, (b) the Streamlit fallback (Q-043), or (c) extending P6.
4. **D-003, D-004, D-009, D-010:** methodology, KP location key, stack, citation style.

## 4. Next actions (Phase 1, weeks 3–6)
| Action | Agent |
|---|---|
| Project charter, stakeholder map, RACI (T-101, T-102) | project-manager |
| Data-governance, privacy, cyber and ethics plan, with **DPIA screening for field sensing** (T-103, T-105) | research-lead |
| Pilot-site selection criteria and scoring (T-104) | field-operations-specialist |
| Run the SLR searches; confirm IPLOCA access and extract practice evidence (T-201, T-205, T-206) | literature-reviewer (P2, in parallel) |
| Prepare the interview guide for the as-is validation (T-301) | process-analyst |

## 5. Quality checklist
- [x] Each deliverable exists and has an owner agent
- [x] Facts, assumptions and recommendations are tagged; all assumptions are logged
- [x] All referenced A/D/Q/R IDs are defined in the root logs (script check)
- [x] No confidential data: placeholders only; synthetic data specified
- [x] CSV and JSON parse; 14 Mermaid diagrams parse (mermaid 11.4.1)
- [x] References are marked VERIFY; none presented as verified
- [x] No platform code written (code gate D-005 respected)
- [ ] User approval of the Phase 0 package (M0)
- [ ] Supervisor review of the research framing
