# SiteOps Twin: MVP Demo (SYNTHETIC data)

A working MVP of the SiteOps Twin, built on the synthetic spread `SYN-SPREAD-01` (25 km, 25 sections, 60 working days, 4 subcontractors, 9 crews). **All data is synthetic.** The demo contains no real company, person, coordinate or contract value.

## Run it (one command after setup)
```bash
cd siteops-twin/prototype
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m siteops.cli build          # generates data/synthetic/*.csv + siteops_demo.db
.venv/bin/uvicorn siteops.api:app --port 8000  # open http://localhost:8000  (field app: /field.html)
.venv/bin/python -m pytest -q                  # 22 tests
```
Leaflet 1.9.4 (BSD-2) and Chart.js 4.4.1 (MIT) are bundled under `web/vendor/`. The app makes no CDN calls, so it works on a site network that is offline or restricted.

## What the demo covers (MVP epics)
| Epic | Where |
|---|---|
| E1 Spread, sections, activities, BoQ | `siteops/generate.py`, `/api/meta`, `/api/geometry` |
| E2 Offline field daily report (PWA) | `web/field.html`: 3 steps, IndexedDB outbox, idempotent sync (`client_uuid`) |
| E3 Subcontractor claims | `subcontractor_claim(_line)`, resource, equipment and standby claims |
| E4 Independent measurements, with uncertainty | Drone (UAV), QA weld and coating logs, as-built survey (top of pipe) |
| E5 Reconciliation engine | `siteops/engine.py::reconcile`: six states, D-063 status rule, D-064 cap, D-041 measurement-time comparison |
| E6 / E11 Alerts AL-01…AL-13 | `siteops/engine.py::alerts` |
| E7 Commercial dashboard | `web/index.html`: S1 overview + KP strip + map, S2 production, S3 reconciliation, S4 scorecard, S5 alerts, S6 section detail |
| E8 / E11 Presence and equipment sensing | S8 presence: check-in, manifest, camera, badge zone counts; telematics |
| E9 Certification | Certify with cap; an override needs a reason code and a comment; certificate draft in JSON and CSV |
| E10 Audit trail and RBAC | `audit_event` with before/after hashes; demo roles via the `X-Role` header; subcontractors see only their own data |

## Commercial rules implemented
- **Status (D-063):**
  - |claimed − measured| ≤ U → MATCHED
  - ≤ U + T → WITHIN_TOLERANCE
  - more than that → DISCREPANCY
  - no measurement → UNVERIFIABLE
  - U = 2σ of the measurement. T = max(absolute, % × measured), with placeholder values in `siteops/config.py`.
- **Cap (D-064):** certifiable without override = M + U + T. Above the cap, the API returns `409 ABOVE_CAP` until a reason code and a comment are given. Nothing is auto-certified.
- **Measurement time (D-041):** only claims up to the latest measurement date are compared. Later claim lines show as *pending verification*.
- **Over-certification:** `over_certified` shows a quantity certified against an earlier flight that is now above the cap, for recovery in the next certificate.

## Verification status (2026-11-23)
- `pytest`: **22 passed**. This covers the status rule, the cap, recall of **all 24 seeded anomalies across the 13 rules**, a precision guard, RBAC, idempotent mobile sync, the override flow, the certificate CSV and the synthetic labelling.
- Real-server end-to-end run in Chromium: all 8 dashboard screens and the field app rendered with **0 console, page or HTTP errors**.
- **Calibration finding:** with daily productivity variability σ = 0.12, the AL-05 25% threshold gave about 1.3% false positives per crew-day. The demo uses σ = 0.08. Calibrate on reference-project data (A-043).

## Load your reference project
See [`../data/templates/REFERENCE_PROJECT_INTAKE.md`](../data/templates/REFERENCE_PROJECT_INTAKE.md). Put CSVs with the same table and column names in a folder, then run `python -m siteops.cli load <folder>`.
