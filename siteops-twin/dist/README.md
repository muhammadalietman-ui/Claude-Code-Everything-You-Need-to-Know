# Stand-alone demo files (no installation needed)

| File | Open with | What it is |
|---|---|---|
| `SiteOps_Twin_Dashboard.html` | Double-click; opens in Edge or Chrome | The full commercial dashboard (S1–S8), interactive. Data and libraries are embedded. Nothing is sent over the network |
| `SiteOps_Twin_FieldApp.html` | Edge or Chrome (also on a phone) | The 3-step field daily report |
| `SiteOps_Twin_Demo.xlsx` | Excel | Reconciliation with **live formulas** for status and cap, plus alerts, scorecard, presence, equipment hours, certificate and rules |

**All data is SYNTHETIC.** In the HTML demo, certifications, alert updates and field reports are kept in memory until you reload the page. Use a recent Edge or Chrome; very old browsers lack the built-in decompression the page uses.

To rebuild after changes: `python -m siteops.export_static` and `python -m siteops.export_excel` in `prototype/`.
