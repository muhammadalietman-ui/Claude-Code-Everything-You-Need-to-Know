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
