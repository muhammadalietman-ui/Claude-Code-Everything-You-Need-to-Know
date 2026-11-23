# Reference-Project Data Intake

Purpose: let the user feed a **reference project** into the MVP step by step, to test the model before running it on live project data (user decision 2026-11-23, Q-003, Q-072).

## Rules before sending anything
1. **Anonymise first.**
   - Replace names with codes: companies → `SUB-A`; people → roles only, never names; equipment → `EQ-001`.
   - Shift coordinates and KP to a local origin, or send only KP values.
   - Rates may be scaled by a constant factor.
2. **Keep the original-to-code key at the company.** Do not send it here.
3. One CSV per table. The file name is the table name (`section.csv`, `field_report_line.csv`, …). **The column names must match exactly** (see the schema in `prototype/siteops/db.py` and the templates in this folder).
4. Missing tables are fine. The engine runs on whatever exists, and rows without an independent measurement show as `UNVERIFIABLE`.

## Minimum dataset by step

| Step | Tables | What it unlocks |
|---|---|---|
| 1. Structure | `spread`, `section`, `activity_type`, `subcontractor`, `crew`, `boq_item`, `planned_quantity` | KP strip, planned progress |
| 2. Daily production | `field_report`, `field_report_line` (with `kp_from_m`/`kp_to_m`, qty, hours, headcount, equipment, downtime reason) | Production view, AL-02, AL-05 |
| 3. Claims | `subcontractor_claim`, `subcontractor_claim_line` (KP range + work date per line) | Reconciliation, AL-03, AL-04, AL-08 |
| 4. Independent measurements | `drone_flight`, `measurement` (cumulative qty per section and activity, with `sigma`); weld/coating log; as-built survey | Status rule, cap, AL-01, AL-06: **the core of H1** |
| 5. Certification history | `certification_line`, `invoice_line` | Certified/invoiced states, certificate draft |
| 6. Sensing (if available) | `resource_claim`, `equipment_claim`, `standby_claim`, `telematics_daily`, `presence_daily`, `vehicle_trip`, `weather_obs` | AL-07, AL-09…AL-13, H5 |

## Questions to answer with step 1 (they set the parameters)
- Contract tolerances for each unit (Q-063) → `siteops/config.py` `TOL_PCT` / `TOL_ABS`.
- How drone volumes and lengths are reported, and their accuracy: RMSE and check points (Q-005, Q-007).
- Whether claims are made per KP range and date, or per period only (Q-053). If per period only, a disaggregation rule is needed.
- Whether subcontracts are measured to German VOB/C ATV rules (e.g. DIN 18300 for earthworks), and whether quantities are exchanged as REB/GAEB files (see `01_governance/germany_context.md`).

## Load
```bash
cd siteops-twin/prototype
.venv/bin/python -m siteops.cli load /path/to/reference_csvs ""   # "" = no file-name prefix
SITEOPS_DB=siteops_demo.db .venv/bin/uvicorn siteops.api:app --port 8000
```
