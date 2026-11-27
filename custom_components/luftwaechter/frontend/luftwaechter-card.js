/* Luftwächter Lovelace card: one room (face + one sentence + values) or a house summary.
   Usage:  type: custom:luftwaechter-card
           room: Office            # omit for the house summary
           rooms: [Office, Bedroom]  # house summary: only these rooms
           title: My air           # house summary title
           values: false           # hide the readings of a room
           compact: true           # one slim line instead of the big card
           symbols: true           # shapes next to the colours (colour-blind friendly)
           accent: true            # coloured edge on the left that follows the air level
           tap_action: panel       # tap opens the Luftwächter panel (default: nothing)
           face_style: emoji       # mascot (default) or emoji instead of the mascot faces  */
const LW_TXT = {
  de: { none: "Luftwächter nicht gefunden", noRoom: "Raum nicht gefunden", house: "Luftwächter", good: "gut", fair: "mittel", poor: "schlecht", unknown: "unbekannt", all: "Alle Räume gut", air: "Luft", openPanel: "Luftwächter öffnen",
    ed_room: "Raum (leer = ganzes Haus)", ed_title: "Titel (Haus)", ed_values: "Messwerte zeigen", ed_compact: "Kompakte Darstellung", ed_symbols: "Symbole zusätzlich zu Farben", ed_accent: "Farbiger Rand", ed_tap: "Antippen", ed_none: "Nichts", ed_panel: "Panel öffnen", ed_house: "Ganzes Haus", ed_face: "Gesichter", ed_mascot: "Maskottchen", ed_emoji: "Emoji" },
  en: { none: "Luftwächter not found", noRoom: "Room not found", house: "Luftwächter", good: "good", fair: "fair", poor: "poor", unknown: "unknown", all: "All rooms good", air: "air", openPanel: "Open Luftwächter",
    ed_room: "Room (empty = whole house)", ed_title: "Title (house)", ed_values: "Show readings", ed_compact: "Compact layout", ed_symbols: "Symbols in addition to colours", ed_accent: "Coloured edge", ed_tap: "Tap action", ed_none: "Nothing", ed_panel: "Open the panel", ed_house: "Whole house", ed_face: "Faces", ed_mascot: "Mascot", ed_emoji: "Emoji" },
};
const LW_FACE = { good: "🙂", fair: "😐", poor: "😷", unknown: "❔" };
const LW_MASCOT = "/luftwaechter_static/mascot/";
/* Face of a room or the house: the mascot image (the halo variant on dark themes) or, with face_style: emoji, the emoji. */
const lwFace = (level, cfg, hass) => {
  const lv = LW_FACE[level] ? level : "unknown";
  if (cfg && cfg.face_style === "emoji") return `<div class="face" aria-hidden="true">${LW_FACE[lv]}</div>`;
  const dark = !!(hass && hass.themes && hass.themes.darkMode);
  return `<img class="face" src="${LW_MASCOT}${lv}${dark ? "-dark" : ""}.png" data-lv="${lv}" width="40" height="40" alt="" aria-hidden="true" decoding="async">`;
};
const LW_SYM = { good: "✓", fair: "!", poor: "✕", unknown: "?" };
const LW_COL = { good: "#2e9e5b", fair: "#e8a317", poor: "#d9472b", unknown: "#7a8594" };
const lwEsc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const lwTxt = (hass) => LW_TXT[((hass && hass.language) || "en").slice(0, 2)] || LW_TXT.en;
const lwHouse = (hass) => {
  const st = hass && hass.states;
  if (!st) return null;
  return Object.values(st).find((s) => s.entity_id.startsWith("sensor.") && s.attributes && Array.isArray(s.attributes.rooms) && s.attributes.summary) || null;
};

class LuftwaechterCard extends HTMLElement {
  constructor() { super(); this.attachShadow({ mode: "open" }); this._cfg = {}; this._hass = null; this._sig = ""; }
  setConfig(cfg) { this._cfg = cfg || {}; this._sig = ""; this._render(); }
  set hass(h) {
    this._hass = h;
    const e = lwHouse(h);
    const sig = e ? h.language + "|" + ((h.themes && h.themes.darkMode) ? "d" : "l") + "|" + e.last_updated + "|" + JSON.stringify(this._cfg) : "none";
    if (sig !== this._sig) { this._sig = sig; this._render(); }
  }
  getCardSize() { return this._cfg.compact ? 1 : this._cfg.room ? 2 : 3; }
  getGridOptions() { return { columns: 6, rows: this._cfg.compact ? 1 : "auto", min_columns: 3 }; }
  static getStubConfig() { return {}; }
  static getConfigElement() { return document.createElement("luftwaechter-card-editor"); }
  _wanted() {
    const r = this._cfg.rooms;
    const list = Array.isArray(r) ? r : typeof r === "string" ? r.split(",") : [];
    return list.map((x) => String(x).trim().toLowerCase()).filter(Boolean);
  }
  _mark(level) {
    const col = LW_COL[level] || LW_COL.unknown;
    return this._cfg.symbols
      ? `<span class="sym" style="background:${col}" aria-hidden="true">${LW_SYM[level] || LW_SYM.unknown}</span>`
      : `<span class="dot" style="background:${col}" aria-hidden="true"></span>`;
  }
  _go(key) {
    const url = "/luftwaechter" + (key ? "#room=" + encodeURIComponent(key) : "");
    history.pushState(null, "", url);
    window.dispatchEvent(new CustomEvent("location-changed", { detail: { replace: false } }));
  }
  _render() {
    const t = lwTxt(this._hass); const house = lwHouse(this._hass); const e = lwEsc;
    const tap = this._cfg.tap_action === "panel" || (this._cfg.tap_action && this._cfg.tap_action.action === "navigate");
    const css = `<style>ha-card{padding:14px 16px;border-left:4px solid var(--lw-accent,transparent)}ha-card.tap{cursor:pointer}ha-card.tap:hover{filter:brightness(1.06)}ha-card.tap:focus-visible{outline:3px solid var(--primary-color,#03a9f4);outline-offset:2px}.row{display:flex;align-items:center;gap:12px}.face{font-size:34px;line-height:1}img.face{width:40px;height:40px;object-fit:contain;flex:none;font-size:34px}h2{margin:0;font-size:16px;font-weight:600}p{margin:2px 0 0;color:var(--secondary-text-color);font-size:13px}.vals{display:flex;gap:14px;flex-wrap:wrap;margin-top:10px;font-size:13px}.v b{font-weight:600}.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:middle}.sym{display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;border-radius:50%;margin-right:6px;color:#fff;font-size:11px;font-weight:700;line-height:1;vertical-align:middle}.list .item{display:flex;align-items:center;justify-content:space-between;padding:5px 0;font-size:14px;border-top:1px solid var(--divider-color,#8883)}.list .item:first-child{border-top:0}.muted{color:var(--secondary-text-color);font-size:13px}.slim{display:flex;align-items:center;justify-content:space-between;gap:10px;font-size:14px}.slim .nm{font-weight:600}.slim .hd{color:var(--secondary-text-color);text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}ha-card.slimcard{padding:8px 14px}</style>`;
    let body = ""; let accent = ""; let label = t.house; let cls = tap ? "tap" : "";
    if (!house) body = `<div class="muted">${e(t.none)}</div>`;
    else {
      const rooms = house.attributes.rooms || [];
      const want = (this._cfg.room || "").toString().toLowerCase();
      if (want) {
        const r = rooms.find((x) => x.key.toLowerCase() === want || x.name.toLowerCase() === want);
        if (!r) body = `<div class="muted">${e(t.noRoom)}: ${e(this._cfg.room)}</div>`;
        else {
          accent = LW_COL[r.level] || LW_COL.unknown; label = `${r.name}: ${t[r.level] || r.level} ${t.air}`;
          if (tap) this._key = r.key;
          if (this._cfg.compact) { cls += " slimcard"; body = `<div class="slim"><span class="nm">${this._mark(r.level)}${e(r.name)}</span><span class="hd">${e(r.headline)}</span></div>`; }
          else {
            const vals = (r.values || []).filter((v) => v.raw != null).map((v) => `<span class="v">${this._mark(["good", "fair", "poor"][v.level])}<b>${e(v.value)}</b> ${e(v.unit)}</span>`).join("");
            body = `<div class="row">${lwFace(r.level, this._cfg, this._hass)}<div><h2>${e(r.name)} · ${e(r.headline)}</h2><p>${e(r.detail)}</p></div></div>${this._cfg.values === false ? "" : `<div class="vals">${vals}</div>`}`;
          }
        }
      } else {
        const filt = this._wanted();
        const shown = filt.length ? rooms.filter((r) => filt.includes(r.key.toLowerCase()) || filt.includes(r.name.toLowerCase())) : rooms;
        const good = shown.filter((r) => r.level === "good").length;
        const allGood = good === shown.length && shown.length > 0;
        const title = this._cfg.title || t.house;
        label = `${title}: ${good} / ${shown.length}`; this._key = "";
        accent = allGood ? LW_COL.good : shown.length ? LW_COL.fair : "";
        if (this._cfg.compact) { cls += " slimcard"; body = `<div class="slim"><span class="nm">${e(title)}</span><span class="hd">${allGood ? e(t.all) : e(good + " / " + shown.length)}</span></div>`; }
        else {
          const items = shown.map((r) => `<div class="item"><span>${this._mark(r.level)}${e(r.name)}</span><span class="muted">${e(r.headline)}</span></div>`).join("");
          body = `<div class="row">${lwFace(allGood ? "good" : "fair", this._cfg, this._hass)}<div><h2>${e(title)}</h2><p>${allGood ? e(t.all) : e(good + " / " + shown.length)}</p></div></div><div class="list" style="margin-top:8px">${items}</div>`;
        }
      }
    }
    const attrs = tap ? ` role="button" tabindex="0" aria-label="${e(label)}. ${e(t.openPanel)}"` : ` role="group" aria-label="${e(label)}"`;
    this.shadowRoot.innerHTML = `${css}<ha-card class="${cls.trim()}" style="--lw-accent:${this._cfg.accent && accent ? accent : "transparent"}"${attrs}>${body}</ha-card>`;
    const card = this.shadowRoot.querySelector("ha-card");
    this.shadowRoot.querySelectorAll("img.face").forEach((im) => im.addEventListener("error", () => {
      const d = document.createElement("div"); d.className = "face"; d.setAttribute("aria-hidden", "true"); d.textContent = LW_FACE[im.dataset.lv] || LW_FACE.unknown; im.replaceWith(d);
    }, { once: true }));
    if (tap && card) {
      card.addEventListener("click", () => this._go(this._key));
      card.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); this._go(this._key); } });
    }
  }
}

/* Visual editor (Edit card dialog): room picker and switches instead of YAML. */
class LuftwaechterCardEditor extends HTMLElement {
  constructor() { super(); this._cfg = {}; this._hass = null; }
  setConfig(cfg) { this._cfg = cfg || {}; this._draw(); }
  set hass(h) { this._hass = h; this._draw(); }
  _schema() {
    const t = lwTxt(this._hass); const house = lwHouse(this._hass);
    const rooms = house ? (house.attributes.rooms || []).map((r) => ({ value: r.key, label: r.name })) : [];
    return [
      { name: "room", selector: { select: { options: [{ value: "", label: t.ed_house }, ...rooms], custom_value: true, mode: "dropdown" } } },
      { name: "title", selector: { text: {} } },
      { type: "grid", name: "", schema: [
        { name: "values", selector: { boolean: {} } }, { name: "compact", selector: { boolean: {} } }, { name: "symbols", selector: { boolean: {} } }, { name: "accent", selector: { boolean: {} } } ] },
      { name: "tap_action", selector: { select: { options: [{ value: "none", label: t.ed_none }, { value: "panel", label: t.ed_panel }], mode: "dropdown" } } },
      { name: "face_style", selector: { select: { options: [{ value: "mascot", label: t.ed_mascot }, { value: "emoji", label: t.ed_emoji }], mode: "dropdown" } } },
    ];
  }
  _draw() {
    if (!this._hass) return;
    let f = this.querySelector("ha-form");
    if (!f) {
      f = document.createElement("ha-form");
      f.addEventListener("value-changed", (ev) => {
        const v = { ...ev.detail.value }; v.type = "custom:luftwaechter-card";
        if (!v.room) delete v.room; if (!v.title) delete v.title;
        if (v.values !== false) delete v.values; if (!v.compact) delete v.compact; if (!v.symbols) delete v.symbols; if (!v.accent) delete v.accent; if (!v.tap_action || v.tap_action === "none") delete v.tap_action; if (!v.face_style || v.face_style === "mascot") delete v.face_style;
        this._cfg = v; this.dispatchEvent(new CustomEvent("config-changed", { detail: { config: v }, bubbles: true, composed: true }));
      });
      this.appendChild(f);
    }
    const t = lwTxt(this._hass);
    const L = { room: t.ed_room, title: t.ed_title, values: t.ed_values, compact: t.ed_compact, symbols: t.ed_symbols, accent: t.ed_accent, tap_action: t.ed_tap, face_style: t.ed_face };
    f.hass = this._hass; f.schema = this._schema(); f.computeLabel = (s) => L[s.name] || s.name;
    const tap = typeof this._cfg.tap_action === "string" ? this._cfg.tap_action : "none";
    f.data = { room: "", title: "", values: true, compact: false, symbols: false, accent: false, face_style: "mascot", ...this._cfg, tap_action: tap };
  }
}
customElements.define("luftwaechter-card", LuftwaechterCard);
customElements.define("luftwaechter-card-editor", LuftwaechterCardEditor);
window.customCards = window.customCards || [];
window.customCards.push({ type: "luftwaechter-card", name: "Luftwächter", description: "Air quality advice for one room or the whole house.", preview: false });
