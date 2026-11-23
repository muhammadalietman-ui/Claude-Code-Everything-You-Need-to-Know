# RISK_REGISTER

Scoring: Likelihood (L) and Impact (I) are each rated 1–5. Score = L × I. **≥ 15 is red (escalate)**, 8–14 is amber, ≤ 7 is green.

| ID | Risk | Category | L | I | Score | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| R-01 | Pilot spread not available in the research window (schedule slip, demobilisation) | Access | 3 | 5 | **15** | Pick the site early (P1). Have a backup spread. Fall back to historical data | project-manager | Open |
| R-02 | Drone volumetric accuracy is insufficient to verify contract quantities | Technical | 3 | 4 | 12 | GCP/RTK protocol; check points; uncertainty budget; use drones as a tolerance test, not as the sole basis for certification | gis-engineer | Open |
| R-03 | Personnel tracking breaches privacy or labour law (GDPR; e.g. Art. 4 of the Italian Workers' Statute if the site is in Italy; local law elsewhere) | Legal/ethical | 3 | 5 | **15** | Crew/zone only; DPIA; consent; worker-representative consultation; legal review; opt-out | research-lead | Open |
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
