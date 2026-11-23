# Subcontractor Documents – Structural Analysis, Batch 3 (RPT-K … RPT-N)

**Project:** SiteOps Twin – ingestion-layer and claim-side design input
**Scope:** Four real subcontractor documents from the onshore DN1000 gas pipeline lot, received by [CONTRACTOR_JV]. This is the first batch to contain **claim-side documents**: a cumulative series of work records used as partial measurements (RPT-K) and a bill-of-quantities claim with weekly evidence sheets (RPT-N). Companion to batch 1 (RPT-A…E), batch 2 (RPT-F…J) and the consolidated design `04_to_be_architecture/data_model/supplier_report_ingestion_design.md`, which this file builds on and does not change.
**Confidentiality:** Anonymised. Companies appear as [SUPPLIER_K], [SUPPLIER_L] (issuer of both RPT-L and RPT-M), [SUPPLIER_N], [CONTRACTOR_JV] and [CLIENT]. People appear by role only. Town, station and order identifiers, signatures, unit rates and monetary amounts are **not** reproduced; they are described qualitatively. Plan-sheet numbers (G-nnn) and crossing/measuring-point codes are kept because they are the location keys being analysed. Structured values, including rates and amounts, are in the git-ignored `data/private/supplier_reports_extract_batch3.json`.

Legend for evidence status: [F] fact read from the document · [C] computed by us · [I] interpretation · [VERIFY] legal or contractual point to be confirmed.

| ID | Issuer trade | Form type | Period | Pages / medium |
|---|---|---|---|---|
| RPT-K | Cathodic-protection (CP, *KKS*) measurement and installation ([SUPPLIER_K]) | Generic *Arbeitsnachweis* (daywork / work-record form) used as *Teilaufmaß* (partial measurement), records Nr. 01–07 | 2025-10-30 … 2026-10-30, 7 records of 1 day to 5.5 months each | 36 pp.; pp. 1–25 scans of signed printouts, pp. 26–36 native digital |
| RPT-L | Field-joint coating / coating repair ([SUPPLIER_L]) | *Tagesbericht – Pipeline*, controlled form (revision stamp) | Daily, 2026-03-30 | 2 pp., digital PDF with text layer |
| RPT-M | Same supplier as RPT-L, station variant | *Tagesbericht – Station*, report no. 1 | Daily, 2026-08-31 | 2 pp., image scan, page order reversed |
| RPT-N | Pressure testing and calibration pigging of cable-protection ducts (*KSR*) ([SUPPLIER_N]) | *Bill of Quantities* claim no. 1 + three weekly *Arbeitsnachweise* (Nr. 1–3) as evidence | Calendar weeks 42–44/2026 (2026-10-14 … 10-29) | 5 pp., digital PDF with text layer |

All 36 + 2 + 2 + 5 = 45 pages were read. No page was unreadable. RPT-K Nr. 02 states "page 1 of 2", but only page 1 is in the bundle (see K-F9).

---

## (a) Profiles

### RPT-K – CP subcontractor, work records Nr. 01–07 (partial measurements)

- **Form [F].** A generic German *Arbeitsnachweis* template with the classic daywork columns: *Beschäftigte – Namen o. Anzahl* (persons: names or number), *gearbeitete Zeiten – Nettoarbeitszeiten angeben* (hours worked, net) and *Art der Arbeit* (type of work). It also has a distribution box (accounting / contractor / client), a *Kontierung* (cost-coding) grid, the tick-boxes *Teilaufmaß / Schlussaufmaß / Leistungen abgenommen* (partial / final measurement / work accepted), an order-number field, a period from/to, and signature fields for contractor (*Auftragnehmer*) and client (*Auftraggeber*). **On all 36 pages the persons and hours columns are empty, the cost-coding grid is empty and "work accepted" is not ticked.** Only *Teilaufmaß* is marked. The form is therefore used as an **interim measurement / billing sheet**, not as a daywork sheet in the VOB/B sense, although it contains daywork-type items.
- **Structure [F].** Continuous position numbers 1–119 across all seven records. Each position is a visit day with sub-lines: a contract item (*LV-Pos.*) with location code and date, technician hours, travel, day rate, and material. Each page carries a running subtotal (*Summe/Übertrag*) and the last page a grand total (*Gesamtsumme*). There is **no cumulative-to-date per contract item, no contract quantity and no previous-claim reference**; each record restarts from zero.
- **Pricing bases (changes over time) [F].**
  - Nr. 01 (5.5 months): site set-up lump sum; **unit rates** per coating-defect test (*elektrolytische Porenprüfung*), in two variants: single visit (*Einzelmaßnahme*) and multiple-in-one-visit, the latter at a lower rate; current-injection measurement (< 1,500 m); **technician waiting hours** under a contract hourly item; **travel per visit**, with the first five trips included and every further trip charged.
  - Nr. 02–07: **day rate per CP technician** (*Tagessatzbasis*). The measurements are listed as zero-value lines inside the day rate. Second (and from 21.10 third) technicians and "2 vehicles travelled separately" are added as "announced and confirmed on <date>". Materials and measuring-point installations are added at contract unit rates. Nr. 07 adds **addendum items** (*Nachtrag 01/02*: temporary earthing, earthing systems) and one line explicitly "billed on a cost-plus basis" (*Abrechnung nach Aufwand*).
  - [C] By value, technician day rates are about two thirds of the seven records; unit-rate measurements about one tenth; addendum items slightly less; travel and materials about one twentieth each; waiting hours about 2 %.
- **Location referencing [F].** Plan sheet + object code, e.g. `G153_SP5_08E`, `G113/114_SK1`, `G178_1663`, `G141_MK`. The infixes (SP, SK, LK, WK, MK) appear to denote crossing or object types (MK = measuring point) [I, VERIFY with the CP engineer]. Sections are given as sheet ranges (`G141–G149`, `G169 bis G174`). Two stations are named by town; they are anonymised here as **station S1** (sheet G141, the same station as RPT-L/RPT-M) and **station S2** (G174). There is no KP.
- **Manpower [F].** Never as persons × hours. Implicit: one technician per day rate; second and third technicians as extra day-rate lines. In Nr. 01, waiting hours give time windows (e.g. 12:00–19:00) but no person. On 13.03, 17.03 and 20.03/2026 the **same waiting-hour line appears twice with an identical time window**, which would require two technicians. No second technician is declared, and on 14.03 and 17.03 there is "no separate travel".
- **Equipment [F].** Only "2 vehicles travelled separately" and "1 special measuring set (IFO, modified)". No hours.
- **Quantities [C].** 110 technician-day units over 78 dates (Nr. 02–07); 27 hourly lines in Nr. 01 (84.5 h waiting + 5 h "immediate-measure surcharge"); 33 charged travel lines; 46 coating-defect tests at one crossing (`G113/114_SK1`) in five days without individual test IDs; about 25 measuring points installed.
- **Downtime [F].** Waiting hours (*Wartezeiten*) without a cause. One line names a JV site representative as the person who agreed it (*Abstimmung*). "No measurement – no feedback", "note without measurement" and two **abortive visits** (*Fehlanfahrt – Messung konnte nicht durchgeführt werden*) are charged at the full item or day rate.
- **Weather / HSE / photos [F].** None.
- **Sign-off [F].** Supplier: place and date on every record. JV: Nr. 01 and Nr. 02 carry a qualified **digital signature of a JV staff member ("reason: verified")** plus handwritten initials and "OK"; reviewer highlighting on positions 1–2. Nr. 03 has a JV stamp, a handwritten signature and a date. Nr. 04–06 have handwritten JV signatures **without a date**. Reviewer ticks and **circled unit rates** appear on Nr. 03–06. **Nr. 07 is not signed by the JV.** A document-management stamp ("attachment 2 … end of original document") on Nr. 04 shows that the records were filed as attachments to a further document, probably an invoice.
- **Data-quality issues [F/C].** Year typos in period headers (Nr. 02 "2025", Nr. 05 pp. 2–3 "2025"). Position 43 is used twice. A carry-forward on Nr. 06 p. 5 reads a single-digit amount below the computed sum, possibly a scan artefact; the grand total is correct. Intermediate totals are placed in the grand-total row (Nr. 07 pp. 8 and 10). Item-code collisions are listed in K-F7. Every other page subtotal and grand total re-computes exactly (AL-19 passed for 35/36 pages).

### RPT-L – Coating subcontractor, "Pipeline" daily report

- **Format [F].** A controlled two-page form (revision date in the footer), digital, German. Page 1 is a weld-joint coating grid (pre-fabrication welds; further welds, full re-coating and defect spots) with weld no., extra width (*ÜB*, m), rock-shield mat (*RS*, m), dew point OK (*TP*), enclosure (*E*), and a joint type (connecting weld, press weld, 4-layer full coating, 2-layer defect spot). Page 2 holds further works (from/to, m, persons, hours, test equipment), material, **daywork hours (*Regiestunden*)** with person, vehicle, special vehicle and blasting unit, personnel deployment, remarks and two signature fields.
- **Content [F].** Report no., cost centre, dew point and test equipment are blank. Weather: showers. The page-1 grid is empty (all auto-totals 0). Daywork: 2 persons × 10.00 h, 1 vehicle. Remark: at **station S1**, an exposed window of 0.50 m × 0.50 m on the client's **existing DN 400 line with a DN 50 branch**, "= 2.20 m" [unit or meaning unclear], coated with three layers of two-component liquid coating; 9 cartridges consumed; "2 men + vehicle + 4 h travel". The material table is empty; the consumption appears only in the remark.
- **Location [F].** Station name and the existing line only. No sheet or KP.
- **Sign-off [F].** Supplier signed on the day. **JV/client field blank.**
- **Issues [I].** (1) 20 man-hours for a repair of about 0.25 m² (or 2.2 m², unclear), with 4 h travel embedded and not separated. (2) Coating applied in showers with no dew-point record, a quality point the form itself demands. (3) Work on the client's existing asset billed as daywork, with no instruction reference. (4) The "Pipeline" form was used for station work.

### RPT-M – Same supplier, "Station" daily report no. 1

- **Format [F].** Station variant of the same form (it adds a fittings/flange grid). Scanned, with page 2 before page 1. Report no. 1, cost centre filled, weather: rain, dew point and test equipment blank.
- **Content [F].** Daywork: **2.00 h "travel from depot to station"** (persons 2, vehicle 1) and **1.00 h "coating with PUR material"** (persons not stated). Personnel: 1 responsible + 1 skilled worker. Material: 1 piece of two-component coating, large. Remark: "valve foot repaired with two-component coating". The station grid is empty, but the first weld-count total shows **1 with no rows filled**, a formula or template residue.
- **Sign-off [F].** Supplier signed 2026-08-31. JV signed by hand, **dated 2026-09-07**, i.e. on the sixth working day (Werktag, Saturdays counted) [C, VERIFY against the §15 deadline].
- **Issues [I].** Travel is two times the productive time, and whether the 2 h is per person (4 man-hours) is ambiguous. There is no repaired area or quantity. **There is no link to the station's lump-sum item or a stage** (see C6, T-507).

### RPT-N – Duct pressure-testing subcontractor, BoQ claim weeks 42–44 (PRIORITY)

- **Structure [F].**
  - **Page 1, *Bill of Quantities*.** Header: lot and scope "pressure tests and calibration pigging", claim **no. 1**, period "KW 42–44". Header quantities: billable route length 30,100 m × 3 ducts = 90,300 duct-m; "monthly performance" 11,661 m × 3 = 34,982 duct-m; remaining 18,439 m × 3 = 55,318 duct-m.
  - **Table:** item, description, unit, quantity, unit rate, amount. Seven lines: (1) mobilisation/demobilisation, 1 pc; (2.1) foam-pig cleaning run; (2.2) calibration with caliper pig; (2.3) air pressure test, each 34,982 m; (3.1) standby/waiting, 11 h; (3.2) repeat pigging and testing, 2,165 m; (3.3) repeat air pressure test, 1,427 m. Then the total for the billing period.
  - **Columns that are not there:** contract quantity per item, previous cumulative, cumulative to date, % complete, location and date per line, evidence reference.
  - **Pages 2–5:** three weekly *Arbeitsnachweise* (Nr. 1–3, one per week). Columns: date, from, to, duration (h), **from plan sheet / to plan sheet**, completed tested route length (m), value = hours × hourly rate, remarks. Each has a weekly total for hours, metres and value, a remaining-length chain, and a field **"JV confirmation" (*Bestätigung ARGE*), blank on all three**.
- **Evidence content [F].** 19 work rows on 10 working days. 98 h in total (12.5 / 49.5 / 36). Route metres 11,660.65 (2,172.65 / 6,765 / 2,723). The remarks record per-duct results by colour (red, green, orange), leaks, defective or badly assembled couplers, ducts damaged by excavation, ducts under water, waiting for an excavator, an excavator withdrawn at 15:00, "unclear which sections to test", repair assistance, travel and induction. One remark names a JV site representative as informed and states that a surveyor "must be commissioned by the client".
- **Location [F].** Plan-sheet ranges G100–G112, G153–G168, two point entries ("G153–G153 … bore", "G165–G165 … bore"). No KP.
- **Sign-off [F].** No signature anywhere. JV confirmation is blank on all three weeks.
- **Arithmetic [C]: see C3 (AL-19).** Internal sums are correct. The findings are structural: hidden cells, the multiplier and overlaps.

---

## (b) Comparison matrix (canonical field × document)

Legend: ● structured and filled · ◐ partial / free text / derivable · ○ field on form but empty · – absent

| Canonical field | RPT-K CP work records | RPT-L Coating "Pipeline" | RPT-M Coating "Station" | RPT-N BoQ claim + weekly records |
|---|---|---|---|---|
| document / claim no. | ● Nr. 01–07, pos. 1–119 | ○ blank | ● 1 | ● claim 1; weekly Nr. 1–3 |
| period / report date | ● from–to; date per line | ● | ● | ● weeks; date per evidence row |
| supplier | ● | ● | ● | ● |
| contract / order ref. | ● (changes between Nr. 01 and Nr. 03) | – | ◐ cost centre | ◐ lot + scope |
| contract item no. (BoQ/LV) | ● LV-Pos. (+ addendum, collisions) | – | – | ● supplier item 1…3.3 (not the contract LV no.) |
| unit / unit rate / amount | ● | – | – | ● |
| contract qty per item | – | – | – | ◐ header route length only |
| previous / cumulative qty | – (restarts each record) | – | – | ◐ remaining-length chain only |
| location | ◐ sheet + object code | ◐ station, free text | ◐ station (project field) | ◐ sheet ranges in evidence only |
| KP chainage | – | – | – | – |
| work date per line | ● | ● | ● | ◐ evidence only, not on claim lines |
| quantity per line | ● (tests, points, m cable) | ◐ in remark | ◐ material count only | ● claim; ● route m per evidence row |
| per-component result (pass/fail) | ◐ "Fehler", "2. Messung" | – | – | ◐ duct colour in remarks |
| persons × hours | ○ columns empty | ● daywork 2 × 10 h | ◐ 2 h × 2 persons? + 1 h | ◐ hours per row, crew not stated |
| hours basis | day rate / billed hours | gross incl. travel | declared | gross (no breaks), billed |
| equipment | ◐ vehicles, special kit | ◐ 1 vehicle | ◐ 1 vehicle | – |
| material | ● priced, "lt. Materialbeistellung" | ◐ remark only | ● 1 item | – |
| downtime / waiting + cause | ◐ hours, no cause | – | – | ◐ remarks; 11 h claimed with no rows |
| instruction reference (daywork) | ◐ "announced and confirmed", 1 named | – | – | – |
| weather | – | ● | ● | – |
| HSE | – | – | – | ◐ induction mentioned |
| photos / test protocols | – | – | – | – |
| supplier sign-off | ● | ● | ● | – |
| JV countersignature | ◐ Nr. 01–06 (dated: 03 only), Nr. 07 none | ○ blank | ● dated +6 working days | ○ blank ×3 |
| machine-readable | OCR (pp. 1–25), text (pp. 26–36) | text | OCR | text (+ hidden cells) |

---

## (c) Design findings

### C1. Ingestion

1. **The claim side is a distinct document family.** A BoQ claim (RPT-N p. 1), weekly evidence sheets (RPT-N pp. 2–5) and cumulative interim measurements (RPT-K) need a `source_document.doc_class ∈ {DAILY_REPORT, WORK_RECORD, DAYWORK_SHEET, INTERIM_MEASUREMENT, BOQ_CLAIM}` and a **claim ↔ evidence link**. Daily-report adapters cannot be reused as they are.
2. **One record, several pricing bases.** RPT-K mixes lump sum, unit rate, hourly, per-visit travel, day rate, addendum and material lines on the same page, and the basis changes between records. Every extracted line needs `pricing_type` and must map to a contract item **including the addendum id**. "003.01" means a measuring point in the base contract and an earthing package in addendum 01.
3. **Hidden spreadsheet cells.** RPT-N's text layer contains values in visually empty columns to the right of the claim total (see N-F1). The PDF text extractor must keep cells that are not printed and flag them. Visual OCR alone would miss them.
4. **Zero-value descriptive lines.** In RPT-K the measurements inside a day rate carry no amount. They are evidence of work done, not billing lines, and should be loaded as `claim_evidence` with `billable = false`.
5. **Location keys.** RPT-K object codes (`G153_SP5_08E`, `G178_1663`, `G141_MK`) and RPT-N sheet ranges (`G106–G112`) both resolve through plan sheet → KP. RPT-K also needs a **CP asset register** (measuring point, test point, anode field, earthing) because installations are billed per asset (AL-31).
6. **Scans with handwriting and stamps.** Reviewer ticks, circled rates, highlights and "OK" are review evidence. They should be detected as annotations with page/line anchors, not discarded.
7. **Privacy.** RPT-K and RPT-N name JV staff in billing lines and remarks, RPT-K carries a JV e-mail inside the digital-signature block, and RPT-L/M name supplier staff. Pseudonymise to role at ingestion (as in batch 2, C1-7).

### C2. Claim-side model changes (delta proposal, not yet in `db.py`)

| Entity | Change | Evidence |
|---|---|---|
| `boq_item` | Composite key `(subcontract_id, addendum_id, item_no)`; + `description`, `pricing_type` (`UNIT_RATE`/`LUMP_SUM`/`DAY_RATE`/`HOURLY`/`MILESTONE`/`COST_PLUS`), `contract_qty` **nullable**, `qty_multiplier` + `multiplier_basis` (e.g. 3 ducts per route m), `stage_weights` for milestone items | RPT-K code collisions; RPT-N ×3 ducts; T-507 |
| `subcontractor_claim` | + `claim_no`, `doc_id`, `claim_type` (`INTERIM`/`FINAL`), `period_label`, `prev_claim_id`, `is_cumulative`, `signoff_supplier_at`, `signoff_jv_at`, `jv_signer_role`, `review_annotations` | RPT-N claim 1; RPT-K Nr. 01–07; sign-off pattern |
| `subcontractor_claim_line` | + `item_no_supplier`, `boq_item_id` (resolved), `qty_prev_cum`, `qty_this`, `qty_cum`, `unit_rate` and `amount` (private store), `component` (e.g. duct colour), `result` (`PASS`/`FAIL`/`N/A`), `is_repeat`, `repeat_of_line_id`, `cause_party` (`SELF`/`JV`/`THIRD_PARTY`/`CLIENT`/`UNKNOWN`), `location_ref_type`/`_value`, `work_date` **nullable**, `evidence_ids[]` | RPT-N period-total lines; repeats; damage by others |
| `claim_evidence` (new) | `evidence_id`, `doc_id`, `work_date`, `start`, `end`, `hours`, `sheet_from`, `sheet_to`, `route_m`, `component_results` {colour: pass/fail}, `remarks`, `billable` | RPT-N weekly rows; RPT-K zero-value lines |
| `daywork_sheet` (new) | `sheet_no`, `work_date`, `instruction_ref` (who/when/how), `persons[]` (pseudonym, role, start, end, break, net h), `equipment[]` (id, h), `material[]` (qty, `client_furnished` flag), `cause`, `submitted_at`, `countersigned_at`, `objection_at`, `status` | Checklist (f); RPT-K, RPT-L, RPT-M |
| `cp_asset` (new) | `asset_id`, type (measuring point R/P/SW/I, reference electrode, coupon, anode field, earthing), sheet, KP, `installed_at`, `billed_claim_line_id` | RPT-K repeated billing per measuring point |

**Q-053 answer (from this batch) [F].** In the one real BoQ claim (RPT-N), **claim lines carry period totals only**, with no KP and no date. The **attached weekly evidence carries date + plan-sheet range + route metres** at route level (not per duct). RPT-K carries **date + location code per line**, but as an interim measurement, not as a BoQ claim. A-054 ("claims at activity × KP × date grain") is therefore **not met as-is**. Disaggregation is feasible through the evidence rows (sheet range → KP) for RPT-N, and directly for RPT-K. We recommend updating Q-053/A-054 accordingly (not done here).

### C3. Arithmetic and consistency (AL-19) – results

| Doc | Check | Result |
|---|---|---|
| RPT-N | Weekly: Σ hours, Σ metres, Σ value; value = hours × rate per row | **All correct** (3/3 weeks, 19/19 rows) [C] |
| RPT-N | Remaining-length chain 30,100 → 27,927 → 21,162 → 18,439 | **Correct** [C] |
| RPT-N | Claim header 3 × 11,661 = 34,983 vs printed 34,982 | Inconsistent by 1 m on the face of the document. It is explained by a hidden underlying value 3 × 11,660.65 = 34,981.95: **displayed quantities are rounded, while amounts use unrounded quantities** [C] |
| RPT-N | Qty × rate = amount (7 lines); Σ lines = total | Lines correct on unrounded quantities. **The printed line amounts add up to one cent less than the printed total** (rounding) [C] |
| RPT-N | Claim total vs evidence | **The claim total equals the hours-based value of the three weekly sheets (98 h × hourly rate) within a few cents.** The reconciliation cells are in columns that look empty (N-F1) [C] |
| RPT-K | 36 page subtotals and 7 grand totals; qty × rate on every priced line | 35/36 pages re-compute exactly. One carry-forward (Nr. 06 p. 5) reads a single-digit amount below the computed sum, possibly a scan artefact; the next page and the grand total are correct [C] |
| RPT-K | Time arithmetic (waiting windows vs hours) | All consistent [C] |
| RPT-L/M | Totals | No totals; page-1 grid auto-totals 0; RPT-M shows a residual "1" in an empty grid [F] |

### C4. Commercial-control risks (findings)

**RPT-N – claim (N-F…)**

- **N-F1 Claim total fitted to an hours-based value.** The BoQ is priced by quantity (m, h, pc), but its total matches hours × rate of the weekly sheets almost exactly. Hidden cells beside the total hold exactly that value and the difference. Standby (11 h), repeat pigging (2,165 m) and repeat air test (1,427 m) **cannot be traced to any evidence row** [C]. Hypothesis [I]: the quantity items were set so that the claim equals the time-based value. **Risk:** the subcontractor can choose whichever basis pays more (dual basis). Ask the supplier for a line-by-line derivation of 3.1–3.3 and confirm the contractual pricing basis [VERIFY].
- **N-F2 Three-duct multiplier not supported by the results.** Items 2.1–2.3 use route metres × 3. The remarks show that individual ducts **failed** on several rows (e.g. 19.10: green still leaking; 23.10: green and orange leaking; 14.10: red defective; 20.10: "all ducts leaking", yet 381 m counted as "completed tested length"). If only ducts with an explicit "passed/OK" are counted, about **25,000 duct-m are supported against 34,982 claimed (≈ 71 %)** [C, I: interpretation of free text, VERIFY against test protocols].
- **N-F3 Overlaps and repeats in route metres.** G106–G107 (20.10) lies inside G106–G112 (19.10). G165–G168 (1,020 m) is counted on 23.10 **and again** on 27.10 (re-test of one duct after repair). The point entries "G153 … bore" and "G165 … bore" lie inside or at the edge of ranges already counted. Up to **≈ 1,700 route-m (≈ 15 % of the period)** may be double-counted [C], **in addition to** the separately claimed repeat items 3.2/3.3 → AL-03.
- **N-F4 Implausible metres per sheet.** Route metres per plan-sheet step are 330–470 m on multi-sheet ranges but **650 m and 605 m for single-sheet steps** (G159–G160, G160–G161) [C]. Check against plan-sheet lengths (location service) → AL-01.
- **N-F5 Mob/demob claimed in full in claim no. 1** with 61 % of the route remaining → front-loading (AL-32).
- **N-F6 Standby without itemisation.** "Waiting" appears in remarks on five days, but no hours are split out. The 11 h has no supporting row → AL-17.
- **N-F7 Third-party causation, a back-charge opportunity.** The remarks attribute leaks to excavation damage, badly assembled couplers and ducts under water. Repair assistance, repeat tests and waiting are therefore caused **by other parties (duct-laying / civil subcontractors)**. The cost should be routed to the causing party, not absorbed (AL-27).
- **N-F8 No acceptance and no evidence.** Claim and weekly sheets are unsigned, JV confirmation is blank, and no pressure-test charts, pig reports or calibration-plate records are attached → AL-21, AL-06.
- **N-F9 Out-of-sequence testing.** Testing while excavation and pipeline work were ongoing at the same sheets (20.10, 23.10) → AL-08.
- **N-F10 Rate structure (qualitative).** The repeat pigging-and-testing rate equals the sum of the three base rates. The repeat air-test rate is **lower** than the base air-test rate. Both should be checked against the subcontract price list [VERIFY].

**RPT-K – work records (K-F…)**

- **K-F1 Duplicate day rate.** Positions 54 and 56 (record Nr. 04) both bill a technician day for **2026-06-08**, listing the same test location → AL-29 / AL-03.
- **K-F2 Identical waiting-hour lines** (same date and time window, twice) on 13.03, 17.03 and 20.03 (8 h in total) with no second technician declared → AL-29 (AL-10-like).
- **K-F3 Billing without the measurement.** A test billed with the note "no measurement" (18.11.2025); tests billed on days whose travel line states "no measurement – no feedback" or "note without measurement"; **abortive visits billed at a full day rate** (06.07, 21.07). The cause is not attributed → AL-27.
- **K-F4 Repeat measurements** at the same location (12 cases, e.g. `G153_SP5_08E`, `G174_1581` "2nd measurement", `G140_SP3_00_1E` after "error") are billed again. Coating defects found by the test (*Fehler*) are attributable to the coating or laying contractor → back-charge candidate (AL-27).
- **K-F5 Asset billed twice.** Measuring point type P/SW at `G160_MK` is billed in Nr. 04 (03.06) **and** Nr. 05 (20.07). Elsewhere the supplier marks repeats as "already billed", so this is an exception → AL-31.
- **K-F6 Pricing-basis switch.** From Nr. 02 onwards, unit-rate tests, hourly waiting and per-visit travel are replaced by **technician day rates**. No change order or addendum is referenced on the records. Waiting and abortive time are thereby absorbed into day rates and become invisible → AL-25 [VERIFY whether the switch was agreed].
- **K-F7 Item-code integrity.** Addendum items reuse base-LV codes (003.01–003.04). Code/rate mismatches: an item 002.01.01 billed at the 002.01 rate; 002.02 described once as "> 1,500 m"; two codes for the same electrode; one priced line without an LV number (duct material at the station) → AL-30.
- **K-F8 Client-furnished material ambiguity.** Installation blocks are headed "lt. *Materialbeistellung*" (literally "as per material provision") and the materials are then **priced**. If the material was furnished by the JV or client, this is double payment [VERIFY the meaning with the supplier] → AL-31.
- **K-F9 Completeness.** Nr. 02 states "1 of 2" but only page 1 is in the bundle, and its grand-total field is blank. Position 43 is duplicated. Year typos appear in period headers → AL-02/AL-19.
- **K-F10 Late, aggregated submission.** Nr. 01 covers **5.5 months** and was dated about 3 weeks after its period end. The hourly waiting items in it were not submitted daily or weekly, contrary to §15(3) VOB/B practice [VERIFY]. The JV verified it digitally five days after the form date. The signature confirms quantities that cannot now be checked against contemporaneous records → AL-28.
- **K-F11 Extra technicians "announced and confirmed"** on dates that include a Saturday and a Sunday, with **no identification of who confirmed** → AL-28.
- **K-F12 Countersignatures without dates** (Nr. 04–06) prevent any check of the 6-working-day rule. Nr. 07 is unsigned → AL-21, AL-28.
- **K-F13 Scope creep into station works.** Nr. 07 bills cable-duct laying, cable laying, an anode field and an LA distributor at station S1, plus IFO measurements with three technicians on two consecutive days over the same section G141–G149. These need scope classification (base LV / addendum / other trade) → AL-30, T-507.

**RPT-L / RPT-M – coating daywork**

- **L-F1** Daywork without an instruction reference; travel bundled into hours (RPT-L) or dominant (RPT-M, 2 h travel vs 1 h work) → AL-28.
- **L-F2** No quantity for the repair (RPT-M) or an ambiguous unit ("= 2.20 m", RPT-L) → AL-14/AL-19.
- **L-F3** Coating in showers or rain without a dew-point record, although the form provides the field → quality hold point; links to an NCR process rather than to billing.
- **L-F4** RPT-L has no JV signature. RPT-M was countersigned on the 6th working day → AL-21/AL-28.

### C5. Applicability of existing (AL-01…14) and proposed (AL-15…24) rules

| Rule | K | L | M | N | Note |
|---|---|---|---|---|---|
| AL-01 claim > measured | ◐ | – | – | ◐ | N: route m vs plan-sheet lengths and per-duct pass; K: tests vs CP test register |
| AL-02 missing report / sequence | ● | ○ | ● | ● | K pos. 1–119 continuous, Nr. 02 p. 2 missing; N weekly Nr. 1–3 complete |
| AL-03 duplicate / overlap | ● | – | – | ● | K 08.06 twice; N overlapping sheet ranges |
| AL-04 cumulative > BoQ | ◐ | – | – | ◐ | Needs contract qty per item (absent) |
| AL-05 productivity | ◐ | ◐ | ◐ | ● | N m/h per row; K tests per technician-day |
| AL-06 no evidence | ● | ● | ● | ● | No protocols or photos in any document |
| AL-08 sequence | ◐ | – | – | ● | N testing during excavation; K test before/after coating repair |
| AL-10 impossible presence | ◐ | – | – | – | K identical time windows; persons not named |
| AL-13/AL-17 standby without cause | ● | – | – | ● | K waiting h; N 11 h |
| AL-14 text vs quantity | ● | ● | ● | ● | "no measurement" billed; "all leaking" with metres |
| AL-15 signed before end of work | – | – | – | – | Not observed |
| AL-16 rework not separated | ● | – | – | ● | Repeats inside base quantities (N 1,020 m) |
| AL-19 arithmetic | ● | ◐ | ◐ | ● | See C3 |
| AL-21 unsigned for payment | ● Nr. 07 | ● | – | ● | |
| AL-22 delivery → installation | ◐ | – | – | – | K material vs asset register |
| AL-24 overhead without output | ● | – | – | ◐ | K day rate on abortive visits |

### C6. Relevance to milestone / percentage measurement (T-507)

- RPT-M (and RPT-L) concern **station S1** but are **daywork repairs**, not percentage progress. They carry no station component, stage or lump-sum item reference. RPT-K Nr. 07 bills further station work (anode field, LA distributor, duct and cable laying, IFO measurements) at day and unit rates. Station scope is therefore **fragmented across at least two subcontractors and three pricing bases**.
- **Design consequence.** The `MILESTONE` measurement type needs (1) a station component breakdown with stage weights (e.g. civil, mechanical, CP, coating, testing), (2) a classifier for every station-related line: *inside lump sum* (not payable separately), *addendum* or *daywork extra*, and (3) a rule that **daywork on a lump-sum component requires an instruction reference and a cause** (AL-28). Without contract data for the station items, T-507 cannot be validated on real data yet. A station BoQ or lump-sum schedule is the missing input.

### C7. New rules proposed (AL-25 … AL-32)

| ID | Rule | Trigger in this batch | Data needed |
|---|---|---|---|
| **AL-25** | **Pricing-basis inconsistency.** The same scope is billed on more than one basis (unit, hourly, day rate); a claim total reconciles to an alternative basis within tolerance; or the basis changes between successive claims without a recorded change order | N-F1, K-F6 | `pricing_type` per line; change-order register |
| **AL-26** | **Multiplied or test quantity without a per-component pass.** Quantity = route × n components, but evidence shows fewer components passed; payable test quantity ≤ Σ passed component-metres | N-F2 | `component_results` in evidence |
| **AL-27** | **Repeat, abortive visit or retest without cause attribution.** The same location + item is billed again ("2. Messung", "Fehler", "Fehlanfahrt", "repeat"); hold until the cause is assigned; if the cause is another subcontractor, create a back-charge candidate | N-F3/F7, K-F3/F4 | `is_repeat`, `cause_party`, keyword dictionary |
| **AL-28** | **Daywork record late or incomplete (§15 VOB/B practice).** Missing instruction reference, persons/hours, or material; submitted > N working days after the work date; JV countersignature undated or outside the 6-Werktage window; weekend extra resources without an authoriser | K-F10/11/12, L-F1, RPT-M | `daywork_sheet` fields, calendar |
| **AL-29** | **Duplicate resource-day.** The same role/resource and date appears in more than one position, record or claim, or identical time-window lines appear without distinct person IDs | K-F1, K-F2 | Pseudonymised person/resource IDs |
| **AL-30** | **Item-code integrity.** A code is not in the contract or addendum; a code collides across addenda; or code, description and rate disagree with the price list | K-F7, K-F13 | `boq_item` composite key + price list |
| **AL-31** | **Installed asset or material billed twice, or client-furnished material billed** | K-F5, K-F8 | `cp_asset` register; `client_furnished` flag |
| **AL-32** | **Front-loaded lump sum / milestone.** A lump-sum or milestone item is claimed beyond its earned stage weight (e.g. 100 % mob/demob in the first claim, demobilisation before completion) | N-F5; also K site set-up in full in Nr. 01 | `stage_weights`; progress % |

Suggested priority for D2b: **AL-26, AL-29, AL-27, AL-25** (largest exposure, data available), then AL-28, AL-31, AL-30, AL-32.

---

## (d) Mapping tables (source field → canonical field)

### RPT-K

| Source field | Canonical field | Transform / note |
|---|---|---|
| Nr. (record) / Seite x von y | `subcontractor_claim.claim_no`, page completeness | y vs pages present → AL-02 |
| Leistungszeitraum von / bis | `period_from`/`period_to` | fix year typos via min/max line dates |
| Bestell-Nr. | `contract_ref` | changes between Nr. 01 and Nr. 03 → map both to one subcontract |
| Teilaufmaß / Schlussaufmaß / Leistungen abgenommen | `claim_type`, `accepted_flag` | tick detection |
| Pos. | `claim_line.pos_no` | duplicates → AL-02/AL-19 |
| Menge, Einh. | `qty_this`, `unit` | unit missing on one line → infer from item |
| LV Pos. xxx.xx (+ "Nachtrag 0n") | `boq_item_id` via (subcontract, addendum, item) | collisions → AL-30 |
| Text "am dd.mm.yyyy" | `work_date` | regex from description |
| Code in brackets (G…_…) | `location_ref_type = SHEET_OBJECT`, value | sheet → KP; object → `crossing` / `cp_asset` |
| "Tagessatzbasis KKS-Techniker" | `pricing_type = DAY_RATE`, resource role = CP technician | one line = one technician-day |
| "(angemeldet und bestätigt am …)" | `daywork_sheet.instruction_ref.date`, confirmer = null | AL-28 |
| "Techniker (Wartezeiten … von–bis)" | `downtime_line` {STANDBY, from, to, h, cause = null} | AL-17; identical windows → AL-29 |
| "Anreise …" | `billing_line` travel | "(n Anfahrten inkl.)" → counter |
| "Fehlanfahrt", "keine Messung", "2. Messung", "(Fehler)", "1. und 2. MA" | `result`, `is_repeat`, `component` | AL-27 |
| Messstelleninstallation … (G…_MK) | `cp_asset` install + material lines | "bereits abgerechnet" → link to the earlier line |
| "lt. Materialbeistellung" | `material.client_furnished = ?` | VERIFY → AL-31 |
| Einheit / Betrag (€) | `unit_rate`, `amount` (private) | |
| Summe/Übertrag, Gesamtsumme | control totals | AL-19 |
| Signatures, stamp, ticks, circles | `signoff_*`, `review_annotations` | pseudonymise signer → role |
| Beschäftigte, gearbeitete Zeiten, Kontierung | `persons[]`, `hours`, `cost_code` | **empty → AL-28** |

### RPT-L

| Source field | Canonical field | Transform / note |
|---|---|---|
| Tagesbericht-Nr. | `report_seq` | blank → AL-02 gap detection impossible |
| Auftraggeber, Projekt, Kostenstelle | `contract_ref`, `cost_code` | cost centre blank |
| Datum, Wetter | `report_date`, `weather` | |
| Taupunkt / Prüfmittel | `qa.dew_point`, `qa.instrument` | blank → quality hold |
| Vorbaunähte / weitere Nähte grid (Naht-Nr., ÜB, RS, TP, E, type) | `coating_joint_line` {weld_no, extra_width_m, rock_shield_m, dew_ok, enclosure, type} | empty this day; weld no. → weld log → KP |
| Weitere Arbeiten (Arbeit, von, bis, FL, m, Pers., Std., Prüfmittel) | `field_report_line` | empty |
| Material (Menge, Einheit, Artikel) | `material[]` | empty; parse consumption from remark |
| Regiestunden (Std., Name, Personal, Fahrzeug, Unimog, Strahleinheit) | `daywork_sheet.persons[]`, `equipment[]` | pseudonymise; hours basis = gross incl. travel |
| Bemerkungen | narrative + parsed {location = station, asset = existing DN 400 + DN 50, area, layers, consumption, travel_h} | NLP; unit check AL-19 |
| Signature fields | `signoff_supplier`, `signoff_jv` | JV blank → AL-21 |

### RPT-M

| Source field | Canonical field | Transform / note |
|---|---|---|
| Tagesbericht-Nr. 1, Projekt (station), Kostenstelle | `report_seq`, `work_front = station`, `cost_code` | station → `work_front(type = STATION)` |
| Regiestunden lines | `daywork_sheet.lines[]` {activity: TRAVEL / COATING_REPAIR, h, persons, vehicles} | separate travel (AL-28) |
| Material | `material[]` | |
| Personaleinsatz | headcount by role | cross-check vs daywork persons |
| Bemerkungen ("Schieberfuß … repariert") | activity = coating repair, asset = valve | link to station component (T-507) |
| Stationsarbeiten grid | `coating_joint_line` | residual "1" → template residue flag |
| JV signature + handwritten date | `countersigned_at` | Δ working days → AL-28 |

### RPT-N

| Source field | Canonical field | Transform / note |
|---|---|---|
| Nr. (claim), Period "KW 42–44" | `subcontractor_claim.claim_no`, `period_from/to` | from first/last evidence date |
| Billable route length, × 3 KSR | `boq_item.contract_qty` (route m), `qty_multiplier = 3` | header-level contract qty |
| Monthly performance / Rest performance | `qty_this`, `qty_remaining` | label says "monthly" for 3 weeks |
| Item, Description, Unit | `item_no_supplier` → `boq_item_id` | map to the contract LV numbers (not on the claim) |
| Quantity | `qty_this` | keep unrounded value from the text layer |
| Unit Rate, Amount | private | |
| Unlabelled cells right of total | `hidden_cells[]` | flag; AL-25 |
| Weekly: Arbeitsnachweis Nr., Leistungszeitraum KW | `claim_evidence.doc_id`, week | |
| Datum, von, bis, Dauer | `work_date`, `start`, `end`, `hours` (gross, billed) | |
| von BPL / bis BPL | `sheet_from`/`sheet_to` → KP range | location service; overlap → AL-03 |
| fertig geprüfte Länge (m) | `route_m` | per-sheet plausibility → AL-01 |
| Leistung h × rate | value (private) | AL-25 |
| Bemerkungen | `component_results` {red/green/orange: pass/fail}, `cause_party`, `downtime`, `repeat` | NLP; AL-26/27/17 |
| Wochenleistung, Stunden, Meter | control totals | AL-19 |
| Bestätigung ARGE | `signoff_jv` | blank → AL-21 |

---

## (e) RPT-N reconciliation readiness

| Check | Status | What is possible now | Missing data / blocker |
|---|---|---|---|
| **AL-19** arithmetic | **Possible** | Done (C3): sums correct, display rounding, hidden reconciliation cells | – |
| **AL-21** unsigned / unaccepted | **Possible** | Fails: no signature, JV confirmation blank ×3 | – |
| **AL-02** sequence / missing evidence | **Possible** | Weekly Nr. 1–3 complete for KW 42–44 | Calendar of planned test days |
| **AL-17** standby without cause | **Possible** | Fails: 11 h claimed, no itemised standby rows | Instruction / cause log |
| **AL-06** claimed without evidence | **Possible** | Fails: no pressure-test protocols, pig reports or calibration-plate records | Test protocol per section and duct |
| **AL-03** duplicate / overlap | **Partially** | Sheet-range overlaps detectable (≈ 1,700 route-m candidates) | Plan-sheet → KP table to measure overlap in metres; whether "bore" entries are separate HDD duct strings |
| **AL-26** multiplier vs per-duct pass | **Partially** | ≈ 71 % of claimed duct-m supported by explicit "passed" remarks | Structured per-duct results; later re-test results for the ducts that failed |
| **AL-01** claim > measured | **Partially** | Metres-per-sheet plausibility flags (650 / 605 m single-sheet steps) | Plan-sheet lengths; as-built duct length per section; independent measurement (survey or JV test witness) |
| **AL-04** cumulative > BoQ | **Partially** | Base items 2.1–2.3 vs 90,300 duct-m: 39 % used | Contract qty for mob/demob, standby and repeat items; future claims need a previous-cumulative column |
| **AL-16 / AL-27** rework / repeat | **Partially** | Repeats identified (G165–G168, G106–G107); causes in free text | Cause attribution per repeat; link to the responsible subcontractor for back-charge |
| **AL-25** pricing basis | **Partially** | Claim total ≈ hours-based value | Subcontract pricing clause; derivation of items 3.1–3.3 |
| **AL-08** sequence | **Partially** | Remarks show testing during excavation | Duct-laying / backfill / tie-in status per sheet (JV progress) |
| **AL-32** front-loaded lump sum | **Partially** | Mob/demob 100 % in claim 1 | Stage split of mob/demob in the price list |
| **AL-05** productivity | **Possible** | m/h per evidence row | Crew size (not stated) |
| **Q-053** KP/date granularity | **Answered** | Claim lines: period totals; evidence: date + sheet range | KP via location service |

**Bottom line [I].** RPT-N can be reconciled at **section (sheet-range) × date** level through its evidence sheets, but not at line level, and not per duct without test protocols. Three checks (AL-21, AL-17, AL-06) fail outright today. The largest quantified exposures are the three-duct multiplier (AL-26) and double-counted route metres (AL-03). Recommended requests to the supplier: per-duct test protocols, a derivation of items 3.1–3.3, and a re-issue with previous / this period / cumulative columns and an evidence reference per line.

---

## (f) Daywork-record (*Stundenlohn*) control checklist – VOB/B §15 practice

Legal points are paraphrased from general VOB/B practice and **must be verified** against the subcontract (its special conditions may change deadlines or forms) and with legal counsel. All points marked [VERIFY].

| # | Control | Basis [VERIFY] | RPT-K | RPT-L | RPT-M | RPT-N weekly |
|---|---|---|---|---|---|---|
| 1 | Daywork **expressly agreed before start** (contract item or written order); otherwise not payable as daywork | §2(10) VOB/B | ◐ LV hourly item exists; day-rate basis from Nr. 02 without a visible agreement | ✗ no reference | ✗ | ◐ hourly rate on the form, basis unclear vs BoQ |
| 2 | **Notice before start** (who instructed, when, scope) | §15(3) S.1 | ◐ "announced and confirmed", confirmer unknown; 1 named agreement | ✗ | ✗ | ✗ |
| 3 | Work **not already covered** by a unit-rate or lump-sum item | §2(1), §2(10) | ✗ waiting / repeat inside test scope? | ✗ repair of an existing asset, scope? | ✗ station lump sum? | ✗ repair assistance vs test items |
| 4 | **Persons** (pseudonymised ID, qualification), start, end, breaks, **net hours** per person | §15(3) S.2 | ✗ columns empty | ◐ 2 persons × 10 h, no times | ◐ ambiguous per-person hours | ◐ hours per row, crew not stated |
| 5 | **Equipment** with hours; **material** with quantity and source (client-furnished?) | §15(3) S.2 | ◐ material priced; "Materialbeistellung" unclear | ◐ in remark only | ● | ✗ |
| 6 | **Location** (sheet / KP / asset) and link to the daily report | good practice | ● codes | ◐ station | ◐ station | ● sheet ranges |
| 7 | **Cause** of waiting, repeat or abortive visit and responsible party | good practice / back-charge | ✗ | – | – | ◐ remarks |
| 8 | Submitted **daily or weekly** as per custom | §15(3) S.2 | ✗ periods of 1–5.5 months | ● daily | ● daily | ● weekly |
| 9 | JV returns the signed sheet **within 6 working days** or **objects in writing**; otherwise deemed accepted | §15(3) S.3–5 | ✗ dates missing (Nr. 04–06), Nr. 07 unsigned | ✗ unsigned | ◐ signed on day 6 | ✗ unsigned |
| 10 | Signature only **acknowledges hours/type**, not entitlement in principle; use a reservation stamp ("hours checked – entitlement reserved") | case law, practice | ✗ "OK" / "verified" without reservation | – | ✗ | – |
| 11 | Daywork invoices submitted **promptly, at intervals ≤ 4 weeks** | §15(4) | ✗ Nr. 01 aggregates 5.5 months | n/a | n/a | ● 3 weeks |
| 12 | If late submission creates doubt, **pay only the economically justified effort** | §15(5) | applicable to Nr. 01 | – | – | – |
| 13 | No **duplicates** (same person/resource/day across sheets or suppliers) | AL-29 / AL-10 | ✗ 08.06; identical windows | – | – | – |
| 14 | **Travel** billable only if agreed; separated from work hours | contract | ◐ per-visit item | ✗ embedded | ✗ dominates | ✗ travel inside billed hours (26.10) |
| 15 | **Weekend / holiday** resources authorised in writing | contract | ✗ Sat/Sun confirmations | – | – | – |
| 16 | Arithmetic and units correct | AL-19 | ● (1 carry-forward query) | ◐ unit unclear | ◐ residual cell | ● |

**Recommended control procedure [R].**
1. A digital daywork sheet (DE/NL), submitted by the next working day 10:00, with a mandatory instruction reference picked from a JV instruction log, pseudonymised persons with start/end/break, equipment hours, material with a client-furnished flag, location, cause and photos.
2. JV review within 6 working days with three outcomes: *accepted (hours only, entitlement reserved)* / *objected (reason)* / *rejected*. The timestamp is enforced by the platform (AL-28).
3. Day-rate or daywork lines on lump-sum components are blocked unless an instruction reference exists (T-507 link).
4. Repeats and abortive visits require a cause; third-party causes generate a back-charge candidate (AL-27).

---

## Summary of design implications

1. Treat **claims and their evidence** as first-class document types linked line-to-evidence. RPT-N proves that the evidence (date × sheet range) is richer than the claim lines.
2. Key `boq_item` by **subcontract + addendum + item**, and give every line a **pricing type**. Pricing bases shift over time and codes collide across addenda.
3. Make **per-component results** and **repeat/cause attribution** part of the claim line. The largest exposures in this batch come from multiplied quantities and repeats, not from arithmetic.
4. Model **daywork sheets** explicitly with the §15-type deadlines. Most daywork in this batch lacks persons, instruction or a timely countersignature.
5. Station works are fragmented across suppliers and pricing bases. T-507 needs a station component and stage schedule before it can be validated on real data.
