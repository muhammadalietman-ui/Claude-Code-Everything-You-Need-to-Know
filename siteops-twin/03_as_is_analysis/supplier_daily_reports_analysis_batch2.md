# Supplier Daily Reports – Structural Analysis, Batch 2 (RPT-F … RPT-J)

**Project:** SiteOps Twin – ingestion-layer design input
**Scope:** Five real subcontractor/vendor reports from an onshore DN1000 gas pipeline lot in Germany, received by [CONTRACTOR_JV]. Companion to the batch-1 analysis (RPT-A … RPT-E), which is kept as a separate document.
**Confidentiality:** Anonymised. Companies appear as [SUPPLIER_F] … [SUPPLIER_J], [CONTRACTOR_JV] and [CLIENT]. People appear by role only. Project numbers, town and road names, registration plates and contact details have been removed. The structured values are in the git-ignored file `data/private/supplier_reports_extract_batch2.json`.

| ID | Issuer trade | Form type | Period | Report date(s) | Medium |
|---|---|---|---|---|---|
| RPT-F | Pipe logistics / special transport ([SUPPLIER_F]) | Supplier's own Excel "site diary" (*Bautagebuch*) | Daily | 2026-03-02 | Digital PDF (Excel export), 2 pp., German |
| RPT-G | Large-diameter HDD drilling ([SUPPLIER_G]) | Rig datalogger "HDD registration sheet" | Cumulative per crossing, issued daily | 2026-03-17 (contains 2026-03-1x … 17) | Digital PDF (Excel export), 4 pp. landscape, Dutch/English |
| RPT-H | Small-diameter HDD (duct/PE pipe) ([SUPPLIER_H]) | ERP-generated *Tagesbericht* | Daily | 2026-09-28 | Image-only scan of signed printout, 1 p., German |
| RPT-I | Non-destructive testing (RT/UT) ([SUPPLIER_I]) | Weekly time-and-billing work report | Weekly (Mon–Sun) | Week 6/2026 (02.02–08.02) | Digital PDF (Print-to-PDF), 1 p., German/English |
| RPT-J | Hydrostatic testing ([SUPPLIER_J]) | Bilingual DE/EN daily report with half-hour grid | Daily, numbered | 2026-10-22, report no. 4 | Image-only scan, rotated 90°, 1 p. |

---

## (a) Report profiles

### RPT-F – Pipe logistics subcontractor, daily site diary

- **Format and language:** Excel template exported to PDF, so a text layer exists. German. The supplier's logo is on the form. There is a header block (project name as the supplier spells it, the supplier's internal job number, date) and a "planned output … m per day" field, which is **left empty**.
- **Sections:** (1) *Personal*: surname, first name, function, start, end, hours, travel by private or company car, remarks. (2) *Equipment / Maschinen / Fahrzeuge*: type, fleet or plate number, cumulative operating hours or odometer reading, defects, remarks. (3) *Leistung* (output): item, count, dimension or length, metres, "transported from … to …". (4) *Bemerkung* (remarks). (5) *Stillstand*: "why? who ordered it (names!)? from when to when?". (6) Internal notes: repairs, damage, accidents, incidents.
- **Location referencing:** Pipe-yard IDs (RLP-3, RLP-4), the generic word *Trasse* (right-of-way), and the **same construction-plan sheet numbers the JV uses** (G-137, G-160). Pipe-number ranges are given for the bends (e.g. "0740-0727"). There is no KP chainage.
- **Manpower:** Six named persons: site manager (no times), 2 truck drivers, 2 machine operators, 1 helper. Each works 07:00–18:00 and is booked at 11.00 h, so **no break is deducted**. The total row is blank; the computed total is 55 man-hours. The travel columns are blank.
- **Equipment:** Nine items: 2 excavators, 2 trucks, tractor, 2 vans, pick-up and compact wheel loader. Only 3 of the 9 carry a reading, and those are **cumulative meter or odometer totals** (unit not stated). No daily hours are given, so daily use can only be derived from the difference to the previous day's reading. Two excavators are tagged to "ROW" and "pipe yard 4", while all transport movements start at pipe yard 3.
- **Quantities:** 2 line pipes (DN1000/18 m, 36.01 m) moved to storage, 4 GRP-coated pipes (48.25 m) moved to sheet G-160, 7 bends (119.39 m) moved to sheet G-137. Computed total: 13 pieces, 203.65 m. The total row is blank. Figures are daily only, with no cumulative.
- **Downtime/standby:** A dedicated section that asks for reason, instructing person and time window. Empty on this day.
- **Weather / HSE:** None. HSE could only go in "internal notes", which is empty.
- **Sign-off:** **No signature block at all.** There is neither a supplier nor a JV countersignature.
- **Data-quality issues:** Blank totals. A typo in a time field ("18.00"). Truncated destination text. Plates and personal names used as keys. Equipment locations do not match the activity locations. Meter readings have no unit.

### RPT-G – Large-diameter HDD contractor, datalogger registration sheet

- **Format and language:** Excel export of the rig's datalogger, with a text layer. Dutch comments and English or Dutch column headers. Four landscape pages. The file name encodes the crossing ID, DN1000 and the date.
- **Structure:** A header block, then one row per **drill rod (joint)** in **reverse chronological order** (newest first). Stages are separated by "/ / / /" rows. Day boundaries are marked only by free-text dates typed into the comment column. The file is cumulative: the "daily" report for 2026-03-17 contains the whole crossing history.
- **Header fields:** Stage label ("Pilot – ream 820 – 1020"), rig size (150 t), datalogger version, tool number, total cone revolutions and cone-wear %, cumulative drill, down and connect times and their total, maximum pull/push forces and torque, a "Cubic" total, pump pressure, and the roles supervisor and driller.
- **Per-joint columns:** Joint no., start, finish, drill time, down time, connect-next time, position (in the pilot: depth m and inclination %; in reaming: advance m/min and cuttings %), pull/push and push/pull force (×10 kN, min/max), torque kNm, rpm, number of pumps, flow L/min, differential pressure bar (off/on), annular pressure bar, direction of returns (rig side / pipe side), formation, and a comment.
- **Stages present (dates partly inferred):**

| Stage | Joints logged | Drill h | Down h | Connect h | Flow L/min | Est. fluid m³ (flow × drill time) |
|---|---|---|---|---|---|---|
| Pilot (≈2 days to 12-03) | 4 → 45 | 4.5 | 0.5 | 18.6 (incl. overnight 13.6 h) | 1,100 | ≈ 290 |
| Ream 820 mm (12-03 → 13-03) | 45 → 1 | 9.4 | 13.9 (incl. overnight 12.8 h) | 3.8 | 1,800 | ≈ 970 |
| Ream 1,020 mm (16-03) | 43 → 1 | 7.0 | 0.5 | 3.1 | 1,800 | ≈ 730 |
| **Ream 1,400 mm (17-03, report day)** | **44 → 26 (19 joints)** | **6.1** | **0.3** | **1.2** | **2,000** | **≈ 725** |

  The header "Cubic 2720" reconciles with the sum of flow × drill time (≈ 2,710 m³ plus the unprinted pilot joints 1–3). It is therefore the cumulative drilling-fluid volume in m³, although the unit is not printed. The header time totals (27:14 / 15:10 / 26:51 = 69:16) are the cumulative sums **including overnight idle time**.
- **Location referencing:** Crossing ID only (in the file name and header). Position along the bore is expressed as a joint number. Neither rod length nor bore length is stated, so **metres drilled cannot be computed without master data**. There is no KP and no plan sheet.
- **Manpower:** Supervisor and driller named in the header. No headcount or hours.
- **Equipment:** Rig capacity only. The pump count is logged per joint. No other plant is listed.
- **Downtime:** Logged per joint as down or connect time, with free-text causes: waiting for water (≈ 1.5 h), waiting for transport, waiting for a rod, mud supply tank empty (×5), exit-pit container full, changing shaker screens (48 min), meeting with the mud engineer, and survey activities (gyro north-seeking, GPS shots). These are valuable for allocating responsibility for delays.
- **Weather / HSE / photos:** None.
- **Sign-off:** None. Supervisor and driller names are printed, but there is no signature or countersignature.
- **Data-quality issues:** A spreadsheet error "#DIV/0!" (Dutch locale). A finish time mistyped (11:42 → 12:55, which gives 112 % cuttings and 9.6 m/min). A missing connect time. A drill time inconsistent with start and finish. An Excel null date "0 Jan 1900" in the header. Pilot joints 1–3 are missing. Reverse ordering and free-text date markers make it hard to slice the file by day.

### RPT-H – Small-diameter HDD subcontractor, ERP daily report

- **Format and language:** Generated by a construction ERP or time-recording system, printed, signed by hand and scanned. The PDF is **image-only** and needs OCR. German.
- **Sections:** Header (supplier logo, the supplier's job number, *Projekt-Id* left blank, weekday and date). *Projektpersonal*: person, person type, activity, component, area, count, hours. *Leistungsergebnisse*: component, area and activity columns, with the actual content entered only as a **free-text remark**. Signature lines for contractor (*Auftragnehmer*) and client (*Auftraggeber*).
- **Location referencing:** "Pilot bore 11 (G153)", meaning a bore sequence number plus a JV plan-sheet number. The structured *Bauteil* (component) and *Baubereich* (area) fields are **empty**.
- **Manpower:** 2 persons (1 operative and 1 site manager), each 07:00–17:45 = 10:45 h, totalling 21:30 h. No break is deducted.
- **Equipment:** None listed, although an HDD rig, mud system and truck were evidently used.
- **Quantities (free text only):** Pilot bore 135.00 m. Pull-in with a 250 mm back-reamer of 1 × PE da160 pipe. **The pipe tore off at rod 10, was pulled out, 135.00 m was pushed again, and the pull-in was restarted.** A trip by truck to the supplier's depot to load bentonite. The report does not say whether the pull-in was completed.
- **Downtime:** Not declared, although the narrative describes a failure, rework and a depot trip.
- **Weather / HSE / photos:** None.
- **Sign-off:** **Both supplier and JV representative signed.** The JV countersignature is therefore applied to an unstructured, partly failed day.
- **Data-quality issues:** The free-text quantity mixes stages (pilot, pull-in, push). A metre figure (135 m) appears twice, once for the pilot and once for the push, which risks being double-counted. The structured fields are empty. There is no time split between drilling, rework and logistics.

### RPT-I – NDT inspection company, weekly work report

- **Format and language:** Excel form, Print-to-PDF, with a text layer. German billing terms and English headers. Includes a work-report number and week/year.
- **Issuer chain:** The "Client" box names an **intra-group affiliate of the NDT company** in another country, not the JV, and the client-reference field is empty. The report therefore belongs to a sub-subcontract chain and only reaches the JV indirectly.
- **Sections:** Header (office, contact, client, work location at lot level, implementation and assessment standard, both blank). A **Mon–Sun grid of inspectors × (start, duration)**. A **billing-item matrix** of rate-schedule code × unit × daily quantity. Examination type (X-ray, Ir, Se, Co, UT, MT, PT, …). Comment, object description, order description. Client acceptance (name, date, signature) and inspector approval.
- **Location referencing:** Lot level only. **The object description is empty and no weld numbers are given**, so the films cannot be linked to welds, KP or plan sheets.
- **Manpower:** 2 RT inspectors at 08:00 + 12 h on Mon and Tue, then "stand by" on Wed and Thu. 1 UT technician shown only as "stand by" on Thu. Reported total: 48 man-hours on Mon and Tue.
- **Billing quantities:** Mon and Tue each: RT crew 1 day, RT equipment 1 day, UT technician 1 day, UT equipment 1 day, dark room 1 day, coordinator 1 day, overtime 2 h. Radiographic films: 2 welds on Mon and 1 weld on Tue (**3 welds in total for the week**). Wed and Thu each: stand-by RT crew, RT equipment, UT crew and UT equipment, 1 day each.
- **Standby:** Billed on 2 days for 2 disciplines with **no reason and no instructing party**. The comment says "only on Thursday one control exposure", which contradicts a full standby day on Thursday, and no film is billed for it.
- **Weather / HSE / photos:** None.
- **Sign-off:** **Client acceptance and inspector signature are both blank.**
- **Data-quality issues:** The UT technician and equipment are billed on Mon and Tue with no matching time entry. Coordinator and dark room are billed per day regardless of output. Productivity is very low (1–2 welds per 12-h crew day plus overtime). The weekly granularity hides which day relates to which weld.

### RPT-J – Hydrotest contractor, bilingual daily report

- **Format and language:** A controlled bilingual DE/EN Excel form (revision and date stamp in the corner, sequential report no. 4). It was printed, signed and scanned on a multifunction printer. The page is **rotated 90°** and image-only, so it needs deskew/rotate and OCR.
- **Sections:** Header (project/lot, job no., customer = [CONTRACTOR_JV], supervisor, location as a town name, length 29,400 m, diameter 1000, date, report no.). An **operations log** of step, from, to and total. A **half-hour attendance grid 00:00–23:30** per employee (x = work, o = break) with daily totals. Machinery and equipment with inventory number and *hours of operation*. Accessories with delivered, size and used. Remarks. Signatures.
- **Location referencing:** Town name, "Hydrotest Sec. 2" and the section length. No KP range.
- **Manpower:** 6 persons (1 site manager and 5 technicians). Four worked 07:30–16:00 with a 1-h break (7:30 h each). Two arrived at 10:30 and worked through to 16:00 with no break shown (5:30 h each). Computed total: 41.0 man-hours.
- **Operations:** Meeting 0:15, modification/rig-up 6:15, function test 2:00 (07:30–16:00).
- **Equipment:** 13 items with inventory numbers: truck with crane and pump, test truck, filling and HP unit, HP pump, 2 cars, 3 fuel tanks, 2 generators (80/40), 2 submersible pumps. **The hours-of-operation column is empty.**
- **Accessories / consumables:** Control valve 4" ×1, fire hose 100 m, pontoon 1 (1 used), silencers 4" ×3, temporary pipe 6" 500 m delivered / 200 m used.
- **Quantities:** No progress quantity. The day is a set-up milestone for test section 2.
- **Weather / HSE / photos:** None.
- **Sign-off:** Supplier site manager by **digital signature, timestamped 15:27**, and the client (JV) by handwritten signature. **The supplier's signature precedes the reported end of work (16:00) and the function test (14:00–16:00)**, so hours were declared before they were worked.
- **Data-quality issues:** Rotated scan. A digital signature embedded in a scanned image cannot be validated. Hours of operation are empty. The test section is only identified as "Sec. 2".

---

## (b) Comparison matrix (canonical field × report)

Legend: ● structured field present and filled · ◐ present but partial, free text or derivable · ○ field on form but empty · – absent

| Canonical field | RPT-F Transport | RPT-G HDD logger | RPT-H Small HDD | RPT-I NDT weekly | RPT-J Hydrotest |
|---|---|---|---|---|---|
| report_date | ● | ◐ cumulative; day from free-text markers | ● (+weekday) | ◐ week + day columns | ● + report no. |
| supplier / subcontractor | ● logo | ● footer | ● logo | ● (client = affiliate) | ● |
| crew | ◐ names, no crew ID | ◐ supervisor/driller | ◐ 2 persons | ● inspectors × method | ● names + positions |
| work front / location | ◐ plan sheet + yard | ◐ crossing ID + joint no. | ◐ bore no. + plan sheet (free text) | – lot only | ◐ town + "Sec. 2" |
| KP chainage | – | – | – | – | – |
| activity | ◐ implicit (transport) | ● stage per block | ◐ free text | ◐ billing codes | ● operations log |
| quantity | ● count + metres | ◐ joints (no rod length) | ◐ 135 m in free text | ● films per weld | – (milestone only) |
| unit | ● pcs / m | ◐ joints, min, L/min, bar | ◐ m | ● day / weld / hour | ◐ accessories m/pcs |
| cumulative quantity | – | ● (whole log) | – | – | – |
| hours worked | ● start/end/hours | ● drill/down/connect per joint | ● start/end/hours | ● start + duration | ● half-hour grid |
| headcount / man-hours by category | ● function; total blank | – | ● person type; total | ● by method (RT/UT) | ● function; per-person total |
| equipment list | ● 9 items | ◐ rig + pumps | – | ◐ as billing items | ● 13 items + inventory no. |
| equipment hours | ◐ cumulative meter (3/9) | ● measured (logger) | – | – | ○ column empty |
| hours basis | meter reading | **measured** | n/a | billed by day | declared |
| downtime + reason | ○ dedicated section, empty | ● per joint + free-text cause | – (implicit in text) | ◐ "stand by", no reason | – |
| weather | – | – | – | – | – |
| HSE events | ○ "internal notes" empty | – | – | – | – |
| photos / evidence | – | ● logger data is evidence | – | ◐ films (not attached) | – |
| sign-off supplier | – | – | ● handwritten | ○ blank | ● digital (time-stamped) |
| client / JV countersignature | – | – | ● | ○ blank | ● |
| narrative | ○ empty | ◐ joint comments | ● free text | ◐ one-line comment | ◐ one-line remark |
| materials / consumables | ◐ pipe nos. moved | ● fluid volume (Cubic) | ◐ bentonite (no qty) | ◐ films | ● delivered/used |
| HDD-specific (stage, joints, forces, torque, flow, pressures) | – | ● full | ◐ stage + reamer size + rod no. of failure | – | – |
| billing / rate-item codes | – | – | – | ● | – |
| machine-readable | text layer | text layer | **OCR** | text layer | **OCR + rotate** |

---

## (c) Key findings for design

### C1. Ingestion requirements

1. **Five reports, five schemas, three media types.** Two image-only scans (RPT-H, RPT-J, the latter rotated) need an OCR path with deskew/rotation detection and a confidence score per field. The three digital PDFs come from Excel and can be parsed from their text layer, but their layouts are positional, so template-specific extractors (one per supplier form revision) are required. RPT-J carries a form revision stamp, which can serve as the template key.
2. **Period normalisation.** RPT-I is weekly and must be split into day records keyed by its day columns. RPT-G is **cumulative and reverse-chronological** and must be sliced by stage and by day using the free-text date markers and time arithmetic. Ingesting it as "today's progress" would re-count the whole crossing every day. Deduplicate by (crossing, stage, joint no.).
3. **Free-text quantity parsing.** RPT-H holds its whole output in a remark. A rule-based or LLM extractor must emit (stage, length, unit, plan sheet, bore no., event type = progress / failure / rework / logistics) and flag low-confidence results for human review.
4. **Master-data dependencies.** RPT-G needs rod length per rig/crossing to convert joints into metres. RPT-F needs a pipe-number register (pipe no. → plan sheet/KP). RPT-I needs a weld register to place films. Location resolution must accept **plan sheet**, **crossing ID**, **bore no.**, **pipe-yard ID**, **test section** and **town**, and map each to a KP range. None of the five reports states a KP.
5. **Hours semantics differ.** RPT-F and RPT-H: start–end without a break deduction. RPT-J: net of breaks. RPT-I: duration incl. overtime. RPT-G: machine drill, down and connect times, which include overnight idle time in the totals. The canonical model needs `hours_basis` (gross / net / measured / billed) and must not sum across bases.
6. **Equipment hours provenance.** Measured (RPT-G logger) ≠ cumulative meter (RPT-F, which needs the delta to the previous day) ≠ declared-but-empty (RPT-J) ≠ billed per day (RPT-I). Store `hours_source ∈ {telematics, logger, meter_delta, declared, billed, assumed}`.
7. **Privacy at ingestion.** Every report carries personal names; RPT-I and RPT-J also carry e-mail addresses and phone numbers, and RPT-F carries plates. Pseudonymise people into role + stable hash at the ingestion boundary. Raw files stay in the restricted store.

### C2. Commercial-control risks observed

- **Unsigned or unaccepted billing documents** (RPT-F, RPT-G, RPT-I). RPT-I bills standby, overtime and daily overhead items with **both acceptance boxes blank**.
- **Signature before work ends** (RPT-J: supplier signed at 15:27 for work declared until 16:00). The JV countersignature is applied without checking the time.
- **Rework presented as output** (RPT-H: pipe torn at rod 10, re-pushed 135 m, with a signed countersignature). Without structured fields the same 135 m can be claimed twice.
- **Standby without cause** (RPT-I: 2 days × 2 disciplines). The internal comment contradicts the standby claim.
- **Billed resources without attendance** (RPT-I: UT technician and UT equipment billed on Mon and Tue with no time entry).
- **Delay causes attributable to the JV** (RPT-G: waiting for water, transport and rods; mud tank empty). These could support supplier delay claims, and conversely give the JV objective evidence of the rig's actual working time.
- **Overhead per day regardless of output** (RPT-I: coordinator and dark room) combined with very low weld throughput.
- **Unused capacity on site** (RPT-J: 13 equipment items, 300 m temporary pipe unused). This is relevant if rental is charged per day.

### C3. Applicability of existing alert rules

| Rule | F | G | H | I | J | Note |
|---|---|---|---|---|---|---|
| AL-01 claim > measured | ◐ | ● | ● | ◐ | – | G logger = independent measure for HDD claims; H pilot length vs logger/as-built; F metres vs pipe register |
| AL-02 missing report | ● | ● | ● | ● | ● | J numbered sequence (no. 4) enables gap detection; I weekly — expect 1/week |
| AL-03 duplicate / overlap claim | ◐ | ● | ● | – | – | G cumulative re-ingestion; H 135 m appears twice |
| AL-04 cumulative > BoQ | ◐ | ● | ◐ | ● | – | I films vs number of welds in BoQ; G joints×rod length vs design length |
| AL-05 productivity drop | ● | ● | ◐ | ● | ◐ | G m/min & joints/day per stage; I welds per crew-day |
| AL-06 claimed without evidence | ● | – | ● | ● | ● | No photos in any report; I no weld IDs |
| AL-07 equipment working vs telematics idle | ● | ◐ | – | – | ● | F/J list plant without hours; G logger itself is evidence |
| AL-08 out of sequence | ◐ | ● | ● | ◐ | ◐ | G pilot→ream 820→1020→1400→pull-back; H pull-in after pilot; J hydrotest before tie-ins/NDT complete |
| AL-09 headcount above sensed | ● | – | ● | ● | ● | Compare declared persons to access-control/geofence |
| AL-10 impossible presence | ● | – | ● | ● | ● | Same person on several suppliers' reports or 24-h overlaps; I 12-h days |
| AL-11 equipment hours vs telematics | ● | ● | – | – | ● | F meter delta; G logger vs rig telematics |
| AL-12 front active without presence | ● | ● | ● | – | ● | e.g. G logger shows drilling while no crew report exists |
| AL-13 weather standby unsupported | ○ | – | – | ● (standby, reason missing) | – | Generalise to any standby |
| AL-14 report text vs quantities disagree | ● | ● | ● | ● | ◐ | I comment vs Thursday standby; H failure text vs claimed metres; F blank totals |

### C4. Proposed new rules

| ID | Rule | Trigger (from this batch) |
|---|---|---|
| **AL-15** | **Signature / submission timestamp earlier than declared end of work** | RPT-J: digital signature 15:27 < 16:00 |
| **AL-16** | **Rework or failed attempt not separated from progress**: free-text keywords (tear-off, re-pull, again, repeat) or repeated metre values in the same report, so the quantity is held until verified | RPT-H |
| **AL-17** | **Standby / idle billed without reason or instructing party** (any cause, not only weather); escalates if the same day shows productive output elsewhere | RPT-I Wed/Thu; RPT-F standby section empty |
| **AL-18** | **Billing line without matching attendance** (rate item billed for a resource with no hours in the time grid) | RPT-I UT technician and equipment, Mon/Tue |
| **AL-19** | **Internal arithmetic failure**: blank or mismatching totals, spreadsheet errors (#DIV/0!), finish < start, rate > physical maximum | RPT-F, RPT-G |
| **AL-20** | **Cumulative meter non-monotonic or implausible delta** (hour meter / odometer per fleet ID day-to-day) | RPT-F |
| **AL-21** | **Unsigned / unaccepted document used for payment**: block certification until the countersignature exists | RPT-F, RPT-G, RPT-I |
| **AL-22** | **Material-movement vs installation chain**: pipes or bends delivered to plan sheet X (pipe nos.) must precede stringing/welding claims at X; claims without a delivery record, or deliveries never installed, are flagged | RPT-F |
| **AL-23** | **HDD logger-to-claim reconciliation**: metres = joints × rod length per stage/day; the downtime causes logged must match the delay or standby claims of the driller or JV | RPT-G (also cross-check RPT-H) |
| **AL-24** | **Pay-item overhead without output**: daily overhead items (coordinator, dark room, site car) billed on days with zero productive quantity | RPT-I |

### C5. HDD-specific observations (independent progress evidence)

- RPT-G provides, per joint, stage, timestamps, drill/down/connect durations, advance rate, forces, torque, rpm, flow and pressures. From these a **daily progress curve per stage** (joints per day, metres once rod length is known) and a **drilling-fluid volume** (≈ 725 m³ on the report day; ≈ 2,720 m³ cumulative) can be derived. Fluid volume is a further check against mud-disposal and water-supply invoices.
- Stage sequence evidenced: pilot → ream 820 → ream 1,020 → ream 1,400 (in progress, 19 of ~44 joints on day 1). Pull-back has not yet been logged. Valid for AL-08.
- Minimal canonical HDD extension: `crossing_id, stage{pilot|ream_d|swab|pullback}, tool_diameter_mm, joint_from, joint_to, rod_length_m, metres, drill_h, down_h, connect_h, down_reasons[], flow_L_min, fluid_m3, max_pull_kN, max_torque_kNm, annular_bar, returns_side, survey_events[]`.
- RPT-H (small HDD) gives only stage, length, reamer size, product pipe and failure rod number. It should be ingested into the same extension with `source_quality = narrative`.

---

## (d) Per-report mapping tables (source field → canonical field)

### RPT-F

| Source field | Canonical field | Transform / note |
|---|---|---|
| Datum | report_date | dd.mm.yyyy |
| Logo / footer | supplier | lookup → supplier_id |
| Projekt, Projekt-Nr. | project_ref (supplier side) | map supplier job no. → JV subcontract no. |
| geplante Leistung (m/Tag) | planned_daily_output | empty → null |
| Name, Vorname | person_id | pseudonymise |
| Tätigkeit | person_category | Bauleiter→site_mgmt (indirect); Kraftfahrer/Maschinist/Helfer→direct operative |
| Beginn, Ende, Anzahl Stunden | hours_worked (gross) | hours_basis = gross_no_break |
| Anfahrt privat/Firmen-PKW | travel_mode | optional |
| Fahrzeugtyp | equipment.type | normalise to equipment class |
| Fahrzeug-Nr./Kennzeichen | equipment.fleet_id | hash plates |
| Betriebsstunden/Kilometerstand total | equipment.meter_reading | daily_hours = Δ previous day; hours_source = meter_delta |
| Bemerkungen (equipment) | equipment.location_note / defect | "Trasse"/"RLP-x" → work_front |
| Leistung: Anzahl, Dimension, Meter | quantity (pcs, m) | activity = pipe_transport |
| Transportiert von … nach … | location_from / location_to | RLP-x → yard; G-xxx → plan_sheet → KP range; pipe nos. → pipe register |
| Bemerkung | narrative | |
| Stillstand | downtime {reason, instructed_by, from, to} | instructed_by → role only |
| interne Vermerke | hse_events / incidents | |
| – | sign_off | none → AL-21 |

### RPT-G

| Source field | Canonical field | Transform / note |
|---|---|---|
| File name / header crossing code | crossing_id | lookup → crossing register (start/target pit, KP) |
| Sheet date / free-text date markers | report_date per row | slice reverse-chronological log by day |
| pas / "/ / / /" separators / formation-column labels | hdd.stage, tool_diameter_mm | pilot / ream 820 / 1020 / 1400 |
| Joint nr | hdd.joint_no | metres = joints × rod_length (master data) |
| start, finish | activity_start/end | |
| Drill / down / connect time | hdd.drill_h / downtime_h / connect_h | split overnight gaps > 4 h as non-working |
| Activity / comments | downtime.reason / survey_event | dictionary NL→canonical cause codes |
| Position end drill | pilot: depth_m, inclination_pct; ream: rate_m_min, cuttings_pct | stage-dependent semantics |
| Pull/Push, Push/Pull, Torque, Rotary | hdd.forces_kN (×10), torque_kNm, rpm | min/max |
| Pump total, Liter/min | hdd.pumps, flow_L_min | fluid_m3 = flow × drill_time |
| Bar differential / annular | hdd.pressures | |
| Direction of returns | hdd.returns_side | Rs / Ps |
| Cubic (header) | hdd.fluid_m3_cumulative | |
| Total cone revolutions / % | hdd.tool_wear | |
| Supervisor / Driller | crew roles | pseudonymise |
| – | sign_off | none |
| – | equipment.hours | rig hours = Σ drill+connect on the day, hours_source = logger |

### RPT-H

| Source field | Canonical field | Transform / note |
|---|---|---|
| Date (with weekday) | report_date | |
| Logo / header | supplier | |
| Supplier job no., Projekt-Id | project_ref | Projekt-Id empty |
| Personal | person_id | pseudonymise |
| Personaltyp | person_category | Gewerblich → direct; Bauleiter → indirect |
| Tätigkeit | activity | "HDD Bohrungen" → hdd_small_diameter |
| Beginn/Ende, Gesamt | hours_worked | gross_no_break |
| Bauteil / Baubereich | work_front | empty → derive from remark |
| Bemerkung (free text) | narrative + parsed quantities | NLP: bore_no = 11, plan_sheet = G153, stage = pilot, length = 135 m; stage = pull-in, reamer 250, pipe PE da160; event = failure at rod 10 (rework); logistics = bentonite trip |
| Unterschrift Auftragnehmer / Auftraggeber | sign_off.supplier / sign_off.jv | presence detection on scan |
| – | equipment, weather, HSE | absent |

### RPT-I

| Source field | Canonical field | Transform / note |
|---|---|---|
| Week / year + day header dd/mm | report_date (one record per day) | explode weekly → daily |
| Workreport-No. | source_doc_id | duplicate check |
| Issuer / Client box | supplier / contract_chain | client = affiliate → map to JV subcontract via order ref (empty) |
| Work location | work_front | lot level only |
| Inspector name, method (RT/UT) | person_id, person_category = NDT_RT / NDT_UT | pseudonymise |
| Anfang, Dauer | hours_worked | basis = billed_duration (incl. overtime) |
| "stand by" | downtime {type = standby, reason = null} | AL-17 |
| Billing item code/text, Einh., Menge | billing_line {rate_code, unit, qty, date} | map rate code → BoQ/price list |
| 8.8 Radiography film DN1000 (Naht) | quantity = welds examined | link to weld IDs (missing) |
| Examination type | ndt_method | |
| Comment | narrative | cross-check vs standby (AL-14) |
| Object / Order description | weld_ids / order_ref | empty |
| Accepted by client / inspector approval | sign_off | blank → AL-21 |

### RPT-J

| Source field | Canonical field | Transform / note |
|---|---|---|
| Datum / Date, Report No. | report_date, report_seq | gap detection AL-02 |
| Project, Job No., Customer | project_ref, supplier job | |
| Standort / Location, Länge, Durchmesser | work_front (town → section), section_length_m, DN | needs test-section register → KP range |
| Bauleiter / Supervisor | crew lead role | pseudonymise |
| Arbeitsschritt, von, bis, Gesamt | activity_log {activity, start, end, duration} | meeting / rig-up / function test |
| Mitarbeiter, Funktion | person_id, person_category | |
| Half-hour grid x/o, Gesamt | hours_worked (net), break windows | basis = net |
| Maschinen, Inventarnummer | equipment.type, fleet_id, count | |
| Betriebsstunden | equipment.hours | empty → hours_source = assumed |
| Zubehör geliefert / verwendet | materials {delivered, used} | |
| Bemerkungen | narrative | "Setup for Hydrotest Sec. 2" → milestone |
| Digital signature (supplier) | sign_off.supplier + signed_at | compare to last worked slot (AL-15) |
| Handwritten client signature | sign_off.jv | presence detection |
| Stand / Rev. | template_version | extractor selection |

---

## Summary of design implications

1. Build a **template registry** with one extractor per supplier form and version, an OCR branch with rotation detection, and confidence scoring.
2. Treat **time basis, equipment-hours source and quantity source** (structured, narrative, logger) as first-class attributes in the canonical model.
3. Add a **location-resolution service**: plan sheet, crossing ID, bore no., pipe no., weld no. and test section all resolve to a KP range. No supplier in this batch reports KP.
4. Add an **HDD extension** fed primarily by datalogger exports. Datalogger data is the strongest independent progress evidence in this batch.
5. Make **sign-off status and timestamp** a gating attribute for certification, and add rules AL-15 to AL-24 to the alert catalogue.
