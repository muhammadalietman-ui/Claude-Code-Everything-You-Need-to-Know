# Handover: P0 / commercial-analyst → data-engineer, data-scientist, full-stack-developer, quality-reviewer

- **Date:** 2026-11-23
- **Task IDs:** T-008

## 1. What was produced
| File | Status | Notes |
|---|---|---|
| `04_to_be_architecture/ux/mvp_backlog.md` §3, §5, E5/E6/E9 stories | Draft | Reconciliation status rule, worked example, period vs cumulative rule, control matrix CTL-01..13, certification stories |

## 2. Key decisions proposed
| ID | Decision | Rationale |
|---|---|---|
| D-063 | Status rule: MATCHED if \|C−M\| ≤ U; WITHIN_TOLERANCE if ≤ U + T; DISCREPANCY if above; UNVERIFIABLE if no valid M. T = max(abs, pct × M) | Combines measurement uncertainty with contractual tolerance |
| D-064 | Certifiable cap without override = M + U + T. Above the cap needs a reason code and a comment; above `[OVERRIDE_CM_VALUE]` also needs CM approval. The platform never auto-certifies | Overpayment control; segregation of duties |
| D-065 | Certificates are based on cumulative-to-date quantities; period = Δ cumulative. Closed periods are not re-certified; corrections go into the next period as adjustment lines | Standard interim-valuation practice |
| D-066 | Out of MVP: retention, advance recovery, escalation, variations (flag only), back-charges, tax, currency | Keep the MVP focused on quantities |

## 3. Assumptions introduced
| ID | Assumption | Validation |
|---|---|---|
| A-063 | Measurement uncertainty U is reported by survey at 95% confidence, per section and activity | Survey team (Q-005, Q-007) |
| A-064 | The "independent" source for welds and coating is the QA/QC record, which is controlled separately from the subcontractor | QA/QC confirmation (A-014) |
| A-065 | Unit-rate valuation (qty × rate per BoQ item) is enough for the MVP certificate draft | Anonymised subcontract review (Q-004) |

## 4. Open questions
| ID | Question |
|---|---|
| Q-063 | Which contractual tolerance values (`[TOL_VOL_PCT]`, `[TOL_LEN_ABS]`) and which measurement rules apply (e.g. trench measured to design profile or to actual)? |
| Q-064 | What override approval threshold `[OVERRIDE_CM_VALUE]` applies, and who approves under the delegation of authority? |
| Q-065 | Are subcontractors paid on daily agreed quantities, on weekly interim agreements, or only monthly? This affects H3 sample size (R-09) |

## 5. Risks proposed
| ID | Risk | L | I | Mitigation |
|---|---|---|---|---|
| R-60 | The tolerance rule is perceived by subcontractors as unilateral and increases disputes in the short term | 3 | 3 | Agree the parameters with subcontractors before the pilot; transparent SC status view (US-E3-03) |
| R-61 | QS over-relies on the platform status and skips the contractual judgement | 2 | 4 | No auto-certification; override and reason design; training |

## 6. What the next agent must know
- The data-engineer must store U, the tolerance version and the measurement QA flag with every reconciliation result, so it can be reproduced later (US-E5-02).
- Synthetic data must seed the §3.2 example (S-07, 2027-03-10) and one case per alert AL-01..AL-08, so the acceptance criteria are testable.

## 7. Known weaknesses / not done
- The business-case model (P8) has not started.
- The controls have not been validated against a real anonymised subcontract (Q-004).
