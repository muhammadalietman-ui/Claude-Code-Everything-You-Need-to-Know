# Handover: P0 / process-analyst → solution-architect, data-engineer, commercial-analyst, quality-reviewer

- **Date:** 2026-11-23
- **Task / backlog IDs:** T-004 (plus a preliminary start on T-303)

## 1. What was produced
| File | Status | Notes |
|---|---|---|
| `03_as_is_analysis/as_is_process_map.md` | Draft ([A] hypothetical) | 8-lane Mermaid swimlane; steps AS-01 to AS-26; step table; BPMN note |
| `03_as_is_analysis/as_is_data_flow.md` | Draft | DFD level 0 and level 1; 9 data stores; integration breaks DB-01 to DB-08 |
| `03_as_is_analysis/pain_point_register.csv` | Draft | PP-01 to PP-15, linked to steps and to H1–H4 |
| `03_as_is_analysis/kpi_baseline_template.csv` | Draft | KPI-01 to KPI-16, aligned with the research-framing targets |
| `03_as_is_analysis/root_cause_preview.md` | Draft ([A]) | Ishikawa (mindmap) and a 5-Whys example |

## 2. Key decisions taken (proposed)
| ID | Date | Decision | Rationale | Owner | Status |
|---|---|---|---|---|---|
| D-030 | 2026-11-23 | Step IDs AS-01 to AS-26 are kept as BPMN element IDs in P3 | Traceability from steps to pain points to KPIs | process-analyst | Proposed |
| D-031 | 2026-11-23 | Map one generic as-is process. Model spread or subcontract variants in P3 only if they differ materially | Keep Phase 0 lean | process-analyst | Proposed |

## 3. Assumptions introduced (ready to paste into ASSUMPTIONS_LOG.md)
| ID | Assumption | Source / basis | Impact if wrong | Validation method | Owner | Due | Status |
|---|---|---|---|---|---|---|---|
| A-030 | The as-is process (AS-01 to AS-26) represents current practice across spreads | Typical contractor practice; user brief | Map and baseline invalid | 6–10 interviews, 2 walkthroughs | process-analyst | P3 | Open |
| A-031 | Step durations in the step table are representative | Practitioner judgement | Wrong baseline expectations | Time-and-motion in the baseline period | process-analyst | P7 | Open |
| A-032 | Quantities are re-keyed 3–4 times between foreman sheet and ERP | Typical practice | PP-07 overstated | Trace 10 quantities | process-analyst | P3 | Open |
| A-033 | Joint measurement happens per claim (weekly or monthly), not daily | Typical practice | Dispute mechanism differs | QS interview | commercial-analyst | P3 | Open |
| A-034 | DPRs and subcontractor reports use landmarks or "corners" rather than consistent KP values | User brief ("corner") | DB-01 less severe | Sample of 20 DPRs | process-analyst | P3 | Open |

## 4. Open questions (ready to paste into OPEN_QUESTIONS.md)
| ID | Question | For | Needed by | Blocking | Status |
|---|---|---|---|---|---|
| Q-030 | Are joint measurement sheets signed by both parties, and at what frequency? | QS / Commercial | P3 | | Open |
| Q-031 | Is there a dispute log (count, value, days to close) for the last 6–12 months that can be anonymised for the baseline? | Commercial | P3 | | Open |
| Q-032 | Who triggers drone flights: a fixed daily plan or requests from site/QS? Is the flight before or after the shift? | Survey | P3 | | Open |
| Q-033 | Which ERP transaction records certified quantities (service entry, goods receipt, or other)? | Finance | P3 | | Open |

## 5. Risks (ready to paste into RISK_REGISTER.md)
| ID | Risk | Category | L | I | Score | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| R-30 | The as-is differs materially between spreads or subcontractors, which weakens generalisation | Validity | 3 | 3 | 9 | Document variants; pick a representative pilot | process-analyst | Open |
| R-31 | Historical dispute data is not available or is too sensitive to use for the baseline | Data access | 3 | 3 | 9 | Prospective baseline during P7; anonymised aggregates | commercial-analyst | Open |

## 5b. What the next agent must know
1. The core design driver is **DB-01 (no common KP key)** plus **DB-07 (commercial states not modelled)**. The architecture must resolve both.
2. The highest-severity pain points are **PP-01, PP-10 and PP-13**, all commercial and all linked to H1 and H3.
3. Buried activities (PP-03) need a **time-window evidence strategy**, not just daily flights. The gis-engineer should reflect this in the measurability matrix.
4. The KPI baseline template (KPI-01 to KPI-16) is the measurement contract for P7. Any change must be agreed with the research-lead.

## 6. Field-operations review (field-operations-specialist)
- **Realistic sequence.** Clearing → grading → stringing → welding/NDT → coating → trenching → lowering → backfill → reinstatement is implied in the activity coverage. Activity-level detail belongs to the taxonomy in P4.
- **Shift-end capture.** Foremen typically complete records in the site vehicle at shift end, with poor signal. The future mobile form must work offline and take under 5 minutes.
- **Flight timing.** Daily flights are usually scheduled when site traffic allows. Lowering-in and backfill can start and finish between two flights, so PP-03 is realistic.
- **Joint measurement on site.** This takes QS and subcontractor time on a long ROW, and travel along the spread is a real cost driver for KPI-12.
- **Personnel location (PP-12).** This is mostly an HSE muster topic. Worker acceptance depends on not using the data for individual performance. This supports D-006.

## 7. Known weaknesses / not done
- Everything is hypothetical. No interviews have been held yet.
- The DFD does not cover client progress claims in detail.
- There is no BPMN XML yet.
- Severity and frequency scores are judgement only.
