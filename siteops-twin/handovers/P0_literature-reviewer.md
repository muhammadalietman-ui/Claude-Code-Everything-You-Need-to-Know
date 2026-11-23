# Handover: P0 / literature-reviewer → research-lead, quality-reviewer, academic-writer

- **Date:** 2026-11-23
- **Task / backlog IDs:** T-003 (feeds T-201…T-204)

## 1. What was produced
| File | Status | Notes |
|---|---|---|
| `02_literature_review/protocol.md` | Draft for review | PRISMA 2020-style; PICOC; IN1–IN5 / EX1–EX8; dual screening with κ ≥ 0.6; QA1–QA8 appraisal; synthesis plan; PRISMA Mermaid template |
| `02_literature_review/search_strings.md` | Draft, **not piloted** | CORE-01 plus C1–C9 and C4-ETH (Scopus + WoS); GS-01…07 (Scholar, top 200); PM-01…03 (POLITesi, RE.PUBLIC@POLIMI, discovery); search-log template; gold-set test |
| `02_literature_review/screening_log_template.csv` | Final template | 2 EXAMPLE rows |
| `02_literature_review/reference_matrix_template.csv` | Final template | C1–C9 flags, H1–H4 relevance, `verified_doi` |
| `02_literature_review/seed_references.md` | Seed only | 18 works + 8 standards, **all VERIFY**; candidate DOIs unverified |
| `02_literature_review/gap_hypotheses.md` | Candidate [A] | G1–G6, each with a test and an RQ mapping |

## 2. Key decisions taken
Proposed D-020, D-021 (rows below).

## 3. Assumptions introduced
A-020, A-021, A-022 (rows below).

## 4. Open questions
Q-020, Q-021, Q-022 (rows below).

## 5. What the next agent must know
1. **No seed reference may be cited until its DOI is verified.** Candidate DOIs come from memory. S12 has an ambiguity: the JCCE 2009 paper or the ITcon 2009 D4AR paper.
2. The strings must be piloted (gold-set test) before the counts are logged. `API*` in C7 may be noisy (A-022).
3. Google Scholar is supplementary only (top 200 per string). The PRISMA counts must show it separately.
4. Standards are cited normatively, not screened.
5. Gaps G1 and G3 are the likely core contribution. Keep the research framing §6 aligned with them.

## 6. Known weaknesses / not done
- No searches have been run. Hit counts are unknown, so the yield risk (under 30 or over 1,500 records) is unassessed.
- Whether OSF registration is needed or wanted is undecided (Q-021).
- Seed list bibliographic details are unverified (pages and issue numbers in particular).

## Proposed log rows (ready to paste)

**DECISIONS_LOG.md**
```
| D-020 | 2026-11-23 | SLR date range 2010–2026 with seminal-work exemption; English (+ Italian for POLIMI sources) | Covers the UAV/DT era; keeps foundational theory | literature-reviewer | Proposed |
| D-021 | 2026-11-23 | Google Scholar limited to first 200 results by relevance per string; reported separately in PRISMA | Scholar ranking is not reproducible; bounded effort | literature-reviewer | Proposed |
```
**ASSUMPTIONS_LOG.md**
```
| A-020 | A second screener is available for ~6–8 h for 20% dual screening | SLR good practice | κ cannot be computed; reliability threat | Confirm with supervisor | literature-reviewer | P2 wk 3 | Open |
| A-021 | Heterogeneity of outcomes precludes meta-analysis; narrative/thematic synthesis with evidence tables | Expected diversity of methods and metrics | If homogeneous UAV accuracy data exist, a simple pooled summary may be added | Check after extraction | literature-reviewer | P2 wk 10 | Open |
| A-022 | The `API*` token in C7 may retrieve American Petroleum Institute noise | Oil & gas terminology | Inflated screening load | String pilot | literature-reviewer | P2 wk 3 | Open |
```
**OPEN_QUESTIONS.md**
```
| Q-020 | Who can act as second screener (co-supervisor, PhD candidate, peer student)? | User → supervisor | P2 wk 5 | | Open |
| Q-021 | Should the SLR protocol be pre-registered (e.g., OSF) before searching? | Supervisor | P2 wk 3 | | Open |
| Q-022 | Does the student have off-campus access to Scopus/WoS via POLIMI credentials (alumni/enrolled status)? | User | P2 wk 3 | **B** | Open |
```
**RISK_REGISTER.md**
```
| R-20 | Loss of POLIMI database access (enrolment/alumni status) blocks Scopus/WoS searches | Access | 2 | 4 | 8 | Confirm access early (Q-022); fall back to Scholar + library ILL; run searches in week 4 | literature-reviewer | Open |
```
