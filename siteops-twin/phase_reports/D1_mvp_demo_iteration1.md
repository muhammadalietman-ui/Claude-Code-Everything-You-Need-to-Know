# D1 Close-Out: MVP Demo, Iteration 1

Date: 2026-11-23 · Lead: full-stack-developer · QA: quality-reviewer

## 1. Completed deliverables
| Item | Location |
|---|---|
| Synthetic generator (seeded; 24 anomalies seeded across the 13 rules, with ground truth) | `prototype/siteops/generate.py` → `data/synthetic/SYNTHETIC_*.csv` |
| SQLite schema (26 tables incl. sensing, certification, audit) | `prototype/siteops/db.py` |
| Reconciliation engine (D-041, D-063, D-064, D-065) and alerts AL-01…AL-13 | `prototype/siteops/engine.py` |
| REST API (contract v1) with demo RBAC and audit | `prototype/siteops/api.py`, `prototype/API_CONTRACT.md` |
| Commercial dashboard S1–S8 | `prototype/web/index.html` |
| Offline field app M1–M4 (PWA) | `prototype/web/field.html` |
| Tests (22) | `prototype/tests/` |
| Reference-project intake guide | `data/templates/REFERENCE_PROJECT_INTAKE.md` |
| Germany context (legal, commercial, technical) | `01_governance/germany_context.md` |

## 2. Verification
- `pytest`: 22 passed. Every seeded anomaly is detected, and the precision guard holds.
- End-to-end run against the real server in Chromium: 8 dashboard screens and the field app, with 0 console, page or HTTP errors.
- Libraries are bundled locally, so the dashboard makes no CDN calls.

## 3. Findings worth keeping for the thesis
1. **AL-05 sensitivity.** At a 25% threshold, natural productivity variability (σ = 0.12) gives about 1.3% false positives per crew-day. Calibration on the reference project is needed (A-043).
2. **Downstream effects are real signals.** One duplicate claim shows up as AL-03, as AL-01 against the QA log, and as AL-04 against the BoQ. Triangulation across rules strengthens the evidence in a dispute.
3. **Over-certification after re-measurement** (D-076). A quantity certified against an earlier flight can exceed the cap after a newer measurement. The platform shows it for recovery in the next certificate.
4. **Pending verification.** Claims after the last flight are kept separate, which avoids false discrepancies on no-fly days (D-041).

## 4. Open questions
Q-063 (tolerances), Q-073 (works council), Q-074 (VOB/GAEB), Q-075 (machine-control and weld data).

## 5. Decisions required
None blocking. The next input is the user's demo feedback and the reference-project data drop 1.

## 6. Next actions
- D2 intake as soon as data arrives.
- D3 backlog: GAEB/Aufmaß export, German UI (i18n), T8 machine-control import, login instead of the `X-Role` header, and a Docker one-command run.

## 7. Quality checklist
- [x] Synthetic data only, labelled in file names and headers
- [x] No CDN, secrets or real identifiers in the code
- [x] Tests pass; e2e clean
- [x] API matches the contract (one addition: `equipment` in `/api/meta`)
- [ ] User demo review
