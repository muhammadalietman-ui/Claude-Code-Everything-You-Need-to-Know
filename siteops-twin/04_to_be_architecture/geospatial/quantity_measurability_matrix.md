# Quantity Measurability Matrix, Linear Referencing and Volume Method

Owner: gis-engineer. Version 0.1 (Phase 0). Status: draft for review by the field-operations-specialist and commercial-analyst.
Supports **RQ1**, **H1**, epics **E1**, **E4** and **E5**.

## 1. Purpose
Not every pipeline quantity can be verified from the air. This matrix classifies each activity by how far daily UAV photogrammetry can measure it independently. The reconciliation engine (E5) uses the classification to decide whether a claimed quantity can be checked against a measured quantity (`MATCHED` / `WITHIN_TOLERANCE` / `DISCREPANCY`), or must be checked against another independent source or marked `UNVERIFIABLE`.

**UAV observability classes:**
- **Yes:** the quantity is visible on the surface once completed, and stays visible.
- **Partial:** visible, but obstructed or only approximately measurable (vegetation, stockpiles, shoring, water).
- **Time-window:** visible only between two events. For example, open trench before lowering-in, or pipe in trench before padding and backfill. It is missed if the flight is not in that window.
- **No:** not observable from the air. An independent non-UAV record is needed.

## 2. Matrix

| # | Activity | Typical unit (BoQ) | UAV observable | UAV method | Required flight timing | Main accuracy drivers | Primary independent source if not UAV / cross-check | Evidence type | MVP |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ROW clearing and topsoil stripping | m (ROW length) · m² (area) · m³ (topsoil stockpile) | Yes (length/area); Partial (stripped volume) | Orthophoto area/edge digitising; DSM differencing for stockpiles | After completion of each daily stretch | Vegetation on the pre-surface; stockpile toe definition; GSD | Survey of ROW pegs | Orthophoto polygon; volume report | ✅ length and area |
| 2 | Grading | m · m² (· m³ cut/fill where paid) | Yes | Orthophoto area; DSM differencing (pre-grade vs post-grade) | Pre-grade baseline flight + post-grade flight | Baseline surface quality (vegetation, if baseline taken before clearing); vertical RMSE | Topographic survey | DSM pair; volume report | ✅ length and area; volume in the roadmap |
| 3 | Access roads / temporary roads | m · m² · m³ of granular material | Yes (length/area); Partial (layer thickness) | Orthophoto digitising; DSM differencing | Before and after placement | Thin layers (< 0.2 m) close to the vertical uncertainty | Delivery tickets (t or m³) | Orthophoto; tickets | Roadmap |
| 4 | Stringing | m of pipe strung · number of joints | Yes | Object counting of pipe joints on the orthophoto (manual or assisted); length along the centreline | Daily, before welding consumes the string | Joint overlap or occlusion; GSD ≥ 3 cm is enough to count 12–18 m joints | Pipe tally sheets (heat/joint numbers) | Orthophoto with counted points | ✅ |
| 5 | Bending | number of field bends | Partial | Detect bent joints visually: possible, but unreliable | Before welding | Small angles not visible | Bending log / bend schedule | Bending log | ❌ (source = log) |
| 6 | Welding, mainline | number of welds (joints) · m of welded line | Partial: continuous welded string is visible, but individual weld count is **not** reliably observable | Length of continuous string on the orthophoto as a plausibility check only | Daily | Cannot distinguish welded from aligned-but-unwelded joints | **Welding log / weld-mapping database** (weld ID, KP, welder ID kept anonymised) | Weld log export | ✅ via log, UAV plausibility |
| 7 | Welding, tie-ins | number of tie-in welds | No (individual welds) | Visible location of the tie-in bellhole only | n/a | n/a | Weld log | Weld log; photo | ✅ via log |
| 8 | NDT (RT/AUT/UT) | number of welds inspected · % accepted / repair rate | No | n/a | n/a | n/a | **NDT database / reports** | NDT report reference | ✅ via log (status only) |
| 9 | Field joint coating | number of joints coated | Partial: sleeves or coating colour may be visible at high resolution; not reliable | Visual check only | Before lowering-in | GSD; shading | Coating records / holiday-test records | Coating log | ✅ via log |
| 10a | Trenching / excavation, normal soil | m of trench · m³ excavated | **Time-window** (open trench) | Length: digitise the open trench on the orthophoto. Volume: DSM differencing pre-trench vs open-trench surface, **corrected for the spoil pile** | Open-trench flight before lowering-in. Pre-trench (graded) baseline needed | Trench walls in shadow; **water in trench** (photogrammetry fails on water surfaces); **shoring or trench boxes**; spoil pile alongside affects the net volume; narrow, deep trench depth is poorly reconstructed (occlusion of the trench floor at low view angles) | Trench depth survey or as-built depth-of-cover readings | Orthophoto line; DSM pair; depth survey | ✅ length; volume as **indicative** only |
| 10b | Trenching, rock | m · m³ (rock class) | Time-window, Partial | As 10a; rock classification is **not** possible from UAV | As 10a | As 10a, plus over-break | Geotechnical classification by the site engineer; blasting records | Classification sheet; photos | ✅ length; rock class from source |
| 11 | Padding (sand/selected material) | m · m³ | Time-window | DSM differencing (pipe-in-trench vs padded surface) | Between lowering-in and backfill. Often the same day, so frequently missed | Short window; thin layers | Material delivery tickets; inspector record | Tickets; photo | Roadmap |
| 12 | Lowering-in | m of pipe lowered | **Time-window** | Digitise the pipe visible in the open trench on the orthophoto | After lowering-in, before padding/backfill | Short window; water; shadow | Lowering-in log with KP from/to; inspector sign-off | Orthophoto line; log | ✅ (time-window flag) |
| 13 | Backfill | m · m³ | Yes (length of closed trench); Partial (volume) | Length of reinstated trench line; DSM differencing for the crown and settlement allowance | After backfill | Crown height and compaction; spoil re-use | Survey | Orthophoto; DSM | ✅ length |
| 14a | Crossings, road (open-cut / bored) | number · m | Partial (open-cut visible; bored only at pits) | Visual confirmation and location | Before and after | Traffic management obstruction | Crossing as-built record | As-built sheet; photo | ✅ count/location |
| 14b | Crossings, river / wetland (open-cut) | number · m | Partial | Visual; water prevents a surface model | Before and after | Water surface | As-built survey | As-built; photo | Roadmap |
| 14c | Crossings, HDD | m drilled · number | No (only entry/exit pits visible) | Pit location only | n/a | n/a | **HDD drilling log / as-built profile** | Drilling log | ✅ via log |
| 15 | Tie-ins (golden welds, section tie-ins) | number | No | Location only | n/a | n/a | Weld log; tie-in register | Weld log | ✅ via log |
| 16 | Hydrotest | test sections passed · m tested | No | n/a | n/a | n/a | **Hydrotest records / certificates** (test section from/to KP) | Test certificate reference | ✅ via record |
| 17 | Cleaning, gauging, drying | test sections · m | No | n/a | n/a | n/a | Pigging/gauging reports | Reports | Roadmap |
| 18 | Reinstatement / restoration | m · m² · m³ topsoil replaced | Yes (area); Partial (topsoil volume) | Orthophoto area; DSM differencing vs the post-backfill surface | After completion; vegetation regrowth months later is a separate milestone | Seasonal vegetation; surface roughness | Landowner sign-off sheets | Orthophoto polygon; sign-off | ✅ length and area |
| 19 | Cathodic protection (test posts, anodes, ground beds) | number · m of cable | Partial (above-ground test posts visible) | Object counting of test posts | After installation | Post size versus GSD | CP installation records | Record; photo | Roadmap |
| 20 | Marker posts / aerial markers | number | Yes | Object counting with KP snapping | After installation | Post size versus GSD (GSD ≤ 3 cm recommended) | Installation register | Orthophoto points | Roadmap |

**Interpretation for E5.**
- **UAV-verifiable in MVP:** activities 1, 2, 4, 10 (length), 12, 13, 18.
- **Log-verifiable** (independent record, not a UAV measurement): 6, 7, 8, 9, 14c, 15, 16.
- **Everything else:** marked `UNVERIFIABLE` in the MVP if no independent record exists. This fires **AL-06** when quantities are claimed with no measurement or evidence.

**Honest limits.**
- Below-ground works can be verified only if a flight falls in the right time window (A-013).
- Water in the trench, shoring, vegetation and steep trench walls reduce reconstruction quality.
- DSM differencing gives a **net** volume change, not the excavated volume, unless the spoil pile is captured separately or excluded with a mask.
- UAV measurement is a **tolerance check** on claims. It is not a replacement for contract-defined measurement (see R-02).

## 3. Linear referencing specification

| Item | Specification |
|---|---|
| CRS policy | All geometry is stored in one projected metric CRS `[CRS_EPSG]` (a local UTM zone or national grid for the real project). Drone products are reprojected on ingest if they differ. Store the vertical datum `[VDATUM]` and geoid model as metadata. For the synthetic dataset, see §6 of the synthetic dataset spec. |
| Centreline | `alignment` stores the centreline as `LINESTRINGM` (PostGIS `geometry(LineStringM, [CRS_EPSG])`). **M = KP in metres** from the spread origin. Versioned: `alignment_version` with `design` / `as-built` / `reroute-n`. |
| KP format | Display as `KP 012+350` (km + m). Store as numeric metres (`12350.0`). |
| Snapping points and lines | A point (photo, equipment position, counted object): `kp = ST_InterpolatePoint(centreline, ST_ClosestPoint(centreline, pt))`, or `ST_LineLocatePoint(centreline, pt) × length + KP_start` when M is linear. Record `offset_m = ST_Distance(pt, centreline)` with a signed side (L/R). Reject or flag a snap if `offset_m > ROW_half_width + buffer` (default 30 m). |
| Snapping footprints | For a drone measurement polygon or digitised line: KP_from and KP_to are the min and max of the snapped vertices. Store the `geometry` and the derived `kp_from` / `kp_to`. A measurement may span sections. Quantities are split pro rata by KP overlap, or, for counted objects, by object location. |
| Sections | `section` = KP interval `[kp_from, kp_to)`. Default length **1,000 m**, configurable per spread (Q-011, D-004). It can follow non-uniform boundaries such as crossings, land parcels or test sections. Section IDs are `[SPREAD_ID]-S##`. Sections are **half-open** to avoid double counting at boundaries. |
| Reroutes and chainage equations | When the as-built route differs from the design, a new alignment version is created. **Chainage equations** (`kp_back`, `kp_ahead`) are stored in `chainage_equation` so a reroute does not renumber downstream KPs. Example: `KP 014+200 (back) = KP 014+050 (ahead)` means 150 m of chainage was skipped. Quantities are always computed on **measured length along the as-built geometry**. KP is a location label. The two differ across equations; that difference must be reported. |
| As-built vs design | Planned quantities refer to the design alignment version. Measured and claimed quantities refer to the as-built version. Reconciliation joins on section (stable KP labels) and records the `alignment_version` used. |

## 4. Volume method (DSM differencing)

1. **Surface pair.** Choose a *before* surface S₀ (e.g. graded ROW, flight date d₀) and an *after* surface S₁ (e.g. open trench, d₁), clipped to a footprint polygon P.
2. **Base surface choice.**
   - For trench and grading: S₀ is the previous-state DSM.
   - For stockpiles with no prior surface: S₀ is a TIN fitted to the stockpile toe ("lowest point" or "triangulated base"). The choice is reported, because it strongly affects the result.
3. **Grid differencing.** `ΔV = Σ (z₁ − z₀) · a_cell` over the cells in P. Cut and fill are reported separately.
4. **Accuracy check.** Vertical RMSE `σz` comes from ≥ 5 independent check points (not used as GCPs) per flight block, reported for each surface. Combined: `σΔz = √(σz₀² + σz₁²)`.
5. **Uncertainty propagation (simplified).**
   - Use **correlated (systematic) error** as the conservative default: `σV ≈ A · σΔz`, where A = footprint area. A vertical bias, such as a datum shift between flights, affects every cell equally.
   - If the error per cell is purely random and uncorrelated across n cells: `σV ≈ σΔz · a_cell · √n`. This is much smaller, and usually over-optimistic, because photogrammetric errors are spatially correlated.
   - Report the **correlated estimate** as the default. State the assumption.
6. **Tolerance comparison** (used by AL-01):
   - `diff = Q_claimed − Q_measured`
   - Contract tolerance T: Q-007, default 3% for volume and 1% for length (A-050).
   - Measurement uncertainty `U = k · σQ`, with k = 2 (≈ 95%). Contract tolerance `T · Q_measured`, with T from the subcontract (e.g. `[TOL_VOL_PCT]`).
   - `|diff| ≤ U` → **MATCHED**. `≤ U + T·Q` → **WITHIN_TOLERANCE**. Otherwise → **DISCREPANCY**. No valid measurement → **UNVERIFIABLE**.
   - The certifiable cap without override is `M + U + T·Q`. This rule is harmonised with D-063 and CTL rules in `ux/mvp_backlog.md`. The earlier "0.5·band" proposal (D-050) was superseded at the P0 quality review.
7. **Length uncertainty** for digitised lines: `σL ≈ √2 · σxy` per end point, plus digitising error ≈ 2 × GSD. This is negligible against tolerance for lengths over 100 m.
8. **Known biases:**
   - Water and specular surfaces (holes in the DSM, which must be masked)
   - Vegetation on S₀ (overestimates the cut)
   - Spoil pile inside P (net volume ≠ excavated volume)
   - Shoring and trench boxes
   - Moving equipment in the footprint (mask it)
   - Different GCP sets or datum between flights (correlated bias)

## 5. Map layer catalogue

| Layer | Geometry | Format (storage / serving) | Update frequency | Source | Epic |
|---|---|---|---|---|---|
| Alignment centreline (versioned) | LineStringM | PostGIS / GeoJSON | On revision | Engineering | E1 |
| KP ticks (every 100 m) and labels | Point | Derived view | On revision | Derived | E1 |
| Sections | LineString (KP interval) + polygon buffer | PostGIS / GeoJSON | On revision | Configured | E1 |
| ROW boundary | Polygon | GeoPackage / GeoJSON | On revision | Land / survey | E1 |
| Daily orthophoto | Raster | Cloud Optimized GeoTIFF (COG), XYZ/WMTS tiles | Daily | `[DRONE_SW]` export | E4 |
| DSM / DTM | Raster | COG (hillshade for display) | Daily / per flight | `[DRONE_SW]` | E4 |
| Point cloud / 3D mesh | 3D | LAZ / 3D Tiles (roadmap) | Per flight | `[DRONE_SW]` | Roadmap |
| Drone measurement footprints | Polygon / LineString / Point | PostGIS / GeoJSON | Per flight | E4 import | E4, E5 |
| Field-report work extents | LineString (KP from–to) | PostGIS view | Daily | E2 | E2 |
| Subcontractor claim extents | LineString (KP from–to) | PostGIS view | Per claim | E3 | E3, E6 |
| Reconciliation status by section × activity | Section line, coloured by status | Derived view / vector tiles | On recompute | E5 | E5, E7 |
| Alerts | Point at KP | GeoJSON | On recompute | E6 | E6, E7 |
| Equipment last-known position (daily) | Point | GeoJSON | Daily (MVP) | Telematics | E8 |
| Crew presence by section (aggregated) | Section line (count) | Derived | Daily | E8 (crew level only) | E8 |
| Crossings, HDD, test sections | Line / point | GeoJSON | On revision | Engineering | E1 |
