# As-Is Data-Flow Diagram (DFD)

Owner: process-analyst. Version 0.1 (Phase 0). **[A] HYPOTHETICAL**: to be validated in P3.
Process numbers align with the step IDs in [as_is_process_map.md](as_is_process_map.md).

## Level 0: Context diagram

```mermaid
flowchart LR
  SUB["Subcontractor [SUBCONTRACTOR_B]"]
  CLIENT["Client / Owner's engineer"]
  DRONE["UAV + [DRONE_SW] vendor platform"]
  BANK["Bank"]
  P0(("0. Contractor production and quantity certification process"))

  SUB -- "Daily reports, timesheets, quantity claims, invoices" --> P0
  P0 -- "Joint measurement sheets, certificates, payments, dispute letters" --> SUB
  DRONE -- "Orthophotos, DSM, volume reports" --> P0
  P0 -- "Flight requests, GCP data" --> DRONE
  P0 -- "Progress reports, contractor interim claims" --> CLIENT
  CLIENT -- "Approved progress, instructions" --> P0
  P0 -- "Payment instructions" --> BANK
```

## Level 1

```mermaid
flowchart TB
  SUB["Subcontractor"]
  FORE["Foremen / Site engineer"]
  DRN["UAV flights"]

  P1(("1. Capture and process drone data"))
  P2(("2. Report daily production"))
  P3(("3. Track progress"))
  P4(("4. Measure and reconcile quantities"))
  P5(("5. Certify and review commercially"))
  P6(("6. Process invoice and payment"))
  P7(("7. Manage disputes"))

  DS1[("D1 Drone data store: [DRONE_SW] cloud / NAS")]
  DS2[("D2 Survey files: CAD, GNSS CSV")]
  DS3[("D3 Daily reports: Excel / PDF")]
  DS4[("D4 Email inboxes and chat groups")]
  DS5[("D5 Subcontractor records")]
  DS6[("D6 QS reconciliation workbooks")]
  DS7[("D7 Document management system")]
  DS8[("D8 [ERP_SYSTEM]")]
  DS9[("D9 Progress tracker / schedule")]

  DRN -- "Images, GNSS logs" --> P1
  P1 -- "Ortho, DSM, volume report" --> DS1
  P1 -- "Volume PDF by email" --> DS4
  FORE -- "Crew, equipment, output sheets" --> P2
  P2 -- "Daily production report" --> DS3
  P2 -- "Photos, WhatsApp messages" --> DS4
  SUB -- "Daily reports, timesheets, claims" --> DS5
  DS5 -- "Claim by email" --> DS4
  DS3 -- "Re-keyed quantities" --> P3
  DS1 -- "Volumes, manual reading" --> P3
  P3 -- "Progress %" --> DS9
  DS4 -- "Evidence attachments" --> P4
  DS1 -- "Screenshots, volumes" --> P4
  DS2 -- "As-built lengths" --> P4
  DS3 -- "Reported quantities" --> P4
  P4 -- "Reconciled quantities" --> DS6
  DS6 -- "Draft certificate" --> P5
  P5 -- "Signed certificate" --> DS7
  P5 -- "Disputed items" --> P7
  P7 -- "Revised quantities" --> DS6
  P7 -- "Letters, minutes" --> DS7
  DS7 -- "Certificate, re-keyed" --> P6
  SUB -- "Invoice" --> P6
  P6 -- "Service entry, invoice, payment" --> DS8
```

## Integration breaks identified [A]

| Break ID | Break | Where | Effect | Requirement it drives |
|---|---|---|---|---|
| DB-01 | **No common location key.** Drone data is indexed by flight area and coordinates. DPRs use KP ranges or landmarks. Subcontractor claims use BoQ items, sometimes with "corners" or sections | D1, D3, D5 | Quantities cannot be joined automatically by location | Linear referencing on KP; section register (D-004) |
| DB-02 | **No common time base.** Flight capture time, shift date and claim period do not align. Work at night or after the flight is attributed to the wrong day | P1, P2, P4 | Daily measured vs reported comparisons are biased | UTC event timestamps; flight-to-shift attribution rule |
| DB-03 | **Manual re-keying** of the same quantity 3–4 times: foreman sheet → DPR → tracker → QS workbook → ERP | D3, D9, D6, D8 | Transcription errors, latency, version drift | Capture once at source; system-of-record per quantity state |
| DB-04 | **Version uncertainty.** Multiple Excel and PDF copies travel by email. There is no single approved version of a daily quantity | D3, D4, D6 | Disputes about which number is "right" | Immutable versioned records; approval status |
| DB-05 | **Evidence not linked to quantities.** Photos, orthophotos and survey points are not attached to the specific quantity record, KP range and date | D1, D4, D6 | Evidence searches during disputes take days | Evidence references on every quantity record |
| DB-06 | **No crew/equipment link to output.** Timesheets and equipment logs are not linked to the activity and section produced | D3, D5 | No productivity per crew or section; late delay detection (H4) | Crew/equipment-to-activity assignment per shift |
| DB-07 | **Commercial states not modelled.** Planned, reported, measured, claimed, certified and invoiced quantities live in different files | D9, D3, D1, D5, D6, D8 | Overpayment and duplicate claims are hard to detect | Five-state quantity model (D-008) |
| DB-08 | **Undocumented tolerance.** Accepted differences between survey and claim are applied case by case | P4, P5 | Inconsistent certification | Tolerance rules per BoQ item |
