/* Luftwächter Lovelace card: one room (face + one sentence + values) or a house summary.
   Usage:  type: custom:luftwaechter-card   room: Office   (omit room for the house summary) */
const LW_TXT = {
  de: { none: "Luftwächter nicht gefunden", noRoom: "Raum nicht gefunden", house: "Luftwächter", good: "gut", fair: "mittel", poor: "schlecht", unknown: "unbekannt", all: "Alle Räume gut" },
  en: { none: "Luftwächter not found", noRoom: "Room not found", house: "Luftwächter", good: "good", fair: "fair", poor: "poor", unknown: "unknown", all: "All rooms good" },
};
const LW_FACE = { good: "🙂", fair: "😐", poor: "😷", unknown: "❔" };
const LW_COL = { good: "#2e9e5b", fair: "#e8a317", poor: "#d9472b", unknown: "#7a8594" };

class LuftwaechterCard extends HTMLElement {
  constructor() { super(); this.attachShadow({ mode: "open" }); this._cfg = {}; this._hass = null; this._sig = ""; }
  setConfig(cfg) { this._cfg = cfg || {}; this._sig = ""; this._render(); }
  set hass(h) {
    this._hass = h;
    const e = this._house();
    const sig = e ? h.language + "|" + e.last_updated + "|" + JSON.stringify(this._cfg) : "none";
    if (sig !== this._sig) { this._sig = sig; this._render(); }
  }
  getCardSize() { return this._cfg.room ? 2 : 3; }
  static getStubConfig() { return {}; }
  _house() {
    const st = this._hass && this._hass.states;
    if (!st) return null;
    return Object.values(st).find((s) => s.entity_id.startsWith("sensor.") && s.attributes && Array.isArray(s.attributes.rooms) && s.attributes.summary) || null;
  }
  _t() { return LW_TXT[(this._hass && this._hass.language || "en").slice(0, 2)] || LW_TXT.en; }
  _esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
  _render() {
    const t = this._t(); const house = this._house(); const e = this._esc.bind(this);
    const css = `<style>ha-card{padding:14px 16px}.row{display:flex;align-items:center;gap:12px}.face{font-size:34px;line-height:1}h2{margin:0;font-size:16px;font-weight:600}p{margin:2px 0 0;color:var(--secondary-text-color);font-size:13px}.vals{display:flex;gap:14px;flex-wrap:wrap;margin-top:10px;font-size:13px}.v b{font-weight:600}.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}.list .item{display:flex;align-items:center;justify-content:space-between;padding:5px 0;font-size:14px;border-top:1px solid var(--divider-color,#8883)}.list .item:first-child{border-top:0}.muted{color:var(--secondary-text-color);font-size:13px}</style>`;
    let body = "";
    if (!house) body = `<div class="muted">${e(t.none)}</div>`;
    else {
      const rooms = house.attributes.rooms || [];
      const want = (this._cfg.room || "").toString().toLowerCase();
      if (want) {
        const r = rooms.find((x) => x.key.toLowerCase() === want || x.name.toLowerCase() === want);
        if (!r) body = `<div class="muted">${e(t.noRoom)}: ${e(this._cfg.room)}</div>`;
        else {
          const col = LW_COL[r.level] || LW_COL.unknown;
          const vals = (r.values || []).filter((v) => v.raw != null).map((v) => `<span class="v"><span class="dot" style="background:${LW_COL[["good", "fair", "poor"][v.level]] || LW_COL.unknown}"></span><b>${e(v.value)}</b> ${e(v.unit)}</span>`).join("");
          body = `<div class="row"><div class="face" style="filter:drop-shadow(0 0 0 ${col})">${LW_FACE[r.level] || LW_FACE.unknown}</div><div><h2>${e(r.name)} · ${e(r.headline)}</h2><p>${e(r.detail)}</p></div></div>${this._cfg.values === false ? "" : `<div class="vals">${vals}</div>`}`;
        }
      } else {
        const good = rooms.filter((r) => r.level === "good").length;
        const items = rooms.map((r) => `<div class="item"><span><span class="dot" style="background:${LW_COL[r.level] || LW_COL.unknown}"></span>${e(r.name)}</span><span class="muted">${e(r.headline)}</span></div>`).join("");
        body = `<div class="row"><div class="face">${good === rooms.length && rooms.length ? "🙂" : "😐"}</div><div><h2>${e(this._cfg.title || t.house)}</h2><p>${good === rooms.length && rooms.length ? e(t.all) : e(good + " / " + rooms.length)}</p></div></div><div class="list" style="margin-top:8px">${items}</div>`;
      }
    }
    this.shadowRoot.innerHTML = `${css}<ha-card>${body}</ha-card>`;
  }
}
customElements.define("luftwaechter-card", LuftwaechterCard);
window.customCards = window.customCards || [];
window.customCards.push({ type: "luftwaechter-card", name: "Luftwächter", description: "Air quality advice for one room or the whole house.", preview: false });
