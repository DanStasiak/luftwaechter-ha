/* Luftwächter panel: vanilla web component, no build step, no external requests. */
const UI = {
  de: { title: "Luftwächter", house: "Haus", outside: "Draußen", values: "Messwerte", devices: "Geräte",
    co2: "CO₂", pm25: "Feinstaub", temperature: "Temperatur", humidity: "Luftfeuchte",
    good: "Gut", fair: "Mittel", poor: "Schlecht", unknown: "Unbekannt",
    none: "Noch keine Räume gefunden. Weise Sensoren (CO₂ oder Feinstaub) einem Bereich zu.",
    wind: "Wind", on: "an", off: "aus", back: "Zurück", limits: "Grenzen" },
  en: { title: "Luftwächter", house: "House", outside: "Outside", values: "Readings", devices: "Devices",
    co2: "CO₂", pm25: "Fine dust", temperature: "Temperature", humidity: "Humidity",
    good: "Good", fair: "Fair", poor: "Poor", unknown: "Unknown",
    none: "No rooms found yet. Assign CO₂ or fine dust sensors to an area.",
    wind: "Wind", on: "on", off: "off", back: "Back", limits: "Limits" },
};
const ICON = { open: "🪟", close: "🔒", keep_open: "🪟", wait: "⏳", keep_closed: "✅", unknown: "❔" };
const LIM = { co2: "< 1000 / < 1500 ppm", pm25: "< 20 / < 50 µg/m³", temperature: "17–23 / 13–25 °C", humidity: "30–60 / 25–70 %" };
const COL = ["#2e9e5b", "#e8a317", "#d9472b"], GREY = "#7a8594";
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

class LuftwaechterPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._sel = null;
    this._hass = null;
    this._sig = "";
  }
  set hass(h) {
    this._hass = h;
    const e = this._house();
    const sig = e ? e.last_updated + "|" + Object.values(h.states).filter((s) => /^(light|switch|climate|cover)\./.test(s.entity_id)).map((s) => s.state).join(",") : "none";
    if (sig !== this._sig) { this._sig = sig; this._render(); }
  }
  set narrow(v) { this._narrow = v; }
  set panel(v) {}
  _house() {
    const st = this._hass && this._hass.states;
    if (!st) return null;
    return Object.values(st).find((s) => s.entity_id.startsWith("sensor.") && s.attributes && Array.isArray(s.attributes.rooms) && s.attributes.summary) || null;
  }
  _t() { const e = this._house(); const l = ((e && e.attributes.lang) || (this._hass && this._hass.language) || "en").slice(0, 2); return UI[l] || UI.en; }
  _col(level) { const i = ["good", "fair", "poor"].indexOf(level); return i < 0 ? GREY : COL[i]; }
  _toggle(eid, type, domain) {
    const h = this._hass, s = h.states[eid];
    if (!s) return;
    if (domain === "cover") return h.callService("cover", s.state === "open" ? "close_cover" : "open_cover", { entity_id: eid });
    if (domain === "climate") return h.callService("climate", s.state === "off" ? "turn_on" : "turn_off", { entity_id: eid });
    if (domain === "button") return h.callService("button", "press", { entity_id: eid });
    return h.callService(domain, "toggle", { entity_id: eid });
  }
  _render() {
    const t = this._t(), e = this._house();
    const root = this.shadowRoot;
    const css = `:host{display:block;min-height:100%;background:var(--primary-background-color,#fff);color:var(--primary-text-color,#222);font-family:var(--paper-font-body1_-_font-family,system-ui,sans-serif)}
*{box-sizing:border-box}.wrap{max-width:760px;margin:0 auto;padding:16px}
header{display:flex;align-items:center;gap:10px;margin-bottom:14px}header h1{font-size:20px;margin:0;flex:1}
.dot{width:14px;height:14px;border-radius:50%;display:inline-block}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.tile{border-radius:14px;padding:12px;background:var(--card-background-color,#f4f6f8);border:2px solid transparent;cursor:pointer;text-align:left;color:inherit;font:inherit}
.tile:focus-visible,.dev:focus-visible,button:focus-visible{outline:3px solid var(--primary-color,#03a9f4);outline-offset:2px}
.tile b{display:block;font-size:15px}.tile small{opacity:.75}.bar{height:6px;border-radius:3px;margin-top:8px}
.card{border-radius:16px;padding:16px;background:var(--card-background-color,#f4f6f8);margin-top:12px}
.head{display:flex;gap:12px;align-items:center}.big{font-size:38px}.head h2{margin:0;font-size:20px}.head p{margin:4px 0 0;opacity:.85}
.vals{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:14px}
.val{border-radius:12px;padding:10px;background:var(--secondary-background-color,#e8ebee);border-left:6px solid}
.val small{display:block;opacity:.7}.val b{font-size:22px}.val i{font-style:normal;opacity:.7;font-size:12px}
.devs{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}.dev{border:0;border-radius:20px;padding:8px 14px;background:var(--secondary-background-color,#e8ebee);color:inherit;font:inherit;cursor:pointer}
.dev.on{background:var(--primary-color,#03a9f4);color:#fff}
.warn{margin-top:10px;font-size:13px;color:#b36b00}h3{margin:16px 0 4px;font-size:14px;opacity:.8}
.back{border:0;background:none;color:var(--primary-color,#03a9f4);font:inherit;cursor:pointer;padding:6px 0}
.out{display:flex;gap:10px;align-items:center}`;
    if (!e) { root.innerHTML = `<style>${css}</style><div class="wrap"><p>…</p></div>`; return; }
    const a = e.attributes, rooms = a.rooms;
    const sel = rooms.find((r) => r.key === this._sel);
    let body = "";
    if (!rooms.length) body = `<div class="card">${esc(t.none)}</div>`;
    else if (!sel) {
      body = `<div class="tiles">${rooms.map((r) => {
        const bad = r.values.filter((v) => v.level >= 1 && v.raw != null).sort((a, b) => b.level - a.level)[0];
        const co2 = r.values.find((v) => v.key === "co2");
        return `<button class="tile" data-room="${esc(r.key)}" style="border-color:${this._col(r.level)}" aria-label="${esc(r.name)}: ${esc(t[r.level])}">
          <b>${esc(r.name)}</b><small>${ICON[r.action] || ""} ${esc(r.headline)}</small>
          ${bad ? `<small style="color:${this._col(["good", "fair", "poor"][bad.level])}"><br>${esc(t[bad.key])}: ${esc(bad.value)} ${esc(bad.unit)}</small>` : co2 && co2.raw != null ? `<small><br>${esc(co2.value)} ppm</small>` : ""}<div class="bar" style="background:${this._col(r.level)}"></div></button>`;
      }).join("")}</div>`;
    } else {
      body = `<button class="back" id="back">← ${esc(t.back)}</button><div class="card">
        <div class="head"><span class="big">${ICON[sel.action] || ""}</span><div><h2>${esc(sel.name)} · ${esc(sel.headline)}</h2><p>${esc(sel.detail)}</p></div></div>
        ${sel.warn ? `<div class="warn">${esc(sel.warn)}</div>` : ""}
        <h3>${esc(t.values)}</h3><div class="vals">${sel.values.map((v) => `<div class="val" style="border-color:${this._col(["good", "fair", "poor"][v.level] || "")}" title="${esc(t.limits)}: ${esc(LIM[v.key])}"><small>${esc(t[v.key])}</small><b>${esc(v.value)}</b> <i>${esc(v.unit)}</i></div>`).join("")}</div>
        ${sel.devices.length ? `<h3>${esc(t.devices)}</h3><div class="devs">${sel.devices.map((d) => {
          const s = this._hass.states[d.entity]; const on = s && !["off", "closed"].includes(s.state);
          return `<button class="dev ${on ? "on" : ""}" data-ent="${esc(d.entity)}" data-dom="${esc(d.domain)}" aria-pressed="${on}">${esc(d.name)}</button>`;
        }).join("")}</div>` : ""}</div>`;
    }
    const o = a.outside;
    const out = o ? `<div class="card out"><span class="big">${esc(o.icon)}</span><div><b>${esc(t.outside)}: ${esc(o.temp)} °C, ${esc(o.cond)}</b><br><small>${esc(t.wind)} ${esc(o.wind)} km/h ${esc(o.windDir)}${o.hum && o.hum !== "–" ? " · " + esc(o.hum) + " %" : ""}</small><br><small>${esc(o.tip)}</small></div></div>` : "";
    root.innerHTML = `<style>${css}</style><div class="wrap"><header><span class="dot" style="background:${this._col(e.state)}"></span><h1>${esc(t.title)} · ${esc(t[e.state] || t.unknown)}</h1></header>${body}${out}</div>`;
    root.querySelectorAll(".tile").forEach((b) => b.addEventListener("click", () => { this._sel = b.dataset.room; this._render(); }));
    const back = root.getElementById ? root.getElementById("back") : root.querySelector("#back");
    if (back) back.addEventListener("click", () => { this._sel = null; this._render(); });
    root.querySelectorAll(".dev").forEach((b) => b.addEventListener("click", () => this._toggle(b.dataset.ent, null, b.dataset.dom)));
  }
}
customElements.define("luftwaechter-panel", LuftwaechterPanel);
