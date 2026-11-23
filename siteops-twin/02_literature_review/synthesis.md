# Literature Synthesis: Clusters C1–C9 and Cross-Cluster Analysis (Phase 2, provisional)

Owner: literature-reviewer (AI-assisted). Date: 2026-11-23. Basis: the 114 Crossref-verified records of the core set (`reference_matrix.csv`, `verified_doi = Y`). The cluster coding and the provisional quality bands come from that file.

> **Status and limits of this text.**
> - It synthesises **abstract-level** evidence from open databases (OpenAlex, with Semantic Scholar abstract enrichment).
> - Stage-2 full-text screening, quality appraisal and snowballing are **pending** (see `prisma_flow.md`).
> - Where an abstract was unavailable, the statement is marked *(title-level)*. Where only a machine summary was available, it is marked *(TLDR)*.
> - Six core records whose DOI could not be verified are **not cited** here.
> - Numerical results are quoted as reported in the abstracts. They have not been re-derived and are not comparable across studies without full-text checks of the reference method, site scale and error metric.
> - Citations follow APA 7 in-text style. Same-author, same-year works are distinguished as listed in `references.bib` (Hamledari & Fischer, 2021a/2021b; Khan et al., 2026a/2026b).

---

## 1. Overview of the evidence base

The core set contains 120 records, of which 114 are verified.
- **Clusters.** It covers all nine clusters, with the heaviest multi-coded presence in progress, quantity and payment (C6, 44 flags), UAV photogrammetry (C2, 35) and tracking (C4, 35). Interoperability (C7, 21) and adoption (C9, 20) are thinner.
- **Context.** Thirty-six core records concern linear projects (pipeline, road, highway, rail). Sixteen concern oil-and-gas or other pipelines. The wider Stage-1 pool (n = 1,854) shows the same imbalance more sharply: only 39 records carry an explicit pipeline-construction context (`gap_stats.json`).
- **Methods.** Engineering studies are dominated by method development with laboratory or single-site validation. Management studies are dominated by questionnaire surveys with structural-equation or ranking analyses. Reviews are frequent in the digital-twin and adoption literature. Designs that compare a baseline with an intervention on commercial outcomes are rare (see `gap_analysis.md`, G6).

---

## 2. Cluster syntheses

### C1. Digital twins in construction and oil & gas

**State of the art.**
- The construction digital twin (DT) is still a contested concept.
- Boje et al. (2020) frame it as a semantic, socio-technical extension of BIM. On their view the DT needs sensor-data management and semantic models beyond what BIM schemas provide.
- Sacks et al. (2020) define *digital twin construction* (DTC) as a closed-loop production-control system. It is built on BIM, lean production control, automated site data acquisition and AI, and articulated through four core information and control concepts.
- Akanmu et al. (2021) distinguish as-planned and as-built replicas. They argue that cyber-physical systems are a precondition for real-time control.
- Zhang et al. (2022) operationalise a construction-site DT by extending BIM levels of detail with IoT data. Their validation consists of questionnaires and interviews.
- Schlenger et al. (2022) argue *against* schema-less DTs. They propose a process-oriented UML data schema for the construction phase, with an ontology mapping.

**Key themes.** Four systematic reviews describe a field that is growing but immature.
- Opoku et al. (2021) characterise DT use in construction as nascent.
- Tuhaise et al. (2023) find that data transmission, interoperability, integration and visualisation are the main technology gaps.
- Omrany et al. (2023) analyse 145 publications. They identify eight application areas: virtual design, planning and management, asset management, safety, energy, quality, supply chain/logistics and structural health monitoring. The leading challenges are data integration and interoperability, data accuracy and completeness, privacy and security, and standards and governance.
- Commercial control (quantity certification, payment, subcontract administration) is **not one of the eight areas** that Omrany et al. (2023) identify.
- Alizadehsalehi and Yitmen (2021) propose a DT-based progress-monitoring framework from reality capture to extended reality. They validate it through practitioners' perceptions (SEM), not through measured performance.
- Greif et al. (2020) show that even a "lightweight" logistics DT (silo fill levels) creates informational, automational and transformational value. It also raises the complexity of operational decisions.

**Oil & gas and pipelines.**
- The pipeline DT literature is mainly operational. Bo et al. (2020) position the DT as the core of China's "intelligent pipeline" strategy, with construction as one stage of the lifecycle. Sarvesh et al. (2024) review XR/DT in the oil-and-gas pipeline industry, with an emphasis on monitoring, training and maintenance.
- The only pipeline-*construction* DT in the core set is Abdelhamid et al. (2025). It is a DT plus discrete-event simulation model for trenching, welding and backfilling, fed by IoT, procurement and geotechnical data, with dashboards. Back-tested on two real projects, it reports less than 2% deviation in total duration and a MAPE below 5% for weekly progress.

**Commercial control and limitations.**
- Only two core DT records address payments.
  - Wu and Li (2025) use a continuously updated DT as a "dynamic oracle" that triggers milestone payments through smart contracts. In a prototype, verification-to-payment time fell from several days to minutes, and disputes were eliminated across milestones.
  - Shehadeh (2025) reports a 30% reduction in financial disputes and a 25% improvement in payment timeliness in one public building project. That study combined DT data, blockchain and game-theoretic cost allocation.
- Both are single-project building studies.
- **Limitations of C1 overall:**
  - conceptual or perception-based validation dominates;
  - buildings are the reference context;
  - commercial outcomes are almost absent.

### C2. UAV photogrammetry, DEM/DSM and volumetrics

**State of the art.** UAV structure-from-motion (SfM) photogrammetry is a mature surveying technique for earthworks.
- The reported accuracy is consistent across settings, but the abstracts use heterogeneous metrics.
- The core studies compare UAV products against independent references: GNSS or RTK points, total station, terrestrial laser scanning (TLS) or LiDAR.

**Typical reported results** (as stated in the abstracts):

| Study | Context | Reference | Reported result |
|---|---|---|---|
| Hugenholtz et al. (2015) | Gravel stockpile, before/after excavation | GPS test points; GPS-interpolated DTM; haul ticket | Vertical RMSE 0.106 / 0.097 m; UAV volume 2.6–3.9% lower than GPS DTM; extracted volume within 2.5% of the haul ticket |
| Varbla et al. (2020) | Construction site, 22 weekly campaigns | TLS | Geometry RMSE better than 2.8 cm with RTK-GNSS UAV and integrated georeferencing; < 5 cm with ≥ 1 GCP |
| Julge et al. (2019) | Road embankment (sand/gravel) | RTK-GNSS | Height accuracy 5.7 cm "with proper measuring techniques"; volumes checked against road administration requirements |
| Kang et al. (2024) | Slope earthworks | GNSS survey | Volume accuracy 94.4% (RTK-UAV photogrammetry) and 95.7% (LiDAR) without GCPs |
| Kang et al. (2026) | Earthworks under dense vegetation | Reference volume | LiDAR volume error 0.3%; photogrammetry "slight deviation"; result depends on the ground-filtering method |
| Akgul et al. (2017) | Road planning (3 roads) | NRTK-GNSS DEM | ~234,385 vs ~35 points/ha; similar cut/fill per metre of road |
| Lee and Lee (2022) | Earthwork site, 8 flight cases | Check points; GPS volumes | Vertical + 40–50° oblique imagery at 50 m most accurate |
| Mohd Safie et al. (2018) | Road maintenance works (2 roads) | Contractor as-built claims | Claimed areas larger than UAV-measured by 3.27% and 4.83%; perimeters by 1.35% and 2.44% |

- Further studies confirm feasibility on highways. Wang et al. (2017) built multi-week progress models. Al-Tahir and Barran (2020) compared UAV surveys with total station on time, personnel and cost.
- Kavaliauskas et al. (2021) compare RTK, PPK and GCP-based workflows for BIM-based earthwork quantity estimation in a 36 ha quarry.
- The seminal work of Siebert and Teizer (2014) evaluated an autonomous UAV mapping system for earthwork projects *(TLDR)*.

**Key themes.**
1. **Accuracy is condition-dependent.** It depends on georeferencing strategy (RTK, PPK, GCP count and placement), flight altitude, camera geometry (oblique imagery helps) and surface conditions (vegetation, moisture).
2. **The sector is moving towards GCP-light RTK workflows** (Kang et al., 2024; Varbla et al., 2020). This lowers the field effort of *daily* surveys.
3. **Uses beyond volumetrics.** Irizarry and Costa (2016) and Li and Liu (2018) document UAV use for progress, logistics, safety and quality inspection. Irizarry and Costa (2016) also highlight regulatory and cost implications.

**Pipelines.**
- Pipeline-specific UAV studies are few and mostly technology-oriented.
- Khan et al. (2026b) compare six photogrammetry tools on a trench-and-pipeline dataset. The comparison is qualitative, with no reference survey in the abstract.
- Hlady et al. (2020) argue that mobile LiDAR and imagery can replace hazardous manual centreline and weld mapping in open ditches on pipeline rights-of-way. This is directly relevant to the lowering-in "witness".
- Yu et al. (2026) detect excavators near gas pipelines under construction from high-altitude UAV imagery (AP50 = 95.8%).
- Rosati et al. (2025) classify excavation work phases with deep learning in an oil-and-gas construction company. Their decision-support system generates reports automatically.

**Limitations.**
- Most studies validate on a single site.
- Errors are reported in heterogeneous metrics: RMSE, percentage of volume, "accuracy %".
- Error is rarely propagated to the quantity that is paid.
- The closest exceptions are:
  - Hugenholtz et al. (2015), who compare with a haul ticket;
  - Julge et al. (2019), who compare with an agency requirement;
  - Mohd Safie et al. (2018), who compare with contractor-claimed as-built quantities.
- None of the verified studies derives a statistical acceptance rule (tolerance band) that links measurement uncertainty to a certification decision.

### C3. BIM/GIS integration and linear referencing

**State of the art.**
- **Alignment geometry.** IFC 4.3 has brought alignment and linear infrastructure into the open BIM standard. Soilán et al. (2020) generate IFC Alignment entities semi-automatically from mobile laser scanning of highways. Garramone and Scaioni (2022) test IfcAlignment for a railway centreline derived from raster GIS.
- **Georeferencing.** Uggla and Horemuz (2018) show that neglected georeferencing and scale distortion in BIM can cause costly delays on site. They analyse the geographic capabilities of IFC 4 and IFC Alignment.
- **Integration in practice.** BIM-GIS integration supports alignment optimisation through semantic web technologies (Zhao et al., 2019). At project scale, Akob et al. (2019) describe "Highway Information Modelling" on the 786 km Pan Borneo Highway. There it is used to monitor and track progress across a long linear construction project.

**Pipelines.**
- Demir and Yomralioglu (2024) review BIM-GIS integration for natural-gas pipeline *asset management*. They stress data standardisation.
- Li et al. (2010) describe a digital pipeline built on the ArcGIS Pipeline Data Model.
- Morakinyo and Sunmonu (2025) map a gas-pipeline right-of-way with chainage-referenced profiles to derive cut and fill for construction.
- The most directly relevant study is Chauhan and Bansal (2026). They show that activity production rates *vary along the pipeline length*, and they quantify this variation with GIS-weighted factors (AHP) compared against achieved field rates. This is empirical support for keying productivity and quantities to chainage rather than to the project as a whole.

**Limitations.** C3 work concentrates on design, asset management and geometry exchange. No verified study uses linear referencing (KP/chainage) as the integration key for *commercial* quantity states, i.e. reported, measured, claimed, certified and invoiced quantities.

### C4. Personnel and equipment tracking (including ethics, C4-ETH)

**State of the art.**
- Sherafat et al. (2020) structure automated workface monitoring in four levels: location tracking, activity recognition, activity tracking and performance monitoring.
- Teizer (2015) surveys vision-based tracking of temporary resources on infrastructure sites *(TLDR)*.
- Omar and Nehdi (2016) compare data-acquisition technologies for progress tracking and their suitability for different project types *(TLDR)*.

**Equipment tracking.** Equipment is better covered than personnel.
- Pradhananga and Teizer (2013) analyse equipment operations automatically from GPS data *(TLDR)*.
- Lee et al. (2018) derive equipment utilisation time logs from GPS-only fleet telematics with geofences, without CAN-bus data. The method was verified in field tests. It is the closest analogue to H5's verified equipment-hours.
- Kinematic sensing is a second route. Akhavian and Behzadan (2015) recognise equipment activities from smartphone sensors *(TLDR)*. Rashid and Louis (2019) use data augmentation to train recurrent networks with limited site data, explicitly to minimise idle time.
- Vision is a third route. Chen et al. (2020) report 87.6% activity-recognition accuracy and 83% productivity-calculation accuracy for multiple excavators from site videos. Zhu et al. (2017) integrate tracking into detection of workforce and equipment *(TLDR)*.

**Personnel tracking accuracy.** Accuracy is modest and environment-dependent.
- WiFi positioning on a metro construction site achieved errors within 5 m (Woo et al., 2011, *TLDR*).
- BLE beacons have an effective RSSI range of about 1–6 m. Signal obstruction and placement strongly affect reliability, but calibrated models with minimal setup are adequate (Gong et al., 2025; indoor testbeds).
- Differential-RSS RFID improves equipment positioning, validated in an LNG training centre (Wu et al., 2019).
- **The tracking studies are short, site-bounded and largely indoor or compact-site.** None of the verified studies reports multi-week tracking over kilometres of right-of-way.

**Ethics and acceptance (C4-ETH).** Worker acceptance is the binding constraint.
- **Who would wear trackers.** In a modified-UTAUT survey, 59% of US field labourers would not voluntarily use location-tracking wearables, and 46% would not use biometric ones (Fugate & Alzraiee, 2023). Intention was associated with performance expectancy, data security and social influence.
- **Sharing on worker-benefit terms.** A survey of 4,385 Finnish construction workers found willingness to share data when it serves their own safety and health. Privacy and security were the main concerns (Häikiö et al., 2020).
- **Real deployment.** On a project worth over USD 1 billion, 1,200 proximity sensors were deployed. TAM-based modelling with 138 workers found that perceived privacy and social influence predicted adoption (Yang et al., 2025).
- **Legal concerns.** Wu et al. (2023) review 63 articles on real-time employee monitoring. They organise the concerns as legal (privacy intrusion, employment relations, compliance liability), ethical and behavioural (trust, work behaviour, mental health). Wu et al. (2022) frame adoption with communication-privacy-management and equity theories.
- **Governance.** Weber-Lewerenz (2021) proposes corporate digital responsibility and ethics-by-design guidelines for construction AI, aligned with EU trustworthy-AI requirements.
- Choi et al. (2017) analyse what drives workers' acceptance of localisation and wearable health devices *(title-level)*.

**Limitations.** Accuracy studies and acceptance studies are disconnected. Few studies evaluate a *tiered* or aggregated presence design of the kind proposed in the SiteOps scope (crew-level aggregates for commercial users).

### C5. Productivity monitoring and earned value

**State of the art.** Automated equipment productivity monitoring is the most mature sub-area.
- Chen et al. (2022) review 119 papers on earthmoving productivity monitoring. They compare kinematic, vision, audio and telematics methods for operation time and soil quantity, and propose a road map.
- Kim and Chi (2020) monitor earthmoving productivity on a highway site with multiple non-overlapping cameras. They report 97.6% equipment-matching accuracy over 371,125 frames.
- Mahamedi et al. (2021) report 99.78% accuracy in measuring the productivity of a demolition activity from smartphone kinematic and noise data with deep learning.
- Navon et al. (2012) derive work area and time for road earthmoving from equipment GPS in a GIS. In a pilot, the control information deviated by ±15%. The deviation fell when averaged over several days, and the system was more economical than manual control at sub-biweekly frequency. **This trade-off between accuracy and frequency is directly relevant to daily production control.**
- Alaloul et al. (2021) review building projects and find that traditional, computer-vision and photogrammetric data acquisition dominate. Samples are small and site coverage is limited.

**Earned value and data fusion.**
- Turkan et al. (2013) argue that conventional progress tracking is "labour intensive, sometimes subject to negotiation, and often driven by arcane rules". They show that converting 3D-recognised objects to earned value can improve the accuracy of progress tracking for billing.
- Shahi et al. (2015) fuse 3D imaging, UWB positioning, foreman reports and schedule data to track *activities* rather than objects. This is a direct antecedent of the planned/reported/measured reconciliation in RQ2.
- Kim et al. (2011) is one of the few studies that compares sensor-derived productivity with **contractors' daily logs and pay-estimate documents**, using paired t-tests and Wilcoxon tests. It found no significant difference.
- Radman et al. (2025) compare four projects that use an integrated real-time data framework (RealCONs) with four that do not. They report significant improvements, verified with EVM/ESM metrics and Wilcoxon tests, in forecasting accuracy and in data-collection and decision delays.

**Pipelines.**
- Pipeline productivity studies are model- or simulation-based.
- Ammar and Samy (2015) fit learning curves to eight Egyptian gas-pipeline projects. A cubic model fits welding best.
- Kuppusamy and Ramar (2011) simulate alternative tie-in methods with a 50% time reduction.

**Limitations.**
- Validations are short and single-site.
- Productivity is rarely linked to *quantities that are paid*.
- With the exception of Radman et al. (2025), the effect on decisions is not measured.

### C6. Progress measurement, quantity take-off and payment

**Technical progress monitoring.** The research base is large.
- Golparvar-Fard et al. (2015) recognise physical progress from unordered daily photographs and IFC models with Bayesian classification. Their 2009 visualisation work (Golparvar-Fard et al., 2009; seed S12) is seminal.
- Kim et al. (2013) *(title-level)* and Rebolj et al. (2017) *(title-level: point-cloud quality requirements for Scan-vs-BIM)* extend the Scan-vs-BIM line. Reja et al. (2022) review computer-vision progress monitoring *(title-level)*.
- For roads:
  - Vick and Brilakis (2018) detect layered design surfaces in as-built point clouds (F1 = 95.2%).
  - Lo et al. (2022) produce UAV-photogrammetry progress reports for a road base course. The reports give percentage complete, the location of the work and the quantity of material used, backed by point-cloud evidence.
  - Patel et al. (2024) measure pavement progress with a sensor-equipped UGV (94.35% layer-change classification accuracy).

**Pipelines.**
- Khan et al. (2026a) provide the first systematic review focused on automated progress monitoring in *pipeline* construction. They state that the focus has been on buildings and that a pipeline-specific review was lacking.
- 张 (2019) discusses progress measurement methods for EPC oil-and-gas pipeline projects.
- Soliman et al. (2017) describe an application that generates ROW footprints and detailed construction quantities (excavation volumes, supply and demand) from progressively refined route data.

**Commercial verification.** A smaller literature links measured quantities to payment.
- **Reality capture and valuation.**
  - Fobiri et al. (2025) use drone point clouds against the as-designed model for interim valuation and work verification on an ongoing project. They note that claim disputes and delayed payment arise from a lack of clarity on the value of work completed.
  - Rahnamayiezekavat et al. (2022) built a UAS that checks the accuracy of work performed and generates progress payment reports, combined with 5D BIM. Interviews identified digital culture as an obstacle.
- **Blockchain and smart contracts.**
  - Hamledari and Fischer (2021b) argue that current payment applications cannot support reliable automation because they rely on centralised control. They present smart-contract payments conditioned on UAV-based progress data. Hamledari and Fischer (2021a) extend this to robotic reality capture *(title-level)*.
  - Das et al. (2020) formalise interim-payment conditions in a blockchain framework with selective transparency.
  - Ahmadisheykhsarmast and Sonmez (2020) test a smart-contract payment-security system on a real project. Sonmez et al. (2022) integrate BIM with smart contracts for progress payment administration *(title-level)*.
  - Elsharkawi et al. (2025) use scan-to-BIM data as off-chain evidence for payments.
  - Alhasan (2026) argues from a doctrinal perspective that blockchain-verified records can meet the evidentiary standards of international arbitration (FIDIC 2017, IBA rules).
- **Payment problem.**
  - Bolton et al. (2022) analyse 355 payments on 30 UK subcontract projects. Payment was late in 77% of subcontracts and for 46% of payments. Retention release was a further burden.
  - Malomane and Musonda (2025) attribute poor progress-payment management to information management, communication, corruption and *failure to agree on measurements of work done*. They propose a common-data-environment framework.
- **Quantity take-off accuracy.**
  - Sadeh et al. (2026) compare AI quantity take-off with contractor takeoffs across 29 line items using Wilcoxon and Kruskal–Wallis tests. Deviations were small but significant, with systematic underestimation of areas.
  - Fürstenberg et al. (2024) find that automated QTO in a Norwegian road project was reproducible for only 40% of cost items. The causes were ambiguous classes and hard-coded cost breakdown structures.

**Limitations.**
- The commercial-verification studies are almost all building projects, prototypes or single cases.
- Blockchain dominates the "payment automation" framing, while the *measurement* question (how good is the evidence that triggers payment) is treated as solved.
- No study models measurement uncertainty within the payment logic.

### C7. Interoperability and standards

**State of the art.**
- IFC remains the anchor schema.
- Pauwels and Terkaj (2016) set requirements for a usable ifcOWL ontology *(TLDR)*.
- Lee et al. (2020) show that IFC/MVD exchanges suffer data-integrity problems caused by human error, inadequate model view definitions and mapping errors. They argue for rule-based validation.
- For linear works, Won et al. (2019) propose IFC property and quantity sets for road quantity take-off and estimating. Fürstenberg et al. (2024) recommend unambiguous ontology classes, decoupled cost breakdown structures and Level of Information Need, so that quantities are reusable across phases.
- Schlenger et al. (2022) contribute a construction-phase DT data schema (process-oriented, UML plus ontology). It covers process performance but not commercial quantity states.

**Gaps.**
- The core set contains no verified study on PODS, LandXML or ISO 15143-3 telematics data in construction-phase integration, and none on OPC UA in construction.
- These standards are documented as normative sources in `seed_references.md` (N01–N08). Their absence from the academic results is itself a finding (G4).

### C8. Data quality, uncertainty and auditability

**State of the art.** Auditability is addressed mainly through blockchain-based provenance.
- **Provenance and audit trails.**
  - Lee et al. (2021) integrate a DT with a blockchain so that every data transaction is traceable. They tested it on a near-real-time positioning stream from a prefabricated element.
  - Celik et al. (2023) record BIM-object provenance (discipline, version, responsibility and liability) on a blockchain. They tested it in a real bridge-construction scenario.
  - Lu et al. (2021) design a dual-layer blockchain for governmental supervision of construction work.
  - Chong et al. (2024) synchronise BIM cost models with bills of quantities for a lifecycle audit trail in a hospital case. Cost variances arose from differences in **measurement rules, model precision and professional errors**. The synchronised approach improved payment verification during construction.
- **Data quality of sensing.** Data quality is treated as an acquisition-planning problem.
  - Zhang et al. (2016) plan laser scans against data-quality requirements and outperform experienced professionals without longer collection time *(TLDR)*.
  - Rebolj et al. (2017) specify point-cloud quality for Scan-vs-BIM *(title-level)*.
- **Defensibility.** Sadok et al. (2026) frame DT-integrated schedule optimisation as "legally defensible" schedule management.

**Gaps.**
- No verified study treats **measurement uncertainty as an explicit attribute that travels with a quantity into a decision**. Examples of such a decision are accepting, querying or rejecting a claimed quantity.
- Uncertainty appears as a validation statistic at the end of C2 studies. It appears as a risk input in scheduling (Sadok et al., 2026). It does not appear as a data-model attribute.

### C9. Technology adoption and change management

**State of the art.**
- Adoption research in construction is survey-based and mostly about BIM.
- Lee et al. (2015) propose a BIM acceptance model, estimated with SEM.
- Qin et al. (2020) combine TAM and TOE and find national policy requirements to be the strongest driver of BIM adoption.
- Hewavitharana et al. (2021) modify UTAUT for construction digital transformation and validate it with experts.
- For DTs, surveys in Nigeria find four barrier categories (Bello et al., 2024): technological and investment; data management and government; project and human resources; digital transformation. Arowoiya et al. (2024) group the drivers into innovation, operation, quality, performance and policy.
- Ammar et al. (2022) interview practitioners and derive 40 DT applications grouped into seven capabilities.
- For smart technologies more broadly, Hwang et al. (2022) find that the top challenges in Singapore are data and information sharing, regulatory compliance and **data ownership**. The most effective strategies are training, incentives and change management.
- Turner et al. (2021) identify industrial connectivity as the key enabler for interconnecting Industry 4.0 technologies on construction sites.
- Sivaraman et al. (2025) find 14 significant predictors of drone adoption in India, among them procurement and operating cost, dedicated budget and equipment availability.

**Limitations.**
- Studies are cross-sectional and single-country.
- They measure perceived intention rather than use.
- They rarely address the field workforce on remote linear sites, or the commercial user (quantity surveyor, contract administrator).

---

## 3. Cross-cluster synthesis against RQ1–RQ5 and H1–H5

### RQ1 / H1: Independent UAV measurement and claim discrepancy

**What the literature supports.**
- UAV photogrammetry can measure earthwork geometry and volumes independently, at centimetre-level vertical accuracy and with volume differences of a few percent against references (Hugenholtz et al., 2015; Julge et al., 2019; Kang et al., 2024; Varbla et al., 2020).
- Accuracy depends on conditions that a pilot can control: georeferencing, flight geometry and vegetation filtering (Kang et al., 2026; Lee & Lee, 2022).
- Three studies come close to the H1 comparison of a claimed quantity with an independently measured one:
  - Mohd Safie et al. (2018) found contractor-claimed road areas 3.3–4.8% larger than UAV measurements.
  - Hugenholtz et al. (2015) reconciled a UAV volume with a haul ticket to within 2.5%.
  - Kim et al. (2011) found sensor productivity data consistent with pay-estimate documents.

**What it does not support.**
- The measurability of **pipeline-specific quantities** has hardly been studied at abstract level: ROW clearing and grading area, trench length and depth, lowering-in and backfill. Hlady et al. (2020) and Khan et al. (2026b) are exploratory.
- No study states the uncertainty of each quantity type in the form needed for a measurability matrix.
- Weld counts and NDT quantities are absent from the UAV literature. This is consistent with the practice rule in `industry_practice_sources.md` that these come from QA/QC records.

**Implication.** H1 is plausible but untested for pipelines. The literature provides analogous methods: Wilcoxon on paired quantities (Sadeh et al., 2026; Kim et al., 2011) and reference-survey comparison (Varbla et al., 2020). It provides no benchmark effect size.

### RQ2: Data model and linear referencing

**Building blocks that exist:**
- IFC 4.3 alignment and georeferencing (Soilán et al., 2020; Uggla & Horemuz, 2018);
- chainage-dependent production rates (Chauhan & Bansal, 2026);
- chainage-referenced ROW quantities (Morakinyo & Sunmonu, 2025; Soliman et al., 2017);
- construction-DT process schemas (Schlenger et al., 2022);
- multi-source fusion of sensor data with foreman reports (Shahi et al., 2015);
- IFC quantity sets for road QTO (Won et al., 2019);
- BIM–BoQ synchronisation for audit trails (Chong et al., 2024).

**What is missing.**
- No verified study integrates these into a model with the key **location (KP) × time × activity × crew × equipment × subcontractor**.
- No verified study carries the commercial states planned → reported → measured → claimed → certified → invoiced with their provenance and uncertainty.
- Fürstenberg et al. (2024) and Chong et al. (2024) show *why* this is hard. Measurement rules and cost breakdown structures differ between the parties, and quantities computed from models do not map cleanly onto contractual items.

### RQ3 / H2: Dashboards, review time and decision quality

**Evidence that integrated real-time data improves control.**
- Radman et al. (2025) compared four projects with and four without the framework, on EVM/ESM and decision delays.
- Abdelhamid et al. (2025) report accurate pipeline progress forecasts with dashboards.
- Alizadehsalehi and Yitmen (2021) and Zhang et al. (2022) report positive *perceived* effects.
- Rosati et al. (2025) automate report generation.

**What is missing.**
- No verified study measures **review time or error detection** in daily production review with a within-subject design.
- No verified study reports SUS for a construction-production dashboard.
- H2's instruments (time-and-motion, SUS) therefore have no direct benchmark in the reviewed literature. This is an opportunity for contribution, not a basis for a prior.

### RQ4 / H3: Reconciliation, disputes and certification-cycle time

**The problem is well documented.**
- Late payment is common (Bolton et al., 2022).
- Disagreements over measurement of work done drive disputes (Malomane & Musonda, 2025).
- Conventional progress tracking is "subject to negotiation" (Turkan et al., 2013).
- Claim disputes arise from unclear value of work completed (Fobiri et al., 2025).

**Solutions are mostly payment-*execution* architectures** (smart contracts, blockchain; Das et al., 2020; Hamledari & Fischer, 2021b; Elsharkawi et al., 2025).

**Quantitative commercial outcomes** come from two single-project studies with weak designs:
- Wu and Li (2025): verification-to-payment time cut from days to minutes, and disputes eliminated (prototype);
- Shehadeh (2025): 30% fewer financial disputes and 25% better payment timeliness.

**Implication.** H3's exploratory status (L-02) is appropriate. The literature indicates the direction of the effect, not its size. The evidence comes from building projects and milestone payments, not from re-measured unit-rate quantities.

### RQ5 / H4–H5: Tracking, productivity visibility and adoption conditions

**Technical feasibility (H4).**
- Automated equipment productivity measurement is technically mature: GPS/telematics (Lee et al., 2018; Navon et al., 2012), vision (Chen et al., 2020; Kim & Chi, 2020) and kinematic sensing (Mahamedi et al., 2021; Rashid & Louis, 2019).
- No study measures the **lead time of a delay signal** against conventional reporting, which is H4's dependent variable.
- Radman et al. (2025) report earlier delay identification qualitatively in the abstract.

**Verified presence (H5).**
- Equipment-hours can be derived from GPS-only telematics (Lee et al., 2018). This supports the equipment half of H5.
- Personnel presence accuracy is only about 1–6 m for BLE and within 5 m for WiFi (Gong et al., 2025; Woo et al., 2011). That is adequate for presence at work-front level but not for task attribution.
- No verified study compares claimed with verified headcount-days or equipment-hours.

**Adoption conditions.**
- Worker acceptance of location tracking is low when it is voluntary (Fugate & Alzraiee, 2023).
- Acceptance depends on privacy, data security, social influence and personal benefit (Häikiö et al., 2020; Yang et al., 2025).
- The governing concerns are legal: privacy intrusion, employment relations and compliance liability (Wu et al., 2023).
- At organisation level, the dominant barriers are data ownership and sharing, regulatory compliance and investment (Bello et al., 2024; Hwang et al., 2022).
- Remote-site connectivity is identified as an enabler (Turner et al., 2021) but not studied empirically for linear sites.

**Implication.** The tiered, aggregated presence design in the project scope (A-012, D-069) is consistent with the acceptance evidence. Its effect on acceptance still has to be tested.

### Summary of RQ coverage

| RQ / H | Literature support | Evidence strength (provisional) | Main gap |
|---|---|---|---|
| RQ1 / H1 | UAV accuracy for earthworks; three claim-vs-measure analogues | Moderate (many single-site validations) | Pipeline quantity measurability; uncertainty → tolerance |
| RQ2 | Building blocks (IFC 4.3, chainage productivity, DT schema, fusion) | Weak–moderate | No integrated commercial-state, linear-referenced model |
| RQ3 / H2 | Comparative EVM framework; perceived benefits | Weak | No review-time / SUS evidence for production dashboards |
| RQ4 / H3 | Problem well documented; 2 quantitative single cases | Weak | No baseline/pilot design on re-measured quantities |
| RQ5 / H4–H5 | Mature equipment tracking; acceptance surveys | Moderate (technical) / moderate (acceptance) | Remote linear sites, long durations, claim-vs-verified presence |
