# Contract-to-Execution decomposition

How to turn the client contract and its documents into owned, executable obligations. Read each document; for each item below that the document contains, create one Obligation Register line with the owner department shown. Record the clause/section exactly as written; if unclear, flag "verify — Contracts/Legal". Never fill a clause number, time limit or value that is not in the document.

## 1. Order of reading
1. Contract agreement and order of precedence (D04) — fixes which document wins in a conflict.
2. Special / particular conditions, then general conditions (D04).
3. Scope of work / Leistungsbeschreibung and BOQ / price schedule (D04, D12).
4. Technical specifications and standards list (D07, D02).
5. Drawings: alignment sheets, crossings, tie-ins, stations (D02).
6. Permits, planning approval and authority conditions (D09).
7. Landowner, environmental and archaeological conditions (D09).
8. HSE and quality requirements, OGE procedures (D08, D07).
9. Client-supplied items and interface documents (D06, D14).
10. Reporting, document control and dossier requirements (D13, D03).
11. Agreed minutes, clarifications and correspondence that modify the above (D04, D14).

## 2. Extraction checklist by document type
### Contract conditions (D04 lead)
- Notices: every event type, recipient, form, time limit → notices calendar.
- Instructions/variations: who may instruct, form, valuation, time limits.
- Time: commencement, key dates, sectional completion, EOT events, delay damages basis.
- Money: payment cycle, milestones, retention, guarantees, advance, indexation, invoicing format → D12.
- Risk: ground conditions, utilities, permits, client-supplied material, weather → mark who bears each.
- Subcontracting: client approval rights, mandatory flow-downs → D05.
- Acceptance: mechanical completion, Abnahme/taking-over, defects period → D11, D13.
- Insurance, liability caps, indemnities, suspension, termination, disputes, governing law.

### Scope of work / BOQ (D04 + D12, D05 for packaging)
- Each scope paragraph → one or more obligations; map to BOQ item.
- Explicit exclusions and client-supplied items → D06/D14.
- Items in SOW with no BOQ line (G1/G3), BOQ lines with no SOW text (ambiguity → TQ).
- Measurement rules and pricing basis per item.
- Assign each scope item an execution vehicle and, if subcontracted, a package (D05 package plan).

### Technical specifications (D07 + D02)
- Governing standards and editions; conflicts between spec and standard → TQ.
- Hold/witness points and client notice periods → ITP.
- Welding, NDT, coating, bending, lowering, backfill, cover, testing criteria → method statements and ITPs.
- Qualification and approval requirements (WPS/PQR, welders, applicators, labs, inspectors).
- Records required per activity → dossier index (D13).

### Drawings (D02)
- Crossing list with type, owner, owner conditions → crossing schedule, D09 for consents.
- Quantities for BOQ check and measurement (D12).
- Tie-in details and shutdown dependencies → D11, D14.

### Permits and authority conditions (D09)
- Each condition → owner dept, action, evidence; flow-down to affected subcontracts (G4 check with D04).
- Validity dates vs schedule (D03).
- Water abstraction/discharge, traffic orders, noise/working hours, ecological windows.

### Landowner and environmental conditions (D09)
- Per parcel: entry conditions, access, drainage, crop compensation, reinstatement standard, contact.
- Pre-entry condition survey and post-reinstatement sign-off as evidence.

### HSE and quality requirements (D08, D07)
- Plans and procedures to submit, approval cycles → D13 MDR.
- Incident reporting time limits → D08 procedure.
- Audits, inspections, KPIs reporting format.

### Client-supplied items and interfaces (D06, D14)
- What, quantity, delivery point, condition, transfer of custody, inspection time limit.
- Client operations interfaces (shutdowns, live-line tie-ins, access to stations).

### Reporting and documentation (D13, D03)
- Report types, frequency, format; programme updates; MDR; dossier structure; as-built format.

## 3. Output of the decomposition
- **Obligation Register** (see `gap-closure.md` §4.1).
- **Notices calendar** (D04) and **permit condition matrix** (D09).
- **Package plan** with flow-down list per package (D05/D04).
- **ITP list and dossier index** (D07/D13).
- **TQ list** for conflicts and missing data, and **Gap Register** seeded from the five-layer trace.

## 4. Back-to-back check per subcontract (D04 with subcontract-gap-check)
For each main-contract obligation assigned to a subcontract package, confirm the subcontract has: same or stricter technical requirement; notice time limit shorter than the main contract (so the JV can still notify OGE); same records and dossier obligations; HSE and permit conditions; liability and damages proportionate to the JV's exposure; interface clause naming the hand-off point, the next party and the test/acceptance at the boundary. Any "no" is a G4 gap.

## 5. Interface definition standard (closes G2)
Every interface between two packages or departments is written as:
`Interface ID | Upstream party/dept | Downstream party/dept | Hand-off point (physical / document) | Condition at hand-off (acceptance criteria) | Test or inspection at boundary | Who supplies what (material, plant, utilities, water) | Who pays | Records produced | Date/trigger | Agreed by (signatures/minutes ref)`.
Example (S-02, to be confirmed): upstream Lorenz Bohrtechnik (HDD pull-in of OD 50 KSR signal-cable pipes) → downstream test party (caliper pigging and pressure test per RN 625-001) — open until owner, price and acceptance criteria are agreed with the construction team and Project Manager.
