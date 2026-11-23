// SiteOps Twin MVP: desktop commercial dashboard (screens S1–S8).
// The data shown is SYNTHETIC. This file is built against prototype/API_CONTRACT.md v1.

const STATUS = {
  MATCHED: { icon: '✔', label: 'Matched' },
  WITHIN_TOLERANCE: { icon: '≈', label: 'Within tol.' },
  DISCREPANCY: { icon: '▲', label: 'Discrepancy' },
  UNVERIFIABLE: { icon: '?', label: 'Unverifiable' },
  OK: { icon: '✔', label: 'OK' },
  OVERCLAIM: { icon: '▲', label: 'Overclaim' },
  NO_SIGNAL: { icon: '⊘', label: 'No signal' },
  NO_DATA: { icon: '⊘', label: 'No data' },
};
const STATUS_COLOR = { MATCHED: '#009E73', WITHIN_TOLERANCE: '#56B4E9', DISCREPANCY: '#D55E00', UNVERIFIABLE: '#7F7F7F' };
const SEV = { HIGH: '▲▲ High', MED: '▲ Medium', LOW: '● Low' };
const EXCEPTION_ORDER = { DISCREPANCY: 0, UNVERIFIABLE: 1, WITHIN_TOLERANCE: 2, MATCHED: 3 };

const state = { meta: null, date: null, role: 'CM', sc: null, currency: 'SYN¤', recoRows: [], chart: null, map: null };
const $ = (sel, root = document) => root.querySelector(sel);
const view = $('#view');

// ---------- helpers ----------
function esc(v) {
  return String(v ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
function kp(m) {
  if (m == null || isNaN(m)) return '';
  const km = Math.floor(m / 1000), r = Math.round(m - km * 1000);
  return `KP ${String(km).padStart(3, '0')}+${String(r).padStart(3, '0')}`;
}
function num(v, d = 0) {
  if (v == null || v === '' || isNaN(v)) return '–';
  return Number(v).toLocaleString('en-GB', { minimumFractionDigits: d, maximumFractionDigits: d });
}
function money(v) { return v == null ? '–' : `${num(v, 0)} ${esc(state.currency)}`; }
function pct(v, d = 1) { return v == null || isNaN(v) ? '–' : `${(v * 100).toFixed(d)}%`; }
function statusChip(s) {
  const st = STATUS[s] || { icon: '', label: s || '–' };
  return `<span class="status ${esc(s)}"><span aria-hidden="true">${st.icon}</span>${esc(st.label)}</span>`;
}
function sevChip(s) { return `<span class="sev ${esc(s)}">${esc(SEV[s] || s)}</span>`; }
function loading(msg = 'Loading…') { return `<div class="state" role="status">${esc(msg)}</div>`; }
function errorBox(err) { return `<div class="state error" role="alert">Could not load data: ${esc(err.message || err)}</div>`; }
function empty(msg = 'No records for this selection.') { return `<div class="state">${esc(msg)}</div>`; }
function qs(params) {
  const p = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => { if (v != null && v !== '') p.set(k, v); });
  const s = p.toString();
  return s ? `?${s}` : '';
}

function headers(extra = {}) {
  const h = { 'X-Role': state.role, ...extra };
  if (state.role === 'SC' && state.sc) h['X-Subcontractor'] = state.sc;
  return h;
}
async function api(path, opts = {}) {
  const res = await fetch(path, { ...opts, headers: headers(opts.headers || {}) });
  let body = null;
  const text = await res.text();
  try { body = text ? JSON.parse(text) : null; } catch { body = { raw: text }; }
  if (!res.ok) {
    const e = new Error((body && (body.error || body.detail && JSON.stringify(body.detail))) || `HTTP ${res.status}`);
    e.status = res.status; e.body = body;
    throw e;
  }
  return body;
}
const post = (path, data) => api(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });

function options(list, valueKey, labelFn, selected, allLabel) {
  const opts = allLabel != null ? [`<option value="">${esc(allLabel)}</option>`] : [];
  list.forEach((x) => {
    const v = typeof x === 'string' ? x : x[valueKey];
    const l = labelFn ? labelFn(x) : v;
    opts.push(`<option value="${esc(v)}"${v === selected ? ' selected' : ''}>${esc(l)}</option>`);
  });
  return opts.join('');
}

// ---------- init ----------
async function init() {
  try {
    try { state.role = localStorage.getItem('siteops.role') || 'CM'; state.sc = localStorage.getItem('siteops.sc'); } catch { /* storage unavailable */ }
    view.innerHTML = loading('Loading project metadata…');
    state.meta = await api('/api/meta');
    const m = state.meta;
    $('#spreadLabel').textContent = `${m.spread.spread_id} · ${kp(m.spread.kp_start_m)} – ${kp(m.spread.kp_end_m)}`;
    const dp = $('#datePick');
    dp.min = m.date_min; dp.max = m.date_max; dp.value = m.default_date || m.date_max;
    state.date = dp.value;
    $('#rolePick').value = state.role;
    $('#scPick').innerHTML = options(m.subcontractors, 'subcontractor_id', (s) => s.subcontractor_id, state.sc);
    if (!state.sc && m.subcontractors.length) state.sc = m.subcontractors[0].subcontractor_id;
    $('#scWrap').hidden = state.role !== 'SC';
  } catch (e) {
    view.innerHTML = errorBox(e) + '<p class="note">Is the backend running? Start it with <code>uvicorn siteops.api:app</code> from <code>prototype/</code>.</p>';
    return;
  }
  $('#datePick').addEventListener('change', (e) => { state.date = e.target.value; route(); });
  $('#rolePick').addEventListener('change', (e) => {
    state.role = e.target.value; $('#scWrap').hidden = state.role !== 'SC';
    try { localStorage.setItem('siteops.role', state.role); } catch { /* ignore */ }
    route();
  });
  $('#scPick').addEventListener('change', (e) => {
    state.sc = e.target.value;
    try { localStorage.setItem('siteops.sc', state.sc); } catch { /* ignore */ }
    route();
  });
  window.addEventListener('hashchange', route);
  setupDialogs();
  route();
}

function route() {
  const hash = location.hash.replace(/^#/, '') || 'overview';
  const [page, arg] = hash.split('/');
  document.querySelectorAll('nav.tabs a').forEach((a) => {
    if (a.getAttribute('href') === `#${page}`) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
  });
  if (state.chart) { state.chart.destroy(); state.chart = null; }
  if (state.map) { state.map.remove(); state.map = null; }
  const pages = { overview, production, reconciliation, scorecard, alerts, section, certificate, presence, dailyreport };
  (pages[page] || overview)(arg ? decodeURIComponent(arg) : undefined);
}

// ---------- S1 Overview ----------
async function overview() {
  view.innerHTML = `<h2>S1 Spread overview <span class="muted">· ${esc(state.date)}</span></h2>${loading()}`;
  try {
    const [ov, geo] = await Promise.all([api(`/api/overview${qs({ date: state.date })}`), api('/api/geometry').catch(() => null)]);
    if (ov.currency) state.currency = ov.currency;
    const k = ov.kpis || {};
    const rs = k.rows_by_status || {}, oa = k.open_alerts || {};
    const tiles = `
      <div class="tiles">
        <div class="tile"><div class="label">Claimed value (cum.)</div><div class="value">${money(k.claimed_value)}</div></div>
        <div class="tile"><div class="label">Certifiable value</div><div class="value">${money(k.certifiable_value)}</div><div class="sub">within measured + U + T</div></div>
        <div class="tile"><div class="label">At-risk value</div><div class="value neg">${money(k.at_risk_value)}</div><div class="sub">claimed above cap</div></div>
        <div class="tile"><div class="label">Rows by status</div><div class="sub">
          ${['DISCREPANCY', 'UNVERIFIABLE', 'WITHIN_TOLERANCE', 'MATCHED'].map((s) => `${statusChip(s)} ${num(rs[s])}`).join('<br>')}</div></div>
        <div class="tile"><div class="label">Open alerts</div><div class="sub">
          ${['HIGH', 'MED', 'LOW'].map((s) => `${sevChip(s)} ${num(oa[s])}`).join('<br>')}</div>
          <div class="sub"><a href="#alerts">Open the alerts inbox</a></div></div>
        <div class="tile"><div class="label">Field reports</div><div class="value">${num(k.reports_received)} / ${num(k.reports_expected)}</div><div class="sub">received / expected today</div></div>
        <div class="tile"><div class="label">Headcount</div><div class="value">${num(k.headcount_claimed)} <span class="muted" style="font-size:14px">claimed</span></div>
          <div class="sub">${num(k.headcount_sensed)} sensed (check-in/manifest) · <a href="#presence">presence</a></div></div>
      </div>`;
    const secs = ov.sections || [];
    const strip = secs.length ? `
      <div class="kpstrip" role="list" aria-label="Sections along the KP, worst reconciliation status">
        ${secs.map((s) => {
          const st = STATUS[s.worst_status] || { icon: '', label: s.worst_status || 'No data' };
          const prog = Object.entries(s.progress || {});
          return `<button class="kpcell" role="listitem" data-sec="${esc(s.section_id)}"
              title="${esc(s.section_id)} ${kp(s.kp_from_m)}–${kp(s.kp_to_m)}: ${esc(st.label)}, ${num(s.open_alerts)} open alerts"
              aria-label="${esc(s.section_id)} ${esc(st.label)}, ${num(s.open_alerts)} open alerts">
            <div class="sid">${esc(s.section_id)}</div>
            <div class="bar ${esc(s.worst_status)}"></div>
            <div class="icon" aria-hidden="true">${st.icon}</div>
            <div class="sid">${s.open_alerts ? `▲${num(s.open_alerts)}` : '&nbsp;'}</div>
            <div class="mini" aria-hidden="true">${prog.map(([a, p]) => `<span title="${esc(a)} ${pct(p, 0)}"><i style="width:${Math.max(0, Math.min(1, p)) * 100}%"></i></span>`).join('')}</div>
          </button>`;
        }).join('')}
      </div>
      <div class="kplabels"><span>${kp(secs[0].kp_from_m)}</span><span>${kp(secs[secs.length - 1].kp_to_m)}</span></div>
      <div class="legend">${['MATCHED', 'WITHIN_TOLERANCE', 'DISCREPANCY', 'UNVERIFIABLE'].map(statusChip).join('')}
        <span class="muted">Mini-bars: cumulative progress per activity (reported ÷ planned)</span></div>` : empty('No sections.');
    view.innerHTML = `<h2>S1 Spread overview <span class="muted">· ${esc(state.date)}</span></h2>${tiles}
      <div class="panel"><h3>KP strip: worst status per section (select one to open its detail)</h3>${strip}</div>
      <div class="panel"><h3 id="mapTitle">Map (local synthetic coordinates, not real geography)</h3><div id="map" role="img" aria-label="Map of the synthetic spread centreline, sections and work fronts"></div></div>`;
    view.querySelectorAll('.kpcell').forEach((b) => b.addEventListener('click', () => { location.hash = `section/${encodeURIComponent(b.dataset.sec)}`; }));
    drawMap(geo, secs);
  } catch (e) { view.innerHTML = `<h2>S1 Spread overview</h2>${errorBox(e)}`; }
}

function drawMap(geo, secs) {
  const el = $('#map');
  if (!el) return;
  if (!geo || !window.L) { el.innerHTML = empty('Map not available (geometry or Leaflet failed to load).'); return; }
  const statusBySec = Object.fromEntries((secs || []).map((s) => [s.section_id, s.worst_status]));
  const real = geo.crs === 'EPSG:4326';
  let map;
  if (real) {
    // Real project route (lon/lat). Basemap tiles load from the internet; the route still shows offline.
    map = L.map(el, { minZoom: 8, maxZoom: 19 });
    const osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '© OpenStreetMap contributors' });
    const sat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 19, attribution: 'Tiles © Esri' });
    osm.addTo(map);
    L.control.layers({ 'Map (OpenStreetMap)': osm, 'Aerial (Esri)': sat }, null, { collapsed: false }).addTo(map);
    const t = $('#mapTitle');
    if (t) t.textContent = geo.title || 'Map: real project route (synthetic data positioned along it)';
  } else {
    map = L.map(el, { crs: L.CRS.Simple, minZoom: -6, attributionControl: false });
  }
  state.map = map;
  // Synthetic: GeoJSON [x, y] metres with CRS.Simple (lat = y, lng = x). Real: [lon, lat].
  const layer = L.geoJSON(geo, {
    coordsToLatLng: (c) => L.latLng(c[1], c[0]),
    style: (f) => {
      const p = f.properties || {};
      if (p.kind === 'section') return { color: STATUS_COLOR[statusBySec[p.section_id]] || '#7F7F7F', weight: 7, opacity: 0.9, dashArray: statusBySec[p.section_id] === 'UNVERIFIABLE' ? '6 6' : null };
      return { color: '#4a5360', weight: 2, opacity: 0.6 };
    },
    pointToLayer: (f, latlng) => L.circleMarker(latlng, { radius: 6, color: '#1b1f24', weight: 2, fillColor: '#ffffff', fillOpacity: 1 }),
    onEachFeature: (f, lyr) => {
      const p = f.properties || {};
      if (p.kind === 'section') {
        const st = STATUS[statusBySec[p.section_id]];
        lyr.bindTooltip(`${p.section_id} · ${kp(p.kp_from_m)}–${kp(p.kp_to_m)} · ${st ? st.icon + ' ' + st.label : 'No data'}`);
        lyr.on('click', () => { location.hash = `section/${encodeURIComponent(p.section_id)}`; });
      } else if (p.kind === 'front') {
        lyr.bindTooltip(`${p.front_id} (${p.type || ''})`);
      } else if (p.kind === 'poi') {
        lyr.setStyle && lyr.setStyle({ radius: 4, color: '#5b2a86', fillColor: '#d9c6ee' });
        lyr.bindTooltip(esc(p.name || ''));
      }
    },
  }).addTo(map);
  try { map.fitBounds(layer.getBounds(), { padding: [20, 20] }); } catch { if (!real) map.setView([0, 0], -4); }
}

// ---------- S2 Production ----------
async function production() {
  view.innerHTML = `<h2>S2 Daily production <span class="muted">· ${esc(state.date)}</span></h2>${loading()}`;
  try {
    const d = await api(`/api/production${qs({ date: state.date })}`);
    const rows = d.rows || [];
    const body = rows.length ? `<div class="tablewrap"><table>
      <thead><tr><th>Crew</th><th>Subcontractor</th><th>Activity</th><th>KP range</th><th class="num">Qty</th><th>Unit</th>
      <th class="num">Hours</th><th class="num">Headcount</th><th class="num">Productivity</th><th class="num">5-day median</th>
      <th class="num">Δ vs median</th><th>Weather</th><th>Report</th></tr></thead><tbody>
      ${rows.map((r) => {
        const slow = r.delta_pct != null && r.delta_pct <= -(state.meta.config?.al05_drop ?? 0.25);
        return `<tr class="${slow ? 'flag' : ''}"><td>${esc(r.crew_id)}</td><td>${esc(r.subcontractor_id)}</td><td>${esc(r.activity_code)}</td>
          <td>${kp(r.kp_from_m)}–${kp(r.kp_to_m)}</td><td class="num">${num(r.qty, 1)}</td><td>${esc(r.unit)}</td>
          <td class="num">${num(r.hours, 1)}</td><td class="num">${num(r.headcount)}</td><td class="num">${num(r.productivity, 2)}</td>
          <td class="num">${num(r.median5, 2)}</td>
          <td class="num ${slow ? 'neg' : ''}">${slow ? '▼ ' : ''}${pct(r.delta_pct, 0)}</td>
          <td>${esc(r.weather || '–')}</td><td>${r.report_received ? '✔ Received' : '<span class="neg">✕ Missing</span>'}</td></tr>`;
      }).join('')}</tbody></table></div>
      <p class="note">Rows highlighted ▼ have productivity ≥ ${pct(state.meta.config?.al05_drop ?? 0.25, 0)} below the crew's 5-day median (rule AL-05; excluded when the weather was not workable).</p>`
      : empty('No production reported for this date.');
    view.innerHTML = `<h2>S2 Daily production <span class="muted">· ${esc(state.date)}</span></h2><div class="panel">${body}</div>`;
  } catch (e) { view.innerHTML = `<h2>S2 Daily production</h2>${errorBox(e)}`; }
}

// ---------- S3 Reconciliation workbench ----------
const recoFilter = { subcontractor: '', status: '', activity: '', section: '' };
function recoTable(rows, { certify = true } = {}) {
  if (!rows.length) return empty('No reconciliation rows match the filters.');
  const canCert = certify && ['QS', 'CM'].includes(state.role);
  return `<div class="tablewrap"><table>
    <thead><tr><th>Section / plan sheets</th><th>Activity</th><th>Subcontractor</th><th>Unit</th><th class="num">Planned</th><th class="num">Reported</th>
    <th class="num">Measured ± U</th><th class="num">Claimed</th><th class="num">Certified</th><th class="num">Invoiced</th>
    <th class="num">Cap (M+U+T)</th><th class="num">Diff</th><th>Status</th><th>Source</th><th>Alerts</th>${canCert ? '<th>Action</th>' : ''}</tr></thead><tbody>
    ${rows.map((r) => `<tr>
      <td><a href="#section/${encodeURIComponent(r.section_id)}">${esc(r.section_id)}</a>${r.plan_sheets ? `<br><span class="muted">${esc(r.plan_sheets)}</span>` : ''}</td><td>${esc(r.activity_code)}</td><td>${esc(r.subcontractor_id)}</td><td>${esc(r.unit)}</td>
      <td class="num">${num(r.planned, 1)}</td><td class="num">${num(r.reported, 1)}</td>
      <td class="num">${r.measured == null ? '–' : `${num(r.measured, 1)} ± ${num(r.u, 1)}`}</td>
      <td class="num">${num(r.claimed, 1)}${r.pending > 0 ? `<br><span class="muted">${num(r.pending, 1)} pending</span>` : ''}</td><td class="num">${num(r.certified, 1)}${r.over_certified > 0 ? `<br><span class="neg">${num(r.over_certified, 1)} over cap</span>` : ''}</td><td class="num">${num(r.invoiced, 1)}</td>
      <td class="num">${num(r.cap, 1)}</td>
      <td class="num ${r.status === 'DISCREPANCY' ? 'neg' : ''}">${num(r.diff, 1)}${r.diff_pct != null ? ` (${pct(r.diff_pct)})` : ''}</td>
      <td>${statusChip(r.status)}</td><td>${esc(r.verification_source || '')}${r.last_flight ? `<br><span class="muted">${r.verification_source === 'UAV' ? 'flight' : 'measured'} ${esc(r.last_flight)}</span>` : ''}</td>
      <td>${(r.alerts || []).map(esc).join(', ') || '–'}</td>
      ${canCert ? `<td><button data-key="${esc(r.key)}" class="certBtn">Certify</button></td>` : ''}</tr>`).join('')}
    </tbody></table></div>`;
}
function bindCertButtons(root, rows, after) {
  root.querySelectorAll('.certBtn').forEach((b) => b.addEventListener('click', () => {
    const row = rows.find((r) => r.key === b.dataset.key);
    if (row) openCertify(row, after);
  }));
}
async function reconciliation() {
  const m = state.meta;
  const filters = `<div class="filters">
    <label>Subcontractor <select id="fSc">${options(m.subcontractors, 'subcontractor_id', null, recoFilter.subcontractor, 'All')}</select></label>
    <label>Status <select id="fSt">${options(Object.keys(EXCEPTION_ORDER), null, (s) => STATUS[s].label, recoFilter.status, 'All')}</select></label>
    <label>Activity <select id="fAc">${options(m.activities, 'activity_code', (a) => `${a.activity_code} · ${a.name}`, recoFilter.activity, 'All')}</select></label>
    <label>Section <select id="fSe">${options(m.sections, 'section_id', null, recoFilter.section, 'All')}</select></label>
  </div>`;
  view.innerHTML = `<h2>S3 Reconciliation workbench <span class="muted">· cumulative to ${esc(state.date)}</span></h2>${filters}<div id="recoBody">${loading()}</div>`;
  [['#fSc', 'subcontractor'], ['#fSt', 'status'], ['#fAc', 'activity'], ['#fSe', 'section']].forEach(([id, k]) => {
    $(id).addEventListener('change', (e) => { recoFilter[k] = e.target.value; loadReco(); });
  });
  loadReco();
}
async function loadReco() {
  const box = $('#recoBody');
  if (!box) return;
  box.innerHTML = loading();
  try {
    const d = await api(`/api/reconciliation${qs({ date: state.date, ...recoFilter })}`);
    const rows = (d.rows || []).slice().sort((a, b) => (EXCEPTION_ORDER[a.status] ?? 9) - (EXCEPTION_ORDER[b.status] ?? 9) || Math.abs(b.diff || 0) - Math.abs(a.diff || 0));
    state.recoRows = rows;
    box.innerHTML = `<p class="muted">${num(rows.length)} rows · exceptions first (Discrepancy, then Unverifiable)</p>${recoTable(rows)}`;
    bindCertButtons(box, rows, loadReco);
  } catch (e) { box.innerHTML = errorBox(e); }
}

// ---------- Certify dialog ----------
let certCtx = null;
function setupDialogs() {
  const dlg = $('#certDialog');
  $('#certCancel').addEventListener('click', () => dlg.close());
  $('#certForm').addEventListener('submit', async (ev) => {
    ev.preventDefault();
    if (!certCtx) return;
    const qty = parseFloat($('#certQty').value);
    const reason = $('#certReason').value || null;
    const comment = $('#certComment').value.trim();
    const msg = $('#certMsg');
    if (isNaN(qty) || qty < 0) { msg.className = 'msg err'; msg.textContent = 'Enter a quantity of 0 or more.'; return; }
    if (!$('#reasonWrap').hidden && (!reason || !comment)) { msg.className = 'msg err'; msg.textContent = 'Above the cap: a reason code and a comment are required.'; return; }
    $('#certSubmit').disabled = true;
    try {
      await post('/api/certify', { key: certCtx.row.key, qty_certified: qty, reason_code: reason, comment });
      dlg.close();
      if (certCtx.after) certCtx.after();
    } catch (e) {
      if (e.status === 409 && e.body && e.body.error === 'ABOVE_CAP') {
        $('#reasonWrap').hidden = false;
        msg.className = 'msg err';
        msg.textContent = `Above the certifiable cap of ${num(e.body.cap, 1)}. Select an override reason and add a comment, then certify again.`;
      } else {
        msg.className = 'msg err'; msg.textContent = `Certification failed: ${e.message}`;
      }
    } finally { $('#certSubmit').disabled = false; }
  });

  const adlg = $('#alertDialog');
  $('#alertCancel').addEventListener('click', () => adlg.close());
  $('#alertForm').addEventListener('submit', async (ev) => {
    ev.preventDefault();
    if (!alertCtx) return;
    const comment = $('#alertComment').value.trim();
    if (!comment) { $('#alertMsg').className = 'msg err'; $('#alertMsg').textContent = 'A comment is required.'; return; }
    $('#alertSubmit').disabled = true;
    try {
      await post(`/api/alerts/${encodeURIComponent(alertCtx.id)}/status`, { status: alertCtx.status, comment });
      adlg.close();
      if (alertCtx.after) alertCtx.after();
    } catch (e) { $('#alertMsg').className = 'msg err'; $('#alertMsg').textContent = `Update failed: ${e.message}`; }
    finally { $('#alertSubmit').disabled = false; }
  });
}
function openCertify(row, after) {
  certCtx = { row, after };
  $('#certInfo').innerHTML = `<strong>${esc(row.section_id)} · ${esc(row.activity_code)} · ${esc(row.subcontractor_id)}</strong><br>
    Claimed ${num(row.claimed, 1)} ${esc(row.unit)} · Measured ${row.measured == null ? '–' : `${num(row.measured, 1)} ± ${num(row.u, 1)}`} · Tolerance ${num(row.tol, 1)}<br>
    Certifiable cap without override: <strong>${num(row.cap, 1)} ${esc(row.unit)}</strong> ${statusChip(row.status)}`;
  const suggested = row.cap != null && row.claimed != null ? Math.min(row.claimed, row.cap) : (row.claimed ?? 0);
  $('#certQty').value = suggested;
  $('#certReason').value = ''; $('#certComment').value = '';
  $('#reasonWrap').hidden = true;
  $('#certMsg').textContent = ''; $('#certMsg').className = 'msg';
  $('#certDialog').showModal();
}

// ---------- S4 Scorecard ----------
async function scorecard() {
  view.innerHTML = `<h2>S4 Subcontractor scorecard <span class="muted">· ${esc(state.date)}</span></h2>${loading()}`;
  try {
    const d = await api(`/api/scorecard${qs({ date: state.date })}`);
    const rows = d.rows || [];
    if (!rows.length) { view.innerHTML = `<h2>S4 Subcontractor scorecard</h2>${empty()}`; return; }
    view.innerHTML = `<h2>S4 Subcontractor scorecard <span class="muted">· ${esc(state.date)}</span></h2>
      <div class="grid2"><div class="panel tablewrap"><table>
        <thead><tr><th>Subcontractor</th><th class="num">Claimed value</th><th class="num">Certifiable</th><th class="num">Over-claim</th>
        <th class="num">Discrepancy rows</th><th>Alerts by rule</th><th class="num">Headcount over-claim days</th><th class="num">Equipment over-claim h</th><th class="num">Reports on time</th></tr></thead>
        <tbody>${rows.map((r) => `<tr><td>${esc(r.subcontractor_id)}</td><td class="num">${money(r.claimed_value)}</td><td class="num">${money(r.certifiable_value)}</td>
          <td class="num ${r.overclaim_pct > 0.05 ? 'neg' : ''}">${pct(r.overclaim_pct)}</td><td class="num">${num(r.rows_discrepancy)}</td>
          <td>${Object.entries(r.alerts_by_rule || {}).map(([k, v]) => `${esc(k)}: ${num(v)}`).join(' · ') || '–'}</td>
          <td class="num">${num(r.headcount_overclaim_days)}</td><td class="num">${num(r.equipment_overclaim_h, 1)}</td><td class="num">${pct(r.reports_on_time_pct, 0)}</td></tr>`).join('')}</tbody>
      </table></div>
      <div class="panel"><h3>Claimed vs certifiable value (${esc(state.currency)})</h3><canvas id="scChart" role="img" aria-label="Bar chart of claimed versus certifiable value per subcontractor"></canvas></div></div>`;
    if (window.Chart) {
      state.chart = new Chart($('#scChart'), {
        type: 'bar',
        data: {
          labels: rows.map((r) => r.subcontractor_id),
          datasets: [
            { label: 'Claimed', data: rows.map((r) => r.claimed_value), backgroundColor: '#D55E00' },
            { label: 'Certifiable', data: rows.map((r) => r.certifiable_value), backgroundColor: '#009E73' },
          ],
        },
        options: { responsive: true, plugins: { legend: { position: 'bottom' } }, scales: { y: { beginAtZero: true } } },
      });
    }
  } catch (e) { view.innerHTML = `<h2>S4 Subcontractor scorecard</h2>${errorBox(e)}`; }
}

// ---------- S5 Alerts ----------
const alertFilter = { status: 'OPEN', rule: '', severity: '', subcontractor: '' };
let alertCtx = null;
function alertTable(list, withActions = true) {
  if (!list.length) return empty('No alerts match the filters.');
  const canAct = withActions && state.role !== 'AUD' && state.role !== 'SC';
  return `<div class="tablewrap"><table>
    <thead><tr><th>Severity</th><th>Rule</th><th>Date</th><th>Where</th><th>Who</th><th>Alert</th><th>Status</th>${canAct ? '<th>Action</th>' : ''}</tr></thead>
    <tbody>${list.map((a) => `<tr>
      <td>${sevChip(a.severity)}</td><td>${esc(a.rule_id)}</td><td>${esc(a.work_date)}</td>
      <td>${a.section_id ? `<a href="#section/${encodeURIComponent(a.section_id)}">${esc(a.section_id)}</a>` : ''}${a.front_id ? ` · ${esc(a.front_id)}` : ''}${a.activity_code ? ` · ${esc(a.activity_code)}` : ''}</td>
      <td>${[a.subcontractor_id, a.crew_id, a.equipment_id].filter(Boolean).map(esc).join('<br>')}</td>
      <td><strong>${esc(a.title)}</strong><br><span class="muted">${esc(a.explanation)}</span></td><td>${esc(a.status)}</td>
      ${canAct ? `<td>${a.status === 'OPEN' ? `<button class="alBtn" data-id="${esc(a.alert_id)}" data-st="ACK">Ack</button> ` : ''}${a.status !== 'CLOSED' ? `<button class="alBtn" data-id="${esc(a.alert_id)}" data-st="CLOSED">Close</button>` : ''}</td>` : ''}
    </tr>`).join('')}</tbody></table></div>`;
}
function bindAlertButtons(root, list, after) {
  root.querySelectorAll('.alBtn').forEach((b) => b.addEventListener('click', () => {
    const a = list.find((x) => x.alert_id === b.dataset.id);
    alertCtx = { id: b.dataset.id, status: b.dataset.st, after };
    $('#alertTitle').textContent = b.dataset.st === 'ACK' ? 'Acknowledge alert' : 'Close alert';
    $('#alertInfo').innerHTML = a ? `${sevChip(a.severity)} <strong>${esc(a.rule_id)}</strong> ${esc(a.title)}<br><span class="muted">${esc(a.explanation)}</span>` : '';
    $('#alertComment').value = ''; $('#alertMsg').textContent = '';
    $('#alertDialog').showModal();
  }));
}
async function alerts() {
  const rules = Array.from({ length: 13 }, (_, i) => `AL-${String(i + 1).padStart(2, '0')}`);
  view.innerHTML = `<h2>S5 Alerts inbox</h2>
    <div class="filters">
      <label>Status <select id="aSt">${options(['OPEN', 'ACK', 'CLOSED'], null, null, alertFilter.status, 'All')}</select></label>
      <label>Rule <select id="aRu">${options(rules, null, null, alertFilter.rule, 'All')}</select></label>
      <label>Severity <select id="aSe">${options(['HIGH', 'MED', 'LOW'], null, (s) => SEV[s], alertFilter.severity, 'All')}</select></label>
      <label>Subcontractor <select id="aSc">${options(state.meta.subcontractors, 'subcontractor_id', null, alertFilter.subcontractor, 'All')}</select></label>
    </div><div id="alertBody">${loading()}</div>`;
  [['#aSt', 'status'], ['#aRu', 'rule'], ['#aSe', 'severity'], ['#aSc', 'subcontractor']].forEach(([id, k]) => {
    $(id).addEventListener('change', (e) => { alertFilter[k] = e.target.value; loadAlerts(); });
  });
  loadAlerts();
}
async function loadAlerts() {
  const box = $('#alertBody');
  if (!box) return;
  box.innerHTML = loading();
  try {
    const d = await api(`/api/alerts${qs(alertFilter)}`);
    const order = { HIGH: 0, MED: 1, LOW: 2 };
    const list = (d.alerts || []).slice().sort((a, b) => (order[a.severity] ?? 9) - (order[b.severity] ?? 9) || String(b.work_date).localeCompare(String(a.work_date)));
    box.innerHTML = `<p class="muted">${num(list.length)} alerts</p>${alertTable(list)}`;
    bindAlertButtons(box, list, loadAlerts);
  } catch (e) { box.innerHTML = errorBox(e); }
}

// ---------- S6 Section detail ----------
async function section(id) {
  if (!id) { location.hash = 'overview'; return; }
  view.innerHTML = `<h2>S6 Section ${esc(id)}</h2>${loading()}`;
  const load = async () => {
    try {
      const d = await api(`/api/sections/${encodeURIComponent(id)}${qs({ date: state.date })}`);
      const s = d.section || {};
      const rows = d.rows || [];
      view.innerHTML = `<h2>S6 Section ${esc(s.section_id || id)} <span class="muted">· ${kp(s.kp_from_m)} – ${kp(s.kp_to_m)} · cumulative to ${esc(state.date)}</span></h2>
        <p><a href="#overview">← Back to overview</a></p>
        <div class="panel"><h3>Quantity states per activity</h3><div id="secReco">${recoTable(rows)}</div></div>
        <div class="grid2">
          <div class="panel"><h3>Drone flights (accuracy)</h3>${(d.flights || []).length ? `<div class="tablewrap"><table>
            <thead><tr><th>Flight</th><th>Date</th><th class="num">GSD cm</th><th class="num">RMSE z m</th><th class="num">Check points</th></tr></thead>
            <tbody>${d.flights.map((f) => `<tr><td>${esc(f.flight_id)}</td><td>${esc(f.flight_date)}</td><td class="num">${num(f.gsd_cm, 1)}</td><td class="num">${num(f.rmse_z_m, 3)}</td><td class="num">${num(f.n_checkpoints)}</td></tr>`).join('')}</tbody></table></div>` : empty('No flights cover this section.')}</div>
          <div class="panel"><h3>Independent measurements (± 1σ)</h3>${(d.measurements || []).length ? `<div class="tablewrap"><table>
            <thead><tr><th>Activity</th><th>Method</th><th>KP range</th><th class="num">Qty ± σ</th><th>Flight date</th></tr></thead>
            <tbody>${d.measurements.map((x) => `<tr><td>${esc(x.activity_code)}</td><td>${esc(x.method)}</td><td>${kp(x.kp_from_m)}–${kp(x.kp_to_m)}</td><td class="num">${num(x.qty, 1)} ± ${num(x.sigma, 1)}</td><td>${esc(x.flight_date)}</td></tr>`).join('')}</tbody></table></div>` : empty('No measurements.')}</div>
        </div>
        <div class="panel"><h3>Alerts</h3><div id="secAlerts">${alertTable(d.alerts || [])}</div></div>
        <div class="panel"><h3>Audit history</h3>${(d.audit || []).length ? `<div class="tablewrap"><table>
          <thead><tr><th>Time</th><th>Role</th><th>Entity</th><th>Action</th><th>Detail</th></tr></thead>
          <tbody>${d.audit.map((a) => `<tr><td>${esc(a.ts)}</td><td>${esc(a.actor_role)}</td><td>${esc(a.entity)} ${esc(a.entity_id)}</td><td>${esc(a.action)}</td><td>${esc(a.detail)}</td></tr>`).join('')}</tbody></table></div>` : empty('No audit events yet.')}</div>`;
      bindCertButtons($('#secReco'), rows, load);
      bindAlertButtons($('#secAlerts'), d.alerts || [], load);
    } catch (e) { view.innerHTML = `<h2>S6 Section ${esc(id)}</h2><p><a href="#overview">← Back to overview</a></p>${errorBox(e)}`; }
  };
  load();
}

// ---------- S7 Certificate ----------
let certSc = null;
async function certificate() {
  const m = state.meta;
  if (state.role === 'SC') certSc = state.sc;
  certSc = certSc || (m.subcontractors[0] && m.subcontractors[0].subcontractor_id);
  view.innerHTML = `<h2>S7 Certificate draft <span class="muted">· period to ${esc(state.date)}</span></h2>
    <div class="filters"><label>Subcontractor <select id="cSc" ${state.role === 'SC' ? 'disabled' : ''}>${options(m.subcontractors, 'subcontractor_id', null, certSc)}</select></label>
    <a id="csvLink" class="muted" href="#">Download CSV</a></div><div id="certBody">${loading()}</div>`;
  $('#cSc').addEventListener('change', (e) => { certSc = e.target.value; loadCert(); });
  // The CSV is fetched with the role headers, so RBAC also applies to the export.
  $('#csvLink').addEventListener('click', async (ev) => {
    ev.preventDefault();
    try {
      const res = await fetch(`/api/certificate/${encodeURIComponent(certSc)}.csv${qs({ date: state.date })}`, { headers: headers() });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const blob = await res.blob();
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `SYNTHETIC_certificate_${certSc}_${state.date}.csv`;
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    } catch (e) { $('#certBody').insertAdjacentHTML('afterbegin', errorBox(e)); }
  });
  loadCert();
}
async function loadCert() {
  const box = $('#certBody');
  if (!box || !certSc) return;
  box.innerHTML = loading();
  try {
    const d = await api(`/api/certificate/${encodeURIComponent(certSc)}${qs({ date: state.date })}`);
    if (d.currency) state.currency = d.currency;
    const lines = d.lines || [];
    box.innerHTML = lines.length ? `<div class="panel tablewrap"><table>
      <thead><tr><th>BoQ item</th><th>Activity</th><th>Section</th><th>Unit</th><th class="num">Cum. certified</th><th class="num">Previous</th>
      <th class="num">This period</th><th class="num">Rate</th><th class="num">Amount</th></tr></thead>
      <tbody>${lines.map((l) => `<tr><td>${esc(l.boq_item_id)}</td><td>${esc(l.activity_code)}</td><td>${esc(l.section_id)}</td><td>${esc(l.unit)}</td>
        <td class="num">${num(l.cum_certified, 1)}</td><td class="num">${num(l.prev_certified, 1)}</td><td class="num">${num(l.this_period, 1)}</td>
        <td class="num">${num(l.rate, 2)}</td><td class="num">${money(l.amount)}</td></tr>`).join('')}</tbody>
      <tfoot><tr><th colspan="8">Total this period</th><th class="num">${money(d.total_this_period)}</th></tr></tfoot></table>
      <p class="note">Draft only. The period quantity is the change in the cumulative certified quantity (D-065). Retention, advances, variations and tax are outside the MVP (D-066).</p></div>`
      : empty('Nothing certified for this subcontractor yet. Certify rows in S3 first.');
  } catch (e) { box.innerHTML = errorBox(e); }
}

// ---------- S8 Presence (field sensing) ----------
async function presence() {
  view.innerHTML = `<h2>S8 Presence and equipment verification <span class="muted">· ${esc(state.date)}</span></h2>${loading()}`;
  try {
    const d = await api(`/api/presence${qs({ date: state.date })}`);
    const fronts = d.fronts || [], eq = d.equipment || [];
    const sortSt = { OVERCLAIM: 0, NO_SIGNAL: 1, NO_DATA: 1, OK: 2 };
    fronts.sort((a, b) => (sortSt[a.status] ?? 9) - (sortSt[b.status] ?? 9));
    eq.sort((a, b) => (sortSt[a.status] ?? 9) - (sortSt[b.status] ?? 9));
    view.innerHTML = `<h2>S8 Presence and equipment verification <span class="muted">· ${esc(state.date)}</span></h2>
      <p class="note">${esc(d.privacy_note || 'Aggregated counts only.')}</p>
      <div class="panel"><h3>Headcount per front: claimed vs sensed</h3>${fronts.length ? `<div class="tablewrap"><table>
        <thead><tr><th>Front</th><th>Crew</th><th>Subcontractor</th><th class="num">Claimed</th><th class="num">Check-in</th><th class="num">Manifest</th>
        <th class="num">Camera max</th><th class="num">Badge zone</th><th>Status</th></tr></thead>
        <tbody>${fronts.map((f) => `<tr><td>${esc(f.front_id)}</td><td>${esc(f.crew_id)}</td><td>${esc(f.subcontractor_id)}</td>
          <td class="num">${num(f.headcount_claimed)}</td><td class="num">${num(f.checkin)}</td><td class="num">${num(f.manifest)}</td>
          <td class="num">${num(f.camera_max)}</td><td class="num">${num(f.badge_zone_count)}</td><td>${statusChip(f.status)}</td></tr>`).join('')}</tbody></table></div>` : empty('No presence data for this date.')}</div>
      <div class="panel"><h3>Equipment hours: claimed vs telematics</h3>${eq.length ? `<div class="tablewrap"><table>
        <thead><tr><th>Equipment</th><th>Type</th><th>Subcontractor</th><th class="num">Hours claimed</th><th class="num">Engine h</th><th class="num">Working h</th><th>Telematics</th><th>Status</th></tr></thead>
        <tbody>${eq.map((x) => `<tr><td>${esc(x.equipment_id)}</td><td>${esc(x.type)}</td><td>${esc(x.subcontractor_id)}</td>
          <td class="num">${num(x.hours_claimed, 1)}</td><td class="num">${num(x.engine_h, 1)}</td><td class="num">${num(x.working_h, 1)}</td>
          <td>${esc(x.telematics)}</td><td>${statusChip(x.status)}</td></tr>`).join('')}</tbody></table></div>` : empty('No equipment claims for this date.')}</div>`;
  } catch (e) { view.innerHTML = `<h2>S8 Presence</h2>${errorBox(e)}`; }
}

// ---------- S9 Client daily report (Bautagesbericht), generated + independently checked ----------
async function dailyreport() {
  const title = `<h2>S9 Bautagesbericht / client daily report <span class="muted">· ${esc(state.date)}</span></h2>`;
  view.innerHTML = title + loading();
  try {
    const r = await api(`/api/daily-report${qs({ date: state.date })}`);
    const wt = (w) => w ? `${esc(w.condition)} · wind ${num(w.wind_ms, 1)} m/s · rain ${num(w.precip_mm, 1)} mm` : '–';
    const lst = (a) => a && a.length ? `<ul>${a.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>` : '<p class="muted">–</p>';
    const grp = { JV_DIRECT: 'ARGE direkt / JV direct', JV_INDIRECT: 'ARGE indirekt / JV indirect' };
    const p = r.personnel || [];
    const tot = (k) => p.reduce((t, x) => t + (x[k] || 0), 0);
    view.innerHTML = `${title}
      <p class="note">Generated from the SiteOps data model in the client's daily-report structure. Columns marked <strong>✓ check</strong> are the independent verification a manual report cannot show. <button type="button" id="printDR">Print / save as PDF</button></p>
      <div class="panel"><h3>Bericht Nr. ${num(r.report_no)} · ${esc(r.date)}</h3>
        <p><strong>1. Wetter / weather</strong>: today ${wt(r.weather.today)}; next working day (${esc(r.next_working_day || '–')}) ${wt(r.weather.next)}</p></div>
      <div class="panel"><h3>2. Personalübersicht / man-hours</h3><div class="tablewrap"><table>
        <thead><tr><th>Group</th><th class="num">Cum. previous</th><th class="num">Today local</th><th class="num">Today external</th><th class="num">Today total</th><th class="num">Cum. + today</th><th class="num">✓ check: sensed today</th><th class="num">✓ unverified h</th></tr></thead>
        <tbody>${p.map((x) => `<tr><td>${esc(grp[x.group] || 'NU / Sub ' + x.group)}</td><td class="num">${num(x.cum_prev)}</td><td class="num">${num(x.today_local)}</td><td class="num">${num(x.today_external)}</td><td class="num">${num(x.today_total)}</td><td class="num">${num(x.cum)}</td><td class="num">${x.sensed_today == null ? '–' : num(x.sensed_today)}</td><td class="num">${x.unverified_today ? `<strong>${num(x.unverified_today)}</strong>` : (x.unverified_today === 0 ? '0' : '–')}</td></tr>`).join('')}
        <tr><td><strong>Gesamt / total</strong></td><td class="num"><strong>${num(tot('cum_prev'))}</strong></td><td class="num">${num(tot('today_local'))}</td><td class="num">${num(tot('today_external'))}</td><td class="num"><strong>${num(tot('today_total'))}</strong></td><td class="num"><strong>${num(tot('cum'))}</strong></td><td></td><td></td></tr></tbody></table></div></div>
      <div class="panel"><h3>3. Geräte / equipment hours</h3><p class="note">${esc(r.notes[0])}</p><div class="tablewrap"><table>
        <thead><tr><th>Owner</th><th class="num">Cum. previous (calc.)</th><th class="num">Today (calc.)</th><th class="num">Cum. + today</th><th class="num">✓ measured engine h</th><th class="num">✓ no telematics (h)</th><th class="num">✓ calc. − measured</th></tr></thead>
        <tbody>${(r.equipment || []).map((x) => `<tr><td>${esc(x.owner)}</td><td class="num">${num(x.cum_prev)}</td><td class="num">${num(x.today_calc)}</td><td class="num">${num(x.cum)}</td><td class="num">${num(x.today_measured_engine_h, 1)}</td><td class="num">${num(x.today_without_telematics_h)}</td><td class="num">${x.calc_minus_measured_h > 0.5 ? `<strong>${num(x.calc_minus_measured_h, 1)}</strong>` : num(x.calc_minus_measured_h, 1)}</td></tr>`).join('')}</tbody></table></div></div>
      <div class="panel grid2"><div><h3>4.1 Heute abgeschlossen / completed today</h3>${lst(r.completed)}</div><div><h3>4.2 Geplant / planned next</h3>${lst(r.planned)}</div></div>
      <div class="panel"><h3>5. Besondere Vorkommnisse / HSE, QA/QC</h3>${lst(r.hse)}
        ${(r.consistency_alerts || []).length ? `<p class="note"><strong>✓ check:</strong> ${r.consistency_alerts.map((a) => esc(a.explanation)).join('<br>')}</p>` : ''}</div>
      <div class="panel"><h3>6. Detaillierter Tätigkeitsbericht / detailed progress</h3><div class="tablewrap"><table>
        <thead><tr><th>Tätigkeit / activity</th><th>Unit</th><th class="num">Total</th><th>Plan sheets today</th><th class="num">Cum. previous</th><th class="num">This period</th><th class="num">Cumulative</th><th class="num">%</th><th class="num">✓ measured cum.</th><th class="num">✓ claimed cum.</th><th>✓ source</th><th>✓ worst status</th><th>✓ alerts</th></tr></thead>
        <tbody>${(r.detail || []).map((x) => `<tr><td>${esc(x.name_de)}<br><span class="muted">${esc(x.name)}</span></td><td>${esc(x.unit)}</td><td class="num">${num(x.total)}</td><td>${esc(x.sheets_today || '–')}</td><td class="num">${num(x.cum_prev)}</td><td class="num">${num(x.this_period)}</td><td class="num">${num(x.cum)}</td><td class="num">${pct(x.pct)}</td><td class="num">${num(x.measured_cum)}</td><td class="num">${num(x.claimed_cum)}</td><td>${esc(x.verification_source)}</td><td>${x.worst_status ? statusChip(x.worst_status) : '–'}</td><td>${esc((x.open_alerts || []).join(', ') || '–')}</td></tr>`).join('')}</tbody></table></div></div>`;
    $('#printDR').addEventListener('click', () => window.print());
  } catch (e) { view.innerHTML = title + errorBox(e); }
}

init();
