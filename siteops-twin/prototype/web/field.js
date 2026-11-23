// SiteOps Twin MVP: mobile field app (M1 report, M2 offline outbox, M3 photo evidence, M4 crew muster).
// Offline-first: every report is saved on the device before it is synced. The data is SYNTHETIC.
// Built against POST /api/field-reports in prototype/API_CONTRACT.md.

const ROLE = 'FM'; // the field app always acts as a foreman (demo RBAC)
const $ = (s, r = document) => r.querySelector(s);
const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
let meta = null, step = 1, headcount = 0, photos = [];

// ---------- storage: IndexedDB with localStorage fallback ----------
const store = (() => {
  const LS_KEY = 'siteops.outbox';
  let dbp = null;
  function openDb() {
    if (dbp) return dbp;
    dbp = new Promise((resolve, reject) => {
      try {
        const req = indexedDB.open('siteops-field', 1);
        req.onupgradeneeded = () => req.result.createObjectStore('outbox', { keyPath: 'client_uuid' });
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
      } catch (e) { reject(e); }
    });
    return dbp;
  }
  function lsAll() { try { return JSON.parse(localStorage.getItem(LS_KEY) || '[]'); } catch { return []; } }
  function lsSave(list) { try { localStorage.setItem(LS_KEY, JSON.stringify(list)); } catch { /* storage full or blocked */ } }
  return {
    async all() {
      try {
        const db = await openDb();
        return await new Promise((res, rej) => { const r = db.transaction('outbox').objectStore('outbox').getAll(); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); });
      } catch { return lsAll(); }
    },
    async put(item) {
      try {
        const db = await openDb();
        await new Promise((res, rej) => { const tx = db.transaction('outbox', 'readwrite'); tx.objectStore('outbox').put(item); tx.oncomplete = res; tx.onerror = () => rej(tx.error); });
      } catch {
        const list = lsAll().filter((x) => x.client_uuid !== item.client_uuid); list.push(item); lsSave(list);
      }
    },
  };
})();
function prefGet(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } }
function prefSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* ignore */ } }
function uuid() {
  if (crypto.randomUUID) return crypto.randomUUID();
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => { const r = (Math.random() * 16) | 0; return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16); });
}

// ---------- metadata (network first; cached copy when offline) ----------
async function loadMeta() {
  try {
    const r = await fetch('/api/meta', { headers: { 'X-Role': ROLE } });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    meta = await r.json();
    prefSet('siteops.meta', meta);
  } catch {
    meta = prefGet('siteops.meta');
  }
  if (!meta) {
    $('#formErr').textContent = 'No project data on this device yet. Connect once to download the crew and activity lists.';
    meta = { crews: [], fronts: [], activities: [], date_max: new Date().toISOString().slice(0, 10) };
  }
}

function fillSelect(sel, list, val, label, selected) {
  sel.innerHTML = list.map((x) => `<option value="${esc(x[val])}"${x[val] === selected ? ' selected' : ''}>${esc(label(x))}</option>`).join('');
}

// ---------- M1 form ----------
function addLine(data = {}) {
  const node = $('#lineTpl').content.firstElementChild.cloneNode(true);
  const act = node.querySelector('.lAct');
  const crew = (meta.crews || []).find((c) => c.crew_id === $('#rCrew').value);
  fillSelect(act, meta.activities || [], 'activity_code', (a) => `${a.activity_code} · ${a.name}`, data.activity_code || (crew && crew.activity_code));
  const setUnit = () => { const a = (meta.activities || []).find((x) => x.activity_code === act.value); node.querySelector('.lUnit').value = a ? a.unit : ''; };
  act.addEventListener('change', setUnit); setUnit();
  // Equipment: /api/meta has no equipment list in contract v1, so meta.equipment is used when the backend provides it.
  const eqSel = node.querySelector('.lEq');
  const eq = meta.equipment || [];
  if (eq.length) {
    eqSel.innerHTML = eq.map((e) => `<option value="${esc(e.equipment_id)}"${(data.equipment_ids || []).includes(e.equipment_id) ? ' selected' : ''}>${esc(e.equipment_id)}${e.type ? ' · ' + esc(e.type) : ''}</option>`).join('');
  } else {
    const inp = document.createElement('input');
    inp.type = 'text'; inp.className = 'lEq'; inp.placeholder = 'Equipment IDs, comma separated';
    inp.value = (data.equipment_ids || []).join(', ');
    eqSel.replaceWith(inp);
  }
  const front = (meta.fronts || []).find((f) => f.front_id === $('#rFront').value);
  node.querySelector('.lFrom').value = data.kp_from_m ?? (front ? front.kp_from_m : '');
  node.querySelector('.lTo').value = data.kp_to_m ?? '';
  node.querySelector('.lQty').value = data.qty ?? '';
  node.querySelector('.lHours').value = data.hours_worked ?? 10;
  node.querySelector('.lHead').value = data.headcount ?? (headcount || '');
  node.querySelector('.lDown').value = data.downtime_h ?? 0;
  node.querySelector('.lReason').value = data.downtime_reason || '';
  node.querySelector('.lRemove').addEventListener('click', () => { if ($('#lines').children.length > 1) node.remove(); });
  // Suggest the quantity from the KP range for linear (m) activities.
  const autoQty = () => {
    const f = parseFloat(node.querySelector('.lFrom').value), t = parseFloat(node.querySelector('.lTo').value);
    if (node.querySelector('.lUnit').value === 'm' && !isNaN(f) && !isNaN(t) && t > f && !node.querySelector('.lQty').value) node.querySelector('.lQty').value = t - f;
  };
  node.querySelector('.lTo').addEventListener('change', autoQty);
  $('#lines').appendChild(node);
}

function readLines() {
  return [...document.querySelectorAll('#lines .line')].map((n) => {
    const eqEl = n.querySelector('.lEq');
    const equipment_ids = eqEl.tagName === 'SELECT'
      ? [...eqEl.selectedOptions].map((o) => o.value)
      : eqEl.value.split(',').map((s) => s.trim()).filter(Boolean);
    const num = (c) => { const v = parseFloat(n.querySelector(c).value); return isNaN(v) ? null : v; };
    return {
      activity_code: n.querySelector('.lAct').value,
      kp_from_m: num('.lFrom'), kp_to_m: num('.lTo'), qty: num('.lQty'), unit: n.querySelector('.lUnit').value,
      hours_worked: num('.lHours'), headcount: num('.lHead') ?? headcount, equipment_ids,
      downtime_h: num('.lDown') ?? 0, downtime_reason: n.querySelector('.lReason').value || null,
    };
  });
}

function validate(s) {
  const errs = [];
  if (s >= 1) {
    if (!$('#rDate').value) errs.push('Select the report date.');
    if (!$('#rCrew').value) errs.push('Select the crew.');
    if (!$('#rFront').value) errs.push('Select the work front.');
  }
  if (s >= 2) {
    readLines().forEach((l, i) => {
      const n = `Line ${i + 1}: `;
      if (l.kp_from_m == null || l.kp_to_m == null) errs.push(n + 'enter KP from and KP to.');
      else if (l.kp_to_m <= l.kp_from_m) errs.push(n + 'KP to must be greater than KP from.');
      if (l.qty == null || l.qty < 0) errs.push(n + 'enter the quantity.');
      if (l.hours_worked == null || l.hours_worked < 0 || l.hours_worked > 24) errs.push(n + 'hours must be between 0 and 24.');
      if (l.downtime_h > 0 && !l.downtime_reason) errs.push(n + 'select a downtime reason.');
    });
  }
  return errs;
}

function showStep(s) {
  step = s;
  document.querySelectorAll('.step').forEach((el) => { el.hidden = Number(el.dataset.step) !== s; });
  document.querySelectorAll('.steps span').forEach((el) => el.classList.toggle('on', Number(el.dataset.s) === s));
  $('#prevBtn').disabled = s === 1;
  $('#nextBtn').textContent = s === 3 ? 'Save report' : 'Next';
  $('#formErr').textContent = '';
  if (s === 3) renderSummary();
  window.scrollTo(0, 0);
}

function renderSummary() {
  const lines = readLines();
  $('#summary').innerHTML = `<strong>${esc($('#rCrew').value)} · ${esc($('#rFront').value)} · ${esc($('#rDate').value)}</strong><br>
    Headcount ${headcount}<br>${lines.map((l) => `${esc(l.activity_code)} ${l.kp_from_m}–${l.kp_to_m} m: ${l.qty} ${esc(l.unit)}, ${l.hours_worked} h`).join('<br>')}`;
}

function setHeadcount(v) {
  headcount = Math.max(0, v);
  $('#hcOut').textContent = headcount;
  document.querySelectorAll('#lines .lHead').forEach((el) => { if (!el.dataset.touched) el.value = headcount; });
}

async function saveReport() {
  const report = {
    client_uuid: uuid(),
    report_date: $('#rDate').value,
    crew_id: $('#rCrew').value,
    front_id: $('#rFront').value,
    lines: readLines(),
    photos: photos.map(({ name, taken_at, kp_m }) => ({ name, taken_at, kp_m })),
    submitted_at: new Date().toISOString(),
  };
  const item = { ...report, _state: 'pending', _thumbs: photos.map((p) => p.thumb).filter(Boolean), _msg: '', _saved_at: Date.now() };
  await store.put(item);
  // Remember this report for "copy yesterday".
  prefSet('siteops.lastReport', { crew_id: report.crew_id, front_id: report.front_id, lines: report.lines, headcount });
  photos = []; renderPhotos();
  $('#lines').innerHTML = ''; addLine();
  showStep(1);
  await renderQueue();
  setPage('pageQueue');
  syncAll();
}

// ---------- M3 photos ----------
function renderPhotos() {
  $('#photoList').innerHTML = photos.map((p, i) => `<div class="qitem">${p.thumb ? `<img src="${p.thumb}" alt="Photo ${i + 1} thumbnail">` : ''}
    <div>${esc(p.name)} · ${esc(p.taken_at)} · KP ${p.kp_m ?? '–'} m</div>
    <button type="button" data-i="${i}" class="pRemove">Remove</button></div>`).join('');
  document.querySelectorAll('.pRemove').forEach((b) => b.addEventListener('click', () => { photos.splice(Number(b.dataset.i), 1); renderPhotos(); }));
}
function thumbnail(file) {
  return new Promise((resolve) => {
    try {
      const img = new Image();
      const url = URL.createObjectURL(file);
      img.onload = () => {
        const s = 96 / Math.max(img.width, img.height);
        const c = document.createElement('canvas'); c.width = Math.round(img.width * s); c.height = Math.round(img.height * s);
        c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
        URL.revokeObjectURL(url);
        resolve(c.toDataURL('image/jpeg', 0.6));
      };
      img.onerror = () => { URL.revokeObjectURL(url); resolve(null); };
      img.src = url;
    } catch { resolve(null); }
  });
}

// ---------- M2 outbox + sync ----------
const STATE_LABEL = { pending: '⏳ Pending', synced: '✔ Synced', duplicate: '≈ Already received', error: '✕ Error' };
async function renderQueue() {
  const items = (await store.all()).sort((a, b) => (b._saved_at || 0) - (a._saved_at || 0));
  const pending = items.filter((i) => i._state === 'pending' || i._state === 'error').length;
  $('#qCount').textContent = pending ? `(${pending})` : '';
  $('#queue').innerHTML = items.length ? items.map((i) => `<div class="qitem">
      <div class="qstate ${esc(i._state)}">${STATE_LABEL[i._state] || esc(i._state)}</div>
      <div><strong>${esc(i.report_date)} · ${esc(i.crew_id)} · ${esc(i.front_id)}</strong></div>
      <div class="muted">${(i.lines || []).map((l) => `${esc(l.activity_code)} ${l.kp_from_m}–${l.kp_to_m}: ${l.qty} ${esc(l.unit)}`).join('; ')}</div>
      ${(i._thumbs || []).map((t, n) => `<img src="${t}" alt="Photo ${n + 1} thumbnail">`).join('')}
      ${i._msg ? `<div class="${i._state === 'error' ? 'err' : 'muted'}">${esc(i._msg)}</div>` : ''}
      ${i.report_id ? `<div class="muted">Server ID ${esc(i.report_id)}</div>` : ''}
    </div>`).join('') : '<p class="muted">No reports saved on this device.</p>';
}

let syncing = false;
async function syncAll() {
  if (syncing) return;
  syncing = true;
  const msg = $('#syncMsg');
  try {
    if (!navigator.onLine) { msg.textContent = 'Offline: reports stay on this device and sync automatically when you are back online.'; return; }
    const items = (await store.all()).filter((i) => i._state === 'pending' || i._state === 'error');
    if (!items.length) { msg.textContent = 'Everything is synced.'; return; }
    msg.textContent = `Syncing ${items.length} report(s)…`;
    let ok = 0;
    for (const it of items) {
      const { _state, _thumbs, _msg, _saved_at, report_id, ...body } = it;
      try {
        const r = await fetch('/api/field-reports', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Role': ROLE }, body: JSON.stringify(body) });
        let data = null; try { data = await r.json(); } catch { /* no body */ }
        if (r.status === 201 || r.status === 200) {
          it._state = data && data.duplicate ? 'duplicate' : 'synced';
          it.report_id = data && data.report_id; it._msg = ''; ok++;
        } else if (r.status === 422 || r.status === 400 || r.status === 403) {
          it._state = 'error';
          it._msg = `Rejected by server (${r.status}): ${data ? JSON.stringify(data.detail || data.error || data) : ''}`;
        } else {
          it._state = 'pending'; it._msg = `Server error ${r.status}; will retry.`;
        }
      } catch {
        it._state = 'pending'; it._msg = 'Network error; will retry.';
      }
      await store.put(it);
    }
    msg.textContent = `${ok} of ${items.length} synced.`;
  } finally {
    syncing = false;
    await renderQueue();
  }
}

// ---------- navigation + network status ----------
function setPage(id) {
  ['pageReport', 'pageQueue'].forEach((p) => { $('#' + p).hidden = p !== id; });
  document.querySelectorAll('.bottomnav button[data-page]').forEach((b) => {
    if (b.dataset.page === id) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current');
  });
  if (id === 'pageQueue') renderQueue();
}
function netStatus() {
  const el = $('#net');
  el.className = 'net ' + (navigator.onLine ? 'online' : 'offline');
  el.textContent = navigator.onLine ? '● Online' : '○ Offline';
}

// ---------- init ----------
async function init() {
  netStatus();
  window.addEventListener('online', () => { netStatus(); syncAll(); });
  window.addEventListener('offline', netStatus);
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(() => { /* SW not available */ });

  await loadMeta();
  $('#rDate').value = meta.default_date || meta.date_max || new Date().toISOString().slice(0, 10);
  if (meta.date_min) $('#rDate').min = meta.date_min;
  const last = prefGet('siteops.lastReport');
  fillSelect($('#rCrew'), meta.crews || [], 'crew_id', (c) => `${c.crew_id} · ${c.activity_code} · ${c.subcontractor_id}`, last && last.crew_id);
  fillSelect($('#rFront'), meta.fronts || [], 'front_id', (f) => `${f.front_id} · ${f.type} · ${f.kp_from_m}–${f.kp_to_m} m`, last && last.front_id);
  const crew = (meta.crews || []).find((c) => c.crew_id === $('#rCrew').value);
  setHeadcount(crew ? crew.nominal_size || 0 : 0);
  addLine();

  $('#rCrew').addEventListener('change', () => { const c = (meta.crews || []).find((x) => x.crew_id === $('#rCrew').value); if (c) setHeadcount(c.nominal_size || 0); });
  $('#hcMinus').addEventListener('click', () => setHeadcount(headcount - 1));
  $('#hcPlus').addEventListener('click', () => setHeadcount(headcount + 1));
  $('#lines').addEventListener('input', (e) => { if (e.target.classList.contains('lHead')) e.target.dataset.touched = '1'; });
  $('#copyYesterday').addEventListener('click', () => {
    const l = prefGet('siteops.lastReport');
    if (!l) { $('#formErr').textContent = 'No previous report saved on this device.'; return; }
    $('#rCrew').value = l.crew_id; $('#rFront').value = l.front_id;
    setHeadcount(l.headcount || 0);
    $('#lines').innerHTML = '';
    // Carry over the activity, equipment and hours; start the KP where yesterday ended. Quantity is left blank.
    (l.lines || []).forEach((x) => addLine({ ...x, kp_from_m: x.kp_to_m, kp_to_m: null, qty: null }));
    if (!$('#lines').children.length) addLine();
    $('#formErr').textContent = '';
  });
  $('#addLine').addEventListener('click', () => addLine());
  $('#prevBtn').addEventListener('click', () => showStep(Math.max(1, step - 1)));
  $('#nextBtn').addEventListener('click', async () => {
    const errs = validate(step);
    if (errs.length) { $('#formErr').innerHTML = errs.map(esc).join('<br>'); return; }
    if (step < 3) showStep(step + 1); else await saveReport();
  });
  $('#photoIn').addEventListener('change', async (e) => {
    for (const f of e.target.files) {
      const kpv = parseFloat($('#photoKp').value);
      photos.push({ name: f.name, taken_at: new Date(f.lastModified || Date.now()).toISOString(), kp_m: isNaN(kpv) ? null : kpv, thumb: await thumbnail(f) });
    }
    e.target.value = '';
    renderPhotos();
  });
  $('#syncBtn').addEventListener('click', syncAll);
  document.querySelectorAll('.bottomnav button[data-page]').forEach((b) => b.addEventListener('click', () => setPage(b.dataset.page)));
  showStep(1);
  renderQueue();
  syncAll();
}

init();
