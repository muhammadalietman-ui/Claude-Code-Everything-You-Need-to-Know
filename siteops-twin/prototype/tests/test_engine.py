"""Reconciliation rule (D-063/D-064) and alert recall against seeded ground truth."""
import pytest

from siteops.engine import classify

RULES = [f"AL-{i:02d}" for i in range(1, 15)]


@pytest.mark.parametrize("claimed,expected", [(1020, "MATCHED"), (1050, "WITHIN_TOLERANCE"), (1100, "DISCREPANCY")])
def test_status_rule_worked_example(claimed, expected):
    # mvp_backlog.md worked example: M = 1000, U = 30, T = 3 % -> cap 1060
    assert classify(claimed, 1000, 30, 30) == expected


def test_unverifiable_without_measurement():
    assert classify(10, None, 0, 0) == "UNVERIFIABLE"


def test_every_rule_is_seeded(computed):
    _, _, _, gt = computed
    assert {g["rule_id"] for g in gt} == set(RULES)


def _match(a, g):
    if a["rule_id"] != g["rule_id"]:
        return False
    eid = g["entity_id"]
    if g["rule_id"] == "AL-03":
        return eid in (a["entity_id"], a.get("related"))
    if g["work_date"] and g["rule_id"] not in ("AL-08", "AL-06", "AL-01", "AL-04", "AL-13", "AL-14"):
        return a["entity_id"] == f"{eid}|{g['work_date']}"
    return a["entity_id"] == eid


def test_recall_all_seeded_anomalies_detected(computed):
    _, _, al, gt = computed
    missed = [g for g in gt if not any(_match(a, g) for a in al.values())]
    assert missed == [], f"missed seeded anomalies: {missed}"


def test_no_alert_floods(computed):
    """Precision guard: downstream effects of seeded anomalies are allowed, floods are not."""
    _, _, al, gt = computed
    from collections import Counter
    n_al, n_gt = Counter(a["rule_id"] for a in al.values()), Counter(g["rule_id"] for g in gt)
    for rule in RULES:
        assert n_al[rule] <= 3 * n_gt[rule] + 1, f"{rule}: {n_al[rule]} alerts for {n_gt[rule]} seeded"


def test_seeded_overclaims_are_discrepancies(computed):
    _, rec, _, _ = computed
    by_key = {r["key"]: r for r in rec}
    for key in ("S07|TRN|SYN-SUB-B", "S12|BKF|SYN-SUB-B"):
        assert by_key[key]["status"] == "DISCREPANCY"
        assert by_key[key]["certified"] < by_key[key]["claimed"]  # over-claim never certified in full
        assert by_key[key]["over_certified"] == max(round(by_key[key]["certified"] - by_key[key]["cap"], 1), 0.0)


def test_honest_rows_mostly_matched(computed):
    _, rec, al, _ = computed
    flagged = {a["rec_key"] for a in al.values() if a.get("rec_key")}
    clean = [r for r in rec if r["key"] not in flagged and r["claimed"] > 0 and r["measured"] is not None]
    ok = [r for r in clean if r["status"] in ("MATCHED", "WITHIN_TOLERANCE")]
    assert len(ok) / len(clean) >= 0.97


def test_cap_formula(computed):
    _, rec, _, _ = computed
    for r in rec:
        if r["measured"] is not None:
            assert abs(r["cap"] - (r["measured"] + r["u"] + r["tol"])) < 0.2


def test_synthetic_files_labelled(built):
    db, _ = built
    out = db.parent / "synthetic"
    files = list(out.glob("*.csv"))
    assert files and all(f.name.startswith("SYNTHETIC_") for f in files)
    assert all(f.read_text().startswith("# SYNTHETIC") for f in files)


def test_deterministic(tmp_path):
    from siteops.generate import generate
    a, b = generate(), generate()
    assert a["subcontractor_claim_line"] == b["subcontractor_claim_line"]
