"""Configurable parameters (placeholders until contract values are known, see A-050, A-043, Q-063)."""
SEED = 20270104
SPREAD_ID = "SYN-SPREAD-01"
SITE_TZ = "Europe/Berlin"
KP_END_M = 25_000
SECTION_LEN_M = 1_000
ROW_WIDTH_M = 30            # converts reinstatement m2 to linear metres
JOINT_LEN_M = 12            # converts welds/coatings (nr) to linear metres
START_DATE = "2027-01-04"
N_WORKING_DAYS = 60

# Contract tolerance T = max(abs, pct * M)   (D-063; values are placeholders [TOL_*])
TOL_PCT = {"m": 0.01, "m2": 0.02, "m3": 0.03, "nr": 0.005}
TOL_ABS = {"m": 2.0, "m2": 20.0, "m3": 2.0, "nr": 3.0}   # nr: count tolerance of 3 joints
U_K = 2.0                   # expanded uncertainty factor, ~95% (A-063)

AL05_DROP = 0.25            # productivity drop vs 5-day rolling median (A-043)
AL06_GRACE_DAYS = 3         # claimed but unverifiable for longer than this -> AL-06
AL03_MIN_OVERLAP_M = 100.0  # overlapping claimed KP length that triggers AL-03
AL08_TOL_M = 20.0           # out-of-sequence tolerance (linear metres)
TOL_HEAD = 2                # AL-09 headcount tolerance
TOL_EQ_H = 1.0              # AL-11 equipment-hour tolerance
AL07_RATIO = 0.5            # AL-07 telematics working hours < ratio x reported hours
AL10_MAX_KMH = 80.0         # AL-10 impossible-travel speed
WEATHER_WIND_LIMIT_MS = 15.0
WEATHER_PRECIP_LIMIT_MM = 20.0

# Precedence pairs for AL-08 (predecessor, successor); configurable per spread (A-016)
PRECEDENCE = [("WLD", "FJC"), ("FJC", "LOW"), ("TRN", "LOW"), ("LOW", "BKF"), ("BKF", "RST")]
CURRENCY = "SYN¤"
