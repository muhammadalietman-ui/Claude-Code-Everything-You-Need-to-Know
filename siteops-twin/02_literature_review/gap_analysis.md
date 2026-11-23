# Gap Analysis: Testing Candidate Gaps G1–G6 (Phase 2, provisional)

Owner: literature-reviewer (AI-assisted). Date: 2026-11-23. Inputs: `gap_hypotheses.md`, `synthesis.md` and `reference_matrix.csv`, plus the corpus counts in `search_runs/gap_stats.json`, produced by `gap_stats.py`.

**Evidence levels used:**
- **(a) Pool counts.** Keyword counts over the title and abstract of all 1,854 records that passed Stage 1. These are indicative only: 16.5% of the records have no abstract, and keyword matches include incidental mentions.
- **(b) Core counts.** Counts from the 120 abstract-coded core records.
- **(c) Qualitative reading** of the verified core studies.

**Verdict scale:** *Supported* (the gap is confirmed), *Partially supported*, *Refuted*. All verdicts are provisional until full-text Stage 2 and snowballing are done.

---

## Summary table

| Gap | Verdict | Key counts | Maps to |
|---|---|---|---|
| G1 Commercial blind spot of construction DTs | **Supported** | Pool: 292 DT records. 178 (61%) contain technical-state terms (progress, schedule, geometry, safety, quality, monitoring). 21 (7.2%) mention payment, invoice, subcontract or valuation anywhere. Manual title check: only **3** have payment or contract administration as the DT's object. Core: 23 C1-flagged records, of which **2** have a payment outcome (Wu & Li, 2025; Shehadeh, 2025) | Main RQ, RQ4, H3 |
| G2 Linear and pipeline under-representation | **Supported** | Pool: 334 linear-context records (18.0%), but only **39 (2.1%)** with explicit pipeline-construction context. Of these, 18 address progress, quantity, productivity, as-built or volume, and **6** combine pipelines with DT. Core (purposively enriched): 36 of 120 linear, 16 pipeline. Khan et al. (2026a) independently state that the automation literature is building-centred | RQ1, RQ2 |
| G3 Uncertainty-to-contract gap | **Supported** | Pool: 118 UAV/photogrammetry records report accuracy or error terms. 10 also mention payment, contract, certification or tolerance. **0** verified records derive an acceptance or tolerance rule from measurement uncertainty. Closest: Julge et al. (2019), who check against a road-administration requirement, and Mohd Safie et al. (2018), who compare claimed and measured values | RQ1, H1 |
| G4 Missing linear-referenced commercial data model | **Supported** | Pool: 527 schema, ontology or IFC records. 39 (7.4%) contain commercial terms (payment, invoice, subcontract, BoQ). **14** combine schema, linear context and quantity or commercial terms; all are QTO, estimating, design or maintenance. **0** model multi-state quantities (reported, measured, claimed, certified, invoiced) against chainage | RQ2 |
| G5 Ethics and practicality of tracking on remote linear sites | **Supported** (practicality); **Partially supported** (ethics) | Pool: 426 tracking records. 82 (19.2%) privacy, ethics or trust terms. 39 linear. 30 remote, connectivity or "km" terms. **5** pipeline. **1** mentions a duration of 4 weeks or more. Ethics is covered by a recognisable stream (≥ 7 core studies), so it is not absent, but it is not linked to linear or remote contexts | RQ5, H4, H5 |
| G6 Weak evidence of commercial outcomes | **Supported** | Pool: 918 C5/C6-type records. 36 (3.9%) with comparative or baseline design terms. 189 mention commercial outcome terms (dispute, payment delay, administrative, rework, claim). Only **1** keyword hit for both, and it is a legal case study. Core: 3 studies with quantitative outcome comparisons: Radman et al. (2025), 4 vs 4 cases on EVM and decision delay; Wu & Li (2025), a prototype; Shehadeh (2025), one project with −30% disputes and +25% payment timeliness | H2, H3 |

---

## G1. Commercial blind spot

**Evidence.**
- **Reviews.** The major DT reviews organise the field around design, planning and management, asset management, safety, energy, quality, logistics and structural health monitoring (Omrany et al., 2023). Technology gaps are framed as data transmission and interoperability (Tuhaise et al., 2023). Neither review names quantity certification or subcontract payment as an application area.
- **Conceptual models.** The DT is framed around production control (Sacks et al., 2020) and semantic lifecycle information (Boje et al., 2020). It is not framed around commercial reconciliation.
- **Where payment appears.** Payment automation is a separate stream built on blockchain and smart contracts (Das et al., 2020; Hamledari & Fischer, 2021b; Ahmadisheykhsarmast & Sonmez, 2020). It treats the measurement that triggers payment as an external oracle.
- **The two DT-payment intersections** (Wu & Li, 2025; Shehadeh, 2025) are recent single-project building studies on milestone payments or cost allocation.

**Verdict: Supported.** About 1% of the DT pool (3 of 292) treats payment or contract administration as the DT's object. In the core, 2 of 23 C1 records (9%) report a payment outcome.

**Refinement.** The blind spot is not that commercial use is unimagined. It is that commercial use is **delegated to payment-execution technology (blockchain) without a measurement and reconciliation layer**. This sharpens the SiteOps contribution: the reconciliation layer *between* measurement and payment.

## G2. Linear and pipeline under-representation

**Evidence.**
- **Distribution.** Linear contexts make up about 18% of the pool, mostly roads, highways and rail. Pipeline construction accounts for about 2% (39 records).
- **Character of the pipeline construction records.** They are mostly:
  - geotechnical or practice papers;
  - GIS routing;
  - learning-curve or simulation studies (Ammar & Samy, 2015; Kuppusamy & Ramar, 2011);
  - early, exploratory technology studies (Khan et al., 2026b; Hlady et al., 2020; Yu et al., 2026).
- **Pipeline DTs** are predominantly operational (Bo et al., 2020; Sarvesh et al., 2024). The exception is a single construction-phase DT-simulation model (Abdelhamid et al., 2025).
- **Independent confirmation.** Khan et al. (2026a) state that a review focused on progress monitoring in pipeline construction had been lacking, because automation reviews concentrate on buildings.
- **The protocol's exclusion EX2** removed 25 operations-only records. Before limits, the SUP-PIPE string returned 3,645 hits, dominated by integrity and operation topics.

**Verdict: Supported.**

**Refinement.** Roads and highways provide the nearest transferable evidence for UAV volumetrics and linear progress (Julge et al., 2019; Lo et al., 2022; Vick & Brilakis, 2018; Kim & Chi, 2020). Two properties of pipeline spreads are unstudied: the **moving, sequenced work fronts** (front-end, mainline and back-end crews over kilometres) and **chainage-dependent productivity** (Chauhan & Bansal, 2026 is the only verified exception).

## G3. Uncertainty-to-contract gap

**Evidence.**
- **Accuracy is reported, but stops at the validation statistic.** Typical figures: vertical RMSE of 0.10 m (Hugenholtz et al., 2015), geometry RMSE under 2.8 cm (Varbla et al., 2020), 5.7 cm height accuracy (Julge et al., 2019), 94–96% volume accuracy (Kang et al., 2024). These numbers are not propagated to a quantity-acceptance decision.
- **Only partial links to an external standard or document exist:**
  - a road-administration volume requirement (Julge et al., 2019);
  - a haul ticket (Hugenholtz et al., 2015);
  - contractor-claimed as-built values (Mohd Safie et al., 2018).
- **Payment-automation studies assume the progress evidence is correct.** Examples: scan-to-BIM as the oracle (Elsharkawi et al., 2025) and drone point clouds for valuation (Fobiri et al., 2025). They do not attach an uncertainty to the triggering quantity.
- **Data-quality studies stop at acquisition planning.** Examples: scan-planning quality (Zhang et al., 2016) and point-cloud quality requirements *(title-level)* (Rebolj et al., 2017).

**Verdict: Supported.** There are 0 verified studies that translate measurement uncertainty into a contractual tolerance or acceptance rule.

**Implication.** This confirms the core contribution claim in `research_framing.md` §6: a measurability-aware reconciliation framework that links UAV uncertainty to contractual tolerance. Together with G1, G3 forms the central gap.

## G4. Missing linear-referenced commercial data model

**Evidence.**
- **Schema work** concentrates on:
  - IFC/ifcOWL semantics (Pauwels & Terkaj, 2016);
  - exchange validation (Lee et al., 2020);
  - alignment geometry (Soilán et al., 2020; Garramone & Scaioni, 2022);
  - georeferencing (Uggla & Horemuz, 2018);
  - BIM-GIS integration for pipeline asset management (Demir & Yomralioglu, 2024).
- **The closest commercial-quantity work:**
  - IFC quantity sets for road estimating (Won et al., 2019);
  - automated QTO to a specification of work, reproducible for 40% of cost items (Fürstenberg et al., 2024);
  - BIM–BoQ synchronisation for an audit trail (Chong et al., 2024);
  - a construction-phase DT process schema (Schlenger et al., 2022).
- **No verified record covers** PODS, LandXML or ISO 15143-3 in construction-phase quantity reconciliation.

**Verdict: Supported.** No model represents planned, reported, measured, claimed, certified and invoiced quantity states keyed by KP × date × activity × crew × equipment × subcontractor.

**New refinement (G4a).** Fürstenberg et al. (2024) and Chong et al. (2024) show that **differences in measurement rules and cost breakdown structures** between parties are a root cause of quantity variance. The data model therefore needs an explicit mapping from measured geometry to *contractual measurement rules*, i.e. the rule of measurement per pay item. Geometry alone is not enough.

## G5. Ethics and practicality of tracking on remote linear sites

**Evidence: practicality.**
- Tracking validations are short and compact, often indoors:
  - BLE testbeds (Gong et al., 2025);
  - a WiFi case in a metro station (Woo et al., 2011);
  - RFID in an LNG training centre (Wu et al., 2019).
- Equipment tracking on earthworks is better developed (Lee et al., 2018; Pradhananga & Teizer, 2013; Kim & Chi, 2020). Even there, validation is site-bounded.
- Only 1 pool record mentions a tracking duration of 4 weeks or more. Only 5 combine tracking with a pipeline context.
- Connectivity is named as an enabler (Turner et al., 2021) but not studied for kilometres of ROW.

**Evidence: ethics.**
- A substantive stream exists: legal, ethical and behavioural concerns (Wu et al., 2023), acceptance surveys (Fugate & Alzraiee, 2023; Häikiö et al., 2020; Yang et al., 2025), and an ethics-by-design framework (Weber-Lewerenz, 2021).
- The stream is mostly about safety-motivated monitoring on building sites.
- **No verified study** examines tracking used for *commercial verification* of claimed manpower or equipment hours. That use raises distinct labour-relations issues.

**Verdict:**
- **Practicality: Supported.**
- **Ethics: Partially supported.** The literature is not thin, but it is not linked to commercial uses or remote linear contexts.

## G6. Weak evidence of commercial outcomes

**Evidence.**
- Most C5/C6 studies evaluate technical accuracy or perception (e.g. Alizadehsalehi & Yitmen, 2021; Zhang et al., 2022).
- **Quantitative comparative outcome evidence is rare:**
  - Kim et al. (2011): sensor productivity vs daily logs and pay estimates, no significant difference;
  - Radman et al. (2025): 4 vs 4 projects, EVM/ESM and decision delays;
  - Wu & Li (2025): prototype, verification-to-payment time;
  - Shehadeh (2025): one project, −30% disputes and +25% payment timeliness.
- **Baseline data on the problem exist** (Bolton et al., 2022: 77% of subcontracts with late payment). They are not paired with an intervention.

**Verdict: Supported.** No verified study measures the effect on **disputed line items, resubmissions or certification-cycle days** with a baseline/pilot design on re-measured quantities.

**Implication.** The H3 design (baseline vs pilot, exploratory) addresses a real gap. Its exploratory framing is consistent with the absence of benchmark effect sizes.

---

## New gaps identified

| ID | New gap | Evidence | Maps to |
|---|---|---|---|
| G7 | **Multi-source triangulation with field reports is rare.** Shahi et al. (2015) and Kim et al. (2011) fuse or compare sensor data with foreman reports and pay estimates. Most studies replace the human report instead of reconciling with it. The as-is commercial ritual (joint measurement, weekly meetings) is not modelled | `industry_practice_sources.md` rules 2–4 | RQ2, RQ3, H1 |
| G8 | **No usability or decision-time evidence for production dashboards.** No verified record reports SUS, review time or error detection for construction production or commercial dashboards. DT studies report perceived benefits only | C1, C5 core | RQ3, H2 |
| G9 | **Claimed vs verified presence (H5) is unstudied.** The tracking literature measures localisation accuracy and acceptance. None compares subcontractor-claimed headcount-days or equipment-hours with sensor-verified values. Workforce verification appears only incidentally, e.g. hiring-mandate monitoring in a record whose DOI could not be verified | C4 core | RQ5, H5 |
| G10 | **Accuracy and frequency trade-off for daily control.** Navon et al. (2012) show that GPS-derived control information improves when averaged over days and is economical at sub-biweekly frequency. No study optimises survey frequency against certification-period needs | C2, C5 | RQ1, RQ4 |

## Implications for the contribution claim

**Central gap.** G1 and G3 are both supported, so the central gap is confirmed: *a measurability-aware reconciliation layer between independent site measurement and commercial certification, for linear projects*. G2, G4 and G4a supply the context and the artefact requirement: a linear-referenced, multi-state data model with measurement-rule mapping. G5, G6 and G9 justify the evaluation design (H3–H5) and the governance moderators in the framework.

**Caveats.**
- All verdicts rest on open-source, abstract-level evidence.
- Two counts in particular must be re-checked after full-text screening and Scopus/WoS searches, if access is obtained: G1's 3/292 and G3's 0 tolerance-rule studies.
- Two candidate counter-examples need full-text checking: the high-relevance record with no DOI on UAV pipeline-corridor surveys versus RTK, and the unverified BIM + photogrammetry quantity-verification record (Zenodo). Both are listed in `reference_matrix.csv` with verified_doi = N.
