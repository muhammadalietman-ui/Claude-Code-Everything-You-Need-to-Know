# Handover: P6 / full-stack-developer (frontend) → full-stack-developer (backend), quality-reviewer

- **Date:** 2026-11-23
- **Scope:** static frontend for the MVP demo. The dashboard covers S1–S8 and the mobile field app covers M1–M4. It is built strictly against `prototype/API_CONTRACT.md` v1.

## 1. What was produced
| File | Status | Notes |
|---|---|---|
| `prototype/web/index.html` | Draft, working | Dashboard shell: top bar (SYNTHETIC DEMO badge, date picker, role and subcontractor pickers), tabs, certify and alert dialogs |
| `prototype/web/app.js` | Draft, working | Hash router: S1 overview (KPI tiles, KP strip, Leaflet map with `L.CRS.Simple`), S2 production, S3 reconciliation workbench (filters, exceptions first, certify with the 409 ABOVE_CAP override flow), S4 scorecard (Chart.js), S5 alerts (Ack/Close with comment), S6 section detail, S7 certificate (JSON table plus CSV download), S8 presence |
| `prototype/web/styles.css` | Draft | Shared styles. Status is shown as colour + icon + text (Okabe–Ito). Dark mode, visible focus, 48 px targets in the field app |
| `prototype/web/field.html`, `field.js` | Draft, working | 3-step report (crew, work, evidence), crew muster stepper (headcount only), copy yesterday, KP validation, photo metadata with a local thumbnail, IndexedDB outbox with localStorage fallback, sync on demand and on the `online` event, per-item status pending / synced / duplicate / error |
| `prototype/web/sw.js`, `manifest.webmanifest` | Draft | App-shell cache. `/api/meta` is fetched network-first and falls back to the cached copy |

## 2. Verification done
- `node --check` passes on app.js, field.js and sw.js. The manifest parses as JSON.
- Playwright smoke test with mocked API responses in the contract's shape:
  - All 8 dashboard routes render content.
  - Certify above the cap returns 409, the reason field appears, and the re-post with a reason succeeds.
  - The field form rejects KP to ≤ KP from; a valid report is POSTed with `client_uuid` and shows as ✔ Synced.
- No page errors. The only console errors were the CDN being blocked in the sandbox and the expected 409.
- **Not tested against the real backend**, because it was being built in parallel. The map and the Chart.js chart could not load in the sandbox (CDN blocked); their fallbacks render.

## 3. Contract ambiguities resolved (backend please confirm)
1. **Equipment list for the field form.** `/api/meta` has no equipment list in v1. `field.js` uses `meta.equipment` (`[{equipment_id, type}]`) if present; otherwise it shows a comma-separated text input. **Recommend adding `equipment` to `/api/meta`.**
2. **Field-app role.** The field app always sends `X-Role: FM`.
3. **Certificate CSV.** It is fetched with the role headers, so RBAC applies, rather than through a plain link. The file is named `SYNTHETIC_certificate_<sc>_<date>.csv`.
4. **Reconciliation filters.** These are sent as `subcontractor`, `status`, `activity` and `section` query params, as in the contract. Exception-first sorting is also applied client-side.
5. **Alert filters.** Default `status=OPEN`. The "All" option sends no param.
6. **Status icons** follow the wireframes (▲ for Discrepancy, ? for Unverifiable), not ✕.
7. **Map coordinates.** GeoJSON `[x, y]` is mapped to `L.latLng(y, x)` under `CRS.Simple`.
8. **Error body.** The frontend reads `body.error` or `body.detail` from non-2xx responses. The field app treats 400/403/422 as permanent errors and 5xx or network failures as retryable.
9. **`/api/sections/{id}` audit items** use the same fields as `/api/audit` events.

## 4. What the next agent must know
- Serve `web/` at `/` from the same origin as `/api`, so the relative fetches and the service worker work.
- `index.html` loads Leaflet 1.9.4 (unpkg) and Chart.js 4.4.1 (jsdelivr) from CDN. Offline demos need internet for these two, or vendored copies.
- The field app's offline outbox depends on `client_uuid` idempotency in `POST /api/field-reports`.

## 5. Known weaknesses / not done
- No automated frontend test file is committed. The smoke script lives in the session scratchpad.
- No i18n yet (German UI later). No photo binary upload (MVP scope).
- The S1 map has no per-front status colouring, because the contract's front features carry no status.
