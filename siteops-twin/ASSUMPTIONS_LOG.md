# ASSUMPTIONS_LOG

Every statement tagged **[A]** in any deliverable must have an entry here. Validation status: **Open**, **Validated**, **Invalidated** (then a decision follows).

| ID | Assumption | Source / basis | Impact if wrong | Validation method | Owner | Due | Status |
|---|---|---|---|---|---|---|---|
| A-001 | Project duration is about 40 weeks, ending with thesis submission around Sep 2027 | Typical POLIMI MSc thesis timeline | Re-plan P6–P9 | Check the graduation calendar with the supervisor | project-manager | P1 | Open |
| A-002 | The student can commit about 15–20 h/week | Part-time alongside the job | Scope reduction | Confirm with the user | project-manager | P0 | Open |
| A-003 | One spread/work front is available for 10 weeks (4 baseline + 6 pilot) in Q2 2027 | User brief, plus the construction schedule | Pilot not possible. Fall back to retrospective/historical evaluation | Company confirmation | project-manager | P1 | Open |
| A-004 | Drone flights happen daily over the active ROW, with RTK/PPK or GCPs | User brief (daily flights). Accuracy method not stated | Volumetric uncertainty too high for certification | Survey-team interview; accuracy report | gis-engineer | P3 | Open |
| A-005 | `[DRONE_SW]` can export orthophotos (GeoTIFF), DSM/DTM, point clouds (LAS/LAZ) and volume reports (CSV/PDF) | Common photogrammetry capability | Manual export or API work needed | Vendor documentation | gis-engineer | P3 | Open |
| A-006 | A pipeline alignment centreline with KP stationing exists in digital form (CAD/GIS/LandXML) | Standard pipeline engineering deliverable | Must digitise the centreline | Engineering document register | gis-engineer | P3 | Open |
| A-007 | Subcontracts are measured on unit rates against a BoQ (e.g. m of trench, m³ of excavation/backfill, joints welded, m² reinstated) | Common practice for pipeline subcontracts | Reconciliation logic changes (e.g. lump sum by milestones) | Review an anonymised subcontract | commercial-analyst | P3 | Open |
| A-008 | Some equipment has OEM telematics (ISO 15143-3 / AEMP 2.0 API) or GPS trackers | Common on modern fleets | Equipment tracking limited to mobile check-in/out | Fleet survey | data-engineer | P3 | Open |
| A-009 | Cellular connectivity is intermittent along the ROW, with a site office link (VSAT/4G) | Remote-site norm | Sync design changes | Field-operations survey | field-operations-specialist | P3 | Open |
| A-010 | Post-hoc document reconciliation causes disputes and payment delays | User brief (stated pain) | Weakens the motivation for H3 | Baseline KPI data | process-analyst | P3 | Open |
| A-011 | The H1–H4 thresholds are reasonable targets | Researcher judgement | Decision rules need revision | Supervisor review; literature | research-lead | P5 | Open |
| A-012 | Crew/zone-level tracking is legally and ethically acceptable with consent and worker-representative consultation | GDPR principles; labour-law caution | Remove personnel tracking from the pilot | Legal/HR/DPO review in the site jurisdiction | research-lead | P1 | Open |
| A-013 | Activities happening below ground (lowering-in, padding) are observable only in a time window. Daily flights may miss them | Pipeline construction sequence | Those quantities rely on field records plus photo evidence | Flight-timing analysis in the pilot | gis-engineer | P4 | Open |
| A-014 | Weld counts and NDT results come from the welding/QA database, not from drones | Industry practice | none | Confirm with QA/QC | data-engineer | P3 | Open |
| A-015 | The certification period is monthly, with interim weekly or daily quantity agreement possible | Common practice | Fewer cycles than expected, so H3 has low power | Commercial records | commercial-analyst | P3 | Open |
| A-016 | Spread crews advance at different rates, with km-scale gaps. The activity order varies by terrain and method | Practice (to be checked against IPLOCA IP-01) | AL-08 false positives | IP-01 extract; spread plan | field-operations-specialist | P3 | Open |
| A-020 | A second screener is available for about 6–8 h | SLR practice | κ cannot be computed | Supervisor | literature-reviewer | P2 | Open |
| A-021 | No meta-analysis; narrative and thematic synthesis | Heterogeneous outcomes | Method change | Pilot screening | literature-reviewer | P2 | Open |
| A-022 | The `API*` term may retrieve American Petroleum Institute noise | O&G terminology | Higher screening load | String pilot | literature-reviewer | P2 | Open |
| A-030 | The generic as-is process (AS-01 to AS-26) represents current practice | Typical practice; user brief | Map and baseline invalid | 6–10 interviews | process-analyst | P3 | Open |
| A-031 | Step durations are representative | Practitioner judgement | Wrong baseline expectation | Time-and-motion | process-analyst | P7 | Open |
| A-032 | Quantities are re-keyed 3–4 times from foreman sheet to ERP | Typical practice | PP-07 overstated | Trace 10 quantities | process-analyst | P3 | Open |
| A-033 | Joint measurement happens per claim (weekly or monthly), not daily | Typical practice | Different dispute mechanism | QS interview | commercial-analyst | P3 | Open |
| A-034 | Reports use landmarks or "corners" rather than consistent KP values | User brief | DB-01 less severe | Sample of 20 DPRs | process-analyst | P3 | Open |
| A-040 | MVP activity tracking is event-level, not minute-level | Feasibility | Objective 3 partly met | User (D-005 C2) | solution-architect | P4 | Open |
| A-041 | Generic formats plus vendor adapters cover `[DRONE_SW]` exports | Common outputs | Adapter effort | Vendor documents (Q-005) | solution-architect | P3 | Open |
| A-042 | MVP effort is about 14–18 developer-weeks | T-shirt estimate | P6 slip | Re-estimate in P4 | solution-architect | P4 | Open |
| A-043 | AL-05 default = drop of 25% or more vs the 5-day rolling median | Judgement | Alert noise | Calibrate on synthetic, then pilot data | data-scientist | P6 | Open |
| A-050 | Default tolerances: 3% for volume, 1% for length (until Q-007 is answered) | Placeholder | Wrong statuses | Contract | commercial-analyst | P4 | Open |
| A-051 | UAV vertical RMSE about 3–5 cm with RTK/PPK; GSD ≤ 3 cm | Typical survey practice | H1 coverage | Accuracy reports | gis-engineer | P3 | Open |
| A-052 | At least 5 check points per flight block | Survey practice | Uncertainty unknown | Survey team | gis-engineer | P3 | Open |
| A-053 | Spoil can be masked for trench volume | Method | TRN volume unverifiable | Pilot trial | gis-engineer | P7 | Open |
| A-054 | Claims are weekly at activity × KP × date grain | Spec | Disaggregation needed | Claim sample (Q-053) | data-engineer | P3 | Open |
| A-055 | One field report per crew per day, with KP from/to | Spec | Model change | Foreman interviews | data-engineer | P3 | Open |
| A-056 | Synthetic productivity rates are illustrative only | Spec | none (not benchmarks) | Field-operations review | data-engineer | P6 | Open |
| A-060 | Story points are relative (MVP ≈ 127 points) | Planning | Re-plan | P4 re-estimate | ux-designer | P4 | Open |
| A-061 | Sync rule: server wins on approved records; device edits on pending records become new versions | Design | Data conflicts | SM review | ux-designer | P4 | Open |
| A-062 | Foremen have a GPS phone or tablet with camera and report at shift end | Practice | Device budget | Field survey | ux-designer | P3 | Open |
| A-063 | Survey reports U at 95% per section and activity | Design | Status rule cannot run | Survey (Q-005, Q-007) | gis-engineer | P4 | Open |
| A-064 | QA/QC records are the independent source for welds and coating | Practice; API 1104 context | Weld verification gap | QA/QC (A-014) | commercial-analyst | P3 | Open |
| A-065 | Unit-rate valuation is enough for the certificate draft | Practice | Valuation logic | Subcontract review (Q-004) | commercial-analyst | P3 | Open |
| A-070 | Inflated manpower and equipment claims, ghost or double-counted workers, and unverifiable fragmented fronts are material practice problems | User statement (2026-11-23) | Weakens H5 motivation | P3 interviews; audit of anonymised timesheets vs attendance | process-analyst | P3 | Open |
| A-071 | E11 adds about 3–4 developer-weeks to the MVP | Estimate | P6 slip (R-40) | P4 re-estimate | solution-architect | P4 | Open |
| A-072 | Some subcontract payments depend on time and resources (daywork, standby, equipment hire, reimbursable manhours) | Practice | E11 value lower if all payments are unit-rate | Subcontract review (Q-004) | commercial-analyst | P3 | Open |
