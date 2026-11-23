# Handover: P0 / ux-designer → full-stack-developer, field-operations-specialist, quality-reviewer

- **Date:** 2026-11-23
- **Task IDs:** T-008 (with commercial-analyst), T-009

## 1. What was produced
| File | Status | Notes |
|---|---|---|
| `04_to_be_architecture/ux/mvp_backlog.md` | Draft for user confirmation (D-005) | 44 stories with Gherkin AC; personas; story map; RBAC matrix; DoR/DoD; field review notes |
| `04_to_be_architecture/ux/mvp_backlog.csv` | Draft | Same stories in machine-readable form |
| `04_to_be_architecture/ux/dashboard_wireframes.md` | Draft (low fidelity) | S1–S7 desktop, M1–M4 mobile, navigation flow, status semantics, WCAG |

## 2. Key decisions proposed (to add to DECISIONS_LOG)
| ID | Decision | Rationale |
|---|---|---|
| D-060 | Status is always encoded as colour + icon + text, using the Okabe–Ito palette | Colour-blind safety; sunlight readability |
| D-061 | Desktop default views are exception-first (DISCREPANCY, UNVERIFIABLE, open alerts) | Supports H2 review time |
| D-062 | Mobile report is ≤ 3 screens with prefill from yesterday; GPS-assisted KP entry with manual override | ≤ 5 min target (US-E2-01) |

## 3. Assumptions introduced (to add to ASSUMPTIONS_LOG)
| ID | Assumption | Validation |
|---|---|---|
| A-060 | Story points are relative estimates for planning only (MVP ≈ 127 pts) | Re-estimate in P4 |
| A-061 | Sync-conflict rule: the server wins for approved records; device edits on pending records become new versions | Field-ops and SM review |
| A-062 | Foremen have a phone or shared rugged tablet with GPS and a camera, and report at shift end | Field survey (P3) |

## 4. Open questions (to add to OPEN_QUESTIONS)
| ID | Question |
|---|---|
| Q-060 | Do foremen report on their own or shared devices? In which language(s) must the app UI be? |
| Q-061 | Map the pain-point categories (DATA, TIME, DISP, EVID, DUP, VIS, ADM) to the process-analyst's pain-point IDs in P3 |
| Q-062 | Is `[REPORT_CUTOFF]` = 20:00 site time realistic for the field-report deadline? |

## 5. What the next agent must know
- The walking skeleton is E1-01 → E1-02 → E2-01 → E3-01 → E4-01 → E5-01 → E6-01 → E7-03 → E9-01 → E10-01. Build this first.
- Every number in the dashboard must link to its evidence (S6).
- Measured quantities must always show ±U and the flight QA flag.
- Personnel data is crew-level only (D-006, US-E8-01/03). Commercial roles never see coordinates.

## 6. Known weaknesses / not done
- The wireframes are ASCII only. There is no clickable prototype or Figma file yet.
- No usability testing with real users yet.
- Field review is a desk review by the agent role, not yet validated with real foremen.
