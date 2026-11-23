# Handover: P0 / gis-engineer → data-engineer, solution-architect, commercial-analyst, field-operations-specialist

- **Date:** 2026-11-23
- **Task / backlog IDs:** T-006

## 1. What was produced
| File | Status | Notes |
|---|---|---|
| `04_to_be_architecture/geospatial/quantity_measurability_matrix.md` | Draft | 20+ activities classified (Yes / Partial / Time-window / No). Also contains the linear-referencing spec, the volume and uncertainty method, and the layer catalogue |

## 2. Key decisions proposed (for DECISIONS_LOG)
| ID | Decision | Status |
|---|---|---|
| D-050 | Reconciliation bands: MATCHED if \|diff\| ≤ 0.5·band; WITHIN_TOLERANCE if ≤ band; band = max(T·Q_measured, 2·σQ) | Proposed |
| D-051 | Report the correlated-error volume uncertainty (σV ≈ A·σΔz) as the default. The uncorrelated estimate is shown only as a lower bound | Proposed |
| D-052 | UAV verification in the MVP is limited to CLR, GRD (length/area), STR, TRN (length), LOW (time-window), BKF (length), RST. WLD, NDT, FJC, HDD, tie-ins and HYD are verified against logs or records | Proposed |
| D-053 | Sections are half-open KP intervals. Quantities that span sections are split pro rata by KP overlap | Proposed |

## 3. Assumptions introduced (for ASSUMPTIONS_LOG)
| ID | Assumption | Validation |
|---|---|---|
| A-050 | Default contract tolerances: 3% for volume, 1% for length, until Q-007 is answered | Commercial / survey |
| A-051 | UAV vertical RMSE is about 3–5 cm with RTK/PPK and check points; GSD ≤ 3 cm | Survey-team accuracy reports |
| A-052 | ≥ 5 independent check points per flight block are available or feasible | Survey team |
| A-053 | The spoil pile can be masked or captured separately for trench volume | Pilot trial |

## 4. Open questions (for OPEN_QUESTIONS)
| ID | Question | Blocking |
|---|---|---|
| Q-050 | At what time of day are flights usually made? Can a flight be scheduled to capture open trench and lowered pipe before backfill (time-window activities)? | No (but affects H1 coverage) |
| Q-051 | Which CRS, vertical datum and geoid does the project use (`[CRS_EPSG]`, `[VDATUM]`)? | P4 |
| Q-052 | Are chainage equations or reroutes already present on the alignment? | P4 |

## 5. Risks proposed (for RISK_REGISTER)
| ID | Risk | L | I | Mitigation |
|---|---|---|---|---|
| R-50 | Time-window activities (LOW, PAD, TRN volume) are missed by the daily flight timing, so H1 coverage drops | 3 | 3 | Coordinate flight timing; supplement with photo evidence linked to KP |
| R-51 | A datum or GCP inconsistency between flights introduces a systematic volume bias | 2 | 4 | A fixed GCP network; check-point RMSE gate before a measurement is accepted (quality_flag) |

## 6. What the next agent must know
1. Drone data is a **tolerance check**, not the contractual measurement basis.
2. Weld counts are **not** measurable from UAV. Use the weld log.
3. DSM differencing gives the **net** volume change. Spoil and water must be masked.
4. KP is a label. Measured length is along the as-built geometry. They differ across chainage equations.

## 7. Known weaknesses / not done
- No real accuracy data yet.
- 3D Tiles and point-cloud serving are deferred to the roadmap.
- Rock classification and padding volume are not addressed in the MVP.
