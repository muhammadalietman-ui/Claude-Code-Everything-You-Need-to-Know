# Supplier Daily Reports: Structural Analysis for the Ingestion Layer

Owner: process-analyst / data-engineer. Version 0.1. Evidence base: five real supplier daily reports, as uploaded by the Commercial Manager of [CONTRACTOR_JV]. Status: **[E] EVIDENCED** (observed in real documents). Interpretations are marked *(interpretation)*.

**Confidentiality.** This document is anonymised. Reports are referred to as RPT-A to RPT-E, issuers as [SUPPLIER_A] to [SUPPLIER_E], the main contractor as [CONTRACTOR_JV] and the pipeline owner as [CLIENT]. People appear by role only. No names, signatures, phone numbers, addresses, road names, town names or project numbers are reproduced. Equipment is described by generic type; manufacturer names are omitted. The values read from the reports are held in the git-ignored file `data/private/supplier_reports_extract.json`.

Reference point: the [CONTRACTOR_JV] client daily report, analysed earlier, has these parts: weather; man-hours by company type and local/external; equipment hours computed from days assigned; narrative of completed work, planned work and HSE; a detailed activity table (unit, total, plan sheet from/to, previous cumulative, this period, cumulative, %); and a crossings table.

---

## 1. Report profiles

### RPT-A: civil / earthworks subcontractor ([SUPPLIER_A])

| Aspect | Observation |
|---|---|
| Format | Single-page PDF generated from a Word form and filled in digitally. Carries one hand-drawn electronic signature. |
| Language / form | German. Generic German "Bautagesbericht" form in the style of the VOB construction-site diary. |
| Trade | Civil works: haul road construction and storage yard (Lagerplatz) logistics. |
| Period | Daily (single date). No report number. |
| Sections | Header (site managers, date, project, sub-location); weather tick boxes (sun, rain, frost, wind, snow, temperature °C); headcount and working time from/to; hours matrix by German wage-group category (Polier, Werkpolier, Bauvorarbeiter, gehobener Baufacharbeiter, Baufacharbeiter, Baufachwerker, Maschinist, Kraftfahrer); free-text work lines; hindrances (Behinderungen/Erschwernisse); variations (Leistungsänderungen); special events and inspections (Besondere Vorkommnisse, Begehungen/Abnahmen); place/date and signature boxes for the client side (AG) and the contractor side (AN). |
| Location referencing | Landmark only: "storage yard" plus the town name. No KP, no plan sheet, no crossing ID. A loading activity names a street at the [CONTRACTOR_JV] yard. |
| Manpower | Headcount (2) plus category and hours: 2 machine operators, "8,5 Std.". The form does not say whether 8.5 h is per person (17 man-hours) or the total. 07:00–16:15 is 9.25 h; the stated 8.5 h implies an unstated 45-minute break. No names. |
| Equipment | Given only in the narrative: "1x wheel loader 8.5 h, 1x roller 4 h". The hours are typed, not measured, and match the shift length *(interpretation: estimated)*. |
| Quantities | Main activity "build and compact haul road, finished" has **no quantity and no unit** (m, m² or m³ expected). The secondary logistics line has a quantity (12 excavator mats, unit "Stk"). Daily values only, no cumulative. |
| Downtime / standby | A dedicated "hindrances" section exists but is empty. Nothing records the absence of downtime explicitly. |
| Weather | Ticked: sun, 15 °C. |
| HSE | No dedicated field. "Special events" could hold one but is empty. |
| Sign-off | Signed by the subcontractor site manager (AN). **The client-side (AG, i.e. [CONTRACTOR_JV]) countersignature box is empty.** |
| Data quality | Main output not quantified; per-person vs total hours ambiguous; equipment hours buried in free text; no location code; the [CONTRACTOR_JV] name is misspelled in the project field; no report number for completeness checks. |

### RPT-B: dewatering / groundwater subcontractor ([SUPPLIER_B])

| Aspect | Observation |
|---|---|
| Format | Single-page PDF printed from Excel ("Print to PDF") and filled in digitally. No signature. |
| Language / form | German, with an English company tag-line. Company-branded own form. |
| Trade | Dewatering (Wasserhaltung): well construction, pumps and generators, groundwater monitoring. |
| Period | Daily. Carries the supplier's internal project number. No report number. |
| Sections | Header (project no., date); "staff names" list next to "machines and vehicles" list; contract positions table (position text, quantity, unit, location); "special notes" (Besonderes). |
| Location referencing | **Construction-plan sheet numbers** (e.g. "G161A und G162") in a dedicated location column. This is the only report with a structured location field. |
| Manpower | **List of five personal names** with no role, no hours and no times. Headcount can be derived (5); man-hours cannot. |
| Equipment | Type × count (e.g. 4x4 pick-up ×2, trailer ×1, tractor with water bowser ×1, wheel loader ×1, telehandler ×1). No hours. Presence only. |
| Quantities | One contract position, "installation of groundwater monitoring well", quantity **"ca. 3"** Stck. The quantity is approximate and the position has no BoQ number. Daily only. A further delivery activity is recorded under special notes with no quantity. |
| Downtime / standby | Absent. |
| Weather | Absent. This matters for a dewatering trade, where rainfall drives pumping effort. |
| HSE | Absent. |
| Sign-off | **None** (no signature boxes on the form). |
| Data quality | Approximate quantity on a contract position; position matched by text, not by code; names without hours; no weather, HSE or sign-off. |

### RPT-C: HDD drilling subcontractor ([SUPPLIER_C])

| Aspect | Observation |
|---|---|
| Format | Native Excel workbook. Two visible sheets ("1-4 Cover", "5. Detailed Activity Report"), no hidden sheets. **Column B (price-list code) is hidden** on sheet 2. The page header contains the [CONTRACTOR_JV] logo and static header text. |
| Language / form | Mixed German/English labels; the narrative is bilingual (an EN line followed by the same text in DE). **The form is the [CONTRACTOR_JV] client daily-report template, reused by the subcontractor**: same section numbering 1–5 and same activity-table columns. |
| Trade | HDD / trenchless drilling. |
| Period | Daily. Cell values: date 20 Oct 2025, report no. 1. **The page header still reads a different date (8 Oct) and report no. 23**, copied over from the template. File metadata shows the workbook was last saved two days after the report date. |
| Sections | (1) Personnel overview: name, job title, hours today; (2) equipment summary: type, hours today; (3) activities: 3.1 completed today, 3.2 planned; (4) focus points (HSE, QA/QC, security); (5) detailed activity table: price-list code, title, unit, total quantity, plan sheet from/to, previous cumulative, this period, cumulative (formula), % complete (formula), plan cumulative, plan %, deviation. |
| Location referencing | **None on the cover.** There is no crossing ID, start/target pit or KP, which is critical for an HDD subcontractor whose work is defined per crossing. The plan-sheet columns exist on sheet 5 but hold dummy data only (see below). |
| Manpower | Named persons with job title (German wage-group terms: Polier, Maschinist, Kraftfahrer) and hours. 5 persons × 10 h = 50 man-hours (SUM formula). Seven empty template rows remain. |
| Equipment | Template list (excavators, dumpers, dozer, wheel loader, mini-excavator, compactor) with hours. 2 excavators × 10 h = 20 h. **Equipment hours equal the crew shift hours**, which indicates presence time rather than engine or productive hours *(interpretation: estimated)*. The drilling rig itself does not appear in the equipment list. |
| Quantities | The narrative describes a mobilisation day (unloading the drilling equipment, fencing, site set-up) with no quantity. **Sheet 5 contains 25 rows of untouched template values**: every row has total 2, previous 1, today 1, cumulative 2, 100 % complete, deviation 0; titles are blank and only 4 rows carry a unit (m, m², m³, "psch"). A naive parser would read this as 25 contract items complete. |
| Downtime / standby | No field. |
| Weather | Single text value ("Rain"). No temperature or wind. |
| HSE | Free text under "focus points": a site-security observation (no security cameras installed). No incident or near-miss structure. |
| Sign-off | **None** (no signature field in the template copy). |
| Data quality | Dummy table; stale header date and number; hidden code column; no location; equipment hours copied from shift hours; drilling rig missing from the equipment list; bilingual duplication complicates text-vs-quantity checks. |

### RPT-D: microtunnelling / pipe-jacking subcontractor ([SUPPLIER_D])

| Aspect | Observation |
|---|---|
| Format | Two-page PDF printed from a spreadsheet form. Page 2 is empty ruled lines plus the signature block. |
| Language / form | **Dutch** ("Dagrapport"). Supplier's own branded form. |
| Trade | Trenchless crossing by TBM (microtunnelling / pipe jacking). The header states bore diameter (≈1 033 mm) and length (≈60 m). |
| Period | **A daily sheet within a weekly file**: header "week 19", day "Fri" plus date; the file name refers to the week and the weekday. The "from/to hours" header fields are blank. Dated May 2025, considerably earlier than the other reports. |
| Sections | Header (project, bore, place, main contractor, supplier project no.); crew allocation (Ploegbezetting) by role (site manager, drilling master, surveyor, mudman, assistants ×3, crane operator, hired-in) with company code and from/to; "own plant" (Eigen materiaal) list; description of work; day-by-day "agreements & remarks"; prepared-on date; signature blocks for contractor/site manager and inspector/supervisor. |
| Location referencing | Town name in the header plus "location 160" in the narrative. The crossing is implied by the bore parameters, but **no crossing ID, pit name or KP** is given. |
| Manpower | Role-based rows with names and a company code (the supplier's abbreviation). **Only one of five persons has times (07:00–12:00 = 5 h)**; the other four have none. Man-hours cannot be derived. |
| Equipment | Bare model codes (four items, e.g. a 35 t crawler excavator and three units identified only by alphanumeric codes). No hours, no count, no description *(interpretation: the codes probably denote jacking/separation/power units)*. |
| Quantities | None. The day records set-up, laying plates, delivery of the TBM and recycling pump, and removal of the remaining items and scaffolding at "location 160" (demobilisation from the previous drive). No jacked metres, even though the form's purpose is a bore. |
| Downtime / standby | No field. The 5 h for the drilling master is unexplained. |
| Weather | Absent. |
| HSE | Absent. |
| Sign-off | Both blocks (supplier site manager; client inspector/supervisor) **empty**. |
| Data quality | Incomplete times; no quantities; equipment as codes only; weekly vs daily ambiguity; no signatures; Dutch free text needs translation before keyword-based checks. |

### RPT-E: sheet-piling crew ([SUPPLIER_E])

| Aspect | Observation |
|---|---|
| Format | Single-page PDF exported from Excel. **A [CONTRACTOR_JV]-branded crew template** (JV logos, "Tagesbericht" with a sequential number). |
| Language / form | German. |
| Trade | Sheet piling (Spundwand) for pit shoring. |
| Period | Daily, **sequentially numbered (012)**. A crew (Kolonne) name is stated. |
| Sections | Header (lot, report no., date, crew); personnel table (pos., name, role abbreviation, start, end, hours, travel mode own/private vehicle, travel date, assigned equipment, inventory/plate no.); work performed; equipment on site; weather (temperature, sun, snow, wind, unsettled, changeable); HSE banner "toolbox meeting / five-minute safety talk carried out"; remarks; three signature boxes (subcontractor, JV site supervisor, JV project manager). |
| Location referencing | Code "BP160" in the work text *(interpretation: pit or crossing point 160)*. Not linked to a KP. |
| Manpower | **Best of the five**: 6 named persons with role abbreviations (PM, BL, MS = machine operator, SFB = skilled operative), start 07:00, end 18:00, 10.0 h each, for 60 man-hours *(1 h break implied)*. All rows carry identical times. **The project manager and site manager are booked for the full 10 h as crew**. |
| Equipment | The two operators are linked to a machine (crawler crane, wheel loader). A separate site inventory lists ~11 item types with counts (vibro hammer + power pack, piling frame, 14 crane mats, containers, diesel drums, generator, trailer). No hours. **The crane unit number differs between the crew table (…45) and the equipment list (…54).** Inventory/plate column blank. |
| Quantities | **None**: "sheet-pile wall installation at BP160" without m², number of piles, tonnes or wall length. |
| Downtime / standby | No field. "Remarks" is empty. |
| Weather | Temperature 0 °C; all other fields blank. |
| HSE | A pre-printed sentence, not a tick box or signature, so it **cannot evidence that the talk actually took place**. |
| Sign-off | Three boxes, **all empty**. |
| Data quality | No quantity; equipment ID mismatch; uniform template-copied times; management hours in crew totals; unverifiable HSE statement; no signatures. |

---

## 2. Comparison matrix

Legend: **P** = present and machine-usable, **p** = partial or ambiguous, **–** = absent.

| Canonical field | RPT-A (civil) | RPT-B (dewatering) | RPT-C (HDD) | RPT-D (microtunnel) | RPT-E (sheet piling) |
|---|---|---|---|---|---|
| report_date | P (dd.mm.yy) | P | p (cell vs header conflict) | P (+ week no.) | P |
| report number / sequence | – | – | p (cell 1 vs header 23) | – | P (012) |
| supplier / subcontractor | p (implied by people only) | P (letterhead) | P (filename/metadata) | P (letterhead + code) | P (crew name) |
| crew | – | – | – | p (role roster) | P (Kolonne) |
| location: KP chainage | – | – | – | – | – |
| location: plan sheet | – | P (G-numbers) | p (column exists, dummy) | – | – |
| location: crossing ID | – | – | – | p (bore Ø/length, "loc. 160") | p ("BP160") |
| location: landmark | P (storage yard, town) | – | – | p (town) | – |
| activity | p (free text) | P (contract position text) | p (narrative + dummy table) | p (free text, NL) | p (free text) |
| quantity | p (logistics only; main activity none) | p ("ca." approximate) | – (dummy values) | – | – |
| unit | p | P | p (4 of 25 rows) | – | – |
| cumulative / previous qty | – | – | p (columns exist, dummy) | – | – |
| BoQ / price-list code | – | – | p (hidden column, dummy) | – | – |
| hours worked (shift) | P (from/to) | – | p (per person only) | p (1 of 5 persons) | P (from/to/h per person) |
| headcount | P | P (count of names) | P | P | P |
| man-hours per person category | p (category matrix, ambiguous) | – | P (job title + h) | – | P (role + h) |
| equipment list | p (narrative) | P (type × count) | P (type list) | p (model codes) | P (inventory + operator link) |
| equipment hours | p (narrative, typed) | – | p (= shift hours) | – | – |
| measured vs estimated flag | – | – | – | – | – |
| downtime + reason | p (section, empty) | – | – | – | – |
| weather | P (ticks + °C) | – | p (one word) | – | p (°C only) |
| HSE events | p ("special events", empty) | – | p (free text) | – | p (pre-printed, unverifiable) |
| photos / evidence | – | – | – | – | – |
| signature: supplier | P | – | – | – (box empty) | – (box empty) |
| signature: contractor countersign | – (box empty) | – | – | – (box empty) | – (2 boxes empty) |
| narrative | P | p (special notes) | P (bilingual) | P (NL) | p (one line) |

**Coverage summary.** No report gives a KP. No report gives photos. No report distinguishes measured from estimated equipment hours. None is countersigned by [CONTRACTOR_JV]. Only two of the five give any quantity, and neither of those is the supplier's primary contract output with an exact quantity.

---

## 3. Key findings for the SiteOps Twin design

### 3.1 What the ingestion layer must handle

1. **Five formats, three source types.** Word-form PDF, Excel-printed PDF and native XLSX, in German, Dutch and bilingual EN/DE. All four PDFs carry a text layer, so OCR is not needed for this sample. The layer still needs an OCR fallback, because handwritten or scanned forms are common on German sites.
2. **Template awareness.** Two of the five suppliers fill in [CONTRACTOR_JV] templates (RPT-C, RPT-E). Ingestion must:
   - detect template residue: values that are identical across all rows, blank titles with numeric quantities, a page header that contradicts the cells;
   - read hidden columns;
   - reject placeholder rows rather than import them.

   A rule of the form *"all rows identical and 100 % complete"* means placeholder data, sent to quarantine.
3. **Location resolution is the main gap.** The schema (`field_daily_report.schema.json`) currently **requires** `kp_from_m`/`kp_to_m`, but 0/5 reports provide a KP. The ingestion layer needs a **location resolver** that maps plan-sheet numbers (G-numbers), crossing/pit codes ("BP160", "location 160") and landmarks (storage yard) to a KP range or a crossing ID through a reference table. KP must become *derived*, with a `location_confidence` attribute (exact / resolved-from-sheet / resolved-from-crossing / landmark / unknown).
4. **Non-production days.** Three of the five reports (RPT-A partly, RPT-C, RPT-D) describe mobilisation, set-up, logistics or demobilisation with no measurable quantity. The canonical model needs activity codes such as `MOB`, `DEMOB`, `SETUP`, `LOGISTICS`, `DEWATER`, `SHEETPILE`, `MTBM` and must allow a line with qty = null when the activity type is non-quantity-bearing. The current enum (CLR…MKR) and `minItems: 1` with a required `qty` would otherwise reject these reports or force a fabricated quantity.
5. **Unit and number normalisation.** Units: Stk/Stck/Stück → nr; psch (lump sum) → `ls`, which needs a new enum value; m²/m2. German decimal comma ("8,5"). Approximate qualifiers ("ca.", "approx."). Times written as "7.00" vs "07:00". Dates as dd.mm.yy, dd-mm-yyyy and Excel serial dates. The weekday plus ISO-week form ("vr.", "Mi", "week 19") should be cross-checked against the date.
6. **Personnel model.** Accept three shapes: name list only (RPT-B), category-by-wage-group matrix (RPT-A), and per-person role + time (RPT-C, RPT-E). Map roles to a controlled vocabulary: Polier, Maschinist, Kraftfahrer, Baufacharbeiter/SFB, Boormeester, Uitvoerder, Mudman, PM/BL. Store **roles and counts only** in the twin; drop names at the ingestion boundary (privacy by design / GDPR).
7. **Equipment identity.** Equipment arrives as narrative text, type × count, bare model codes and unit numbers, with inconsistencies (RPT-E …45 vs …54). An **equipment register** (unit no. ↔ type ↔ telematics ID) and fuzzy matching are needed before AL-07 or AL-11 can work. Every equipment-hours value must carry a `hours_basis` flag (measured / estimated / shift-copied); in this sample, all are estimated.
8. **Language.** Store DE/NL free text verbatim with a machine translation, and run keyword extraction (e.g. "fertig", "Behinderung", "Stillstand", "Regen", "afvoeren") for text-vs-quantity checks. Bilingual duplicates (RPT-C) must be de-duplicated.

### 3.2 Commercial-control risks created by the formats

| Risk | Evidence | Consequence |
|---|---|---|
| Hours that cannot be verified | Equipment hours = shift hours (RPT-A, RPT-C); identical 07:00–18:00 for all (RPT-E); only one of five timed (RPT-D) | Day-work and hire claims cannot be checked against actual use. |
| Management time billed as crew | PM and site manager at 10 h each (RPT-E) | Over-recovery of overhead in day-rate or day-work claims. |
| Quantities without location | 0/5 with KP; RPT-A has no location code | No way to test duplicate claims or overlaps across fronts or periods. |
| Approximate or absent quantities | "ca. 3" (RPT-B); none for haul road, sheet piling, tunnel | Monthly claims later appear without a daily trail, which forces negotiation instead of reconciliation. |
| False progress from template residue | 25 dummy rows at 100 % (RPT-C) | If accepted, overstates progress and cumulative quantities. |
| No contractor countersignature | 0/5 countersigned | Reports have weak evidential value in a later dispute (e.g. VOB/B § 2 / § 6 claims); hindrance notices are not acknowledged. |
| Standby / weather not structured | Downtime field present in 1/5 and empty; weather absent in 2/5 | Later standby or weather claims can neither be supported nor rebutted. |
| HSE unverifiable | Pre-printed toolbox statement (RPT-E) | Compliance record without evidence. |

### 3.3 Alert rules applicable per report

| Rule | A | B | C | D | E | Rationale |
|---|---|---|---|---|---|---|
| AL-01 claim > measured | ● | ● | ● |  | ● | Applies once monthly claims arrive: the daily trail gives no measurable baseline (A haul road, B "ca.", C dummy, E sheet piling). |
| AL-02 missing report | ● | ● | ○ | ● | ● | Only RPT-E has a usable sequence number; the others need calendar-based gap detection. In RPT-C the stale header number makes the sequence unreliable. |
| AL-03 duplicate / overlap KP claim | ○ | ● | ○ | ○ | ○ | Only plan sheets (B) can be tested; for the others the location must first be resolved (○ = blocked until it is). |
| AL-04 cumulative > BoQ |  |  | ● |  |  | The dummy table shows cumulative = total at 100 %. Applying the rule would catch implausible values. |
| AL-05 productivity drop |  |  |  |  | ● | Needs quantity per crew-hour. Possible for RPT-E only after quantities are added. |
| AL-06 claimed without evidence | ● | ● | ● | ● | ● | 0/5 have photos; 0/5 are countersigned. |
| AL-07 equipment working vs telematics idle | ● |  | ● |  | ● | Hours equal shift hours; operator–machine link (E) allows a check. |
| AL-08 out of sequence |  |  |  | ● | ● | Tunnel "set-up" vs other works at the same crossing; sheet piling must precede excavation/HDD at the pit. Needs a crossing-level sequence. |
| AL-09 headcount above sensed | ● | ● | ● | ● | ● | All give headcount; compare against site-access / geofence presence. |
| AL-10 impossible presence | ○ | ● | ● | ● | ● | Named persons could appear on two suppliers' reports or two fronts on the same day. Check via pseudonymised IDs, not names. |
| AL-11 equipment hours vs telematics | ● |  | ● |  |  | Only A and C state equipment hours. |
| AL-12 front active without presence |  | ● |  |  | ● | Location codes (G-sheets, BP160) can be tested against geofence presence. |
| AL-13 weather standby unsupported | ● | ● | ● | ● | ● | Weather absent or minimal in B and D. Any future standby claim must be tested against an external weather feed. |
| AL-14 report text vs quantities disagree | ● |  | ● | ● | ● | A "finished" with no quantity; C narrative = mobilisation while the table = 25 items done; D/E work described without a quantity. |

● = applicable now; ○ = applicable after location/identity resolution.

### 3.4 Five headline design findings

1. **Location is the weakest link.** None of the reports gives a KP. A reference-data resolver (plan sheet, crossing/pit code or landmark mapped to KP/crossing) is a prerequisite for AL-03, AL-08 and AL-12, and KP must become optional and derived in the canonical schema.
2. **Most reports carry no quantity.** Daily reports record *presence*, not *production*. Quantity reconciliation therefore has to rely on independent measurement (drone, survey, as-built) and claims. The daily report serves mainly as resource and timeline evidence.
3. **Template residue is a real ingestion hazard.** Copies of [CONTRACTOR_JV] templates bring dummy rows, hidden columns and stale headers. A placeholder/quarantine rule (AL-14 class) is mandatory.
4. **All equipment hours are estimated.** The canonical model needs `hours_basis`, and telematics (AL-07, AL-11) is the only route to verifiable hire or standby claims.
5. **There is no countersignature and no evidence.** A daily digital approval step by the [CONTRACTOR_JV] site supervisor, with photos attached, is the cheapest control with the largest effect on dispute position.

---

## 4. Proposed source → canonical mappings

Canonical names follow `data/templates/field_daily_report.schema.json`. Fields marked **(new)** are proposed extensions.

### RPT-A (German Word form, PDF)

| Source field | Canonical field | Transformation / rule |
|---|---|---|
| Datum (dd.mm.yy) | report_date | Parse, century 20xx; cross-check against the AN place/date. |
| Bauleiter (header) | supervisor_role = SUPERINTENDENT | Drop names. |
| (no company field) | supplier_id | Resolve from a sender/e-mail mapping or a configured form fingerprint. |
| Bauvorhaben line 2 (sub-location) | location_text **(new)** → location resolver | Landmark → site-facility ID (e.g. storage yard) → no KP; location_confidence = landmark. |
| Witterung ticks + Temperatur | weather, temperature_c **(new)** | First ticked box → enum; °C numeric. |
| Anzahl der beschäftigten Arbeiter | headcount **(new)** | Integer. |
| Arbeitszeit von/bis | shift_start, shift_end **(new)**; hours_worked | Span minus break; record break_h (new) = span − stated hours. |
| Category matrix (count / Std.) | labour[] {role, count, hours} **(new)** | Ambiguity flag where hours could be per person or total; default per person if equal to the net shift. |
| Free-text lines | lines[].remarks + NLP | Split at "-"; detect "Nx <equipment> <h>std" → equipment[]; detect "<n> Stk" → qty/unit. |
| Narrative equipment hours | equipment[] {type, count, hours, hours_basis = estimated} **(new)** | Regex `(\d+)x\s+(\w+)\s+([\d,]+)\s*std`. |
| Activity "Baustraße herstellen…" | activity_code = GRD/ACR-type (new code `HAUL_ROAD`) | qty = null → raise AL-14 "complete without quantity". |
| Behinderungen/Erschwernisse | downtime_reason, downtime_h | Empty → `NONE_STATED` (≠ NONE). |
| Leistungsänderungen | variation_note **(new)** | Text; non-empty → notify the commercial team. |
| Besondere Vorkommnisse | hse_events[] / inspections **(new)** | Text. |
| Unterschrift AN / AG + Ort/Datum | signoff.supplier, signoff.contractor **(new)** | Boolean presence + date; no image stored. |

### RPT-B (German Excel form, PDF)

| Source field | Canonical field | Transformation / rule |
|---|---|---|
| Letterhead | supplier_id | Form fingerprint. |
| Project no. | supplier_project_ref **(new)** | Keep in the private mapping table. |
| Datum | report_date | dd.mm.yyyy. |
| Name Mitarbeiter (list) | headcount = count(non-empty); labour[] role = UNSPECIFIED | **Discard names** after counting (or hash for AL-10). |
| Maschinen und Fahrzeuge "type x n" | equipment[] {type, count, hours = null} | Regex `(.+?)\s*x\s*(\d+)`; map type to the equipment vocabulary. |
| Vertrag Positionen | lines[].activity_text → boq_item_id **(new)** | Fuzzy match to the subcontract BoQ (e.g. groundwater monitoring well). |
| Anzahl ("ca. 3") | qty = 3, qty_is_estimate = true **(new)** | Strip "ca."; flag. |
| Einheit (Stck) | unit = nr | Unit map. |
| Standort (G161A und G162) | plan_sheet_from/to **(new)** → KP via resolver | Split at "und"/","; location_confidence = sheet. |
| Besonderes | lines[] (activity LOGISTICS, qty = null) / remarks | Text. |
| — | weather, downtime, hse, signoff | Set to `NOT_REPORTED` (explicit null-reason). |

### RPT-C (Excel workbook, [CONTRACTOR_JV] template copy)

| Source field | Canonical field | Transformation / rule |
|---|---|---|
| Cover!C2 (date) | report_date | Excel date. **Ignore the page-header date**; flag if it differs (template_residue = true). |
| Cover!C4 (No.) | supplier_report_no **(new)** | Integer; compare with the header and the previous report. |
| Cover!C3 (weather) | weather | "Rain" → RAIN. |
| Cover!B8:D19 | labour[] {role = C, hours = D}; headcount = count(D>0) | Skip rows where hours = 0; drop names (B). |
| Cover!D20 | man_hours_total (control total) | Recompute and compare. |
| Cover!B25:C36 | equipment[] {type = B, hours = C, hours_basis = estimated} | Skip blank hours; if hours == shift hours → hours_basis = shift_copied. |
| Cover!B42:B47 (3.1, EN/DE) | narrative_completed; lines[] activity via NLP | Keep the EN line, drop the DE duplicate; "unloading drilling equipment / set-up" → MOB. |
| Cover!B49:B54 (3.2) | narrative_planned **(new)** | Text. |
| Cover!B56:B62 (4.) | hse_events[] | Text; classify (security / safety / environment / QA). |
| Sheet5!B (hidden) | boq_item_id | Read hidden column. |
| Sheet5!C | activity_text | Required; a blank title with a quantity → placeholder. |
| Sheet5!F, G | unit, boq_total_qty **(new)** | Unit map (psch → ls). |
| Sheet5!H, I | plan_sheet_from / plan_sheet_to → KP | Resolver. |
| Sheet5!J, K, L, M | qty_prev_cum, qty (this period), qty_cum, pct | Recompute L = J + K and M = L / G; **if all rows are identical → quarantine the whole table**. |
| Sheet5!N, O, P | planned_cum, planned_pct, deviation | For S-curve only; not a claim basis. |
| — | location (crossing ID / pits), signoff | Missing → require at the template level. |

### RPT-D (Dutch form, PDF)

| Source field | Canonical field | Transformation / rule |
|---|---|---|
| Letterhead / Aannemer / Projectnr | supplier_id, supplier_project_ref | Fingerprint. |
| Boring (Ø, length) | crossing_ref **(new)** via resolver | Match diameter + length to the crossing register → crossing ID. |
| Plaats | location_text | Landmark. |
| Week + dd. (weekday dd-mm-yyyy) | report_date, iso_week **(new)** | Parse dd-mm-yyyy; validate the weekday and week number. |
| Header van / tot uur | shift_start, shift_end | Blank → null. |
| Ploegbezetting rows (role, name, firma, van/tot) | labour[] {role, employer_code, start, end, hours} | Role map NL → canonical (Uitvoerder → SUPERINTENDENT; Boormeester → DRILL_MASTER; Mudman → MUD_TECH; Assistent → OPERATIVE; Kraan → CRANE_OPERATOR); drop names; hours null if van/tot blank. |
| Inhuur | labour[].hired = true **(new)** | — |
| Eigen materiaal (model codes) | equipment[] {model_code, type via register, hours = null} | Register lookup required. |
| Omschrijving werkzaamheden | lines[] activity via NLP (NL) | "opbouwen" → SETUP, "TBM gebracht" → MOB, "afvoeren" → DEMOB; qty = null. |
| "locatie 160" | location_text → resolver | Possible plan/crossing reference; location_confidence = low. |
| Afspraken & opmerkingen (per day) | remarks / instructions **(new)** | Text. |
| Aannemer/Uitvoerder; Inspecteur/Toezichthouder | signoff.supplier, signoff.contractor | Presence check only. |

### RPT-E ([CONTRACTOR_JV] crew template, PDF)

| Source field | Canonical field | Transformation / rule |
|---|---|---|
| TAGESBERICHT nnn | supplier_report_no | Integer sequence → AL-02. |
| Datum | report_date | — |
| Kolonne | crew_id | Map the crew name to a crew ID. |
| Pos./Name/role (PM, BL, MS, SFB) | labour[] {role, count} | Role map: PM/BL → MANAGEMENT (flag as non-productive), MS → OPERATOR, SFB → SKILLED_OPERATIVE; drop names. |
| Anfang / Ende / Std. | shift_start, shift_end, hours | Validate hours = end − start − break; flag uniform copied times. |
| An/Abr. FW/priv., Datum | travel_mode, travel_date **(new)** | For travel-cost claims. |
| Geräte (per person) | equipment[].operator_role, unit_no | Links operator to machine (supports AL-07/AL-11). |
| Inv. Nr. / Kennz. | equipment[].unit_no / plate | Required for the telematics join. |
| Ausgeführte Arbeiten | lines[] activity_code = SHEETPILE (new), location → resolver ("BP160") | qty null → AL-14. |
| Geräte, Equipment auf Baustelle | site_equipment_inventory[] {type, count} **(new)** | Parse "type nx"; reconcile unit numbers with the per-person column (…45 vs …54 → data-quality flag). |
| Wetter (Temp, Sonne, Schnee, Wind, …) | weather, temperature_c | — |
| Toolbox banner | hse_toolbox_held = unknown **(new)** | Pre-printed text ≠ confirmation; require a tick and the attendee count. |
| Bemerkungen | remarks / downtime via NLP | — |
| 3 signature boxes | signoff.supplier / contractor_supervisor / contractor_pm | Presence check. |

---

## 5. Recommended minimum standard daily-report template for subcontractors

Design intent: a single page, bilingual DE/NL (EN optional), fillable as XLSX or in a mobile form, printable for crews without a device. Every field is either a code from a pick-list or a number with a unit. Free text is limited to one remarks box.

### 5.1 Fields

| # | Block | Field | Format / pick-list | Mandatory |
|---|---|---|---|---|
| 1 | Header | Subcontract no. (assigned by [CONTRACTOR_JV]) | code | Yes |
| 2 | | Report date | YYYY-MM-DD | Yes |
| 3 | | Report sequence no. (per subcontract, no gaps) | integer | Yes |
| 4 | | Crew / Kolonne / Ploeg ID | code from crew list | Yes |
| 5 | | Work front | crossing ID **or** KP from–to **or** plan sheet from–to (at least one) | Yes |
| 6 | Weather | Condition, temp °C, precipitation (none/light/heavy) | pick-list + number | Yes |
| 7 | Labour | Per role row: role (pick-list), number of persons, start, end, break, hours | numbers | Yes |
| 8 | | Personnel ID (badge/pseudonym, not names) | code | Optional; enables AL-10 |
| 9 | | Management/supervision shown separately from operatives | flag | Yes |
| 10 | Equipment | Unit no. (from [CONTRACTOR_JV] register), type, hours working, hours standby, hours basis (meter/telematics/estimate) | code + numbers | Yes |
| 11 | Production | One row per activity: BoQ item no. (pick-list), activity code, location (as #5), qty today, unit (fixed by BoQ), previous cumulative (pre-filled by [CONTRACTOR_JV]) | code + numbers | Yes, or "no measurable output" ticked with a reason (MOB/DEMOB/SETUP/LOGISTICS) |
| 12 | Downtime | Hours, reason code (weather, breakdown, waiting for preceding work, access/landowner, HSE stop, client instruction, other), affected crew/equipment | pick-list + number | Yes ("0 h" is explicit) |
| 13 | HSE | Toolbox held (Y/N, attendees), incidents/near-misses (count + ref), permits | tick + number | Yes |
| 14 | Evidence | Photo references (min. 2 per production row, with GPS/time stamp) | file refs | Yes for production rows |
| 15 | Variations / instructions | Instruction ref, description | ref + text | If applicable |
| 16 | Remarks | Free text (one box, ≤ 500 characters) | text | Optional |
| 17 | Sign-off | Supplier site manager (role, date/time); [CONTRACTOR_JV] site supervisor countersignature (role, date/time, "accepted / accepted with comment / rejected") | e-sign or wet-ink + scan | Yes, both, within 24 h |

### 5.2 Rules

1. **Submission deadline:** next working day, 10:00. A missing sequence number triggers AL-02.
2. **No quantity without a location and a BoQ item; no BoQ item without a unit.** Units are locked to the BoQ, so there is no free-text unit.
3. **Write "0", never leave a cell blank:** zero downtime and zero incidents must be entered explicitly, so that blank means "not reported".
4. **No approximate quantities** ("ca.", "~") in the production block. Estimates go to remarks and are not claimable.
5. **Equipment hours must state their basis.** Hours equal to shift length are accepted only with basis "estimate" and are subject to AL-07/AL-11.
6. **Names stay at the supplier.** The twin uses role + count, optionally pseudonymous badge IDs (GDPR data minimisation).
7. **Template integrity:** [CONTRACTOR_JV] issues a locked template per subcontract with pre-filled BoQ codes, units, previous cumulative and the crossing/front list. There are no sample values in distributed templates, and headers are formula-driven, not static.
8. **Countersignature does not equal acceptance of quantity:** the [CONTRACTOR_JV] supervisor confirms presence, resources and downtime daily. Quantities are confirmed through joint measurement (Aufmaß) and reconciled in the twin.
9. **Language:** labels in DE + NL. Pick-list codes are language-neutral, so the twin needs no translation for structured fields.
10. **Delivery format:** XLSX (preferred) or the mobile form. PDF is accepted only if it was generated from the template (text layer); photo-of-paper is accepted only as a fallback with OCR and a manual-review flag.

---

## 6. Limitations

- Sample of one report per supplier, from different dates spanning about eight months. Patterns may vary day to day.
- Interpretations of location codes ("BP160", "location 160", G-sheets) and equipment model codes must be confirmed against the crossing register and the equipment register.
- All five files were machine-readable (text layer / native XLSX). No handwriting was encountered in content fields; the only hand-drawn element is one signature (RPT-A).
