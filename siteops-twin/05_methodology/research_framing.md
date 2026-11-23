# Research Framing: Questions, Hypotheses, Scope and Success Criteria

Owner: research-lead. Version 0.1 (Phase 0). Status: for user and supervisor review (D-002).

## 1. Problem statement
**[F] From the user brief:**
- Daily production on the pilot contractor's pipeline spreads is recorded manually or semi-manually.
- Subcontractor quantities are tracked separately from survey measurements.
- Personnel, equipment, work fronts and quantities are not integrated.
- Daily UAV photogrammetry already exists, but it is used mainly for site overviews and earthwork volumes. It is not used as an independent source for verifying quantities.

**[A] A-010.** As a result, quantity certification relies on reconciling documents after the fact. This leads to disputes, rework in commercial administration, and payment delays.

## 2. Research questions

**Main RQ.** How can an integrated digital-twin and site-data platform improve the accuracy, traceability and commercial control of daily production and subcontractor quantity certification in oil-and-gas pipeline construction?

| ID | Sub-question | Mainly answered by |
|---|---|---|
| RQ1 | Which pipeline construction quantities can be measured independently from UAV photogrammetry, and with what uncertainty, compared with field reports and subcontractor claims? | Measurability matrix, parallel measurement (P7) |
| RQ2 | What data model and linear-referencing scheme (chainage/KP × date × activity × crew × equipment × subcontractor) is needed to reconcile planned, measured, claimed, certified and invoiced quantities? | Artefact design (P4) |
| RQ3 | How does a visual operational dashboard affect the time and quality of daily production review and of commercial decisions? | Pilot, time-and-motion, SUS (P7) |
| RQ4 | To what extent does automated reconciliation reduce disputes, administrative rework and certification-cycle time? | Baseline vs pilot (P7), business case (P8) |
| RQ5 | What technical, organisational, legal and ethical conditions govern the adoption of personnel and equipment tracking on remote pipeline sites? | SLR, interviews, UTAUT survey |

## 3. Hypotheses and operationalisation

| H | Statement | Dependent variable(s) | Instrument | Comparison | Decision rule [R] |
|---|---|---|---|---|---|
| H1 | Integrating UAV-derived site measurements with structured field-production data reduces discrepancies between subcontractor claims and independently measured quantities. | Absolute % discrepancy \|claimed − measured\| / measured, per activity, per section, per period | Reconciliation engine; parallel survey | Baseline (as-is) vs pilot; Bland–Altman agreement against the reference survey | Median discrepancy falls by 30% or more (Wilcoxon signed-rank, α = 0.05). Report the effect size. |
| H2 | A visual operational dashboard improves the speed and quality of daily production review and commercial decisions. | Review time (min/day); errors found per review; decision latency (h); SUS score | Time-and-motion study, review log, SUS questionnaire | Within-subject: manual vs dashboard review of the same days | Review time falls by 40% or more. Detected errors do not decrease. SUS ≥ 68. |
| H3 | Automated quantity reconciliation reduces invoicing disputes, rework in commercial administration, and payment-cycle delays. | Disputed line items per certificate; resubmissions; days from period end to certificate | Commercial records, certificate log | Baseline vs pilot periods; the historical periods give context | A trend is observed. Treat as exploratory, because the pilot has few billing cycles (L-02). |
| H4 | Personnel, equipment and activity tracking improves visibility of work-front productivity and supports early identification of delays. | Productivity (unit/crew-h); lead time of the delay signal vs the conventional report; % of equipment idle time visible | Telematics, mobile logs, activity sampling | Pilot: alert date vs date of the conventional recognition | Median lead time of 2 days or more on detected slowdowns. Qualitative confirmation from interviews. |

**[A] A-011.** The thresholds above are initial targets for discussion with the supervisor. They are not findings.

## 4. Scope

**In scope:**
- One pipeline spread or work front, onshore and cross-country.
- Activities from ROW clearing to reinstatement.
- Daily UAV outputs from the existing `[DRONE_SW]`.
- Mobile daily reports and subcontractor daily reports.
- Equipment telematics where it is available.
- Personnel tracking at crew or zone level only (A-012).
- The commercial certification workflow up to invoice approval.
- Prototype on synthetic data. Pilot on anonymised data.

**Out of scope for the thesis:**
- Replacing `[DRONE_SW]`.
- Real-time video analytics and computer-vision model training.
- Individual worker biometrics.
- ERP write-back. ERP integration stays read-only or file-based.
- Offshore, facilities and station works.
- Automatic payment execution.
- Contractual or legal determination of disputes.

## 5. Success criteria

| ID | Criterion | Target |
|---|---|---|
| SC1 | Artefact | A working MVP demonstrates end-to-end reconciliation on a synthetic spread, and all MVP acceptance criteria pass |
| SC2 | Evidence | Baseline (≥ 4 weeks) and pilot (≥ 6 weeks) datasets reach ≥ 90% completeness |
| SC3 | H1–H4 | Each hypothesis is evaluated against its pre-registered decision rule, with results reported whether they are positive or negative |
| SC4 | Users | SUS ≥ 68, and at least 70% of pilot users say they would keep using it |
| SC5 | Business | The risk-adjusted NPV is positive under base assumptions, and payback is under 24 months at spread scale |
| SC6 | Academic | Thesis approved; one conference paper submitted (ISARC, CIB W78 or EC3) |
| SC7 | Compliance | No confidentiality or privacy incident; consent obtained where required |

## 6. Expected contributions
- **Theory:**
  - A measurability-aware reconciliation framework for linear infrastructure, linking UAV uncertainty to contractual tolerance.
  - Evidence on digital-twin value in commercial (not only technical) control.
- **Practice:**
  - A reusable data model and control matrix for subcontractor quantity certification.
  - An MVP and an adoption playbook for pipeline contractors.
