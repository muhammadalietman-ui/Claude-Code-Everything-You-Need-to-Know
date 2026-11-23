# Handover: D1 / full-stack-developer (backend) → data-engineer, data-scientist (D2)

## 1. What was produced
Generator, schema, engine, API, CLI and tests. See `phase_reports/D1_mvp_demo_iteration1.md`.

## 2. Key decisions
D-075 (stack), D-076 (over-certification).

## 5. What the next agent must know
1. Reference data goes in through `siteops.cli load <dir> ""`. Column names must match `db.py` exactly; unknown columns are rejected.
2. `measurement.qty_cum` is **cumulative per section and activity**. Its `sigma` drives U. If `sigma` is missing, the status degrades to a pure tolerance check.
3. All thresholds are in `siteops/config.py`: placeholder tolerances until Q-063 is answered.
4. The work front equals the section in the demo. Real fronts (tie-ins, HDD, camps) need `work_front` rows with KP ranges.

## 6. Not done
- No real authentication (demo `X-Role` header).
- No GAEB export.
- No German UI.
- No machine-control import.
- Single-user SQLite.
