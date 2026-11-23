# SiteOps Twin: Executive Brief

**A digital twin for commercial control of pipeline construction production.** Master's research project with Politecnico di Milano. `[PROJECT_CODE]` · v0.1 · November 2026 · Confidential: internal and academic use

---

**The problem.**
- Our daily drone flights already produce accurate orthophotos and earthwork volumes, but this data is not used to verify what subcontractors claim.
- Production is recorded in manual daily reports.
- Subcontractor quantities are tracked separately.
- Crews, equipment and work fronts are not visible in one view.
- As a result, quantities are reconciled after the fact, at invoice time. That is where disputes, overpayment risk and payment delays arise. *(Assumption, to be measured in the baseline.)*

**The proposal.** SiteOps Twin is a lightweight platform that sits on top of the existing drone workflow, not in place of it.

The drone is a once-a-day snapshot of physical progress. It cannot verify **manpower, equipment hours or activity at scattered fronts**, so the platform adds a **structured field-sensing layer**:
- muster check-in at each front;
- GPS on crew buses, vehicles and hired plant;
- equipment telematics;
- count-only AI cameras at key fronts;
- optional HSE-led badges.

Commercial users see crew- and front-level counts and hours. They never see individual tracks. It links every quantity to:
- **where** it was done (chainage/KP section)
- **when** it was done
- **who** did it (crew, subcontractor)
- **with what** equipment
- **what evidence** supports it (drone measurement, photos, records)

For every activity and section, it compares six quantity states: **Planned → Reported → Measured → Claimed → Certified → Invoiced**. It flags exceptions automatically:
- claims above the measured quantity or the BoQ
- duplicate or overlapping chainage claims
- missing reports
- out-of-sequence progress
- productivity drops
- claimed headcount or equipment hours above what was sensed
- workers checked in at two fronts at the same time
- fronts reported active with no presence recorded

**Research question.** How can an integrated digital twin improve the accuracy, traceability and commercial control of daily production and subcontractor quantity certification?

| Hypothesis | Target tested in the pilot |
|---|---|
| H1 Drone and field data integration reduces claim-vs-measured discrepancy | −30% median discrepancy |
| H2 A visual dashboard speeds up production review | −40% review time, SUS ≥ 68 |
| H3 Automated reconciliation reduces disputes and certification delays | Exploratory trend |
| H4 Crew/equipment tracking gives earlier warning of delays | ≥ 2 days' earlier warning |
| H5 *(proposed)* Presence sensing reduces claimed vs verified manpower and equipment hours | −30% median discrepancy |

**Method.**
- Design is **grounded in industry practice**, with **IPLOCA** (*Onshore Pipelines: The Road to Success*, Novel Construction Initiative) as the primary practitioner reference.
- Design Science Research with an embedded action-research pilot on **one spread**: a 4-week baseline using the current workflow, then a 6-week pilot with parallel measurement.
- The prototype is built and demonstrated on **synthetic data**.
- Personnel sensing follows a DPIA and the applicable labour-law route, such as worker-representative agreement. There is **no facial recognition or biometrics**.

**MVP scope (proposed, for confirmation).**
- Chainage section model
- Offline mobile daily report
- Subcontractor claim import
- Drone measurement import, with uncertainty
- Work-front presence sensing
- Reconciliation engine and 13 alert rules
- Commercial dashboard and subcontractor scorecard
- QS certification with an audit trail

ERP integration, 3D viewer, badges/RFID, computer vision and ML forecasting are on the roadmap, not in the MVP.

**Expected value.**
- Fewer overpayments and disputes
- Faster certification and better cash flow
- A defensible audit trail for claims
- Earlier visibility of slowdowns

A full risk-adjusted business case (ROI, NPV, payback) will be built from the pilot data.

**Timeline (indicative).**
| Period | Work |
|---|---|
| Dec 2026 – Jan 2027 | Governance, ethics, pilot-site selection |
| Dec 2026 – Mar 2027 | Literature review and process analysis |
| Mar 2027 | MVP scope frozen |
| Mar – May 2027 | Prototype |
| May – Jul 2027 | Field pilot |
| Sep 2027 | Thesis submission |

**Decisions requested from management.**
1. Nominate a pilot spread and a backup.
2. Nominate a company sponsor who is independent of the researcher.
3. Approve use of anonymised drone, daily-report and certification records for research.
4. Choose which sensing tiers to pilot, and engage HR, Legal and the DPO on the consent and DPIA route.
5. Confirm IPLOCA membership, for access to *The Road to Success*.

**Requested from POLIMI.**
1. Confirm the supervisor, the methodology framing and the thesis calendar.
2. Advise whether ethics committee review is required.

*Safeguards: no company, client, personnel or location identifiers appear in any academic output. Publications are subject to company review.*
