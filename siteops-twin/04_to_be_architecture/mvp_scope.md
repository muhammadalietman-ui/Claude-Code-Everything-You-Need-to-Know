# MVP Scope vs Roadmap

Owner: solution-architect. Version 0.1 (Phase 0). Status: **waiting for user confirmation (D-005, code gate)**.

User stories and acceptance criteria for each epic are in `ux/mvp_backlog.md` (ux-designer and commercial-analyst). The synthetic data that feeds the demo is specified in `data_model/synthetic_dataset_spec.md`.

## 1. MVP goal
**[R]** Show, on **one synthetic pipeline spread**, that field reports, subcontractor claims and drone-derived measurements can be joined on activity × KP section × date × subcontractor.

The demo must also show that the joined data can be:
- reconciled through the quantity states with explicit tolerances
- surfaced as explainable alerts
- certified by a QS in one dashboard, with a full audit trail

This is the minimum artefact needed to evaluate H1–H3 and to give H4 a first, partial test.

## 2. MVP vs roadmap

| Epic | Description | MVP | Rationale | Depends on | Effort |
|---|---|---|---|---|---|
| E1 | Spread and section model: synthetic alignment, KP sections, activity catalogue, BoQ → activity mapping | **In** | Base for all joins (D-004) | none | M |
| E2 | Field daily report capture: offline-capable form (activity, KP from–to, qty, crew, equipment, hours, photos, delays/weather) | **In** (simple PWA/form, offline queue) | Source of Reported qty; addresses H2/H4 | E1 | L |
| E3 | Subcontractor daily claim capture/import (form or CSV) | **In** | Source of Claimed qty; core to H1/H3 | E1 | S |
| E4 | Drone measurement import: per-flight measured qty per section with uncertainty and footprint | **In** (file import only) | Independent Measured qty; core to H1 | E1 | M |
| E5 | Reconciliation engine: 6 states, tolerance rules, statuses MATCHED / WITHIN_TOLERANCE / DISCREPANCY / UNVERIFIABLE | **In** | Central artefact contribution | E1–E4 | L |
| E6 | Alerts AL-01…AL-08 | **In** (rule-based, thresholds configurable) | Addresses objective 8 and H4 | E5, E8 | M |
| E7 | Commercial dashboard: KP strip + map, daily production, reconciliation workbench, subcontractor scorecard, timeline | **In** | Addresses H2 | E5, E6 | L |
| E8 | Crew and equipment presence: crew-level check-in, telematics CSV (hours, idle per section) | **In** (crew-level only, D-006; CSV only) | Needed for AL-07 and productivity (H4) | E1 | S |
| E9 | Certification workflow: QS certifies line items with comment, certificate draft export | **In** (single approval step) | Closes the loop to Certified; H3 | E5, E10 | M |
| E10 | Audit trail and basic RBAC | **In** (roles + change log; local auth) | Traceability and dispute evidence | none | S |
| R1 | 3D mesh / point-cloud viewer (3D Tiles) | Out | High effort; 2D ortho + KP strip is enough to test the hypotheses | E4 | L |
| R2 | Live GNSS streaming of equipment/vehicles | Out | Needs vendor integration; CSV is enough for the evaluation | E8 | M |
| R3 | BLE/RFID badges for personnel | Out | Privacy (R-03), hardware, consent | Ethics clearance | L |
| R4 | Computer vision (activity recognition, object counting on ortho) | Out | Research topic in its own right | E4 | XL |
| R5 | ERP / PM / DMS API integration and write-back | Out (ERP invoice import by CSV, read-only, is **In** for the Invoiced state) | No confirmed APIs (R-08); IT approval | Q-006 | L |
| R6 | Earned value management (EVM) | Out (data model supports it) | Needs cost-loaded schedule | E5 | M |
| R7 | ML forecasting of productivity and finish dates | Out | Needs pilot data history | E6 | M |
| R8 | Multi-spread / enterprise tenancy | Out | Single pilot spread | all | L |
| R9 | Digital claims and dispute module (variations, notices, evidence packs) | Out (evidence export is In) | Scope control | E9, E10 | L |

Effort sizes are relative, for one developer: S < 1 week, M is 1–2 weeks, L is 2–4 weeks, XL is more than 4 weeks. **[A] A-042.** The total MVP effort is about 14–18 developer-weeks, which fits the P6 window of 10 weeks only with a lean scope.

**[R]** If time runs short, cut in this order:
1. E2 offline queue: fall back to an online form plus CSV upload.
2. E7 timeline view.
3. E8 telematics, which also drops AL-07.
4. E9 PDF export: keep XLSX only.

## 3. MVP boundaries
- **One synthetic spread** (e.g. 25 km, 25 sections of 1 km), about 10 activities, 2–3 subcontractors, a pilot period of about 30 working days. All data is synthetic and labelled `SYNTHETIC`.
- **Imports are file-based:** alignment, BoQ/plan, drone measurements, telematics, ERP invoice lines.
- **One production line, one currency, one certification period type.** The certification period is monthly, with a daily or weekly agreement view.
- **No production deployment and no real users' credentials.** Local accounts per role for the demo.
- **Not a document-management system:** evidence files are linked by hash and path.

## 4. Non-functional requirements

| ID | Category | Requirement | Verification |
|---|---|---|---|
| NFR-01 | Offline | The field form captures, stores and queues at least 50 reports with no connection. No data is lost on app restart. Sync is idempotent (client UUID) | Airplane-mode test |
| NFR-02 | Sync conflicts | Duplicate or overlapping submissions are flagged, never silently merged | Test case using seeded duplicates |
| NFR-03 | Performance | Dashboard loads one spread-month (about 10k quantity records) in under 3 s on a laptop. Reconciliation run under 30 s | Timed test on synthetic data |
| NFR-04 | Field usability | A daily report takes under 5 minutes. Touch targets are at least 48 px. Readable in sunlight (high contrast) | Usability test, SUS |
| NFR-05 | Desktop usability | The QS reviews one day's discrepancies for a spread in under 15 minutes. SUS ≥ 68 | Time-and-motion, SUS (H2) |
| NFR-06 | Auditability | Every create, update or certify action logs user, role, timestamp (UTC), before and after values, and reason. Logs are append-only | Audit-trail test |
| NFR-07 | Traceability | Every certified quantity can be drilled down to its source reports, claims, measurements and evidence | Drill-down test |
| NFR-08 | Security | RBAC (Field, Subcontractor, Survey, QS, Commercial, PM, Admin, Auditor). Subcontractors see only their own data. Passwords are hashed. TLS when networked. No secrets in the repository | Role-permission test matrix |
| NFR-09 | Privacy | No individual location history is stored or shown. Presence is aggregated by crew and zone (D-006) | Schema review |
| NFR-10 | Data quality | Every record carries source, provenance, version and a DQ flag. Records failing validation are quarantined with a reason | Import test with bad files |
| NFR-11 | Reproducibility | One-command local run. The synthetic data generator uses a fixed seed | Clean-clone test |
| NFR-12 | Uncertainty | Every Measured qty displays ± uncertainty. Reconciliation uses that uncertainty in its tolerance test | Unit tests |

## 5. Demo scenario (synthetic spread `[SPREAD_ID]` = SYN-01)
1. **Set-up.** Load the synthetic alignment (KP 000+000 to 025+000), the sections, the BoQ and the plan for `[SUBCONTRACTOR_A]` (earthworks) and `[SUBCONTRACTOR_B]` (welding and coating).
2. **Day D (field).** The foreman submits a report offline for trenching at KP 012+100 to 012+850. It syncs later.
3. **Day D (drone).** The drone measurement import gives a trench length of 690 m ± 5 m and an excavation volume with ± uncertainty in section S13.
4. **Day D (claim).** `[SUBCONTRACTOR_A]` claims 800 m of trenching.
5. **Reconcile.** The claimed vs measured gap (+16%) exceeds tolerance, so the status is DISCREPANCY and alert AL-01 fires.
   - A seeded duplicate claim triggers AL-03.
   - Backfill reported ahead of lowering-in triggers AL-08.
6. **Workbench.** The QS opens AL-01, sees the orthophoto, the footprint, the field report and the photos, and certifies 690 m with a comment.
7. **Scorecard.** The subcontractor's claim accuracy and discrepancy history update.
8. **Period close.** The Commercial Manager approves the certificate draft (XLSX) and imports the ERP invoice lines. The dashboard then shows the full chain: Planned → Reported → Measured → Claimed → Certified → Invoiced for each section.
9. **Audit.** The Auditor role replays the history of the line item.

## 6. ✅ CONFIRMATION REQUIRED (D-005)
Please confirm, or change, each item before any platform code is written:

- [ ] **C1. Single synthetic spread** (about 25 km, 1-km sections) is the MVP boundary. Q-011 asks you to define "corner" and the section length.
- [ ] **C2. Epics E1–E10 are In.** R1–R9 are roadmap only.
- [ ] **C3. Alert set AL-01…AL-08** as defined. Thresholds are configurable (e.g. the AL-05 drop is set to 25% by default, A-043).
- [ ] **C4. Personnel granularity** is crew/zone level only, with no individual tracking (D-006).
- [ ] **C5. File-based imports** only: drone exports, telematics, BoQ/plan, ERP invoice lines. No live APIs.
- [ ] **C6. Tech stack (D-009):** Python, FastAPI, PostgreSQL/PostGIS (SQLite/SpatiaLite acceptable for the demo), MapLibre/Leaflet web map, PWA form. *Alternative:* Streamlit, for a faster but less realistic UI.
- [ ] **C7. Quantity states** are Planned, Reported, Measured, Claimed, Certified and Invoiced (D-008). Reconciliation statuses are MATCHED, WITHIN_TOLERANCE, DISCREPANCY and UNVERIFIABLE.
- [ ] **C8. Local single-instance deployment** for the prototype. The hybrid architecture is documented only (ADR-009).
- [ ] **C9. Certification** uses a single approval step (QS certifies, then the Commercial Manager approves the period).
- [ ] **C10. Cut order** if time runs short, as listed in §2.
