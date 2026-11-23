"""SQLite schema and connection helpers."""
import sqlite3
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parent.parent / "siteops_demo.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS spread(spread_id TEXT PRIMARY KEY, name TEXT, site_tz TEXT, crs_code TEXT,
  kp_start_m REAL, kp_end_m REAL, is_synthetic INTEGER);
CREATE TABLE IF NOT EXISTS section(section_id TEXT PRIMARY KEY, spread_id TEXT, kp_from_m REAL, kp_to_m REAL);
CREATE TABLE IF NOT EXISTS activity_type(activity_code TEXT PRIMARY KEY, name TEXT, unit TEXT, sequence_no INTEGER,
  uav_observability TEXT, verification_source TEXT);
CREATE TABLE IF NOT EXISTS subcontractor(subcontractor_id TEXT PRIMARY KEY, scope TEXT);
CREATE TABLE IF NOT EXISTS crew(crew_id TEXT PRIMARY KEY, subcontractor_id TEXT, activity_code TEXT, nominal_size INTEGER);
CREATE TABLE IF NOT EXISTS equipment(equipment_id TEXT PRIMARY KEY, type TEXT, owner TEXT, crew_id TEXT, telematics_enabled INTEGER);
CREATE TABLE IF NOT EXISTS boq_item(boq_item_id TEXT PRIMARY KEY, subcontractor_id TEXT, activity_code TEXT, unit TEXT,
  unit_rate REAL, contract_qty REAL);
CREATE TABLE IF NOT EXISTS planned_quantity(section_id TEXT, activity_code TEXT, planned_qty REAL, unit TEXT,
  PRIMARY KEY(section_id, activity_code));
CREATE TABLE IF NOT EXISTS work_front(front_id TEXT PRIMARY KEY, type TEXT, name TEXT, kp_from_m REAL, kp_to_m REAL);
CREATE TABLE IF NOT EXISTS field_report(report_id TEXT PRIMARY KEY, client_uuid TEXT UNIQUE, report_date TEXT, crew_id TEXT,
  front_id TEXT, submitted_at TEXT, source_system TEXT, record_version INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS field_report_line(line_id TEXT PRIMARY KEY, report_id TEXT, activity_code TEXT, kp_from_m REAL,
  kp_to_m REAL, qty REAL, unit TEXT, hours_worked REAL, headcount INTEGER, equipment_ids TEXT, downtime_h REAL,
  downtime_reason TEXT, photo_refs TEXT);
CREATE TABLE IF NOT EXISTS subcontractor_claim(claim_id TEXT PRIMARY KEY, subcontractor_id TEXT, period_from TEXT,
  period_to TEXT, submitted_at TEXT, status TEXT);
CREATE TABLE IF NOT EXISTS subcontractor_claim_line(claim_line_id TEXT PRIMARY KEY, claim_id TEXT, boq_item_id TEXT,
  activity_code TEXT, section_id TEXT, kp_from_m REAL, kp_to_m REAL, work_date TEXT, qty_claimed REAL, unit TEXT);
CREATE TABLE IF NOT EXISTS resource_claim(rc_id TEXT PRIMARY KEY, subcontractor_id TEXT, crew_id TEXT, front_id TEXT,
  work_date TEXT, headcount_claimed INTEGER, hours_claimed REAL);
CREATE TABLE IF NOT EXISTS equipment_claim(ec_id TEXT PRIMARY KEY, subcontractor_id TEXT, equipment_id TEXT, work_date TEXT,
  hours_claimed REAL);
CREATE TABLE IF NOT EXISTS standby_claim(sb_id TEXT PRIMARY KEY, subcontractor_id TEXT, crew_id TEXT, work_date TEXT,
  reason TEXT, hours REAL);
CREATE TABLE IF NOT EXISTS drone_flight(flight_id TEXT PRIMARY KEY, flight_date TEXT, kp_cover_from_m REAL, kp_cover_to_m REAL,
  gsd_cm REAL, rmse_xy_m REAL, rmse_z_m REAL, n_gcp INTEGER, n_checkpoints INTEGER);
CREATE TABLE IF NOT EXISTS measurement(measurement_id TEXT PRIMARY KEY, source TEXT, flight_id TEXT, measure_date TEXT,
  activity_code TEXT, section_id TEXT, method TEXT, kp_from_m REAL, kp_to_m REAL, qty_cum REAL, unit TEXT, sigma REAL,
  quality_flag TEXT);
CREATE TABLE IF NOT EXISTS telematics_daily(equipment_id TEXT, work_date TEXT, engine_h REAL, idle_h REAL, working_h REAL,
  last_kp_m REAL, data_status TEXT, PRIMARY KEY(equipment_id, work_date));
CREATE TABLE IF NOT EXISTS presence_daily(work_date TEXT, front_id TEXT, crew_id TEXT, checkin_count INTEGER,
  manifest_count INTEGER, camera_max INTEGER, badge_zone_count INTEGER, PRIMARY KEY(work_date, front_id, crew_id));
CREATE TABLE IF NOT EXISTS badge_event(badge_pid TEXT, front_id TEXT, ts TEXT);
CREATE TABLE IF NOT EXISTS vehicle_trip(trip_id TEXT PRIMARY KEY, vehicle_id TEXT, crew_id TEXT, work_date TEXT,
  front_id TEXT, arrive_ts TEXT, pax INTEGER);
CREATE TABLE IF NOT EXISTS weather_obs(work_date TEXT PRIMARY KEY, wind_ms REAL, precip_mm REAL, condition TEXT);
CREATE TABLE IF NOT EXISTS certification_line(cert_id TEXT PRIMARY KEY, rec_key TEXT, cert_date TEXT, cum_certified REAL,
  certified_by_role TEXT, reason_code TEXT, comment TEXT);
CREATE TABLE IF NOT EXISTS invoice_line(invoice_line_id TEXT PRIMARY KEY, rec_key TEXT, invoice_date TEXT, cum_invoiced REAL,
  invoice_no TEXT);
CREATE TABLE IF NOT EXISTS alert_state(alert_id TEXT PRIMARY KEY, status TEXT, comment TEXT, updated_at TEXT, actor_role TEXT);
CREATE TABLE IF NOT EXISTS audit_event(event_id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, actor_role TEXT, entity TEXT,
  entity_id TEXT, action TEXT, detail TEXT, before_hash TEXT, after_hash TEXT);
CREATE TABLE IF NOT EXISTS anomaly_ground_truth(anomaly_id TEXT PRIMARY KEY, rule_id TEXT, entity TEXT, entity_id TEXT,
  work_date TEXT, description TEXT);
"""

TABLES = [line.split("(")[0].split()[-1] for line in SCHEMA.split(";") if "CREATE TABLE" in line]


def connect(path=None):
    conn = sqlite3.connect(str(path or DEFAULT_DB), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def table_columns(conn, table):
    return [r[1] for r in conn.execute(f"PRAGMA table_info({table})")]
