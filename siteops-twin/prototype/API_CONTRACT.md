# SiteOps Twin MVP: API Contract v1 (demo)

Backend: FastAPI on `http://localhost:8000`. The static frontend is served from `/` (the `prototype/web/` folder). All responses are JSON, unless the path ends in `.csv`. All data is **SYNTHETIC** (spread `SYN-SPREAD-01`).

## Conventions
- **Dates:** `YYYY-MM-DD`.
- **KP:** metres as numbers. The UI formats them as `KP 012+350`.
- **Demo RBAC:** the request header `X-Role` is one of `CM` (Commercial Manager), `QS`, `SM` (Spread Manager), `FM` (Foreman), `SV` (Survey), `SC` (Subcontractor; also send `X-Subcontractor: SYN-SUB-A`), `ADM`, or `AUD` (Auditor).
  - Default role: `CM`.
  - `SC` sees only its own subcontractor's rows.
  - Only `QS` and `CM` may POST `/api/certify`.
  - `FM`, `SM` and `ADM` may POST field reports.
- **Status values:** `MATCHED` | `WITHIN_TOLERANCE` | `DISCREPANCY` | `UNVERIFIABLE`.
- **Alert severity:** `HIGH` | `MED` | `LOW`. Alert status: `OPEN` | `ACK` | `CLOSED`.
- **Rules:** AL-01 … AL-13 (see `04_to_be_architecture/field_sensing_layer.md` and `ux/mvp_backlog.md`).

## Endpoints

### GET /api/meta
```json
{"spread":{"spread_id":"SYN-SPREAD-01","kp_start_m":0,"kp_end_m":25000,"site_tz":"Europe/Berlin","synthetic":true},
 "date_min":"2027-01-04","date_max":"2027-03-13","default_date":"2027-03-13",
 "sections":[{"section_id":"S01","kp_from_m":0,"kp_to_m":1000}],
 "activities":[{"activity_code":"TRN","name":"Trenching","unit":"m","sequence_no":6,"verification_source":"UAV"}],
 "subcontractors":[{"subcontractor_id":"SYN-SUB-A","scope":"Clearing, grading, reinstatement"}],
 "crews":[{"crew_id":"SYN-CRW-01","subcontractor_id":"SYN-SUB-A","activity_code":"CLR","nominal_size":12}],
 "fronts":[{"front_id":"FR-01","type":"MAINLINE","kp_from_m":0,"kp_to_m":1000,"name":"Front 01"}],
 "config":{"tol_pct":{"m":0.01,"m3":0.03,"m2":0.02,"nr":0.0},"al05_drop":0.25,"tol_head":2,"tol_eq_h":1.0},
 "roles":["CM","QS","SM","FM","SV","SC","ADM","AUD"]}
```

### GET /api/geometry
GeoJSON FeatureCollection in a **local synthetic CRS**: x/y in metres. Use Leaflet `L.CRS.Simple`; this is not lat/lon. Features:
- `{"kind":"centreline"}`: a LineString.
- `{"kind":"section","section_id":"S01","kp_from_m":0,"kp_to_m":1000}`: a LineString.
- `{"kind":"front","front_id":"FR-01","type":"TIE_IN"}`: a Point.

### GET /api/overview?date=YYYY-MM-DD
```json
{"date":"2027-03-13",
 "kpis":{"claimed_value":123456.0,"certifiable_value":118000.0,"at_risk_value":5456.0,
         "rows_by_status":{"MATCHED":120,"WITHIN_TOLERANCE":30,"DISCREPANCY":12,"UNVERIFIABLE":8},
         "open_alerts":{"HIGH":5,"MED":9,"LOW":3},"reports_received":7,"reports_expected":8,
         "headcount_claimed":180,"headcount_sensed":171},
 "sections":[{"section_id":"S07","kp_from_m":6000,"kp_to_m":7000,"worst_status":"DISCREPANCY",
              "open_alerts":2,"progress":{"CLR":1.0,"GRD":1.0,"TRN":0.6,"LOW":0.3,"BKF":0.0}}],
 "currency":"SYN¤"}
```
`progress` is the cumulative reported quantity divided by the planned quantity per activity (0–1).

### GET /api/reconciliation?date=&subcontractor=&status=&activity=&section=
These are cumulative-to-date rows (D-041, D-065):
```json
{"rows":[{"key":"S07|TRN|SYN-SUB-B","section_id":"S07","activity_code":"TRN","subcontractor_id":"SYN-SUB-B","unit":"m",
  "planned":1000,"reported":640,"measured":600,"u":6.0,"tol":6.0,"claimed":690,"certified":600,"invoiced":600,
  "cap":612.0,"diff":90.0,"diff_pct":0.15,"status":"DISCREPANCY","verification_source":"UAV",
  "last_flight":"2027-03-12","alerts":["AL-01"],"rate":12.5}]}
```

### GET /api/sections/{section_id}?date=
```json
{"section":{"section_id":"S07","kp_from_m":6000,"kp_to_m":7000},
 "rows":[ /* same shape as the reconciliation rows */ ],
 "flights":[{"flight_id":"SYN-FLT-20270312","flight_date":"2027-03-12","gsd_cm":2.5,"rmse_z_m":0.04,"n_checkpoints":6}],
 "measurements":[{"measurement_id":"M-1","activity_code":"TRN","method":"LENGTH_DIGITISE","kp_from_m":6000,"kp_to_m":6600,"qty":600,"sigma":3.0,"flight_date":"2027-03-12"}],
 "alerts":[ /* alert objects */ ],
 "audit":[ /* audit events for this section */ ]}
```

### GET /api/production?date=
```json
{"date":"2027-03-13","rows":[{"crew_id":"SYN-CRW-05","subcontractor_id":"SYN-SUB-C","activity_code":"WLD","unit":"nr",
  "qty":26,"hours":10,"headcount":18,"productivity":2.6,"median5":4.4,"delta_pct":-0.41,"weather":"WORKABLE","report_received":true,"kp_from_m":9100,"kp_to_m":9412}]}
```
- `productivity` = qty / hours.
- `weather` is one of `WORKABLE`, `RESTRICTED`, `STOPPED`.

### GET /api/alerts?status=&rule=&severity=&subcontractor=
```json
{"alerts":[{"alert_id":"A-0001","rule_id":"AL-09","severity":"HIGH","work_date":"2027-03-10","section_id":"S07","front_id":"FR-07",
  "activity_code":null,"subcontractor_id":"SYN-SUB-B","crew_id":"SYN-CRW-04","equipment_id":null,
  "title":"Claimed headcount above sensed","explanation":"Claimed 32; check-in 24; manifest 25 (tolerance 2)","status":"OPEN"}]}
```

### POST /api/alerts/{alert_id}/status
Body `{"status":"ACK|CLOSED","comment":"..."}` → the updated alert. Writes an audit event.

### GET /api/scorecard?date=
```json
{"rows":[{"subcontractor_id":"SYN-SUB-B","claimed_value":50000,"certifiable_value":46000,"overclaim_pct":0.087,
  "rows_discrepancy":5,"alerts_by_rule":{"AL-01":3,"AL-09":2},"headcount_overclaim_days":4,"equipment_overclaim_h":22.5,
  "reports_on_time_pct":0.95}]}
```

### GET /api/presence?date=
```json
{"date":"2027-03-10",
 "fronts":[{"front_id":"FR-07","crew_id":"SYN-CRW-04","subcontractor_id":"SYN-SUB-B","headcount_claimed":32,"checkin":24,
            "manifest":25,"camera_max":22,"badge_zone_count":23,"status":"OVERCLAIM"}],
 "equipment":[{"equipment_id":"SYN-EQ-014","type":"Excavator","subcontractor_id":"SYN-SUB-B","hours_claimed":10,
               "engine_h":4.5,"working_h":3.9,"telematics":"OK","status":"OVERCLAIM"}],
 "privacy_note":"Aggregated counts only. Identifiable presence data is restricted to HR/HSE."}
```
- Front `status` is one of `OK`, `OVERCLAIM`, `NO_SIGNAL`.
- Equipment `status` is one of `OK`, `OVERCLAIM`, `NO_DATA`.

### POST /api/field-reports (mobile, offline queue)
The body carries a `client_uuid`, which makes the request idempotent:
```json
{"client_uuid":"b9c...","report_date":"2027-03-13","crew_id":"SYN-CRW-04","front_id":"FR-07",
 "lines":[{"activity_code":"TRN","kp_from_m":6600,"kp_to_m":6700,"qty":100,"unit":"m","hours_worked":10,"headcount":20,
           "equipment_ids":["SYN-EQ-014"],"downtime_h":0,"downtime_reason":null}],
 "photos":[{"name":"p1.jpg","taken_at":"2027-03-13T14:02:00Z","kp_m":6650}],"submitted_at":"2027-03-13T17:30:00Z"}
```
Responses:
- `201 {"report_id":"FR-...","status":"RECEIVED","duplicate":false}`.
- Re-posting the same `client_uuid` returns `200` with `duplicate: true`.
- `422` on validation errors (`kp_to_m` ≤ `kp_from_m`, unknown crew).

### GET /api/field-reports?date=&crew=
Returns `{"reports":[...]}`.

### POST /api/certify (QS or CM only)
Body `{"key":"S07|TRN|SYN-SUB-B","qty_certified":612,"reason_code":null,"comment":"..."}`.
- If `qty_certified` > `cap` and there is no `reason_code` → `409 {"error":"ABOVE_CAP","cap":612.0}`.
- Valid `reason_code` values: `JOINT_MEASUREMENT`, `SURVEY_RECHECK`, `CONTRACT_RULE`, `OTHER`.
- Success → the updated row, plus an audit event.

### GET /api/certificate/{subcontractor_id}?date=  and  GET /api/certificate/{subcontractor_id}.csv?date=
```json
{"subcontractor_id":"SYN-SUB-B","period_to":"2027-03-13",
 "lines":[{"key":"...","boq_item_id":"BOQ-B-TRN","activity_code":"TRN","section_id":"S07","unit":"m",
   "cum_certified":612,"prev_certified":500,"this_period":112,"rate":12.5,"amount":1400.0}],
 "total_this_period":1400.0,"currency":"SYN¤"}
```

### GET /api/audit?entity=&entity_id=
Returns `{"events":[{"ts":"...","actor_role":"QS","entity":"certification","entity_id":"...","action":"CERTIFY","detail":"..."}]}`.
