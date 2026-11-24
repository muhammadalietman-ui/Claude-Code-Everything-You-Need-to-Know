# Tender — Commercial Team Orchestrator

Run a full tender with the commercial team: the **Tender Manager** and **Technical Manager** analyse the client documents, decide whom to hire, the hired specialists produce their deliverables, the managers review, and the Document Controller compiles the submission package.

## Usage
`/tender <TENDER-ID> [phase]` e.g. `/tender DE063` or `/tender DE063 review`

## Variables
- TENDER_ID: $ARGUMENTS (first word). Workspace = `tenders/<TENDER_ID>/`
- PHASE (optional): `analyse` | `mobilise` | `review` | `compile` | `status`. Default = continue from the last completed phase recorded in `tenders/<TENDER_ID>/tender-log.md`.

## You (the main session) are the orchestrator
Subagents cannot spawn other subagents. The managers therefore **hire** by writing a staffing plan; **you** execute it by launching the requested agents with the Agent tool. Never do a specialist's work yourself — delegate. Launch independent hires in parallel (several Agent calls in one message).

---

## Phase 0 — Set-up
1. If `tenders/<TENDER_ID>/` does not exist, copy `tenders/_template/` to it.
2. Check `00_client_docs/` contains the client documents. If empty, stop and ask the user to upload the ITB/RFP package.
3. Check `tenders/_company/` — if company profile, references or CVs are missing, warn the user that those sections will carry `[[DATA REQUIRED]]` placeholders.
4. Create/append `tender-log.md` (date, phase, action, files, decisions).

## Phase 1 — Analyse (parallel)
Launch **in the same message**:
- `tender-manager` — "Phase 1 tender analysis for tenders/<ID>. Produce all Phase 1 outputs and staffing-plan-commercial.md."
- `technical-manager` — "Phase 1 technical analysis for tenders/<ID>. Produce all Phase 1 outputs and staffing-plan-technical.md."
- `document-controller` — "Build the document register and deliverables tracker for tenders/<ID>."

Then merge both staffing plans into `01_analysis/staffing-plan.md` (remove duplicate hires, check every deliverable in `submission-structure.md` and `technical-deliverables.md` has an owner — if not, add a hire and flag it).

### 🚦 Gate 1 — Bid Director decision (STOP and ask the user)
Present: tender headline & key dates, bid/no-bid recommendation, top risks, clarifications to send, and the **staffing plan as a table** (id, role, wave, deliverables, due). Ask the user to approve / edit the team. Do not proceed without approval.

## Phase 2 — Mobilise the team
Execute the approved staffing plan wave by wave:
- For every hire in the current wave, launch its `agent` with a task message containing the full YAML entry (role_title, discipline/expertise, brief, inputs, deliverables, due, handover_to) plus the tender ID and paths to `tender-brief.md`, `scope-matrix.md` and `compliance-matrix.md`.
- Launch all hires of one wave in parallel. Wait for the wave to finish, record each return (files, open items, handovers) in `tender-log.md` and the deliverables tracker, then start the next wave and pass the relevant handovers into those briefs.
- Typical waves: **1** contracts, discipline engineers, HSE, quality, procurement strategy/RFQs, on-demand specialists → **2** planning (needs methods & long-lead items), procurement TBE/CBE (needs quotes) → **3** cost-estimator (needs MTO, quotes, schedule, risk registers).
- If an agent reports missing data that the user can supply, collect these into one list and ask the user once per wave.

## Phase 3 — Review (parallel)
Launch `technical-manager` (technical review) and `tender-manager` (commercial & compliance review) in parallel. For each Critical/Major finding, relaunch the owning hire with the finding and required action. Maximum 2 review rounds; anything still open goes to the user.

## Phase 4 — Compile
Launch `document-controller` to compile `04_submission/` per `submission-structure.md`, produce DOCX/XLSX/PDF outputs, the transmittal and submission checklist.

### 🚦 Gate 2 — Final sign-off (STOP)
Present to the user: package index, checklist with any ❌, unresolved `[[DATA REQUIRED]]` items (run `grep -rn "DATA REQUIRED" tenders/<ID>/04_submission`), deviations being submitted, and the pricing summary **with margin left for the user to set**. The team never submits to the client — the user does, after signing, stamping and final authorised review.

## Status
`/tender <ID> status` → summarise `tender-log.md` and the deliverables tracker: phase, % deliverables complete, blockers, days to submission.
