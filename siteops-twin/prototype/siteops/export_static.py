"""Build stand-alone demo files that open by double-click (no Python, no server, no internet).

    python -m siteops.export_static      ->  ../dist/SiteOps_Twin_Dashboard.html
                                             ../dist/SiteOps_Twin_FieldApp.html

How it works: the real FastAPI backend is run once in-process. Every GET response for every
working day is captured, gzip-compressed and embedded in the HTML. A small in-browser shim
replaces `fetch('/api/...')`. It serves the snapshots, applies the role filters, and simulates
POSTs in memory: certification with the cap rule, alert status, field reports. All data is SYNTHETIC.
"""
from __future__ import annotations

import base64
import gzip
import json
import re
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
DIST = ROOT.parent / "dist"
DASH, FIELD = "SiteOps_Twin_Dashboard.html", "SiteOps_Twin_FieldApp.html"


def capture(db_path=None) -> dict:
    from .api import create_app
    c = TestClient(create_app(db_path))
    g = lambda p, **params: c.get(p, params=params).json()  # noqa: E731
    meta = g("/api/meta")
    data = {"meta": meta, "geometry": g("/api/geometry"), "audit": g("/api/audit")["events"], "by_date": {}}
    dates = sorted({r["report_date"] for r in g("/api/field-reports")["reports"]} | {meta["date_max"]})
    subs = [s["subcontractor_id"] for s in meta["subcontractors"]]
    for d in dates:
        snap = {"overview": g("/api/overview", date=d), "reconciliation": g("/api/reconciliation", date=d)["rows"],
                "production": g("/api/production", date=d), "alerts": g("/api/alerts", date=d)["alerts"],
                "scorecard": g("/api/scorecard", date=d), "presence": g("/api/presence", date=d),
                "certificate": {s: g(f"/api/certificate/{s}", date=d) for s in subs}, "sections": {}}
        for s in meta["sections"]:
            sd = g(f"/api/sections/{s['section_id']}", date=d)
            # rows and alerts are rebuilt from the date snapshot in the browser; keep only the extra parts
            snap["sections"][s["section_id"]] = {"section": sd["section"], "flights": sd["flights"],
                                                 "measurements": sd["measurements"]}
        data["by_date"][d] = snap
    data["dates"] = dates
    return data


SHIM = r"""
// ---- SiteOps Twin stand-alone shim: replaces the backend with embedded SYNTHETIC snapshots ----
window.__SITEOPS_READY__ = (async () => {
  const b64 = document.getElementById('siteops-data').textContent.trim();
  const bytes = Uint8Array.from(atob(b64), (ch) => ch.charCodeAt(0));
  const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
  const D = JSON.parse(await new Response(stream).text());
  const audit = D.audit.slice();
  const certOverride = {};   // key -> qty (in-memory certifications)
  const alertState = {};     // alert_id -> {status, comment}
  const reports = [];
  const nowIso = () => new Date().toISOString().replace(/\.\d+Z$/, 'Z');
  const snapFor = (date) => {
    const ds = D.dates; let pick = ds[ds.length - 1];
    if (date) { pick = ds[0]; for (const d of ds) if (d <= date) pick = d; }
    return [pick, D.by_date[pick]];
  };
  const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });
  const scope = (arr, role, sc) => role === 'SC' ? arr.filter((x) => x.subcontractor_id === sc) : arr;
  const withState = (rows) => rows.map((r) => certOverride[r.key] != null ? { ...r, certified: certOverride[r.key] } : r);
  const alertsWithState = (al) => al.map((a) => alertState[a.alert_id] ? { ...a, ...alertState[a.alert_id] } : a);
  const addAudit = (role, entity, entity_id, action, detail) => audit.unshift({ event_id: audit.length + 1, ts: nowIso(), actor_role: role, entity, entity_id, action, detail, before_hash: null, after_hash: 'demo' });

  const realFetch = window.fetch.bind(window);
  window.fetch = async (input, init = {}) => {
    const url = new URL(typeof input === 'string' ? input : input.url, 'http://demo.local');
    if (!url.pathname.startsWith('/api/')) return realFetch(input, init);
    const h = new Headers(init.headers || {});
    const role = (h.get('X-Role') || 'CM').toUpperCase(); const sc = h.get('X-Subcontractor');
    if (role === 'SC' && !sc) return json({ detail: 'X-Subcontractor header required for role SC' }, 400);
    const method = (init.method || 'GET').toUpperCase();
    const q = Object.fromEntries(url.searchParams.entries());
    const [date, S] = snapFor(q.date);
    const p = url.pathname;
    if (method === 'GET') {
      if (p === '/api/meta') return json({ ...D.meta, date_min: D.dates[0], date_max: D.dates[D.dates.length - 1], standalone: true, snapshot_dates: D.dates });
      if (p === '/api/geometry') return json(D.geometry);
      if (p === '/api/health') return json({ ok: true, synthetic: true, standalone: true });
      if (p === '/api/overview') {
        if (role !== 'SC') return json(S.overview);
        const rows = scope(S.reconciliation, role, sc);
        const ov = JSON.parse(JSON.stringify(S.overview));
        const cv = rows.reduce((t, r) => t + r.claimed * r.rate, 0), ce = rows.reduce((t, r) => t + r.certifiable * r.rate, 0);
        ov.kpis.claimed_value = +cv.toFixed(2); ov.kpis.certifiable_value = +ce.toFixed(2); ov.kpis.at_risk_value = +(cv - ce).toFixed(2);
        const bs = { MATCHED: 0, WITHIN_TOLERANCE: 0, DISCREPANCY: 0, UNVERIFIABLE: 0 }; rows.forEach((r) => { if (r.claimed > 0) bs[r.status]++; });
        ov.kpis.rows_by_status = bs; return json(ov);
      }
      if (p === '/api/reconciliation') {
        let rows = withState(scope(S.reconciliation, role, sc));
        for (const [k, f] of [['subcontractor', 'subcontractor_id'], ['status', 'status'], ['activity', 'activity_code'], ['section', 'section_id']]) if (q[k]) rows = rows.filter((r) => r[f] === q[k]);
        return json({ rows });
      }
      if (p === '/api/production') return json({ ...S.production, rows: scope(S.production.rows, role, sc) });
      if (p === '/api/alerts') {
        let al = alertsWithState(scope(S.alerts, role, sc));
        for (const [k, f] of [['status', 'status'], ['rule', 'rule_id'], ['severity', 'severity'], ['subcontractor', 'subcontractor_id']]) if (q[k]) al = al.filter((a) => a[f] === q[k]);
        return json({ alerts: al });
      }
      if (p === '/api/scorecard') return json({ ...S.scorecard, rows: scope(S.scorecard.rows, role, sc) });
      if (p === '/api/presence') return json({ ...S.presence, fronts: scope(S.presence.fronts, role, sc), equipment: scope(S.presence.equipment, role, sc) });
      if (p === '/api/audit') return role === 'SC' ? json({ detail: 'audit log not available to subcontractors' }, 403) : json({ events: audit.filter((e) => (!q.entity || e.entity === q.entity) && (!q.entity_id || e.entity_id === q.entity_id)) });
      if (p === '/api/field-reports') return json({ reports });
      let m = p.match(/^\/api\/sections\/([^/]+)$/);
      if (m) {
        const sid = decodeURIComponent(m[1]); const x = S.sections[sid];
        if (!x) return json({ detail: 'unknown section' }, 404);
        return json({ ...x, rows: withState(scope(S.reconciliation.filter((r) => r.section_id === sid), role, sc)), alerts: alertsWithState(scope(S.alerts.filter((a) => a.section_id === sid), role, sc)), audit: audit.filter((e) => (e.detail || '').includes(sid)) });
      }
      m = p.match(/^\/api\/certificate\/([^/]+?)(\.csv)?$/);
      if (m) {
        const sub = decodeURIComponent(m[1]);
        if (role === 'SC' && sub !== sc) return json({ detail: 'subcontractors can only see their own certificate' }, 403);
        const c = JSON.parse(JSON.stringify(S.certificate[sub] || { lines: [] }));
        c.lines.forEach((l) => { if (certOverride[l.key] != null) { l.cum_certified = certOverride[l.key]; l.this_period = +(l.cum_certified - l.prev_certified).toFixed(1); l.amount = +(l.this_period * l.rate).toFixed(2); } });
        c.total_this_period = +c.lines.reduce((t, l) => t + l.amount, 0).toFixed(2);
        if (!m[2]) return json(c);
        const cols = ['key', 'boq_item_id', 'activity_code', 'section_id', 'unit', 'cum_certified', 'prev_certified', 'this_period', 'rate', 'amount'];
        const csv = `# SYNTHETIC certificate draft ${sub} period_to ${date}\n` + cols.join(',') + '\n' + c.lines.map((l) => cols.map((k) => l[k]).join(',')).join('\n') + '\n';
        return new Response(csv, { status: 200, headers: { 'Content-Type': 'text/csv' } });
      }
      return json({ detail: 'not available in the stand-alone demo' }, 404);
    }
    const body = init.body ? JSON.parse(init.body) : {};
    if (p === '/api/certify') {
      if (!['QS', 'CM'].includes(role)) return json({ detail: 'only QS or CM may certify' }, 403);
      const row = S.reconciliation.find((r) => r.key === body.key);
      if (!row) return json({ detail: 'unknown reconciliation key' }, 404);
      const qty = Number(body.qty_certified);
      if (!(qty >= 0)) return json({ detail: 'qty_certified must be >= 0' }, 422);
      if (qty > row.cap + 1e-6) {
        if (!body.reason_code) return json({ error: 'ABOVE_CAP', cap: row.cap, status: row.status }, 409);
        if (!(body.comment || '').trim()) return json({ detail: 'comment required for an override above cap' }, 422);
      }
      certOverride[row.key] = qty;
      addAudit(role, 'certification', row.key, body.reason_code ? 'CERTIFY_OVERRIDE' : 'CERTIFY', `${row.section_id} ${row.activity_code}: ${row.certified} -> ${qty} ${row.unit} (cap ${row.cap})${body.reason_code ? ' reason ' + body.reason_code : ''}`);
      return json({ ...row, certified: qty });
    }
    let m = p.match(/^\/api\/alerts\/([^/]+)\/status$/);
    if (m) {
      if (['SC', 'AUD', 'FM'].includes(role)) return json({ detail: 'role not allowed to change alert status' }, 403);
      const a = S.alerts.find((x) => x.alert_id === m[1]);
      if (!a) return json({ detail: 'unknown alert' }, 404);
      alertState[a.alert_id] = { status: body.status, comment: body.comment };
      addAudit(role, 'alert', a.alert_id, `STATUS_${body.status}`, `${a.rule_id} -> ${body.status}: ${body.comment || ''}`);
      return json({ ...a, ...alertState[a.alert_id] });
    }
    if (p === '/api/field-reports') {
      if (!body.lines || !body.lines.length) return json({ detail: 'at least one line required' }, 422);
      if (body.lines.some((l) => !(Number(l.kp_to_m) > Number(l.kp_from_m)))) return json({ detail: 'kp_to_m must be greater than kp_from_m' }, 422);
      const dup = reports.find((r) => r.client_uuid === body.client_uuid);
      if (dup) return json({ report_id: dup.report_id, status: 'RECEIVED', duplicate: true }, 200);
      const rid = 'FR-DEMO-' + (reports.length + 1);
      reports.push({ ...body, report_id: rid });
      addAudit(role, 'field_report', rid, 'CREATE', `${body.crew_id} ${body.report_date}`);
      return json({ report_id: rid, status: 'RECEIVED', duplicate: false }, 201);
    }
    return json({ detail: 'not available in the stand-alone demo' }, 404);
  };
})();
"""

BANNER = ('<div style="background:#5b2a86;color:#fff;font:600 13px system-ui;padding:6px 12px;text-align:center">'
          'STAND-ALONE DEMO · SYNTHETIC DATA · runs in the browser only, nothing is sent anywhere · '
          'changes are kept in memory until the page is reloaded</div>')


def _inline(html: str, data_b64: str, page_js: str) -> str:
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    html = re.sub(r'<link rel="manifest"[^>]*>\s*', "", html)
    html = html.replace('<link rel="stylesheet" href="styles.css">', f"<style>{css}</style>")
    if 'vendor/leaflet/leaflet.css' in html:
        html = html.replace('<link rel="stylesheet" href="vendor/leaflet/leaflet.css">',
                            f"<style>{(WEB / 'vendor/leaflet/leaflet.css').read_text(encoding='utf-8')}</style>")
        html = html.replace('<script src="vendor/leaflet/leaflet.js"></script>',
                            f"<script>{(WEB / 'vendor/leaflet/leaflet.js').read_text(encoding='utf-8')}</script>")
        html = html.replace('<script src="vendor/chartjs/chart.umd.min.js"></script>',
                            f"<script>{(WEB / 'vendor/chartjs/chart.umd.min.js').read_text(encoding='utf-8')}</script>")
    page_js = page_js.replace("navigator.serviceWorker.register('sw.js')", "Promise.reject()")
    page_js = page_js.replace("location.href='index.html'", f"location.href='{DASH}'")
    tail = (f'<script id="siteops-data" type="application/octet-stream">{data_b64}</script>\n'
            f"<script>{SHIM}</script>\n"
            f'<script type="module">await window.__SITEOPS_READY__;\n{page_js}\n</script>')
    html = re.sub(r'<script type="module" src="[^"]+"></script>', lambda _: tail, html)
    html = html.replace("index.html", DASH).replace('href="field.html"', f'href="{FIELD}"')
    return html.replace("<body>", "<body>" + BANNER, 1)


def build(out_dir: Path = DIST, db_path=None) -> list[Path]:
    data = capture(db_path)
    raw = json.dumps(data, separators=(",", ":")).encode()
    b64 = base64.b64encode(gzip.compress(raw, 9)).decode()
    out_dir.mkdir(parents=True, exist_ok=True)
    outs = []
    for src, js, name in [("index.html", "app.js", DASH), ("field.html", "field.js", FIELD)]:
        html = _inline((WEB / src).read_text(encoding="utf-8"), b64, (WEB / js).read_text(encoding="utf-8"))
        p = out_dir / name
        p.write_text(html, encoding="utf-8")
        outs.append(p)
    print(f"raw JSON {len(raw) / 1e6:.1f} MB -> embedded {len(b64) / 1e6:.1f} MB; dates {len(data['dates'])}")
    return outs


if __name__ == "__main__":
    for p in build():
        print(p, f"{p.stat().st_size / 1e6:.1f} MB")
