# Market Scan: Index

Status as of 2026-11-23. Owners: solution-architect and commercial-analyst. This scan feeds Chapter 2 (state of practice), the build-vs-buy decision (ADR stubs in `04_to_be_architecture/conceptual_architecture.md` §10) and the business case (P8).

| File | Content |
|---|---|
| `market_scan_report.md` | The full report. It covers: method; the landscape in categories A–F; a capability heat-map (54 solutions × O1–O9); gap analysis; integration with Propeller; build/buy/integrate; positioning; German-market specifics (GDPR, BetrVG, GAEB/REB/VOB); and references |
| `solutions_catalogue.csv` | One row per solution (54 rows, 23 columns). Columns: id, name, vendor, category, core functions, linear/pipeline suitability, integration/API and standards, offline, data residency/GDPR, pricing, status, O1–O9 flags (Y / Partial / N), evidence level (V1 vendor, V2 independent, V3 filing), source URLs, notes |

**Categories:**
- A: drone / reality capture (10)
- B: digital twin / 4D / progress and quantity platforms (9)
- C: pipeline-construction-specific (10)
- D: workforce and equipment tracking (10)
- E: field daily reporting (7)
- F: commercial / QS / GAEB / AVA / contracts (8)

**Key caveat.** Capability flags record *documented* capability, mostly taken from vendor material. Source URLs were returned by web search and read through the search tool's page extracts, because direct page fetches were blocked by the session's network allowlist. Before any row is cited as a finding, verify it by direct page review or vendor demo (report §10).

**Headline finding.** Each data stream is well served on its own: UAV measurement, weld/QA records, telematics, daily reports and German AVA billing. No solution documents three things:
1. reconciling subcontractor claims against independently measured, uncertainty-bounded quantities on a KP-referenced key;
2. triangulating resource-based claims with multiple presence signals;
3. handing certified quantities to German AVA as GAEB X31/REB with an evidence pack.

O8 (commercial deviation and duplicate-claim alerts) has no full ("Y") coverage among the 54 products.
