# Drone Measurement Reports – As-Is Analysis (DRN-1 … DRN-3)

**Owner:** gis-engineer + data-engineer. **Version:** 0.1. **Status:** draft for review by the field-operations-specialist and the drone/survey team.
**Supports:** RQ1, H1; epics E4 (drone ingest) and E5 (reconciliation). Builds on `04_to_be_architecture/geospatial/quantity_measurability_matrix.md` (methods, σ, status rule) and the `drone_flight` / `measurement` tables in `prototype/siteops/db.py`. It does not change either.
**Confidentiality:** Anonymised. The contractor logo, project label, people (shown by role only), the UTM zone, absolute elevations and the platform deep links are **not** reproduced. The reports contain no planimetric coordinates. Plan-sheet codes (G102, G113, G114) are kept because they are the location key being analysed. Quantities here are rounded; exact values are in the git-ignored `data/private/drone_reports_extract.json`.

Legend: [F] read from the document · [C] computed by us · [I] interpretation · [A] assumption · [VERIFY] to confirm with the drone team.

| ID | Plan sheet | Surveyed (flight) | Measurements digitised | Report generated | Pages | Subject |
|---|---|---|---|---|---|---|
| DRN-1 | G102 | 2026-09-07 | +1 day | +73 days | 8 | Launch and receiving pits of a trenchless road crossing |
| DRN-2 | G113 | 2026-09-28 | +2 days | +50 days | 6 | Shored excavation at a bend, pipe lowered in |
| DRN-3 | G114 ("HDD exit side"; measurement labelled G113) | 2026-03-18 | +244 days | +244 days | 4 | HDD rig site, width of the rig anchor ("deadman") |

All 18 pages were read (8 + 6 + 4). No page was unreadable.

---

## 1. Profiles

### Common format (all three reports) [F]

- **Producer.** Standard "Measurement Report" of the Propeller web platform, printed to PDF from a Chromium-based browser. Report preparer = a drone/survey team member; the measurements in DRN-1/2 were digitised by a second operator, in DRN-3 by the preparer.
- **Structure.** (1) Cover: project label, "Surveyed <date>", CRS statement, "Prepared by <role> <date>", QR code / "View in Propeller" link. (2) Overview: a cropped orthophoto with the measured lines drawn in yellow and numbered. (3) A **DISTANCE** table: legend number, free-text measurement name, horizontal distance and max/min elevation (DRN-3: terrain, horizontal and slope distance). (4) One card per measurement: orthophoto crop, name, created date, creator, values, deep link.
- **CRS.** "ETRS89 / UTM zone *nn*N (N-E)": a projected ETRS89-based UTM system, which matches our CRS policy. The "(N-E)" label shows northing-first **display** order; the EPSG definition is easting-first, so axis order must be fixed explicitly on ingest [I]. **No vertical datum or geoid model is stated** [F]. The elevation magnitudes suggest German normal heights (DHHN2016) [I, VERIFY].
- **Accuracy information: none** [F]. No GSD, GCP count, checkpoint RMSE, PPK/RTK statement or survey accuracy report.
- **No KP/chainage, no design alignment, no design-vs-as-built comparison, no depth-of-cover requirement, no compliance indicator, no volumes, no cross-sections or profiles** [F].
- **Measurement types used.** Only (a) **polyline distances** along pit/trench edges and (b) **short "depth" lines** whose max and min elevation on the surface model are read off. No points, polygons, areas, volumes, surface comparisons or design overlays.
- **Totals row.** The table automatically sums all horizontal distances, including opposite edges of the same pit and edges of different pits. The total is **physically meaningless** and must never be ingested as a quantity [C].
- **Per date, not cumulative.** Each report is a snapshot of one survey. There is no link to earlier flights and no progress-to-date figure.
- **Exports.** No export format is mentioned. The only data path is the platform deep link [F]. The platform's general export options (CSV/DXF/GeoJSON of measurements, GeoTIFF orthophoto/DEM, point cloud, volume and design-comparison reports) are **not** evidenced in these documents [VERIFY].

### DRN-1 – G102, trenchless road-crossing pits

- **Scene [I].** A road crossing under a junction/roundabout. On one side there is an elongated, shored **launch ("entry") pit** with timber struts and the pipe inside. On the other side there is a near-square **receiving ("exit") pit** with shoring, pump hoses and the pipe end. The overview also shows a road, a cycle path, parked trucks and a site container.
- **Measured [F].** Nine items: four entry-pit edges, three exit-pit edges (named "length front/left/right"), and one "depth" line in each pit.
- **Quantities [F, rounded].** Entry pit ≈ 24 m × 6 m; exit pit ≈ 6 m × 6 m; entry depth ≈ 3.8 m, exit depth ≈ 5.7 m (as max − min elevation).
- **Derived [C].** Plan areas ≈ 140 m² and ≈ 36 m². Indicative prismatic volumes (area × single-line depth, vertical walls) ≈ 540 m³ and ≈ 200 m³. Opposite edges agree within 2–6 cm. The pit-floor levels of the two pits agree within ≈ 7 cm, a plausible common invert. The rim levels differ by ≈ 1.8 m: real terrain difference, or the "max" was picked on spoil, a waling beam or a fence [VERIFY].
- **Not measured.** The **crossing length** (distance between the pits / along the bore) and the cover above the bore under the road. The report does not say whether "min" is the pit floor, the top of the pipe or a water surface.
- **Naming.** "entry … / length …" are mixed. The exit pit is only recognisable from the image [I].

### DRN-2 – G113, shored excavation at a bend

- **Scene [I].** An L-shaped open excavation at a horizontal change of direction, with cross-struts/walings and a large-diameter pipe lowered in. Pumps/generators, hoses, an excavator and big bags sit alongside. It is probably a tie-in or bend pit, possibly next to the crossing that spans G113/G114 [I].
- **Measured [F].** Left edge in two parts and right edge in two parts (split where a strut or walkway interrupts the edge), plus one depth line at the trench wall next to the pipe.
- **Quantities [F, rounded].** Left edge ≈ 19 m in total; right (outer) edge ≈ 29 m in total; depth ≈ 5.1 m.
- **Derived [C].** The left/right difference (≈ 10 m) is the inner vs outer side of the bend plus gaps. A **trench length along the centreline cannot be derived** from edge lines. The total row (≈ 47 m) double-counts.
- **Time window.** The flight caught **pipe-in-open-trench** (after lowering-in, before backfill). This is exactly the window the matrix classes as "Time-window" for TRN/LOW, and the only window in which a top-of-pipe level, and so cover, could be measured from the air.

### DRN-3 – G114 "HDD exit side", rig anchor width

- **Scene [I].** An HDD work site on temporary ground mats: a drill rig with rod rack, containers, mud tanks and a shored pit with drilling fluid at the rig front. The single measurement spans the rig **deadman** (anchor/thrust block).
- **Measured [F].** One line: horizontal ≈ 5.3 m, slope ≈ 5.3 m, terrain ≈ 5.8 m. Terrain distance follows the surface over the structure; for quantities, horizontal distance is the relevant value [I].
- **Label inconsistency [F].** The file name says G114 / exit side, but the measurement is named "G113 deadman". A drilling rig normally stands at the **entry** side [I]. Both points must be checked [VERIFY]. A CP subcontractor record (batch 3, RPT-K) references a crossing object at "G113/114", which is consistent with a crossing spanning both sheets [I].
- **Retrospective measurement.** The line was digitised **eight months after the flight**, on the day the report was generated. Archived surveys can therefore be re-measured later as evidence. However, **measurement date ≠ survey date**: the survey date is the date the quantity refers to.
- **No HDD quantity.** The report gives no drilled length, no entry/exit point positions, no pit dimensions and no pull-back status. As the matrix states, HDD stays log-verifiable; the drone only gives the site location and the state of the site.

---

## 2. Capability: activity × report

Can the report, **as delivered**, independently verify the activity? Then: what could the **same flight** verify with a proper export? The σ values are our assumptions [A], because the reports state no accuracy. Defaults follow the matrix: σxy ≈ 2–3 cm and σz ≈ 3–5 cm on open ground with GCP/PPK. Depth inside narrow, shored pits is worse (occlusion, struts, shadow, water): **σ_depth ≈ 0.10–0.30 m, default 0.15 m**.

| Activity | DRN-1 (G102) | DRN-2 (G113) | DRN-3 (G114) | Same flight, with a proper export | Indicative σ |
|---|---|---|---|---|---|
| CLR – clearing / topsoil | ✗ not measured | ✗ | ✗ | ROW polygon area / length from orthophoto | length ±0.5 m + 0.2 %; area ±1–2 % |
| GRD – grading | ✗ | ✗ | ✗ (mat-covered pad visible) | Area; cut/fill only with pre-grade baseline DSM | volume σV ≈ A·σΔz (correlated) |
| STR – stringing | ✗ | ✗ | ✗ | Joint count / string length if flown before welding | ±1 joint |
| TRN – trenching (length) | ✗ (pits only) | ◐ edge lengths of one excavation, no centreline | ✗ | Centreline polyline of the open trench, snapped to KP | ±0.1 m per end |
| TRN – excavation depth / volume | ◐ two single-point depths; volume only indicative [C] | ◐ one single-point depth | ✗ | DSM-difference volume vs graded surface; depth profile along the centreline | depth ±0.15 m; volume ±5–10 % in pits |
| LOW – lowering-in | ◐ pipe visible in both pits (qualitative) | ◐ pipe in open trench visible (qualitative) | ✗ | Pipe polyline in trench + **top-of-pipe (TOP) points** → length lowered, as-built TOP levels | TOP z ±0.05–0.10 m where the crown is visible |
| BKF – backfill | ✗ (open) | ✗ (open) | ✗ | Closed-trench length; finished-ground level for cover | length ±0.5 m |
| RST – reinstatement | ✗ | ✗ | ✗ (temporary mats in place) | Reinstated area polygon | ±1–2 % |
| Crossings (open-cut / trenchless) | ◐ pit dimensions and existence; **no crossing length** | ◐ possibly crossing-adjacent pit | ✗ | Pit polygons + launch/receive points → straight-line crossing length; plausibility vs crossing record | ±0.1 m (plan) |
| HDD | ✗ | ✗ | ◐ site/rig presence, anchor width; **no drilled length** | Entry/exit point positions and pit areas only; drilled length stays log-based | n/a (log) |
| Depth of cover | ✗ (no TOP point, no reference ground) | ✗ (depth line at wall, target not stated) | ✗ | Cover = finished (or design) ground − TOP, from a flight before backfill + a flight after reinstatement | σ_cover ≈ √(σ_TOP² + σ_ground²) ≈ 0.07–0.15 m |
| Excavation pits (bellholes, tie-in, crossing pits) as BoQ items | ◐ dims + depth → indicative m³ | ◐ edges + depth | ✗ | Polygon + DSM volume per pit | ±5–10 % |

✓ verifiable · ◐ partial / indicative only · ✗ not covered.

**Bottom line.** As delivered, the three reports verify **no BoQ activity** to reconciliation grade. They give **ad-hoc dimensional evidence** (pit sizes and depths, an anchor width) that supports a dispute or a variation, not the routine `measured` quantity per section and activity. The underlying flights could do much more (TRN length, LOW length, TOP levels, cover, pit volumes), provided the measurements are taken systematically and exported in a machine-readable form.

---

## 3. Gaps for automated reconciliation

| # | Gap | Effect on SiteOps Twin | Severity |
|---|---|---|---|
| G1 | **No machine-readable quantities**: browser-printed PDF only; free-text names; meaningless total row | Needs PDF/OCR parsing and manual interpretation; the risk of ingesting the total is high | High |
| G2 | **No accuracy metadata** (GSD, GCP/checkpoints, RMSE, PPK/RTK) | `drone_flight` accuracy fields stay NULL; σ cannot be computed per the matrix §4, so the status rule falls back to assumed σ or `UNVERIFIABLE` | High |
| G3 | **No vertical datum / geoid** | Elevations cannot be compared with design levels or GNSS as-built data without risking a datum offset | High for levels/cover |
| G4 | **No KP / chainage, no geometry export** (no coordinates in the report at all) | Cannot snap to the alignment, assign `section_id` or split by section; the plan sheet is the only location key | High |
| G5 | **No activity semantics**: names say "entry front", "length (1)", "deadman"; no link to BoQ item, activity or crossing ID | Activity mapping is manual and ambiguous | High |
| G6 | **No design reference**: no design alignment, design invert/TOP, minimum cover or crossing profile loaded | No as-built vs design deviation, no cover compliance | High |
| G7 | **Depth semantics undefined**: "max/min elevation" along a hand-drawn line; target (floor / pipe crown / water) unknown; max may sit on struts or spoil | Depth ≠ cover; σ unknown; the value is only indicative | Medium |
| G8 | **Ad-hoc, event-driven coverage**: one excavation per report; reports generated 7–35 weeks after the flight | No continuous `qty_cum` series per section; measurements arrive too late for weekly/monthly certification | High |
| G9 | **Label errors** (G114 file vs G113 measurement; "length" used for exit-pit edges; exit-side label vs rig present) | Wrong sheet assignment; needs a validation step | Medium |
| G10 | **Three dates** (survey, digitising, report) without a clear "as-of" | Risk of dating the quantity at report date instead of survey date (cf. D-041 "measure at measurement date") | Medium |
| G11 | **No volumes / surface comparison** although the platform is designed for them | Excavation, backfill and topsoil m³ cannot be checked | Medium |
| G12 | **Personal names** of operators on every card | Must be stripped on ingest (data-minimisation rule) | Low (process) |

---

## 4. Mapping to `drone_flight` and `measurement`

### 4.1 `drone_flight` (one row per survey)

| Column | Source in report | DRN-1 | DRN-2 | DRN-3 | Comment |
|---|---|---|---|---|---|
| `flight_id` | not given; platform survey ID only behind the deep link | derive `DRN-G102-20260907` | `DRN-G113-20260928` | `DRN-G114-20260318` | Request the platform survey ID |
| `flight_date` | "Surveyed <date>" [F] | 2026-09-07 | 2026-09-28 | 2026-03-18 | ✓ available |
| `kp_cover_from_m` / `kp_cover_to_m` | – | NULL | NULL | NULL | Derive from plan-sheet KP range (`plan_sheet` table) as a coarse fallback; flag `KP_FROM_SHEET` |
| `gsd_cm` | – | NULL | NULL | NULL | Missing (G2) |
| `rmse_xy_m`, `rmse_z_m` | – | NULL | NULL | NULL | Missing (G2) |
| `n_gcp`, `n_checkpoints` | – | NULL | NULL | NULL | Missing (G2) |

**New `drone_flight` fields proposed:** `platform` (e.g. "Propeller"), `platform_survey_id`, `crs_code` (EPSG), `axis_order`, `vertical_datum`, `geoid_model`, `georef_method` (GCP / PPK / RTK / GCP+PPK), `accuracy_report_ref`, `coverage_geom` (survey footprint polygon), `plan_sheets_covered` (list), `processing_completed_at`, `ingested_at`, `source_doc_ref`.

### 4.2 `measurement` (one row per measured feature)

| Column | Mapping rule | Example (DRN-1, item 1) |
|---|---|---|
| `measurement_id` | `<flight_id>-<legend no>` | `DRN-G102-20260907-01` |
| `source` | `UAV_REPORT_PDF` (manual) vs `UAV_EXPORT` (machine) | `UAV_REPORT_PDF` |
| `flight_id` | from 4.1 | `DRN-G102-20260907` |
| `measure_date` | **survey date**, never the digitising or report date | 2026-09-07 |
| `activity_code` | from the naming convention (§6); today manual | `TRN` (crossing pit) → better a new `XPIT` |
| `section_id` | KP snap of the geometry; today only via the plan sheet | NULL / sheet-derived |
| `method` | `LENGTH_DIGITISE`, `DEPTH_LINE_MAXMIN`, new `TOP_POINT`, `DSM_VOLUME`, `DESIGN_DEVIATION` | `LENGTH_DIGITISE` |
| `kp_from_m`, `kp_to_m` | from geometry; NULL now | NULL |
| `qty_cum` | **Problem:** the reports are per-feature snapshots, not cumulative per section. Store as a feature-level value and aggregate per section/date in a view | 5.88 |
| `unit` | `m`, `m2`, `m3` | m |
| `sigma` | from accuracy metadata via matrix §4; now assumed [A] and flagged | 0.05 |
| `quality_flag` | `OK` / `ASSUMED_SIGMA` / `NO_KP` / `LABEL_CONFLICT` / `INDICATIVE` | `ASSUMED_SIGMA,NO_KP` |

**New `measurement` fields proposed:** `plan_sheet_id` (FK to `plan_sheet`), `feature_type` (TRENCH_CL, PIT, PIPE_TOP, CROSSING, ANCHOR, STOCKPILE…), `feature_ref` (crossing/pit ID), `qty_kind` (`snapshot` / `cumulative` / `increment`), `geom` (WKT/GeoJSON in the project CRS), `z_max_m`, `z_min_m`, `z_target` (FLOOR / PIPE_TOP / GROUND), `distance_type` (horizontal / slope / terrain), `digitised_at`, `digitised_by_role`, `design_ref` (design alignment/profile version), `design_value`, `deviation`, `cover_m`, `cover_min_req_m`, `compliance_status` (PASS / FAIL / NA), `evidence_uri` (platform link, internal only).

Recommended additional table **`as_built_point`** (`point_id`, `flight_id`, `kp_m`, `offset_m`, `z_top_of_pipe`, `z_ground`, `z_design_top`, `cover_m`, `sigma_z`, `source`) to hold top-of-pipe and cover readings, so they are not squeezed into `qty_cum`.

### 4.3 How DRN-1..3 would load today

- 3 `drone_flight` rows with date only. All accuracy fields NULL → every derived measurement gets `quality_flag=ASSUMED_SIGMA`.
- 15 `measurement` rows (9 + 5 + 1). None qualifies as a reconciliation `measured` quantity for a BoQ activity. The engine would classify them as **evidence attachments** (`INDICATIVE`), and claims for the related activities stay `UNVERIFIABLE` unless another source exists.

---

## 5. Proposed checks and alerts

Numbering continues after AL-32 (the last rule in the batch-3 / ingestion design). All are **proposals**.

| ID | Rule | Inputs | Default threshold | Severity |
|---|---|---|---|---|
| AL-33 | **Depth of cover below minimum**: cover = (finished or design ground) − TOP < required minimum at KP | `as_built_point`, design min cover per KP (normal / road / watercourse) | Fail if `cover + 2σ < min_req`; warn if `cover − 2σ < min_req`. Typical regular minimum 1.0 m for gas transmission lines, higher at crossings [VERIFY project spec / DVGW G 463] | High |
| AL-34 | **As-built deviates from design** (TOP level or horizontal offset) beyond tolerance | as-built TOP points vs design profile/alignment version | e.g. horizontal > 0.3 m, vertical > 0.1 m beyond 2σ [VERIFY spec] | Medium/High |
| AL-35 | **Measured length per plan sheet vs claimed** (TRN, LOW, BKF) | Σ measured length by sheet × activity vs Σ claim lines by sheet | Matrix status rule (`|diff| ≤ U + T·Q`) | High (feeds AL-01) |
| AL-36 | **Crossing / pit dimensions vs claim or design** (e.g. claimed pit m³ > drone-indicative m³ + U; crossing length claimed vs measured pit-to-pit distance) | pit polygons + depths; crossing register | 10 % on indicative volumes; 1 % + U on lengths | Medium |
| AL-37 | **Measurement without accuracy metadata** (GSD/RMSE/datum missing) | `drone_flight` | Any NULL in GSD, RMSE_z, vertical datum | Medium (data quality) |
| AL-38 | **Label / location conflict**: sheet in file name ≠ sheet in measurement name, or geometry outside the sheet's KP range | report metadata, geometry | Any mismatch | Medium |
| AL-39 | **Late measurement**: survey-to-delivery lag exceeds the certification cycle, or a claim period has no flight | survey date vs ingest date; claim periods | > 7 days for a weekly cycle | Medium |
| AL-40 | **Missed time window**: a section reported as LOW/BKF complete with no flight between lowering-in and backfill → TOP/cover unverifiable | field reports (E2), flight log | No flight in window | Medium (planning) |

Guard rails: totals rows are never ingested; terrain/slope distances are not used for plan quantities; `measure_date` is always the survey date.

---

## 6. Standard export specification (request to the drone team / platform)

**Goal:** every flight arrives machine-readable, per plan sheet and survey date, with accuracy metadata, so E4 can ingest it without manual PDF reading.

**6.1 Delivery package per flight** (one folder `<YYYYMMDD>_<flightID>/`):

| File | Content | Format |
|---|---|---|
| `flight_meta.json` | platform survey ID, survey date/time (local + UTC), area/plan sheets covered, coverage polygon, CRS (EPSG code + axis order), vertical datum + geoid model, GSD, georef method (GCP / PPK / RTK), number of GCPs and checkpoints, checkpoint RMSE x/y/z, processing date | JSON |
| `accuracy_report.pdf` | platform survey-accuracy / checkpoint report | PDF (evidence) |
| `measurements.csv` | one row per measured feature (schema below) | CSV, UTF-8, `.` as decimal separator |
| `measurements.geojson` | the same features with geometry (LineString/Polygon/Point, 3D) | GeoJSON in the project CRS (or DXF/LandXML if preferred) |
| `ortho.tif`, `dsm.tif` | clipped to the ROW buffer | Cloud-Optimised GeoTIFF |
| `volumes.csv` (when relevant) | surface-comparison results: base surface, compare surface, cut, fill, net, area | CSV |
| `design_deviation.csv` (roadmap) | design profile vs as-built TOP per station | CSV / LandXML |

**6.2 `measurements.csv` columns:** `flight_id, survey_date, plan_sheet, feature_id, feature_type, activity_code, measurement_type (LENGTH|AREA|VOLUME|POINT_Z|DEPTH), distance_type (HORIZONTAL), value, unit, z_target (FLOOR|PIPE_TOP|GROUND), z_value, kp_from, kp_to, sigma (if available), digitised_at, digitiser_role, remarks`. No personal names.

**6.3 Naming convention** for features on the platform: `<sheet>_<activity>_<feature>_<seq>`, e.g. `G102_XPIT_LAUNCH_01`, `G113_TRN_CL_01`, `G113_TOP_PT_05`. A controlled list of activity and feature codes is given to the drone team.

**6.4 Minimum measurement set per flight** (systematic, not event-driven):
1. Open trench: **centreline polyline** per day-front (not edges) → TRN length.
2. Pipe in open trench: **pipe polyline + TOP points every 10–25 m** and at bends/crossings → LOW length, as-built TOP levels.
3. Reinstated / backfilled: closed-trench length and **ground points at the same stations** → BKF length, cover.
4. Crossing and tie-in pits: **polygon + floor point + TOP point**, pit ID → pit volume, crossing pit-to-pit length.
5. Stockpiles / topsoil: surface-comparison volumes with the base-surface method stated.
6. HDD: entry/exit point positions and pit polygons with the crossing ID (length stays from the drilling log).

**6.5 Design inputs to load into the platform:** design alignment and longitudinal profile (TOP or invert) and the minimum-cover rules per segment (LandXML/DXF), so the platform's design comparison produces deviation and cover values directly.

**6.6 Timing:** survey processed and exported **within 48 h of the flight**; at least one flight per active front per week, plus event flights for the "pipe-in-trench" window (AL-40).

**6.7 Integration option:** if the platform API is licensed, pull `flight_meta` and the measurement exports automatically (roadmap). Otherwise use a shared folder or SFTP drop with the structure above [VERIFY licence/API scope].

---

## 7. Open questions [VERIFY]

1. Vertical datum and geoid model used by the drone team; GCP/PPK practice and typical checkpoint RMSE.
2. Platform survey IDs and whether measurement exports (CSV/GeoJSON/DXF) and the API are available under the current licence.
3. In DRN-1/2, what was the "min elevation" point: pit floor, pipe crown or water?
4. DRN-3: sheet G113 or G114; entry or exit side?
5. Project minimum depth of cover per segment type and the as-built tolerances for TOP level and horizontal position.
6. Can design alignment/profile files be shared with the drone team for in-platform design comparison?
