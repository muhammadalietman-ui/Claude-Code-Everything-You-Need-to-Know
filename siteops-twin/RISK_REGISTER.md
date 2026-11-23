# RISK_REGISTER

Scoring: Likelihood (L) and Impact (I) are each rated 1–5. Score = L × I. **≥ 15 is red (escalate)**, 8–14 is amber, ≤ 7 is green.

| ID | Risk | Category | L | I | Score | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| R-01 | Pilot spread not available (re-scoped by D-071: reference project first, so lower impact) | Access | 3 | 3 | 9 | Pick the site early (P1). Have a backup spread. Fall back to historical data | project-manager | Open |
| R-02 | Drone volumetric accuracy is insufficient to verify contract quantities | Technical | 3 | 4 | 12 | GCP/RTK protocol; check points; uncertainty budget; use drones as a tolerance test, not as the sole basis for certification | gis-engineer | Open |
| R-03 | Personnel tracking and cameras breach privacy or labour law (GDPR; e.g. Art. 4 of the Italian Workers' Statute if the site is in Italy; local law elsewhere). **Exposure higher after D-069** | Legal/ethical | 3 | 5 | **15** | Crew/zone only; DPIA; consent; worker-representative consultation; legal review; opt-out | research-lead | Open |
| R-04 | Researcher bias: the Commercial Manager evaluates their own process and tool | Validity | 4 | 3 | 12 | Pre-registered metrics; independent QS checks; supervisor audit; report negative results | research-lead | Open |
| R-05 | Subcontractor resistance or refusal to use digital daily reports | Adoption | 3 | 4 | 12 | Early engagement; show the subcontractor's benefit (faster payment); keep paper fallback; contractual clause for future projects | commercial-analyst | Open |
| R-06 | Low field adoption (time burden, gloves, sunlight, connectivity) | Adoption | 3 | 4 | 12 | Form under 5 min; offline-first; foreman champions; field-operations review | ux-designer | Open |
| R-07 | Confidential data leaks into the public repository or publication | Confidentiality | 2 | 5 | 10 | Placeholders; synthetic data; QA grep checks; private repo option; company review before publication | quality-reviewer | Open |
| R-08 | Integration with `[DRONE_SW]` / `[ERP_SYSTEM]` is not possible (no API) | Technical | 3 | 3 | 9 | File-based import in the MVP; APIs in the roadmap | solution-architect | Open |
| R-09 | Too few certification cycles in the pilot for statistical tests of H3 | Validity | 4 | 3 | 12 | Weekly interim agreements as the unit; mixed methods; treat H3 as exploratory | research-lead | Open |
| R-10 | Cybersecurity exposure from new devices and cloud services on the OT/IT network | Security | 2 | 4 | 8 | IEC 62443 / ISO 27001-aligned controls; segregated network; IT approval | solution-architect | Open |
| R-11 | Fabricated or unverifiable references in the SLR | Academic integrity | 2 | 5 | 10 | Verify every DOI; `VERIFY` flag; quality-reviewer check | literature-reviewer | Open |
| R-12 | Student workload conflicts with the day job | Delivery | 4 | 3 | 12 | Timeboxed phases; MVP minimalism; agent delegation | project-manager | Open |
| R-13 | HSE: drone flights or device use near operating equipment create safety exposure | HSE | 2 | 4 | 8 | Use the existing flight permits and procedures; no new flight types; HSE review of pilot devices | field-operations-specialist | Open |
| R-14 | Clocks are not synchronised across sources, so events misalign | Data quality | 3 | 3 | 9 | UTC timestamps; NTP/GNSS time; tolerance windows; data-quality flags | data-engineer | Open |
| R-15 | IPLOCA *Road to Success* is members-only; access through the company may not be possible | Access | 3 | 3 | 9 | Confirm membership (Q-013); use public Novel Construction outputs, Yearbook articles and interviews instead | literature-reviewer | Open |
| R-20 | Loss of POLIMI database access blocks Scopus/WoS | Access | 2 | 4 | 8 | Confirm early (Q-022); fall back to Scholar and interlibrary loan | literature-reviewer | Open |
| R-30 | The as-is differs materially between spreads | Validity | 3 | 3 | 9 | Document variants; choose a representative pilot | process-analyst | Open |
| R-31 | Historical dispute data unavailable or too sensitive | Data access | 3 | 3 | 9 | Prospective baseline; anonymised aggregates | commercial-analyst | Open |
| R-40 | MVP exceeds the P6 window (**closed**: no fixed calendar, D-071; first MVP iteration built) | Delivery | 1 | 3 | 3 | Cut order in `mvp_scope.md` §2; Streamlit fallback (Q-043) | solution-architect | Open |
| R-41 | Offline sync produces duplicate or conflicting records | Data quality | 3 | 3 | 9 | Client UUIDs; append-only versions; data-quality flags | data-engineer | Open |
| R-50 | Time-window activities are missed by the flight timing | Technical | 3 | 3 | 9 | Coordinate flights; as-built survey as witness; KP-linked photos | gis-engineer | Open |
| R-51 | Datum or GCP inconsistency causes systematic volume bias | Technical | 2 | 4 | 8 | Fixed GCP network; RMSE gate | gis-engineer | Open |
| R-52 | Claims are coarser than the model's grain | Data | 3 | 4 | 12 | Disaggregation rules; mandatory KP and date in the pilot claim form | data-engineer | Open |
| R-53 | Synthetic data is too clean and overstates detection performance | Validity | 3 | 3 | 9 | Noise, degraded flights, access-restricted sections; validate on pilot data | data-scientist | Open |
| R-60 | Subcontractors perceive the tolerance rule as one-sided | Adoption | 3 | 3 | 9 | Agree parameters before the pilot; transparent subcontractor view | commercial-analyst | Open |
| R-61 | QS over-relies on platform status | Control | 2 | 4 | 8 | No auto-certification; override with reason; training | commercial-analyst | Open |
| R-70 | Workforce or union resistance to check-in, cameras or badges leads to a stoppage or reputational issue | Labour relations | 3 | 4 | 12 | Consultation before deployment; HSE-led framing; aggregates only; transparency and opt-out for wearables | research-lead | Open |
| R-71 | Camera trailers or trackers are stolen, vandalised or lose power at remote fronts | Technical | 3 | 2 | 6 | Solar plus battery; tamper alerts; insurance; relocatable units | field-operations-specialist | Open |
| R-72 | Subcontractors refuse presence verification without a contract basis | Commercial | 3 | 4 | 12 | Written pilot agreement; clauses in future subcontracts; show faster payment as the benefit | commercial-analyst | Open |
| R-73 | No works agreement (BetrVG §87(1) No. 6) in time for live sensing | Labour relations | 3 | 4 | 12 | Early engagement; template works agreement; aggregates-only design; demo shows the safeguards | research-lead | Open |
| R-74 | Legal basis for employee data challenged (BDSG §26 after CJEU C-34/21) | Legal | 2 | 4 | 8 | GDPR Art. 6 bases + works agreement; DPIA; legal review | research-lead | Open |
| R-75 | Reference-project data is incomplete (no KP on claims, no σ on measurements) | Data | 3 | 3 | 9 | Step-wise intake; UNVERIFIABLE status; disaggregation rules | data-engineer | Open |
| R-76 | Findings from real claims are communicated as accusations before verification, damaging subcontractor relations | Relationship | 2 | 4 | 8 | Platform outputs are queries with evidence, not conclusions; QS confirms before contact | commercial-analyst | Open |
