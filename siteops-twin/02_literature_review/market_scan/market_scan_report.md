# Market Scan: Commercial Solutions Relevant to SiteOps Twin

Owners: solution-architect and commercial-analyst. Version 0.1, 2026-11-23. Status: for supervisor review.
Companion files: `solutions_catalogue.csv` (54 solutions, one row each) and `README.md`.

> **How to read this document.** Each capability rating is a *documented-capability* rating. It records what the vendor's or a third party's public material says. It is **not** a hands-on test. Ratings use the SiteOps Twin target objectives O1–O9 from `04_to_be_architecture/conceptual_architecture.md` §4. Where the evidence was thin, the rating is conservative ("Partial" or "N") and the CSV says why.

## 1. Purpose and research questions

The scan supports Chapter 2 (state of practice) and the build-vs-buy decision for the MVP. It answers four questions:

1. Which commercially available products already deliver each SiteOps objective (O1–O9) for onshore pipeline construction?
2. Which objectives remain uncovered, and is the gap specific to linear projects, to commercial certification, or to the German market?
3. How can SiteOps Twin plug into the pilot JV's existing Propeller workflow and its likely German AVA/ERP back-end instead of replacing them (design principle 1, D-007)?
4. What does this imply for positioning the thesis contribution and the product?

## 2. Method

### 2.1 Search strategy
- **Window.** All searches were run on 2026-11-23. They reflect the market "as of late 2026". Events up to November 2026 were captured where indexed, for example Procore's DroneDeploy acquisition closing on 9 Sep 2026, Nemetschek closing the HCSS deal on 1 Jul 2026, and Buildots' Sep 2026 round.
- **Engine and modes.** About 45 web searches were run, in "standard" mode by default. "Extended" mode was used for hard or recent facts: acquisitions, pricing tiers, and pipeline-specific products.
- **Query families.** Queries were built per category A–F:
  - vendor and product name + capability (API, GAEB, ISO 15143-3, offline, EU hosting);
  - generic need + domain ("pipeline construction software daily progress chainage spread right of way", "Baustelle Zutrittskontrolle Nachunternehmer Mindestlohn");
  - status queries ("acquired", "retirement", "2026 release").
- **Languages.** Both English and German queries were used. The German market is covered through German trade sources (baulinks.de, softguide.de, Baunetz Wissen) and vendor brochures.

### 2.2 Inclusion and exclusion criteria
**Included** products that are:
- commercially offered (not research prototypes);
- active, or recently changed status (a status change is itself a finding);
- relevant to at least one of O1–O9;
- documented by at least one indexed source that names the product and describes its function.

**Excluded:**
- products that could not be tied to a real, current source;
- pure hardware without a data service;
- generic BI tools;
- integrity-phase (operations) pipeline products with no construction use.

Some products were found but left out of the catalogue because the evidence was too thin to rate them. They are mentioned in §3 only: Samsara, Doxel, Fluor Weld-Console, CCi SiteSense, STREIT Aufmaß app, Skycatch, Kespry and Oracle Aconex.

### 2.3 Evidence grading
Each catalogue row has an `evidence_level`:
- **V1:** vendor material (product page, help documentation, brochure, release notes, vendor blog).
- **V2:** independent or third-party material (trade press such as Construction Dive, GIM International, Equipment World or baulinks.de; review and directory sites; Wikipedia).
- **V3:** regulatory or official filings, for example Procore's SEC 10-Q on the DroneDeploy merger.

Most capability evidence is V1. This is normal for a market scan, but it is a real limitation (§2.5).

### 2.4 Capability coding
Each solution was coded against O1–O9:
- **Y:** the function is documented as a standard capability.
- **Partial:** the function is covered only in part, only in an adjacent domain (e.g. buildings, not linear), or only by a combination with another product. A typical case is design-vs-as-built surface comparison counting as Partial for O7.
- **N:** not documented.
- **?:** contradictory evidence. In practice the "?" code was not needed. Uncertain cases were coded "Partial" or "N", with a note.

Two coding rules matter for interpretation:
- **O5 (measurement per section/chainage)** is rated Y only where an *independent measurement* is produced, e.g. photogrammetry or survey. A self-reported production entry by KP counts as Partial.
- **O7/O8** are rated Y only where *commercial* states are compared: claimed, certified and invoiced. Schedule or design deviations alone are Partial.

A simple indicative score (Y = 1, Partial = 0.5) is shown in the heat-map. It is unweighted and must not be read as a ranking of product quality.

### 2.5 Limitations
1. **Vendor claims vs verified capability.** Almost all capability statements come from vendors. None was tested hands-on. Features such as "offline", "API" or "real-time" vary greatly in depth.
2. **Pages were not opened directly.** The plan was to confirm vendor pages with a page fetch. In this research environment, direct fetches of vendor hosts were blocked by the network allowlist (e.g. propelleraero.com, support.esri.com). Every source URL in the catalogue was **returned by the search engine**, and its content was read through the search tool's extract of that page. The URLs are real, indexed pages, not reconstructed ones. But the reading of each page depends on the search extract, so confirming the decision-relevant rows by direct page review or vendor demo (§9) is mandatory before the thesis is submitted.
3. **Snapshot bias.** The market is consolidating fast (§3.7). Ownership and product names may change again before submission.
4. **Pricing** is rarely public in this segment. Most entries say "not public".
5. **Coverage.** The scan is broad, not exhaustive. Regional pipeline-construction tools (e.g. in-house contractor systems) are under-represented because they are rarely indexed.

## 3. Landscape by category

### 3.1 A — Drone / reality capture and earthworks analytics (10 solutions)
**Propeller** (A01) is the incumbent at the pilot JV. Its documented functions are:
- processed 3D site models, volumes, and cut-fill against design;
- a shared corridor map for tracking progress along the ROW;
- integrations with Procore and HCSS.

A read-only public API and WMTS tile streaming are reported for the top ("Scale") tier. Sources for this are third-party directories and Propeller's integrations blog. In February 2026 Propeller acquired Spacesium (geospatial algorithms). Its first output is an AI "Haul Road Analysis" aimed at mining. Propeller's development focus is therefore *physical-site intelligence*, not commercial certification. Trimble Stratus (A02) is a co-branded channel of the same engine.

**DroneDeploy** (A03) is the most important 2026 change in this category. Procore signed a merger agreement on 27 Jul 2026 and closed the ~USD 845m acquisition on 9 Sep 2026 (SEC 10-Q; Construction Dive). *Lead-agent check 2026-11-23: the July 2026 announcement is widely reported; the closing date appears in fewer sources, so re-verify it before thesis submission. The Nemetschek–HCSS closing (1 Jul 2026) is confirmed by multiple sources.* DroneDeploy's 2026 "Progress AI" adds schedule matching, deviation reports and P6 import, and field notes now sync two ways with Procore and Autodesk. This is the clearest move towards "reality capture → project management". It is aimed at schedule progress, not at measured-vs-claimed quantities.

The other entries in this category:
- **Pix4D** (A04): offers fully offline desktop processing, which matters for data sovereignty.
- **Esri** (A05): retired Site Scan Flight / Flight LE on 1 Jul 2025 in favour of ArcGIS Flight. Site Scan for ArcGIS itself remains in the ArcGIS Reality suite. This churn should be checked before any adoption.
- **Datumate DatuBIM** (A07): the closest German linear-infrastructure precedent, through a Deutsche Bahn framework tender for drone progress monitoring (2022, 2+2 years). Its schedule-linked Progress Tracking module has been available since 1 Sep 2026.
- **Cyberhawk iHawk** (A08): an O&G-owner-side visualisation platform, including Shell's global construction projects.
- **OpenSpace** (A09): building-centric and low fit for a ROW.
- **Bentley iTwin Capture + Cesium** (A10): a possible 3D Tiles viewer stack for the SiteOps roadmap.
- **Virtual Surveyor** (A06): a surveyor's tool for extracting section-wise quantities from imported surfaces.

**Not catalogued:** Skycatch and Kespry. No 2026 status could be confirmed for either.

### 3.2 B — Construction digital twin, 4D, progress and quantity platforms (10 solutions, including Oracle Textura listed under F)
**Bentley SYNCHRO 4D** (B01) is the only 4D platform that markets itself explicitly for *linear* projects. It has rail and road case studies (Italferr, ACCIONA M80) and covers planned-vs-actual progress and automated quantity take-off. SYNCHRO+ (AI-assisted, Cesium-based) entered early access in Dec 2025, with general availability announced for 2026. GA could not be confirmed.

**Autodesk** (B02) has renamed Build to **Forma Build**. Autodesk documents Germany as a selectable primary storage region for Forma Build, Takeoff and Estimate.

**Procore** (B03) offers an EU Application Zone hosted in Germany. With DroneDeploy it now holds drone data and project financials in one company. Procore is therefore the most credible future *platform* competitor. Its public material does not show linear referencing, or reconciliation of subcontractor claims against independently measured quantities.

**Enterprise project-controls suites** are natural O9 back-ends, not field tools:
- Oracle Primavera Cloud/P6 + Unifier (B04: EVM, progress measurement, advanced work packaging);
- Hexagon EcoSys / HxGN Smart Build (B05: EIA-748 EVM, automated percent complete).

**InEight Plan & Progress + Control** (B06) comes closest to the commercial core of SiteOps. Field users record installed quantities and hours against planned work. Quantities are claimed under rules of credit and then synced to Control, where they are compared with cost and man-hours. The claimed quantities, however, are entered by the contractor's own staff. Nothing in the documentation shows an independent drone or survey witness, or a subcontractor-claim layer.

**Trimble WorksManager + Siteworks + B2W Track** (B09) has the most explicit *measured vs reported* workflow in heavy civil. A project manager requests a measured production quantity in B2W Track. A surveyor fulfils it at survey grade in Siteworks. The result is reconciled with field logs and can be passed to Viewpoint accounting. This is the closest architectural analogue to SiteOps' reconciliation engine. It is contractor-internal and survey-driven, not subcontract certification.

**Buildots** (B07) and **Sablono** (B08, Berlin) represent AI-camera and activity-level progress tracking:
- Buildots raised USD 130m in Sep 2026. Its July 2026 Buildots Field (ex-Genda) explicitly pairs *crew activity with built output*, with GA targeted for Q4 2026. The idea matches SiteOps' O2/O4 triangulation, but the product is built for buildings and data centres.
- Sablono's unit-based model, demonstrated on solar trenches, could transfer to KP sections.

**Not catalogued:** Doxel (2026 activity is limited to data-centre agreements) and Oracle Aconex (no current capability evidence was retrieved).

### 3.3 C — Pipeline-construction-specific software (10 solutions)
Pipeline-specific products cluster around **QA/weld traceability and material tracking**:
- Metegrity Pipeline Enterprise (C03): GPS weld map, welder certification, offline inspections; used on Enbridge Line 3 Replacement.
- Epilogue with C.A.T.S. (C04): weld lifecycle by barcode, NDE/repairs, S-curves and SPI/CPI.
- Unistal PCMS (C05): pipe tags from PO to installation, design BOQ vs consumed reconciliation, tie-in/crossing reports, e-pipe-book.
- Pipetrak IT (C06).
- Kemppi WeldEye (C07): WPS/WPQR, welder qualification expiry, arc-time capture.
- CRC-Evans DATA 360 (C08): weld-level digital history. The only source is a sponsored article, so treat it as unverified.

**Trimble Access Pipelines** (C01) is the survey-side tool. It handles pipe tally, joint mapping (weld ID ↔ joints ahead/behind), the as-built weld survey with depth of cover, and automated checks of surveyed welds against the tally. This is exactly the "second independent witness" that the practice-grounding rules require (industry_practice_sources.md §3, rule 3).

**Esri ArcGIS Pipeline Referencing** (C02) is the reference implementation of pipeline linear referencing, built on UPDM/PODS. It is designed for operators, not for construction commercial control.

Two North American products target *linear production and field tickets*:
- **Vitruvi** (C09): GIS-enabled utility/linear construction management with production tracking by location, crew and task.
- **Aimsio** (C10): offline field tickets and LEMs (labour, equipment, materials) with client digital sign-off.

These are the closest operational competitors for O4/O6. Neither documents independent measurement (drone or survey) or a claimed-vs-measured reconciliation.

**Not catalogued** (insufficient evidence): Fluor Weld-Console (internal/licensed) and CCi SiteSense (named only in a listicle).

### 3.4 D — Workforce and equipment tracking (10 solutions)
**OEM telematics.** ISO 15143-3 (AEMP 2.0) is now the common interface:
- **Caterpillar** documents an ISO 15143-3-based API, limited to 50,000 requests per client per day (D01).
- **My Komatsu** pulls in other OEMs' ISO feeds at no extra cost (D02).
- **Liebherr** is moving from LiDAT to **MyLiebherr**, with *no data migration* (D03). This is a practical risk for historical equipment-hour evidence. Liebherr plant is common on German pipeline spreads.

Vendor-neutral analyses note that the depth of AEMP data is uneven across OEMs. Proemion's white paper is one example.

**Mixed and hired fleets:**
- **Trackunit IrisX** (D04): retrofit devices + 100+ OEM feeds, an ISO 15143-3 export, a time-series API, and (2026) an MCP server for AI clients.
- **Tenna** (D05): AEMP aggregation, GPS/QR/RFID.
- **Hilti ON!Track** (D06): BLE tags/gateways for tools and small plant.

**People presence:**
- **Triax Spot-r** (D07): wearables; now owned by biometric access-control firm Invixium (Jul 2024), which matters for the works council.
- **Evercam** (D08): AI people, vehicle and equipment counts from site cameras.
- **AddSecure/Telekom VIDEO GUARD** (D09): >5,000 mobile camera towers in Germany, video processed in Germany, security-first.
- **Bausicht** (D10): German digital access control with subcontractor certificate management, minimum-wage confirmations and on-demand customs (Zoll) reports.

No product in this category links presence data to *commercial claims* (daywork, standby, hours on timesheets), with one exception. HCSS (E01) documents exception reports that compare equipment hours reported on time cards with telematics hours.

### 3.5 E — Field daily reporting and site diary apps (7 solutions)
**International tools:**
- **HCSS HeavyJob** (E01): foreman time cards, quantities, diaries, productivity against budget, and the telematics cross-check above. Nemetschek acquired HCSS (announced 13 Apr 2026, closed 1 Jul 2026), placing it in the same Build & Construct segment as Bluebeam and **NEVARIS**. A German heavy-civil field-to-AVA chain inside one group (HCSS/123erfasst → NEVARIS) is now plausible.
- **Raken** (E02) and **Fieldwire by Hilti** (E03): generic daily reports.

**D-A-CH tools:**
- **Capmo** (E04, Munich): Bautagebuch, offline, ERP API. A reseller states German ISO 27001 hosting; the AVV must be verified.
- **PlanRadar** (E05, Vienna): ticket-based documentation.
- **123erfasst** (E06, NEVARIS): construction time and attendance aware of SKUG/winter-pay rules, subcontractor performance records, equipment/telematics, offline capture, and direct import into NEVARIS Build.

**Esri Survey123 + Field Maps** (E07) is the low-code option for building SiteOps' structured daily report, with documented offline use.

### 3.6 F — Commercial / QS, Aufmaß, GAEB/AVA, contracts and claims (8 solutions)
**German AVA and Aufmaß tools.** These are mature for *document-based* measurement and billing:
- **RIB iTWO / RIB 4.0** (F01): BVBS GAEB DA XML 3.3 AVA certification in 2026; REB 23.003 Aufmaß; Prüfrechnung; a new road-construction configuration package in 2026.
- **NEVARIS Build** (F02): certified GAEB, REB 23.003, subcontractor management, Leistungsmeldung.
- **MWM-Libero / Aufmaß365 / Ponto** (F03): GAEB-certified for Mengenermittlung, X31 and REB DA11 import/export. Utilities use it to check interim and final invoices.
- **BRZ 365** (F06): NU-management, Leistungsmeldung, mobile LV with Nachtragsmanagement, REB Mengenermittlung.
- **ORCA AVA** and **California.pro** (F04, F05): client/planner-side AVA with billing and change-order functions.

**Contract and claims tools:**
- **Thinkproject CONTRACTS + CDE** (F07, Munich): FIDIC/NEC templates and an ISO 19650-attested CDE. VOB/B templates were not found.
- **Oracle Textura** (F08): US subcontractor pay applications.

The common pattern in this category is that *quantities enter as typed or imported measurement sheets*. None of these tools ingests drone measurements or presence data, or tests a subcontractor's Aufmaß against an independent measurement before certification.

### 3.7 Market dynamics (2026)
Three consolidation moves define the year:
1. **Procore + DroneDeploy** (closed Sep 2026): reality capture absorbed into a PM/financials platform.
2. **Nemetschek + HCSS** (closed Jul 2026): heavy-civil field operations joined with a German AVA/ERP vendor (NEVARIS).
3. **Buildots + Genda → Buildots Field** (2025–26): progress AI joined with workforce data.

Each pairs *what was built* with *who did it*. None of them, on the public evidence, pairs these with *what was claimed and certified under the subcontract*. That third leg is where SiteOps Twin is positioned.

## 4. Capability heat-map (54 solutions × O1–O9)

Legend: ● = Y (documented); ◐ = Partial; · = N / not documented. Score = Y + 0.5 × Partial (indicative only, unweighted). Objectives:
- O1: live map/model
- O2: personnel/equipment/work-front visualisation
- O3: event-level tracking
- O4: automated daily production records
- O5: independent measurement per section/chainage
- O6: subcontractor quantity tracking
- O7: planned vs measured vs claimed vs certified comparison
- O8: deviation/duplicate-claim/invoicing alerts
- O9: EVM/claims data foundation

| ID | Solution | Cat. | O1 | O2 | O3 | O4 | O5 | O6 | O7 | O8 | O9 | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A01 | Propeller platform | A | ● | ◐ | · | ◐ | ● | · | ◐ | · | ◐ | 4 |
| A02 | Trimble Stratus | A | ● | · | · | · | ● | · | ◐ | · | · | 2.5 |
| A03 | DroneDeploy | A | ● | ◐ | · | · | ● | · | ◐ | ◐ | · | 3.5 |
| A04 | PIX4Dmatic + PIX4Dcloud | A | ● | · | · | · | ● | · | ◐ | · | · | 2.5 |
| A05 | Site Scan for ArcGIS / ArcGIS Flight | A | ● | · | · | · | ◐ | · | · | · | · | 1.5 |
| A06 | Virtual Surveyor | A | ◐ | · | · | · | ● | · | · | · | · | 1.5 |
| A07 | DatuBIM | A | ● | · | · | · | ● | · | ◐ | · | · | 2.5 |
| A08 | iHawk | A | ● | · | · | · | ◐ | · | · | · | · | 1.5 |
| A09 | OpenSpace | A | ● | · | · | · | ◐ | · | ◐ | · | · | 2 |
| A10 | iTwin Capture + Cesium ion | A | ● | · | · | · | ◐ | · | · | · | · | 1.5 |
| B01 | SYNCHRO 4D / SYNCHRO+ | B | ● | ◐ | ◐ | ◐ | ◐ | · | ◐ | ◐ | ◐ | 4.5 |
| B02 | Autodesk Forma Build | B | ◐ | · | · | ◐ | · | ◐ | ◐ | · | ◐ | 2.5 |
| B03 | Procore | B | ● | ◐ | · | ◐ | · | ◐ | ◐ | ◐ | ◐ | 4 |
| B04 | Oracle Primavera Cloud / P6 + Primavera Unifier | B | · | · | · | · | · | ◐ | ◐ | ◐ | ● | 2.5 |
| B05 | HxGN EcoSys / HxGN Smart Build Project Controls | B | · | · | · | · | · | ◐ | ◐ | ◐ | ● | 2.5 |
| B06 | InEight Plan & Progress + InEight Control | B | · | ◐ | · | ● | ◐ | ● | ● | ◐ | ● | 5.5 |
| B07 | Buildots | B | ◐ | ◐ | · | ◐ | · | · | ◐ | ◐ | · | 2.5 |
| B08 | Sablono | B | · | ◐ | · | ◐ | ◐ | · | ◐ | ◐ | · | 2.5 |
| B09 | Trimble WorksManager + Siteworks + B2W Track | B | ● | ◐ | ◐ | ◐ | ● | ◐ | ◐ | · | ◐ | 5 |
| C01 | Trimble Access Pipelines | C | · | · | ◐ | ◐ | ● | · | · | ◐ | · | 2.5 |
| C02 | ArcGIS Pipeline Referencing | C | ◐ | · | · | · | ◐ | · | · | · | · | 1 |
| C03 | Pipeline Enterprise | C | ◐ | · | ◐ | ◐ | ◐ | · | · | ◐ | · | 2.5 |
| C04 | Epilogue | C | ◐ | · | ◐ | ◐ | ◐ | · | ◐ | ◐ | ◐ | 3.5 |
| C05 | PCMS — Pipeline Construction Management System | C | ● | · | ◐ | ◐ | ◐ | · | ◐ | · | ◐ | 3.5 |
| C06 | Pipetrak IT | C | ◐ | · | ◐ | ◐ | ◐ | · | · | · | · | 2 |
| C07 | WeldEye | C | · | · | ● | · | · | · | · | ◐ | · | 1.5 |
| C08 | DATA 360 | C | · | · | ● | · | · | · | · | · | · | 1 |
| C09 | Vitruvi | C | ● | ◐ | ◐ | ● | ◐ | ◐ | ◐ | ◐ | ◐ | 5.5 |
| C10 | Aimsio | C | · | ◐ | ◐ | ● | ◐ | ● | ◐ | ◐ | ◐ | 5 |
| D01 | VisionLink | D | · | ◐ | ● | · | · | · | · | ◐ | · | 2 |
| D02 | My Komatsu | D | · | ◐ | ● | · | · | · | · | ◐ | · | 2 |
| D03 | MyLiebherr Maintenance & Performance | D | · | ◐ | ● | · | · | · | · | ◐ | · | 2 |
| D04 | Trackunit IrisX | D | · | ◐ | ● | · | · | · | · | ◐ | · | 2 |
| D05 | Tenna | D | · | ◐ | ● | · | · | · | · | ◐ | · | 2 |
| D06 | Hilti ON!Track | D | · | ◐ | ◐ | · | · | · | · | · | · | 1 |
| D07 | Spot-r | D | · | ◐ | ◐ | · | · | · | · | · | · | 1 |
| D08 | Evercam | D | ◐ | ● | ◐ | ◐ | · | · | · | · | · | 2.5 |
| D09 | VIDEO GUARD | D | ◐ | ◐ | ◐ | · | · | · | · | · | · | 1.5 |
| D10 | Bausicht | D | · | ◐ | ◐ | · | · | ◐ | · | ◐ | · | 2 |
| E01 | HCSS HeavyJob | E | · | ◐ | ◐ | ● | ◐ | ◐ | ◐ | ◐ | ◐ | 4.5 |
| E02 | Raken | E | · | · | · | ● | · | ◐ | · | · | · | 1.5 |
| E03 | Fieldwire by Hilti | E | · | · | · | ◐ | · | · | · | · | · | 0.5 |
| E04 | Capmo | E | · | · | · | ◐ | · | · | · | · | · | 0.5 |
| E05 | PlanRadar | E | · | · | · | ◐ | · | · | · | · | · | 0.5 |
| E06 | 123erfasst | E | · | ◐ | ◐ | ● | · | ◐ | · | · | · | 2.5 |
| E07 | ArcGIS Survey123 + ArcGIS Field Maps | E | ● | ◐ | ◐ | ◐ | · | ◐ | · | · | · | 3 |
| F01 | RIB iTWO / RIB 4.0 | F | · | · | · | · | ◐ | ● | ◐ | ◐ | ● | 3.5 |
| F02 | NEVARIS Build | F | · | · | · | ◐ | ◐ | ● | ◐ | ◐ | ◐ | 3.5 |
| F03 | MWM-Libero / Aufmaß365 / MWM-Ponto | F | · | · | · | · | ◐ | ● | ◐ | ◐ | · | 2.5 |
| F04 | ORCA AVA | F | · | · | · | · | · | ◐ | ◐ | · | · | 1 |
| F05 | California.pro | F | · | · | · | · | · | ◐ | ◐ | ◐ | · | 1.5 |
| F06 | BRZ 365 | F | · | · | · | ◐ | ◐ | ● | ◐ | ◐ | ◐ | 3.5 |
| F07 | Thinkproject CONTRACTS + CDE | F | · | · | · | · | · | ◐ | ◐ | ◐ | ● | 2.5 |
| F08 | Oracle Textura Payment Management | F | · | · | · | · | · | ◐ | ◐ | · | · | 1 |

**Coverage per objective (count of solutions):**

| Objective | Y | Partial | N | Best covered by |
|---|---|---|---|---|
| O1 | 15 | 9 | 30 | A01, A02, A03, A04, A05, A07, A08, A09 |
| O2 | 1 | 22 | 31 | D08 |
| O3 | 7 | 17 | 30 | C07, C08, D01, D02, D03, D04, D05 |
| O4 | 6 | 19 | 29 | B06, C09, C10, E01, E02, E06 |
| O5 | 8 | 19 | 27 | A01, A02, A03, A04, A06, A07, B09, C01 |
| O6 | 6 | 15 | 33 | B06, C10, F01, F02, F03, F06 |
| O7 | 1 | 27 | 26 | B06 |
| O8 | 0 | 27 | 27 | — |
| O9 | 5 | 12 | 37 | B04, B05, B06, F01, F07 |

**Reading the heat-map.**
- **O1 (map/model) and O5 (independent measurement)** are well served. Category A dominates, and the pilot already owns a strong O1/O5 tool (Propeller).
- **O3 (event-level tracking)** is served in silos: telematics events (D01–D05) and weld events (C07, C08).
- **O4 (daily production records)** and **O6 (subcontractor quantity tracking)** are served, but by *self-reported* capture: HeavyJob, Aimsio, Vitruvi, InEight, 123erfasst and the AVA tools.
- **O9 (EVM/claims foundation)** is served by enterprise controls (Unifier, EcoSys, InEight Control, RIB, Thinkproject).
- **O7** has only one "Y" (InEight). It compares claimed quantities with cost and hours, not with an independent measurement.
- **O8** has **no "Y" at all**. Every alerting capability found concerns schedule deviation, QA (certificate expiry, weld rejects) or equipment-hour exceptions. None concerns commercial deviation between independently measured, claimed and certified quantities, or duplicate claims.
- **O2** has a single "Y" (Evercam counts), and only for camera-covered fronts.

## 5. Gap analysis: what is covered and what is not

### 5.1 Covered by existing tools (buy or integrate)
| Need | Covered by | Comment |
|---|---|---|
| Daily orthophoto, DSM, volumes, cut-fill vs design along a corridor | Propeller (in use), DroneDeploy, Pix4D, DatuBIM | Mature. Do not rebuild (D-007) |
| Weld/joint traceability, tally, as-built weld survey, cover depth | Trimble Access Pipelines; Metegrity; Epilogue; WeldEye | The quantity *source of truth* for weld/NDT items (A-014) |
| Equipment hours, idle, location from OEM and retrofit devices | ISO 15143-3 feeds (Cat, Komatsu, Volvo per Komatsu list), Trackunit, Tenna | Standardised. Coverage depth varies by OEM |
| Foreman daily reports, time cards, LEMs, offline | HeavyJob, Aimsio, 123erfasst, Raken, Survey123 | Commodity. Choose by DE fit and offline |
| German AVA, REB/GAEB Aufmaß, invoicing, Nachträge | RIB iTWO/4.0, NEVARIS, MWM-Libero, BRZ | Mature and certified. Do not rebuild |
| 4D / EVM / enterprise controls | SYNCHRO, Unifier, EcoSys, InEight Control | Back-end targets for O9 |
| Site access and subcontractor compliance documents (MiLoG/AEntG) | Bausicht | Gate-based. Fragmented ROW fit unverified |

### 5.2 Not covered (the gap)
The scan found no product whose public documentation covers any of the following:

1. **Commercial reconciliation on a linear-referenced key.** There is no product that holds, for the same *KP section × activity × period × subcontractor*, all five of: **planned**, **independently measured** (drone/survey with stated uncertainty), **reported** (foreman), **claimed** (subcontractor) and **certified/invoiced** quantities. Nor is there one that computes the discrepancies against a contractual tolerance. Partial analogues exist:
   - InEight: claimed vs cost/hours;
   - B2W/Siteworks: measured vs field log, contractor-internal;
   - Unistal PCMS: design BOQ vs material consumed;
   - Propeller: design vs as-built surface.

   None closes the loop to the *subcontractor's* claim and the certificate.
2. **Measurement uncertainty as a commercial parameter.** No product documents carrying photogrammetric uncertainty (e.g. ± volume per section) into a certification decision. That means no rule of the form "accept the claim if it lies within measured ± U, otherwise escalate". This is the theoretical contribution in research_framing.md §6.
3. **Multi-source triangulation of presence against resource-based claims.** Telematics, check-in, vehicle GPS and camera counts are each available. The only documented cross-check against claims is HCSS's comparison of time-card hours with telematics hours for the *contractor's own* equipment. Nothing triangulates **subcontractor** daywork/standby/manpower claims against ≥ 2 independent presence signals at crew/front level (H5, field_sensing_layer.md §2). Nothing does it with privacy-by-design aggregation either.
4. **Duplicate and overlap detection across fronts and periods.** The scan found no product that documents detecting the same KP range or quantity claimed twice (across periods, crews or subcontractors), or a crew claimed at two fronts at once (AL-xx rules).
5. **Bridge from field evidence to German subcontract measurement.** The AVA tools accept REB/X31 measurement data. No field or drone tool documents *producing* a measured quantity as a GAEB X31/REB-compatible measurement record with an evidence pack attached (orthophoto tile, survey points, presence summary). The REB/X31 formats are fully specified, so the bridge is technically straightforward. But no product sold today offers it.
6. **Fragmented-front work-front registry.** Pipeline spreads run dozens of short-lived, dispersed fronts (tie-ins, crossings, HDD, reinstatement). Building-oriented progress AI (Buildots, OpenSpace) and gate-based access control (Bausicht) both assume a bounded site.

### 5.3 Is the gap real or an artefact of the method?
Three checks reduce the risk that the gap is just a gap in the search:
- **Targeted queries.** Queries naming the gap directly ("pipeline construction digital twin platform contractor", "measured vs claimed quantities") returned no integrated contractor product.
- **2026 consolidations.** All three moves (§3.7) stop short of subcontract certification.
- **Closest analogues.** The products nearest the gap (InEight, B2W/Siteworks, Vitruvi, Aimsio) document *their own* reconciliation scopes, and those scopes exclude independent measurement or subcontract claims.

The gap is still a *documented-capability* gap. Enterprise deployments with custom configuration (for example Unifier or EcoSys with bespoke business processes) may achieve parts of it. The demos planned in §9 test this.

## 6. Integration opportunities with the existing Propeller workflow
Design principle: **Propeller stays the measurement engine. SiteOps Twin is the commercial reconciliation layer.**

| Integration | Mechanism (documented) | SiteOps use | Risk / check |
|---|---|---|---|
| Orthophoto/DSM tiles in the SiteOps map | Propeller WMTS (Scale tier, third-party listing) or file export to COG | O1 base layer without re-processing | Confirm tier, licence terms for re-display, export formats (Q-005, A-041) |
| Section volumes and surfaces | Read-only Propeller API (Scale tier) or manual export (CSV/LandXML/DXF — formats to confirm) | O5 measured quantity per KP section, with flight timestamp | API read-only, so no write-back needed. Rate limits unknown |
| Design surfaces / alignment | Same alignment (LandXML) loaded in both Propeller and SiteOps | One location key (design principle 2) | Station equations, reroutes |
| Procore / HCSS connectors | Propeller already integrates natively with both | If the JV uses either, a single shared project ID simplifies joins | Check which ERP/PM the JV actually uses |
| As-built weld survey | Trimble Access Pipelines CSV/.map → SiteOps | Second independent witness for weld count, lowering-in, cover | Surveyor workflow ownership |
| Telematics | ISO 15143-3 pulls (Cat, Komatsu, others) + Trackunit/retrofit for hired plant | O2/O3 equipment hours, H5 | Liebherr LiDAT → MyLiebherr transition; OEM data depth |
| German AVA | Emit GAEB X31 / REB DA11 measurement files to RIB/NEVARIS/MWM | O6/O7 certified quantity hand-off with evidence pack link | Confirm which AVA the JV uses; BVBS certification not needed for import into a certified tool, but test round-trip |

## 7. Build vs buy vs integrate: implications for SiteOps Twin
| Layer | Decision | Rationale |
|---|---|---|
| UAV processing, volumes, 3D | **Integrate** (Propeller; Pix4D as fallback) | Mature, owned, out of scope (D-007) |
| Weld/NDT/QA records | **Integrate** (import from the QA system or Trimble Access) | Source of truth is the QA record |
| Telematics | **Integrate** via ISO 15143-3 + one mixed-fleet aggregator | Standard exists; no value in rebuilding |
| Daily reporting capture | **Buy or configure** (Survey123/ODK-style form, or a DE app such as 123erfasst) with a SiteOps schema; **build** only the thin structured form if no tool can emit the event model offline | Commodity UI; what matters is the data contract (KP, activity, crew, equipment, event time) |
| Presence sensing | **Buy** devices/services (check-in app, vehicle GPS, cameras with count-only output). **Build** only the aggregation and triangulation rules | Privacy-by-design aggregation is the differentiator, not the sensors |
| Linear-referenced data model, reconciliation engine, uncertainty-aware tolerance rules, commercial alerts (O5–O8), evidence pack, X31 export | **Build** (thesis artefact) | This is the documented gap (§5.2) |
| EVM, contract and claims management | **Integrate** (export to Unifier/EcoSys/RIB/Thinkproject) | O9 is a *data foundation*, not a new EVM tool |

**Commercial implication.** The MVP is a *thin, standards-based middle layer*:
- inputs: CSV + GeoPackage + COG, ISO 15143-3 JSON, LandXML alignment;
- outputs: GAEB X31 / CSV / OGC API–Features.

It sits between existing systems the JV already pays for. That keeps the business-case capex low (SC5) and avoids head-on competition with platform vendors whose product scope may grow into this space. The main strategic risk is a platform vendor adding a "measured vs claimed" feature. Procore + DroneDeploy is the most likely. The mitigations are:
- the German subcontract (REB/GAEB/VOB) specificity;
- linear referencing;
- uncertainty-aware rules;
- the privacy-by-design presence layer.

US-centric platforms do not currently document any of these.

## 8. Positioning statement
> *For commercial and project-controls teams of onshore pipeline contractors who must certify subcontractor quantities and resource claims along a linear spread, SiteOps Twin is a linear-referenced reconciliation layer. It combines daily UAV measurement (with its uncertainty), structured field reports, telematics and privacy-preserving presence signals, and it compares planned, measured, claimed, certified and invoiced quantities per KP section. Reality-capture platforms (Propeller, DroneDeploy) measure what was built. Construction-management platforms (Procore, InEight, HCSS) record what crews report. German AVA tools (RIB, NEVARIS, MWM) bill what is entered. SiteOps Twin tests the claim against independent evidence before certification, and hands the result to the existing AVA as a standard GAEB X31/REB measurement with a traceable evidence pack.*

**Research gap (for Ch. 2).** The commercial market offers mature point solutions for each data stream. It offers no documented solution that:
- (i) reconciles subcontractor claims against independently measured quantities on a linear-referenced key;
- (ii) treats measurement uncertainty as a contractual tolerance;
- (iii) triangulates resource-based claims with multiple presence signals under GDPR/works-council constraints.

This matches the gap hypotheses in `02_literature_review/gap_hypotheses.md`, which the SLR must confirm on the academic side.

## 9. German-market specifics
- **GDPR (EU 2016/679) and BDSG §26** (its role as a lawful basis is qualified since CJEU C-34/21, 2023; legal review required). Personnel presence data is personal data. Several things are needed for tracking:
  - a lawful basis;
  - a DPIA (Art. 35), required for systematic monitoring of employees;
  - data minimisation (crew/front counts for commercial users, as in D-069);
  - processor agreements (AVV, Art. 28) with every SaaS vendor.

  Vendor hosting evidence found:

  | Vendor | Hosting evidence | Source type |
  |---|---|---|
  | Procore | EU Application Zone hosted in Germany | vendor |
  | Autodesk | Germany storage for Forma Build | vendor |
  | AddSecure/Telekom | video processed in Germany | vendor |
  | Capmo | servers in Germany | reseller statement |

  For most other vendors, including Propeller, DroneDeploy, Trackunit and Evercam, residency was **not stated** in the sources reviewed and must be requested. US-owned vendors also raise third-country transfer questions (SCCs / EU–US Data Privacy Framework status to be checked at contract stage).
- **Works council (Betriebsverfassungsgesetz §87(1) no. 6).** Introducing technical devices *suitable* for monitoring employee behaviour or performance requires co-determination. Each of the following needs a works agreement (Betriebsvereinbarung) covering purpose limitation, aggregation level, retention and access:
  - telematics with operator attribution;
  - check-in apps;
  - camera counts;
  - wearables (e.g. Spot-r, now owned by a biometric access-control company).

  For **subcontractor** personnel, the JV's own works council is not the co-determining body. The subcontract must still impose equivalent transparency, and the subcontractor's own works council may be involved. Field_sensing_layer.md §6 already reflects this.
- **Subcontractor compliance (MiLoG, AEntG, SOKA-BAU, customs inspections).** German sites already have to evidence who worked and was paid the minimum wage. Tools such as Bausicht and 123erfasst show that *compliance-driven* attendance data exists and is accepted. Re-using it as an aggregated *commercial* signal is a lower-friction path than new tracking. The purpose change still needs a legal check.
- **GAEB / REB / VOB.**
  - VOB/B §14 requires prüfbare Abrechnung (verifiable billing) with measurement evidence.
  - REB 23.003 (1979/2009) and GAEB X31 define the measurement-data exchange.
  - BVBS certifies GAEB interfaces (RIB 4.0 AVA, 2026; MWM-Libero for Mengenermittlung).

  SiteOps Twin should emit measured quantities as X31/REB records and attach the evidence pack by reference. That respects the "commercial ritual" of the joint measurement (gemeinsames Aufmaß) instead of bypassing it (practice rule 4).
- **Infrastructure precedent.** The Deutsche Bahn–Datumate framework shows German public infrastructure clients accept drone-based progress monitoring. RIB's 2026 road-construction package shows German AVA vendors investing in linear infrastructure.

## 10. Limitations and next steps
1. **Verify the decision-relevant rows** by direct page review or demo before the thesis is submitted. Priority order:
   - Propeller API/WMTS tier and export formats;
   - InEight claiming workflow;
   - Trimble B2W/Siteworks reconciliation;
   - Vitruvi and Aimsio (any independent-measurement feature?);
   - Procore + DroneDeploy roadmap on quantities;
   - the JV's own AVA (RIB/NEVARIS/BRZ) X31 import.

   Log each result in the screening log with the date and evidence grade.
2. **Hands-on tests** in the prototype phase:
   - an ISO 15143-3 sample pull from one OEM;
   - X31 round-trip into the JV's AVA;
   - Propeller export of a KP-section volume.
3. **Re-run the scan** before submission, because consolidation is ongoing (§3.7).
4. **Do not cite vendor claims as findings.** In the thesis, cite this scan as "documented capability as of 2026-11-23".

## 11. References (URLs consulted, accessed 2026-11-23)
Each URL was returned by the web search tool on 2026-11-23 and read through the tool's page extract (see §2.5). The catalogue ID in brackets links each URL to its row in `solutions_catalogue.csv`.

1. [A01] https://www.propelleraero.com/blog/api-integration-for-efficient-project-management/ (accessed 2026-11-23)
2. [A01] https://www.propelleraero.com/blog/propeller-acquires-spacesium/ (accessed 2026-11-23)
3. [A01] https://www.propelleraero.com/workflows/construction-progress-tracking-workflow/ (accessed 2026-11-23)
4. [A01] https://www.capterra.com/p/179319/Propeller-Platform/ (accessed 2026-11-23)
5. [A01] https://datadrivenaec.com/tools/propeller-aero (accessed 2026-11-23)
6. [A02] https://www.propelleraero.com/blog/introducing-trimble-stratus-powered-by-propeller/ (accessed 2026-11-23)
7. [A02] https://www.khl.com/news/Trimble-s-drone-based-tech-for-construction/1146125.article (accessed 2026-11-23)
8. [A03] https://www.constructiondive.com/news/punch-list-procore-closes-deal-jacobs-wins-skanska-granite/830146/ (accessed 2026-11-23)
9. [A03] https://www.sec.gov/Archives/edgar/data/0001611052/000162828026051460/pcor-20260630.htm (accessed 2026-11-23)
10. [A03] https://aecmag.com/news/procore-agrees-to-acquire-dronedeploy-for-845m (accessed 2026-11-23)
11. [A03] https://www.autodesk.com/integrations/partner/dronedeploy (accessed 2026-11-23)
12. [A03] https://dronedeploy.com/blog/ai-construction-software-that-tracks-progress-without-adding-work (accessed 2026-11-23)
13. [A04] https://www.pix4d.com/discover-pix4dcloud/ (accessed 2026-11-23)
14. [A04] https://www.pix4d.com/industry/construction (accessed 2026-11-23)
15. [A04] https://www.pix4d.com/blog/drone-driven-construction-monitoring-PIX4Dcloud/ (accessed 2026-11-23)
16. [A05] https://support.esri.com/en-us/knowledge-base/deprecation-site-scan-flight-for-arcgis-limited-edition-000034234 (accessed 2026-11-23)
17. [A05] https://www.esri.com/en-us/arcgis/products/site-scan-for-arcgis (accessed 2026-11-23)
18. [A05] https://community.esri.com/t5/site-scan-blog/deprecation-notice-for-recap-mesh-processing-in/ba-p/1329736 (accessed 2026-11-23)
19. [A06] https://virtual-surveyor.com/ (accessed 2026-11-23)
20. [A06] https://www.gim-international.com/content/news/virtual-surveyor-now-processes-larger-drone-survey-projects (accessed 2026-11-23)
21. [A07] https://www.gim-international.com/content/news/datumate-wins-deutsche-bahn-tender-award-for-monitoring-railway-infrastructure-projects (accessed 2026-11-23)
22. [A07] https://www.constructiondive.com/press-release/20260828-datumate-launches-datubim-progress-tracking-1/ (accessed 2026-11-23)
23. [A07] https://www.deutschebahn.com/en/Digitalization/startups/db_startups/Datumate-6935340 (accessed 2026-11-23)
24. [A08] https://jpt.spe.org/cyberhawk-secures-5-year-multimillion-dollar-software-contract-shell (accessed 2026-11-23)
25. [A08] https://dronelife.com/2026/09/08/bechtel-cyberhawk-drone-construction-monitoring/ (accessed 2026-11-23)
26. [A09] https://www.openspace.ai/products/air/ (accessed 2026-11-23)
27. [A09] https://www.openspace.ai/products/clearsight/ (accessed 2026-11-23)
28. [A09] https://support.openspace.ai/en/articles/6617755-release-notes (accessed 2026-11-23)
29. [A10] https://www.bentley.com/en/news/bentley-cesium-reality-modeling-geospatial-infrastructure-2025/ (accessed 2026-11-23)
30. [B01] https://www.bentley.com/pds-synchro-4d-product-ltr-en (accessed 2026-11-23)
31. [B01] https://www.bentley.com/en/blog/bentley-unveils-synchro-at-yii-2025-ushering-in-a-new-era-of-ai-powered-4d-construction-planning/ (accessed 2026-11-23)
32. [B01] https://www.bentley.com/en/blog/yii-project-profile-italferr-builds-italys-first-strategic-digital-site-with-synchro/ (accessed 2026-11-23)
33. [B02] https://www.autodesk.com/blogs/construction/closer-to-home-now-you-can-store-build-takeoff-and-estimate-project-data-in-the-uk-germany-india-japan-and-canada/ (accessed 2026-11-23)
34. [B02] https://help.autodesk.com/cloudhelp/ENU/Docs-About-ACC/files/Regional_Data_Storage.html (accessed 2026-11-23)
35. [B02] https://www.autodesk.com/trust/availability (accessed 2026-11-23)
36. [B03] https://www.procore.com/whats-new/eu-application-zone (accessed 2026-11-23)
37. [B03] https://v2.support.procore.com/en-gb/faq-where-and-how-does-procore-store-customer-information (accessed 2026-11-23)
38. [B03] https://www.procore.com/press/dronedeploy-launches-ground-pro-bringing-measurable-3d-records-into-procore (accessed 2026-11-23)
39. [B04] https://www.oracle.com/industries/construction-engineering/unifier-asset-lifecycle-management/ (accessed 2026-11-23)
40. [B04] https://www.oracle.com/uk/construction-engineering/primavera-unifier-project-controls-asset-management/advanced-work-packaging-tour/ (accessed 2026-11-23)
41. [B05] https://hexagon.com/products/ecosys (accessed 2026-11-23)
42. [B05] https://hexagon.com/solutions/earned-value-performance-management (accessed 2026-11-23)
43. [B05] https://hexagon.com/products/hxgn-smart-build-project-controls (accessed 2026-11-23)
44. [B06] https://learn.ineight.com/integrated_solutions/Content/Business-Processes/Earned-Value-Management/Imported/sample_styling.htm (accessed 2026-11-23)
45. [B06] https://ineight.com/products/ineight-plan-and-progress/ (accessed 2026-11-23)
46. [B07] https://siliconangle.com/2026/09/14/buildots-raises-130-million-to-expand-ai-powered-construction-platform/ (accessed 2026-11-23)
47. [B07] https://www.prnewswire.com/news-releases/buildots-commercializes-genda-under-the-buildots-field-brand-on-track-to-bring-field-operations-into-its-construction-intelligence-platform-302826272.html (accessed 2026-11-23)
48. [B07] https://buildots.com/buildots-field/ (accessed 2026-11-23)
49. [B08] https://www.sablono.com/en/solutions/sectors/infrastructure-construction (accessed 2026-11-23)
50. [B08] https://sablono.com/customers/case-study/qenergy (accessed 2026-11-23)
51. [B08] https://www.rolandberger.com/en/Insights/Publications/Interview-with-Sablono-GmbH.html (accessed 2026-11-23)
52. [B09] https://www.equipmentworld.com/technology/article/15744618/trimble-b2w-integration-automates-production-quantity-tracking (accessed 2026-11-23)
53. [B09] https://help.fieldsystems.trimble.com/worksmanager/release-notes-q1-2026.htm (accessed 2026-11-23)
54. [B09] https://news.trimble.com/2025-04-24-Trimble-Expands-Field-to-Office-Connectivity-for-Heavy-Civil-Contractors (accessed 2026-11-23)
55. [C01] https://help.fieldsystems.trimble.com/trimble-access/latest/en/pipelines/pipelines-introduction.htm (accessed 2026-11-23)
56. [C01] https://geospatial.trimble.com/en/products/software/trimble-access-pipelines (accessed 2026-11-23)
57. [C02] https://www.esri.com/en-us/arcgis/products/arcgis-pipeline-referencing/overview (accessed 2026-11-23)
58. [C02] https://www.esri.com/en-us/arcgis/products/arcgis-pipeline-referencing/pricing (accessed 2026-11-23)
59. [C02] https://pro.arcgis.com/en/pro-app/help/data/location-referencing-pipelines/get-started-with-arcgis-pipeline-referencing.htm (accessed 2026-11-23)
60. [C03] https://metegrity.com/pipeline-enterprise/features (accessed 2026-11-23)
61. [C03] https://pipeline-journal.net/news/metegritys-pipeline-enterprise-software-captures-digital-data-accelerates-production-north (accessed 2026-11-23)
62. [C03] https://www.worldpipelines.com/equipment-and-safety/20112017/metegrity-releases-new-version-of-pipeline-software (accessed 2026-11-23)
63. [C04] https://projectconsulting.com/epilogue/pipelines-facilities (accessed 2026-11-23)
64. [C04] https://projectconsulting.com/cats (accessed 2026-11-23)
65. [C05] https://unistal.com/pipeline-construction/ (accessed 2026-11-23)
66. [C05] https://unistal.com/assets/img/Unistal-(PCMS-Brochure).pdf (accessed 2026-11-23)
67. [C05] https://proceedings.esri.com/library/userconf/proc11/abstracts/a3806.html (accessed 2026-11-23)
68. [C06] https://www.esri.com/partners/petro-it-usa-inc-a2T5x000006Qir0EAC/pipetrak-it-a2d5x000003kf5wAAA (accessed 2026-11-23)
69. [C06] https://apps.apple.com/at/app/pipetrak-it/id1273712434?l=en-GB (accessed 2026-11-23)
70. [C07] https://www.kemppi.com/en/blogs/how-weldeye-sets-the-standard-for-welding-traceability (accessed 2026-11-23)
71. [C08] https://pgjonline.com/magazine/2026/june-2026-vol-253-no-6/partner-perspectives/turning-critical-infrastructure-data-into-long-term-intelligence (accessed 2026-11-23)
72. [C09] https://www.esri.com/partners/vitruvi-software-inc-a2T5x000009ChyUEAS/vitruvi-web-a2d5x000004Sn7mAAC (accessed 2026-11-23)
73. [C09] https://www.g2.com/products/vitruvi-software/reviews (accessed 2026-11-23)
74. [C10] https://aimsio.com/industries/pipeline-construction/ (accessed 2026-11-23)
75. [C10] https://aimsio.com/industries/oilfield-construction/ (accessed 2026-11-23)
76. [C10] https://aimsio.com/features/tickets/ (accessed 2026-11-23)
77. [D01] https://digital.cat.com/node/7281 (accessed 2026-11-23)
78. [D01] https://aem.org/standards/iso15143/3 (accessed 2026-11-23)
79. [D02] https://www.komatsu.com/en/newsroom/2022/my-komatsu-telematics-data/ (accessed 2026-11-23)
80. [D02] https://www.forconstructionpros.com/construction-technology/equipment-monitoring-logistics/article/22197990/komatsu-america-corp-my-komatsu-achieves-aemp-20iso-151433-interoperability (accessed 2026-11-23)
81. [D03] https://www.liebherr.com/en-au/earthmoving/services/customer-service/myliebherr-performance-4868955 (accessed 2026-11-23)
82. [D03] https://intercom.help/equipmentshare/en/articles/13133566-liebherr-integration-with-t3 (accessed 2026-11-23)
83. [D04] https://trackunit.com/irisx (accessed 2026-11-23)
84. [D04] https://developers.trackunit.com/docs/reference/getting-started/iris-api-overview/ (accessed 2026-11-23)
85. [D05] https://www.tenna.com/?p=218044 (accessed 2026-11-23)
86. [D05] https://www.tenna.com/blog/best-construction-telematics-software (accessed 2026-11-23)
87. [D06] https://www.hilti.com/ontrack (accessed 2026-11-23)
88. [D06] https://www.hilti.co.uk/content/hilti/E1/GB/en/business/business/equipment/on-track.html (accessed 2026-11-23)
89. [D07] https://securityjournalamericas.com/invixium-triax-technologies-critical/ (accessed 2026-11-23)
90. [D07] https://en.wikipedia.org/wiki/Triax_Technologies (accessed 2026-11-23)
91. [D08] https://cordis.europa.eu/project/id/889670 (accessed 2026-11-23)
92. [D08] https://en.wikipedia.org/wiki/Evercam (accessed 2026-11-23)
93. [D08] https://www.cita.ie/wp-content/uploads/2026/05/Beyond-Visibility-Evercam-_-CitA-AI-on-Site.pdf (accessed 2026-11-23)
94. [D09] https://iot.telekom.com/en/blog/video-guard-construction-site-monitoring-with-iot-and-ai (accessed 2026-11-23)
95. [D10] https://bausicht.com/en/product/digital-access-control/ (accessed 2026-11-23)
96. [D10] https://www.bauindustrie-bayern.de/fileadmin/Webdata/Themen/20260709_Innovationstalk/Bausicht_Praesentation_copy.pdf (accessed 2026-11-23)
97. [E01] https://hcss.com/heavyjob (accessed 2026-11-23)
98. [E01] https://hcss.com/products/field-productivity-tracking/ (accessed 2026-11-23)
99. [E01] https://www.hcss.com/press/nemetschek-group-completes-hcss-acquisition/ (accessed 2026-11-23)
100. [E01] https://www.constructiondive.com/news/nemetschek-group-acquires-hcss-contech-merger-acquisition/817673/ (accessed 2026-11-23)
101. [E02] https://www.rakenapp.com/features/daily-progress-reporting (accessed 2026-11-23)
102. [E02] https://www.autodesk.com/integrations/partner/raken (accessed 2026-11-23)
103. [E03] https://www.fieldwire.com/de/lp/baustellenmanagement-software (accessed 2026-11-23)
104. [E03] https://www.g2.com/compare/fieldwire-by-hilti-vs-raken (accessed 2026-11-23)
105. [E04] https://www.capmo.com/en/loesungen/bautagebuch-fotos (accessed 2026-11-23)
106. [E04] https://www.capmo.com/en/loesungen/api-integrationen (accessed 2026-11-23)
107. [E04] https://www.heinze.de/apps/capmo-baumanagement/22319422/ (accessed 2026-11-23)
108. [E05] https://www.ki-syndikat.de/baudokumentation-apps-vergleich/ (accessed 2026-11-23)
109. [E05] https://apps.apple.com/at/app/planradar-die-baustellen-app/id720159081 (accessed 2026-11-23)
110. [E06] https://www.softguide.de/programm/123erfasst (accessed 2026-11-23)
111. [E06] https://www.baulinks.de/bausoftware/2017/0061.php4 (accessed 2026-11-23)
112. [E07] https://www.esri.com/en-us/arcgis/products/arcgis-survey123/overview (accessed 2026-11-23)
113. [E07] https://doc.arcgis.com/en/arcgis-solutions/latest/reference/use-stormwater-construction-activity-management.htm (accessed 2026-11-23)
114. [F01] https://www.rib-software.com/pdf/de/rib-itwo-broschuere-ava-planen-projektsteuerung.pdf (accessed 2026-11-23)
115. [F01] https://www.baulinks.de/webplugin/2026/1443.php4 (accessed 2026-11-23)
116. [F01] https://www.baulinks.de/webplugin/2026/1562.php4 (accessed 2026-11-23)
117. [F02] https://nevaris.com/wp-content/uploads/2023/09/nevaris_build_produktbroschuere_2024.pdf (accessed 2026-11-23)
118. [F02] https://www.allplan.com/fileadmin/user_upload/countries/germany/pdfs/products/Funktionsumfang_NEVARIS_Build_ab_2020.pdf (accessed 2026-11-23)
119. [F03] https://www.baulinks.de/bkd_file/mwm-software/MWM_Libero_20260921.pdf (accessed 2026-11-23)
120. [F03] https://www.baulinks.de/bkd_file/mwm-software/MWM_Aufmass365_20260921.pdf (accessed 2026-11-23)
121. [F03] https://www.baulinks.de/bausoftware/2014/0059.php4 (accessed 2026-11-23)
122. [F04] https://www.softguide.de/programm/orca-ava-ausschreibungsprogramm-software (accessed 2026-11-23)
123. [F04] https://orca-software.com/wp-content/uploads/Seminar-Abrechnung-Nachtraege.pdf (accessed 2026-11-23)
124. [F05] https://www.baulinks.de/bausoftware/2017/0094.php4 (accessed 2026-11-23)
125. [F06] https://www.softguide.de/programm/brz-365 (accessed 2026-11-23)
126. [F06] https://portal.brz365.eu/online-hilfe/reb-mengenermittlung/grundlagen (accessed 2026-11-23)
127. [F07] https://www.thinkproject.com/products/contracts/ (accessed 2026-11-23)
128. [F07] https://www.thinkproject.com/lp/thinkproject-contracts-cde/ (accessed 2026-11-23)

**Supplementary context sources (standards, interoperability, research; not catalogue rows):**
- https://www.proemion.com/en/resources/knowledge/white-paper/aemp-whitepaper.html (AEMP/ISO 15143-3 coverage limits)
- https://www.komatsu.com/en/newsroom/2022/my-komatsu-telematics-data/ (list of ISO 15143-3-compliant OEMs)
- https://pygaeb.readthedocs.io/en/latest/guides/quantity-phases/ (GAEB X31 role: measurement rows per REB 23.003 referencing an external BoQ)
- https://portal.brz365.eu/online-hilfe/reb-mengenermittlung/grundlagen (REB 23.003 1979 vs 2009)
- https://rosap.ntl.bts.gov/view/dot/89391/dot_89391_DS1.pdf (Missouri DOT 2026: privacy-preserving site-level worker presence)
- https://www.itcon.org/papers/2025_56-ITcon-Khazen.pdf (BLE RTLS for construction; BLE vs UWB accuracy)
- https://www.tandfonline.com/doi/pdf/10.1080/27525783.2026.2639891 (2026 pipeline digital-twin paper: construction records as static inputs)
- https://www.nemetschek.com/en/news-media/successful-first-half-2026 (Nemetschek H1 2026, HCSS)
- https://www.tradingview.com/news/tradingview:e7eea1d9c80d8:0-procore-completes-845m-cash-acquisition-of-dronedeploy/ (Procore–DroneDeploy completion)

**Legal and normative background (not market sources; cite the primary texts in the thesis):** GDPR (EU) 2016/679, Art. 28 and Art. 35; BDSG §26; CJEU C-34/21 (2023); BetrVG §87(1) no. 6; VOB/B §14; REB-Verfahrensbeschreibung 23.003; GAEB DA XML 3.3; ISO 15143-3; MiLoG; AEntG.
