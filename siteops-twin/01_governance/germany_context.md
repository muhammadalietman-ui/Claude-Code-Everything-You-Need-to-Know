# Germany Context: Legal, Commercial and Technical Implications

Owners: research-lead (legal/ethics) and commercial-analyst (contract practice). Version 0.1, 2026-11-23. Trigger: the user confirmed the site jurisdiction is **Germany** (Q-008).

> **Status of this note.** These are planning pointers, not legal advice. Every item marked **VERIFY** must be confirmed with the company's legal counsel, DPO and works council before any real deployment. The demo uses synthetic data only, so none of these items blocks the demo.

## 1. Worker presence sensing: German labour and data-protection law

| Topic | Pointer | Implication for SiteOps Twin | Status |
|---|---|---|---|
| Works council co-determination | **BetrVG §87(1) No. 6**: introducing and using technical devices *suitable* to monitor employee behaviour or performance requires works-council co-determination | Check-in, vehicle GPS of crew buses, badges, cameras and telematics linked to operators all need a **works agreement (Betriebsvereinbarung)** before deployment. Plan it as a P1/P7 deliverable | VERIFY scope |
| GDPR + national employee data protection | GDPR Art. 5, 6, 35 (DPIA), Art. 88; **BDSG §26**. Note: the CJEU's 2023 ruling (C-34/21) cast doubt on the general §26(1) clause as a stand-alone legal basis. Rely on GDPR Art. 6 bases and/or a works agreement | DPIA is mandatory for systematic monitoring. Data minimisation is already designed in (aggregates for commercial users, pseudonymised IDs) | VERIFY |
| Video surveillance | BDSG §4 (publicly accessible areas) and GDPR. Signage and short retention | Count-only, on-device blurring, no audio; ROW is usually not publicly accessible, but road crossings may be | VERIFY |
| Biometrics | GDPR Art. 9 (special category) | Stays **excluded** (T7) | Confirmed in design |
| Subcontractor wage and illegal-employment controls | **MiLoG §13 / AEntG §14** (main-contractor liability for subcontractors' minimum wage); **SchwarzArbG** (identity-document duty in construction) | Strong **commercial and compliance rationale** for verified headcount: AL-09, AL-10 and AL-12 support the contractor's due diligence on subcontractor labour. This strengthens the business case for H5 | VERIFY |
| Drones | EU 2019/947 and 2019/945; German LuftVO | Existing operations; no new flight types (R-13) | Existing |

**[R]** Design response, already implemented in the MVP:
- Commercial users see only crew/front counts.
- Badge IDs are pseudonymised.
- There are no individual tracks and no biometrics.
- Every action is audited.

Add to Phase 1:
- a works-agreement template (purpose limitation, retention, access, evaluation ban on individual performance);
- DPIA screening (T-105).

## 2. Commercial measurement practice in Germany

| Topic | Pointer | Implication | Status |
|---|---|---|---|
| Measurement and billing | **VOB/B §14** (billing; *gemeinsames Aufmaß*, joint measurement) | The joint-measurement evidence pack (S6/S7) maps directly onto the *Aufmaß* practice | VERIFY whether subcontracts use VOB/B |
| Measurement rules per trade | **VOB/C ATV**, e.g. **DIN 18300** (earthworks), each with a section 5 on billing/measurement rules | Contract tolerance and measurement rules (Q-063) come from the ATV and the subcontract. Encode them per activity in `config.py` and the BoQ | VERIFY |
| Electronic quantity calculation | **REB** procedures (e.g. REB-VB 23.003) and the **GAEB DA XML** exchange format (including quantity-determination phases) | Roadmap: export the certified *Aufmaß* in GAEB format for the client and the ERP; the MVP exports CSV | VERIFY phase numbers |
| Site diary | *Bautagebuch* | The daily field report plus weather plus presence can generate the site-diary entry (roadmap) | Practice |

## 3. Technical / pipeline standards (Germany)

| Topic | Pointer | Implication | Status |
|---|---|---|---|
| Gas pipeline construction | **DVGW** rules, e.g. G 463 (steel pipelines > 16 bar) and GW 301 (contractor qualification) | Activity taxonomy, as-built and hydrotest documentation; supports A-014 (weld/QA records as the independent source) | VERIFY applicability |
| Machine guidance | 3D GNSS machine control on excavators is common on German infrastructure sites | A **new independent sensor**: as-built trench depth and length from machine-control logs (T8, see the field-sensing layer §9) | Practice, VERIFY availability |

## 4. Impact on the project
- **H5 is strengthened.** Germany adds a *compliance* driver (MiLoG/AEntG due diligence) to the *commercial* driver for headcount verification.
- **New risks.** R-73: works council does not agree a works agreement in time for the live pilot. R-74: legal basis for employee data is challenged.
- **Thesis contribution (RQ5).** Adoption conditions under German co-determination are a distinctive, under-researched angle.
