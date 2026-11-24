# Tender Workspace — Commercial Team

A Claude Code team that turns a client tender package into a submission-ready bid.

## The team
| Role | Agent | Hired by |
|---|---|---|
| Tender Manager (commercial lead) | `tender-manager` | always |
| Technical Manager (technical lead) | `technical-manager` | always |
| Document Controller | `document-controller` | always |
| Contracts Specialist | `contracts-specialist` | Tender Manager |
| Cost Estimator | `cost-estimator` | Tender Manager |
| Procurement Specialist | `procurement-specialist` | either manager |
| Planning Engineer | `planning-engineer` | Technical Manager |
| HSE Specialist | `hse-specialist` | Technical Manager |
| QA/QC Specialist | `quality-specialist` | Technical Manager |
| Discipline Engineer ×N (Electrical, Mechanical, Civil, …) | `discipline-engineer` | Technical Manager |
| Any other role (local content, tax, logistics, …) | `specialist-on-demand` | either manager |

The managers read the client documents and write a **staffing plan** saying exactly who is needed, with briefs, inputs, deliverables and due dates. The `/tender` command then mobilises those people. Only the roles the tender needs get hired.

## How to run a tender
1. Put the client ITB/RFP package (PDF, DOCX, XLSX, drawings) in `tenders/<ID>/00_client_docs/`, or let `/tender <ID>` create the folder from `_template/` first.
2. Fill in `tenders/_company/` once (profile, references, CVs, certificates). The team never invents company data.
3. Run `/tender <ID>`. The flow is:
   **Analyse** (managers + doc control) → 🚦 **Gate 1: you approve bid/no-bid and the team** → **Mobilise** (hires run in parallel waves) → **Review** (managers review, owners fix) → **Compile** → 🚦 **Gate 2: you sign off**.
4. Run `/tender <ID> status` at any time.

## Folder layout per tender
```
00_client_docs/   client documents, as received (read-only)
01_analysis/      tender brief, bid/no-bid, submission structure, evaluation criteria,
                  scope matrix, compliance matrix, clarifications, staffing plan
02_technical/     discipline write-ups, method statements, MTO, schedule, HSE, quality
03_commercial/    contract review, deviations, risk register, procurement, pricing
04_submission/    the final package by envelope/volume, plus transmittal and checklist
05_review/        manager review findings
tender-log.md     decisions and progress log
```

## Guardrails
- Every requirement cites the client document clause.
- Missing data is marked `[[DATA REQUIRED: …]]` and never made up. That covers prices, rates, vendor quotes, experience and certificates.
- You make the margin, bid/no-bid, deviation and signatory decisions. Nothing is submitted to the client automatically.
