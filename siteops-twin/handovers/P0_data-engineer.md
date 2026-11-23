# Handover: P0 / data-engineer → full-stack-developer, data-scientist, commercial-analyst, quality-reviewer

- **Date:** 2026-11-23
- **Task / backlog IDs:** T-007

## 1. What was produced
| File | Status | Notes |
|---|---|---|
| `04_to_be_architecture/data_model/synthetic_dataset_spec.md` | Draft | Covers `SYN-SPREAD-01` (25 km, 25 sections, 60 days, 4 subcontractors): 23 entities, a Mermaid ERD, generation logic, seeded anomalies AL-01 to AL-08 with ground truth, outputs and validation checks |
| `data/templates/field_daily_report.template.csv` | Draft | Header row plus a SYNTHETIC EXAMPLE row |
| `data/templates/subcontractor_claim.template.csv` | Draft | Same |
| `data/templates/drone_measurement.template.csv` | Draft | Includes `sigma_qty` and `quality_flag` |
| `data/templates/telematics_daily.template.csv` | Draft | ISO 15143-3-like daily aggregate |
| `data/templates/field_daily_report.schema.json` | Draft | JSON Schema 2020-12, validated as parseable. Role only, no personal data |

## 2. Key decisions proposed
| ID | Decision | Status |
|---|---|---|
| D-054 | Random seed `20270104`. All synthetic files are prefixed `SYNTHETIC_` and carry a comment header | Proposed |
| D-055 | The reconciliation grain is activity × section × work_date × subcontractor, keyed as in `reconciliation_result` | Proposed |
| D-056 | Records are append-only and versioned (`record_version`). Audit events carry before/after hashes | Proposed |
| D-057 | Claim and report lines link to sections spatially (KP intervals), not through a foreign key, so they can be split pro rata | Proposed |

## 3. Assumptions introduced
| ID | Assumption | Validation |
|---|---|---|
| A-054 | Claims are weekly, at activity × KP-range × work-date granularity. Real claims may be monthly or summary-level, which would need disaggregation rules | Anonymised claim sample (Q-004) |
| A-055 | Field reports are made per crew per day, with KP from/to captured | Interview with foremen |
| A-056 | The nominal productivity rates in §4 are plausible for a synthetic 24" spread. They are illustrative and not benchmarks | Field-operations review |

## 4. Open questions
| ID | Question |
|---|---|
| Q-053 | Do subcontractor claims today carry a KP range and a work date, or only period totals? |
| Q-054 | Is there a weld-mapping or QA database export (CSV/API) that can serve as the "LOG" verification source? |
| Q-055 | What is the default X% for AL-05 (proposed 40%)? What is the duplicate-overlap threshold for AL-03 (proposed ≥ 100 m)? |

## 5. Risks proposed
| ID | Risk | L | I | Mitigation |
|---|---|---|---|---|
| R-52 | Real claim granularity is coarser than the model, so line-level reconciliation becomes impossible | 3 | 4 | Disaggregation rules; make KP range and date mandatory in the digital claim form for the pilot |
| R-53 | Synthetic data is "too clean" and overstates detection performance | 3 | 3 | Background noise; degraded flights; report precision; validate on pilot data |

## 6. What the next agent must know
1. Use `anomaly_ground_truth` as the test oracle. Target recall is 1.0 on seeded anomalies.
2. Crew presence is **aggregated only** (D-006). Do not add individual person tracks.
3. JSON Schema cannot enforce `kp_to_m > kp_from_m`. Add that check in application validation.
4. The CSV templates use `;` as the separator inside list cells (`equipment_ids`, `photo_refs`).

## 7. Known weaknesses / not done
- Only the field daily report has a JSON Schema. Schemas for claims, drone measurements and telematics are due in P4.
- The generator is not written yet (P6, after D-005).
- The full data dictionary is due in P4.
