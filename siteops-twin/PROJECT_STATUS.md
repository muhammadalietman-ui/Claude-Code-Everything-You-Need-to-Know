# PROJECT_STATUS

| Field | Value |
|---|---|
| Project | SiteOps Twin `[PROJECT_CODE]` |
| Current phase | **P0: Research and solution structure** |
| Phase status | Delivered, **waiting for user review** |
| Overall RAG | 🟢 Green (schedule) · 🟡 Amber (pilot access, ethics/DPIA route for field sensing, MVP size vs P6 window) |
| Last updated | 2026-11-23 |
| Next gate | M0: user approval of the Phase 0 package. Then M4, the MVP-scope code gate (D-005) |

## Phase tracker
| Phase | Status | Lead |
|---|---|---|
| P0 Structure | ✅ Delivered, QA passed with conditions (in user review) | project-manager |
| P1 Governance and access | ⏳ Planned | project-manager |
| P2 SLR | ⏳ Planned (protocol ready) | literature-reviewer |
| P3 As-is (validated) | ⏳ Planned (hypothetical draft ready) | process-analyst |
| P4 To-be design | ⏳ Planned (concept ready) | solution-architect |
| P5 Methodology | ⏳ Planned (framing ready) | research-lead |
| P6 Prototype | 🔒 Blocked by D-005 (MVP scope confirmation) | full-stack-developer |
| P7 Pilot | ⏳ Planned | research-lead |
| P8 Business case | ⏳ Planned | commercial-analyst |
| P9 Thesis and paper | ⏳ Planned | academic-writer |

## Phase 0 changes during the phase (user instructions)
1. Work organised into 14 specialist agents (`agents/`), with handovers and shared logs.
2. **IPLOCA** adopted as the primary industry-practice reference (D-011, Approved). See `02_literature_review/industry_practice_sources.md` and `03_as_is_analysis/industry_practice_alignment.md`.
3. **Field-sensing layer** beyond the drone proposed (D-069, E11, H5): check-in, vehicle GPS, plant trackers, count-only cameras, optional badges. See `04_to_be_architecture/field_sensing_layer.md`.

## Quality gate
Phase 0 QA: **Pass with conditions** (`qa/phase_0_quality_review.md`). The open major item is QA-03 (MVP size).

## Top items needing user attention
- **Blocking questions:** Q-001 (POLIMI calendar and supervisor), Q-003 (pilot spread), Q-008 (jurisdiction and ethics), Q-022 (database access), Q-072 (sensing tiers and DPO).
- **Decisions to approve:** D-002 (research framing), D-005 (MVP scope, code gate), D-069 (sensing tiers), D-070 (H5).
