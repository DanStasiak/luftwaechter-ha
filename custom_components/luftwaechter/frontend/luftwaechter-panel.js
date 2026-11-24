/* Luftwächter panel: vanilla web component, no build step, no external requests. */
const UI = {
  de: { title: "Luftwächter", outside: "Draußen", values: "Messwerte", devices: "Geräte", problems: "Was auffällt", history: "Verlauf (24 h)",
    co2: "CO₂", pm25: "Feinstaub", temperature: "Temperatur", humidity: "Luftfeuchte",
    good: "Gut", fair: "Mittel", poor: "Schlecht", unknown: "Unbekannt",
    none: "Noch keine Räume gefunden. Weise Sensoren (CO₂ oder Feinstaub) einem Bereich zu.",
    wind: "Wind", back: "Zurück", limits: "Grenzen", help: "Hilfe", close: "Schließen", sortWorst: "Schlechteste zuerst", sortName: "A–Z",
    updated: "Stand", ago: "vor {n} min", now: "gerade eben", prev: "Vorheriger Raum", next: "Nächster Raum",
    loading: "Lade Verlauf …", nohist: "Kein Verlauf verfügbar", now_: "jetzt", h24: "vor 24 h", min: "min", max: "max",
    on: "an", off: "aus", open: "offen", closed: "zu", opening: "öffnet", closing: "schließt", heating: "heizt", idle: "ruht",
    cover_open: "Auf", cover_stop: "Stopp", cover_close: "Zu", allgood: "Alle Werte im grünen Bereich.",
    isPoor: "ist schlecht", isFair: "ist mittel", tooHigh: "zu hoch", tooLow: "zu niedrig", limit: "Grenze",
    helpTitle: "Was bedeuten die Messwerte?", causes: "Mögliche Ursachen", todo: "Was hilft",
    hCo2: "CO₂ (Kohlendioxid) zeigt, wie verbraucht die Raumluft ist. Wir atmen es aus.",
    cCo2: "Viele Personen im Raum, Schlafen bei geschlossenem Fenster, kleine Räume, geschlossene Türen, Kerzen oder Gasflammen.",
    dCo2: "Stoßlüften: Fenster ganz öffnen, 5–10 Minuten.",
    hPm: "Feinstaub (PM2,5) sind winzige Partikel, die tief in die Lunge gelangen.",
    cPm: "Kochen und Braten, Kerzen, Kamin oder Ofen, Rauchen, Staubsaugen, Rauch oder Smog von draußen, Sensor direkt neben Heizung oder Toaster.",
    dPm: "Abzug einschalten, nicht dauerhaft lüften wenn es draußen auch staubt, Luftreiniger nutzen, Quelle abstellen.",
    hT: "Die Temperatur bestimmt, ob man sich im Raum wohlfühlt. 17–23 °C gilt als gut.",
    cT: "Zu kalt: Heizung aus, Fenster offen. Zu warm: Sonne, viele Geräte, Heizung zu hoch.",
    dT: "Heizung anpassen, Rollos bei Sonne schließen, kurz stoßlüften.",
    hH: "Die relative Luftfeuchte beeinflusst Komfort und Schimmelrisiko. 30–60 % ist gut.",
    cH: "Zu hoch: Duschen, Kochen, Wäsche trocknen, viele Pflanzen, zu wenig Lüften. Zu niedrig: trockene Heizungsluft im Winter.",
    dH: "Zu hoch: stoßlüften. Zu niedrig: Wäsche drinnen trocknen, Pflanzen, nicht zu stark heizen." },
  en: { title: "Luftwächter", outside: "Outside", values: "Readings", devices: "Devices", problems: "What stands out", history: "History (24 h)",
    co2: "CO₂", pm25: "Fine dust", temperature: "Temperature", humidity: "Humidity",
    good: "Good", fair: "Fair", poor: "Poor", unknown: "Unknown",
    none: "No rooms found yet. Assign CO₂ or fine dust sensors to an area.",
    wind: "Wind", back: "Back", limits: "Limits", help: "Help", close: "Close", sortWorst: "Worst first", sortName: "A–Z",
    updated: "Updated", ago: "{n} min ago", now: "just now", prev: "Previous room", next: "Next room",
    loading: "Loading history …", nohist: "No history available", now_: "now", h24: "24 h ago", min: "min", max: "max",
    on: "on", off: "off", open: "open", closed: "closed", opening: "opening", closing: "closing", heating: "heating", idle: "idle",
    cover_open: "Open", cover_stop: "Stop", cover_close: "Close", allgood: "All readings are in the green.",
    isPoor: "is poor", isFair: "is fair", tooHigh: "too high", tooLow: "too low", limit: "Limit",
    helpTitle: "What do the readings mean?", causes: "Possible causes", todo: "What helps",
    hCo2: "CO₂ (carbon dioxide) shows how stale the room air is. We breathe it out.",
    cCo2: "Many people in the room, sleeping with the window closed, small rooms, closed doors, candles or gas flames.",
    dCo2: "Burst ventilation: open the window fully for 5–10 minutes.",
    hPm: "Fine dust (PM2.5) are tiny particles that reach deep into the lungs.",
    cPm: "Cooking and frying, candles, fireplace or stove, smoking, vacuuming, smoke or smog from outside, a sensor right next to a heater or toaster.",
    dPm: "Use the extractor hood, do not ventilate continuously if it is dusty outside, run an air purifier, stop the source.",
    hT: "Temperature decides whether the room feels comfortable. 17–23 °C counts as good.",
    cT: "Too cold: heating off, window open. Too warm: sun, many devices, heating too high.",
    dT: "Adjust the heating, close blinds in the sun, ventilate briefly.",
    hH: "Relative humidity affects comfort and mould risk. 30–60 % is good.",
    cH: "Too high: showering, cooking, drying laundry, many plants, too little ventilation. Too low: dry heating air in winter.",
    dH: "Too high: burst ventilation. Too low: dry laundry indoors, plants, do not overheat." },
};
const ICON = { open: "🪟", close: "🔒", keep_open: "🪟", wait: "⏳", keep_closed: "✅", unknown: "❔" };
const LVLICON = ["✅", "⚠️", "⛔"];
const LIM = { co2: "< 1000 / < 1500 ppm", pm25: "< 20 / < 50 µg/m³", temperature: "17–23 / 13–25 °C", humidity: "30–60 / 25–70 %" };
const COL = ["#2e9e5b", "#e8a317", "#d9472b"], GREY = "#7a8594";
const KEYS = ["co2", "pm25", "temperature", "humidity"];
const HELPKEY = { co2: ["hCo2", "cCo2", "dCo2"], pm25: ["hPm", "cPm", "dPm"], temperature: ["hT", "cT", "dT"], humidity: ["hH", "cH", "dH"] };
/* gauge scales: [min, max, [[from, to, level]...]] */
const SCALE = {
  co2: [400, 2000, [[400, 1000, 0], [1000, 1500, 1], [1500, 2000, 2]]],
  pm25: [0, 80, [[0, 20, 0], [20, 50, 1], [50, 80, 2]]],
  temperature: [5, 35, [[5, 13, 2], [13, 17, 1], [17, 23, 0], [23, 25, 1], [25, 35, 2]]],
  humidity: [0, 100, [[0, 25, 2], [25, 30, 1], [30, 60, 0], [60, 70, 1], [70, 100, 2]]],
};
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const store = {
  get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* ignore */ } },
};

class LuftwaechterPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._hass = null;
    this._sig = "";
    this._sel = store.get("lw_room");
    this._sort = store.get("lw_sort") || "worst";
    this._chartKey = "co2";
    this._help = false;
    this._hist = {};
    this._onKey = (ev) => this._key(ev);
  }
  connectedCallback() { window.addEventListener("keydown", this._onKey); }
  disconnectedCallback() { window.removeEventListener("keydown", this._onKey); }
  set hass(h) {
    this._hass = h;
    const e = this._house();
    const sig = e ? e.last_updated + "|" + Object.values(h.states).filter((s) => /^(light|switch|climate|cover)\./.test(s.entity_id)).map((s) => s.state + (s.attributes && s.attributes.current_position)).join(",") : "none";
    if (sig !== this._sig) { this._sig = sig; this._render(); }
  }
  set narrow(v) { this._narrow = v; }
  set panel(v) { /* unused */ }
  _house() {
    const st = this._hass && this._hass.states;
    if (!st) return null;
    return Object.values(st).find((s) => s.entity_id.startsWith("sensor.") && s.attributes && Array.isArray(s.attributes.rooms) && s.attributes.summary) || null;
  }
  _t() { const e = this._house(); const l = ((e && e.attributes.lang) || (this._hass && this._hass.language) || "en").slice(0, 2); return UI[l] || UI.en; }
  _col(level) { const i = ["good", "fair", "poor"].indexOf(level); return i < 0 ? GREY : COL[i]; }
  _lcol(i) { return i == null ? GREY : COL[i] || GREY; }
  _rooms() {
    const e = this._house(); if (!e) return [];
    const rooms = e.attributes.rooms.slice();
    if (this._sort === "worst") {
      const rank = (r) => ({ poor: 0, fair: 1, good: 2 }[r.level] ?? 3);
      rooms.sort((a, b) => rank(a) - rank(b) || a.name.localeCompare(b.name));
    } else rooms.sort((a, b) => a.name.localeCompare(b.name));
    return rooms;
  }
  _select(key) { this._sel = key; if (key) store.set("lw_room", key); else store.set("lw_room", ""); this._render(); }
  _key(ev) {
    if (this.offsetParent === null && !this.isConnected) return;
    if (ev.key === "Escape") { if (this._help) { this._help = false; this._render(); } else if (this._sel) this._select(null); return; }
    if (!this._sel || this._help) return;
    if (ev.key === "ArrowRight" || ev.key === "ArrowLeft") {
      const rooms = this._rooms(); const i = rooms.findIndex((r) => r.key === this._sel);
      if (i < 0) return;
      const n = rooms[(i + (ev.key === "ArrowRight" ? 1 : rooms.length - 1)) % rooms.length];
      this._select(n.key);
    }
  }
  _call(domain, service, eid, extra) { this._hass.callService(domain, service, { entity_id: eid, ...(extra || {}) }); }
  _toggle(eid, domain) {
    const s = this._hass.states[eid]; if (!s) return;
    if (domain === "climate") return this._call("climate", s.state === "off" ? "turn_on" : "turn_off", eid);
    if (domain === "button") return this._call("button", "press", eid);
    return this._call(domain, "toggle", eid);
  }
  _devState(d, t) {
    const s = this._hass.states[d.entity]; if (!s) return { text: "", on: false };
    const a = s.attributes || {};
    if (d.domain === "cover") {
      const m = { open: t.open, closed: t.closed, opening: t.opening, closing: t.closing }[s.state] || s.state;
      return { text: a.current_position != null ? `${m} · ${a.current_position} %` : m, on: s.state !== "closed" };
    }
    if (d.domain === "climate") {
      const act = a.hvac_action ? { heating: t.heating, idle: t.idle, off: t.off }[a.hvac_action] || a.hvac_action : (s.state === "off" ? t.off : t.on);
      const cur = a.current_temperature != null ? ` · ${a.current_temperature} °C` : "";
      return { text: act + cur, on: s.state !== "off" };
    }
    const on = s.state === "on";
    return { text: on ? t.on : t.off, on };
  }
  /* ---- history ---- */
  _histKey(room, key) { return room.key + "|" + key; }
  async _loadHist(room, key) {
    const hk = this._histKey(room, key); const c = this._hist[hk];
    if (c && (c.loading || Date.now() - c.at < 300000)) return;
    const ids = (room.sources && room.sources[key === "pm25" ? "pm25" : key === "co2" ? "carbon_dioxide" : key]) || [];
    this._hist[hk] = { loading: true, at: Date.now() };
    if (!ids.length || !this._hass.callWS) { this._hist[hk] = { error: true, at: Date.now() }; return this._render(); }
    try {
      const end = new Date(), start = new Date(end.getTime() - 24 * 3600 * 1000);
      const res = await this._hass.callWS({ type: "history/history_during_period", start_time: start.toISOString(), end_time: end.toISOString(), entity_ids: ids, minimal_response: true, no_attributes: true, significant_changes_only: false });
      const N = 96, t0 = start.getTime() / 1000, step = 900;
      const series = ids.map((id) => {
        const pts = (res[id] || []).map((p) => {
          const v = parseFloat(p.s ?? p.state); let tm = p.lu ?? p.lc;
          if (tm == null && (p.last_updated || p.last_changed)) tm = Date.parse(p.last_updated || p.last_changed) / 1000;
          if (typeof tm === "string") tm = Date.parse(tm) / 1000;
          return [tm ?? t0, v];
        }).filter((p) => !isNaN(p[1])).sort((a, b) => a[0] - b[0]);
        const out = []; let j = 0, last = null;
        for (let i = 0; i < N; i++) {
          const tt = t0 + i * step;
          while (j < pts.length && pts[j][0] <= tt) { last = pts[j][1]; j++; }
          out.push(last);
        }
        return out;
      });
      const avg = [];
      for (let i = 0; i < N; i++) { const vs = series.map((s) => s[i]).filter((v) => v != null); avg.push(vs.length ? vs.reduce((a, b) => a + b, 0) / vs.length : null); }
      this._hist[hk] = { data: avg, at: Date.now() };
    } catch (e) { this._hist[hk] = { error: true, at: Date.now() }; }
    this._render();
  }
  _chart(room, t) {
    const key = this._chartKey, hk = this._histKey(room, key), h = this._hist[hk];
    const tabs = KEYS.map((k) => `<button class="chip ${k === key ? "sel" : ""}" data-chart="${k}" aria-pressed="${k === key}">${esc(t[k])}</button>`).join("");
    let body;
    if (!h || h.loading) body = `<div class="muted">${esc(t.loading)}</div>`;
    else if (h.error || !h.data || !h.data.some((v) => v != null)) body = `<div class="muted">${esc(t.nohist)}</div>`;
    else {
      const d = h.data, sc = SCALE[key]; const vals = d.filter((v) => v != null);
      const mn = Math.min(...vals), mx = Math.max(...vals);
      const lo = Math.min(sc[0], mn), hi = Math.max(sc[1] * (key === "co2" || key === "pm25" ? 0.6 : 1), mx);
      const W = 600, H = 150, X = (i) => (i / (d.length - 1)) * W, Y = (v) => H - ((v - lo) / (hi - lo)) * H;
      const bands = sc[2].map(([a, b, l]) => { const y1 = Math.max(0, Y(Math.min(b, hi))), y2 = Math.min(H, Y(Math.max(a, lo))); return y2 > y1 ? `<rect x="0" y="${y1.toFixed(1)}" width="${W}" height="${(y2 - y1).toFixed(1)}" fill="${COL[l]}" opacity=".13"/>` : ""; }).join("");
      let path = "", pen = false;
      d.forEach((v, i) => { if (v == null) { pen = false; return; } path += `${pen ? "L" : "M"}${X(i).toFixed(1)},${Y(v).toFixed(1)} `; pen = true; });
      const unit = room.values.find((v) => v.key === key)?.unit || "";
      body = `<div class="chartwrap"><svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" role="img" aria-label="${esc(t[key])} ${esc(t.history)}">${bands}<path d="${path}" fill="none" stroke="var(--primary-text-color,#222)" stroke-width="2" vector-effect="non-scaling-stroke"/><line id="cur" x1="0" x2="0" y1="0" y2="${H}" stroke="var(--primary-color,#03a9f4)" stroke-width="1.5" vector-effect="non-scaling-stroke" visibility="hidden"/></svg>
        <div class="axis"><span>${esc(t.h24)}</span><span id="readout" aria-live="off">${esc(t.min)} ${mn.toFixed(key === "temperature" ? 1 : 0)} · ${esc(t.max)} ${mx.toFixed(key === "temperature" ? 1 : 0)} ${esc(unit)}</span><span>${esc(t.now_)}</span></div></div>`;
      this._chartMeta = { d, unit, key, mn, mx, t };
    }
    return `<div class="card"><h3>${esc(t.history)}</h3><div class="chips">${tabs}</div>${body}</div>`;
  }
  _gauge(v) {
    const sc = SCALE[v.key]; if (!sc || v.raw == null) return "";
    const [a, b, segs] = sc; const pos = Math.max(0, Math.min(100, ((v.raw - a) / (b - a)) * 100));
    const parts = segs.map(([f, to, l]) => `<i style="left:${((f - a) / (b - a)) * 100}%;width:${((to - f) / (b - a)) * 100}%;background:${COL[l]}"></i>`).join("");
    return `<div class="gauge" aria-hidden="true">${parts}<b style="left:${pos}%"></b></div>`;
  }
  _problems(room, t) {
    const rows = room.values.filter((v) => v.level >= 1 && v.raw != null).sort((a, b) => b.level - a.level).map((v) => {
      const sc = SCALE[v.key]; let dir = "";
      if (v.key === "temperature" || v.key === "humidity") dir = v.raw < (v.key === "temperature" ? 17 : 30) ? t.tooLow : t.tooHigh;
      return `<li><span style="color:${COL[v.level]}">${LVLICON[v.level]}</span> <b>${esc(t[v.key])}</b> ${esc(v.value)} ${esc(v.unit)} ${v.level === 2 ? esc(t.isPoor) : esc(t.isFair)}${dir ? " (" + esc(dir) + ")" : ""} <small>${esc(t.limit)} ${esc(LIM[v.key])}</small></li>`;
    });
    return rows.length ? `<ul class="probs">${rows.join("")}</ul>` : `<p class="muted">${esc(t.allgood)}</p>`;
  }
  _devices(room, t) {
    if (!room.devices.length) return "";
    const names = {};
    room.devices.forEach((d) => { const k = d.group + "|" + d.name; names[k] = (names[k] || 0) + 1; });
    const groups = {};
    room.devices.forEach((d) => {
      let name = d.name;
      if (names[d.group + "|" + d.name] > 1) { const s = this._hass.states[d.entity]; if (s && s.attributes.friendly_name) name = s.attributes.friendly_name; }
      (groups[d.group] = groups[d.group] || []).push({ ...d, label: name });
    });
    return `<div class="card"><h3>${esc(t.devices)}</h3>${Object.entries(groups).map(([g, list]) => `<div class="grp"><small>${esc(g)}</small><div class="devs">${list.map((d) => {
      const st = this._devState(d, t);
      if (d.domain === "cover") {
        return `<div class="cov"><span class="covname">${esc(d.label)} <small>${esc(st.text)}</small></span><span class="covbtns"><button class="dev" data-cov="open_cover" data-ent="${esc(d.entity)}">${esc(t.cover_open)}</button><button class="dev" data-cov="stop_cover" data-ent="${esc(d.entity)}">${esc(t.cover_stop)}</button><button class="dev" data-cov="close_cover" data-ent="${esc(d.entity)}">${esc(t.cover_close)}</button></span></div>`;
      }
      return `<button class="dev ${st.on ? "on" : ""}" data-ent="${esc(d.entity)}" data-dom="${esc(d.domain)}" aria-pressed="${st.on}"><span>${esc(d.label)}</span><small>${esc(st.text)}</small></button>`;
    }).join("")}</div></div>`).join("")}</div>`;
  }
  _helpDlg(t) {
    if (!this._help) return "";
    return `<div class="ovl" id="ovl"><div class="dlg" role="dialog" aria-modal="true" aria-label="${esc(t.helpTitle)}"><div class="dh"><h2>${esc(t.helpTitle)}</h2><button class="x" id="hclose" aria-label="${esc(t.close)}">✕</button></div>
      ${KEYS.map((k) => `<section><h3>${esc(t[k])} <small>${esc(LIM[k])}</small></h3><p>${esc(t[HELPKEY[k][0]])}</p><p><b>${esc(t.causes)}:</b> ${esc(t[HELPKEY[k][1]])}</p><p><b>${esc(t.todo)}:</b> ${esc(t[HELPKEY[k][2]])}</p></section>`).join("")}</div></div>`;
  }
  _age(e, t) {
    const u = e.attributes.updated; if (!u) return "";
    const m = Math.max(0, Math.round((Date.now() / 1000 - u) / 60));
    return `${t.updated}: ${m < 1 ? t.now : t.ago.replace("{n}", m)}`;
  }
  _render() {
    const t = this._t(), e = this._house(), root = this.shadowRoot;
    const css = `:host{display:block;min-height:100%;background:var(--primary-background-color,#fff);color:var(--primary-text-color,#222);font-family:var(--paper-font-body1_-_font-family,system-ui,sans-serif)}
*{box-sizing:border-box}.wrap{max-width:1000px;margin:0 auto;padding:16px}
header{display:flex;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap}header h1{font-size:20px;margin:0;flex:1;min-width:150px}
.dot{width:14px;height:14px;border-radius:50%;display:inline-block}.upd{font-size:12px;opacity:.65}
button{font:inherit;color:inherit}.tool{border:1px solid var(--divider-color,#8884);background:none;border-radius:18px;padding:6px 12px;cursor:pointer}
.tool:hover,.tile:hover,.dev:hover,.chip:hover{filter:brightness(1.12)}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px}
.tile{border-radius:14px;padding:12px;background:var(--card-background-color,#f4f6f8);border:2px solid transparent;cursor:pointer;text-align:left}
:focus-visible{outline:3px solid var(--primary-color,#03a9f4);outline-offset:2px}
.tile b{display:block;font-size:15px}.tile small{display:block;opacity:.85;margin-top:2px}.bar{height:6px;border-radius:3px;margin-top:8px}
.card{border-radius:16px;padding:16px;background:var(--card-background-color,#f4f6f8);margin-top:12px}
h3{margin:0 0 8px;font-size:14px;opacity:.85}h3 small{font-weight:400;opacity:.7;margin-left:6px}
.nav{display:flex;align-items:center;gap:8px;margin-bottom:4px}.nav .sp{flex:1}
.back{border:0;background:none;color:var(--primary-color,#03a9f4);cursor:pointer;padding:6px 0}
.head{display:flex;gap:14px;align-items:center}.big{font-size:38px;line-height:1}.head h2{margin:0;font-size:20px}.head p{margin:4px 0 0;opacity:.85}
.badge{display:inline-block;border-radius:12px;padding:2px 10px;font-size:12px;color:#fff;margin-left:8px;vertical-align:middle}
.cols{display:grid;grid-template-columns:1fr;gap:0 12px}@media(min-width:860px){.cols{grid-template-columns:1fr 1fr}}
.vals{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.val{border-radius:12px;padding:10px;background:var(--secondary-background-color,#e8ebee);border-left:6px solid}
.val small{display:block;opacity:.75}.val b{font-size:22px}.val i{font-style:normal;opacity:.7;font-size:12px}
.gauge{position:relative;height:6px;border-radius:3px;overflow:hidden;margin-top:8px;background:#8883}.gauge i{position:absolute;top:0;bottom:0;opacity:.55}.gauge b{position:absolute;top:-2px;width:4px;height:10px;background:var(--primary-text-color,#fff);border-radius:2px;transform:translateX(-2px)}
.probs{list-style:none;margin:0;padding:0;display:grid;gap:6px}.probs small{opacity:.6;margin-left:4px}.muted{opacity:.7;margin:0}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}.chip{border:1px solid var(--divider-color,#8884);background:none;border-radius:16px;padding:4px 12px;cursor:pointer}.chip.sel{background:var(--primary-color,#03a9f4);color:#fff;border-color:transparent}
.chartwrap svg{width:100%;height:150px;display:block;border-radius:8px;touch-action:pan-y}.axis{display:flex;justify-content:space-between;font-size:12px;opacity:.75;margin-top:4px;gap:8px}
.grp{margin-top:8px}.grp>small{opacity:.7}.devs{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
.dev{border:0;border-radius:20px;padding:8px 14px;background:var(--secondary-background-color,#e8ebee);cursor:pointer;display:inline-flex;flex-direction:column;align-items:flex-start;line-height:1.2}
.dev small{opacity:.8;font-size:11px}.dev.on{background:var(--primary-color,#03a9f4);color:#fff}
.cov{display:flex;align-items:center;gap:10px;flex-wrap:wrap;width:100%}.covname small{opacity:.7;margin-left:4px}.covbtns{display:flex;gap:6px;margin-left:auto}.covbtns .dev{flex-direction:row;padding:6px 12px}
.warn{margin-top:10px;font-size:13px;color:#b36b00}.out{display:flex;gap:12px;align-items:center}
.ovl{position:fixed;inset:0;background:#0009;display:flex;align-items:center;justify-content:center;padding:16px;z-index:10}.dlg{background:var(--card-background-color,#fff);border-radius:16px;max-width:620px;max-height:90vh;overflow:auto;padding:18px;width:100%}
.dh{display:flex;justify-content:space-between;align-items:center}.dh h2{margin:0;font-size:18px}.x{border:0;background:none;font-size:20px;cursor:pointer}.dlg section{margin-top:14px}.dlg p{margin:4px 0;font-size:14px}
@media (prefers-reduced-motion:no-preference){.tile,.dev,.chip{transition:filter .15s}}`;
    if (!e) { root.innerHTML = `<style>${css}</style><div class="wrap"><p>…</p></div>`; return; }
    const a = e.attributes, rooms = this._rooms();
    const sel = rooms.find((r) => r.key === this._sel);
    let body = "";
    if (!rooms.length) body = `<div class="card">${esc(t.none)}</div>`;
    else if (!sel) {
      body = `<div class="tiles">${rooms.map((r) => {
        const bad = r.values.filter((v) => v.level >= 1 && v.raw != null).sort((x, y) => y.level - x.level)[0];
        const co2 = r.values.find((v) => v.key === "co2");
        return `<button class="tile" data-room="${esc(r.key)}" style="border-color:${this._col(r.level)}" aria-label="${esc(r.name)}: ${esc(t[r.level] || t.unknown)}">
          <b>${esc(r.name)}</b><small>${LVLICON[["good", "fair", "poor"].indexOf(r.level)] || "❔"} ${esc(r.headline)}</small>
          ${bad ? `<small style="color:${COL[bad.level]}">${esc(t[bad.key])}: ${esc(bad.value)} ${esc(bad.unit)}</small>` : co2 && co2.raw != null ? `<small>${esc(co2.value)} ppm</small>` : ""}<div class="bar" style="background:${this._col(r.level)}"></div></button>`;
      }).join("")}</div>`;
    } else {
      const li = rooms.findIndex((r) => r.key === sel.key);
      body = `<div class="nav"><button class="back" id="back">← ${esc(t.back)}</button><span class="sp"></span><button class="tool" id="prev" aria-label="${esc(t.prev)}">‹</button><button class="tool" id="next" aria-label="${esc(t.next)}">›</button></div>
      <div class="card"><div class="head"><span class="big">${["keep_closed", "unknown"].includes(sel.action) && LVLICON[["good", "fair", "poor"].indexOf(sel.level)] ? LVLICON[["good", "fair", "poor"].indexOf(sel.level)] : ICON[sel.action] || ""}</span><div><h2>${esc(sel.name)} · ${esc(sel.headline)}<span class="badge" style="background:${this._col(sel.level)}">${esc(t[sel.level] || t.unknown)}</span></h2><p>${esc(sel.detail)}</p></div></div>${sel.warn ? `<div class="warn">${esc(sel.warn)}</div>` : ""}</div>
      <div class="cols"><div><div class="card"><h3>${esc(t.problems)}</h3>${this._problems(sel, t)}</div>
        <div class="card"><h3>${esc(t.values)}</h3><div class="vals">${sel.values.map((v) => `<div class="val" style="border-color:${this._lcol(v.level)}" title="${esc(t.limits)}: ${esc(LIM[v.key])}"><small>${esc(t[v.key])}</small><b>${esc(v.value)}</b> <i>${esc(v.unit)}</i>${this._gauge(v)}</div>`).join("")}</div></div></div>
        <div>${this._chart(sel, t)}${this._devices(sel, t)}</div></div>`;
      this._pendingHist = sel;
    }
    const o = a.outside;
    const out = o ? `<div class="card out"><span class="big">${esc(o.icon)}</span><div><b>${esc(t.outside)}: ${esc(o.temp)} °C, ${esc(o.cond)}</b><br><small>${esc(t.wind)} ${esc(o.wind)} km/h ${esc(o.windDir)}${o.hum && o.hum !== "–" ? " · " + esc(o.hum) + " %" : ""}</small><br><small>${esc(o.tip)}</small></div></div>` : "";
    root.innerHTML = `<style>${css}</style><div class="wrap"><header><span class="dot" style="background:${this._col(e.state)}"></span><h1>${esc(t.title)} · ${esc(t[e.state] || t.unknown)}</h1><span class="upd">${esc(this._age(e, t))}</span>
      ${!sel && rooms.length > 1 ? `<button class="tool" id="sort">${esc(this._sort === "worst" ? t.sortWorst : t.sortName)}</button>` : ""}<button class="tool" id="help" aria-label="${esc(t.help)}">? ${esc(t.help)}</button></header>${body}${out}${this._helpDlg(t)}</div>`;
    const q = (s) => root.querySelector(s), qa = (s) => root.querySelectorAll(s);
    qa(".tile").forEach((b) => b.addEventListener("click", () => this._select(b.dataset.room)));
    q("#back")?.addEventListener("click", () => this._select(null));
    const step = (d) => { const rs = this._rooms(); const i = rs.findIndex((r) => r.key === this._sel); this._select(rs[(i + d + rs.length) % rs.length].key); };
    q("#prev")?.addEventListener("click", () => step(-1)); q("#next")?.addEventListener("click", () => step(1));
    q("#sort")?.addEventListener("click", () => { this._sort = this._sort === "worst" ? "name" : "worst"; store.set("lw_sort", this._sort); this._render(); });
    q("#help")?.addEventListener("click", () => { this._help = true; this._render(); q("#hclose")?.focus(); });
    q("#hclose")?.addEventListener("click", () => { this._help = false; this._render(); });
    q("#ovl")?.addEventListener("click", (ev) => { if (ev.target.id === "ovl") { this._help = false; this._render(); } });
    qa(".chip").forEach((b) => b.addEventListener("click", () => { this._chartKey = b.dataset.chart; this._render(); }));
    qa(".dev[data-dom]").forEach((b) => b.addEventListener("click", () => this._toggle(b.dataset.ent, b.dataset.dom)));
    qa("[data-cov]").forEach((b) => b.addEventListener("click", () => this._call("cover", b.dataset.cov, b.dataset.ent)));
    const svg = q(".chartwrap svg");
    if (svg && this._chartMeta) {
      const m = this._chartMeta, cur = q("#cur"), ro = q("#readout");
      const mv = (ev) => {
        const r = svg.getBoundingClientRect(); const f = Math.max(0, Math.min(1, (ev.clientX - r.left) / r.width));
        const i = Math.round(f * (m.d.length - 1)); const v = m.d[i];
        cur.setAttribute("x1", f * 600); cur.setAttribute("x2", f * 600); cur.setAttribute("visibility", "visible");
        const hrs = Math.round((m.d.length - 1 - i) * 0.25 * 10) / 10;
        if (v != null) ro.textContent = `${v.toFixed(m.key === "temperature" ? 1 : 0)} ${m.unit} · -${hrs} h`;
      };
      svg.addEventListener("pointermove", mv);
      svg.addEventListener("pointerleave", () => { cur.setAttribute("visibility", "hidden"); ro.textContent = `${m.t.min} ${m.mn.toFixed(m.key === "temperature" ? 1 : 0)} · ${m.t.max} ${m.mx.toFixed(m.key === "temperature" ? 1 : 0)} ${m.unit}`; });
    }
    if (sel && this._pendingHist) { const r = this._pendingHist; this._pendingHist = null; this._loadHist(r, this._chartKey); }
  }
}
customElements.define("luftwaechter-panel", LuftwaechterPanel);
