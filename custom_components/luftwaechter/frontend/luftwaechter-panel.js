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
    attention: "Jetzt tun", nothing: "Nichts zu tun, alles in Ordnung.", rooms_n: "{a} von {n} Räumen brauchen Aufmerksamkeit", stale: "Die Daten sind möglicherweise veraltet (letztes Update vor {n} min).", silent: "Sensor meldet nichts mehr: {r}", mold: "Schimmelgefahr (hohe Luftfeuchte): {r}", avg: "Ø {c} ppm · {t} °C · {h} %", kAlerts: "Browser-Hinweise an / aus", kCb: "Farbenblind-Modus", kSize: "Textgröße", kCsv: "Verlauf als CSV speichern", kLang: "Sprache wechseln", kEnds: "Erster / letzter Raum",
    alerts: "Browser-Hinweise", alertsOn: "Browser-Hinweise: an", alertsDenied: "Browser-Hinweise sind im Browser blockiert", alertBody: "{r}: {l}", kiosk: "Kiosk-Modus", kioskOff: "Kiosk-Modus beenden", langOpt: "Sprache", langAuto: "automatisch", resetView: "Ansicht zurücksetzen", goodOf: "{g} von {n} Räumen haben gute Luft", print: "Drucken / als PDF speichern", kTitle: "Tastenkürzel", kRoom: "Raum wechseln", kNum: "Raum Nr. 1–9 wählen", kRange: "Zeitraum des Verlaufs (6 h, 24 h, 7 T)", kBack: "Zurück", kSearch: "Suchen", kSort: "Sortieren", kPin: "Raum anheften", kOnly: "Nur Probleme", kList: "Listenansicht", kCopy: "Hausübersicht kopieren", kMenu: "Menü", kRot: "Räume durchschalten", kFs: "Vollbild", kHelp: "Hilfe", swiped: "Wischen wechselt den Raum", size: "Textgröße", onbTitle: "So kommen Räume ins Panel", onb1: "Weise CO₂-, Feinstaub-, Temperatur- oder Luftfeuchte-Sensoren einem Bereich zu (Einstellungen → Bereiche).", onb2: "Der Raum erscheint automatisch, sobald ein Sensor Werte liefert.", onb3: "Optional: Gib einem Fenstersensor die Geräteklasse „Fenster“, dann bekommst du Lüftungsempfehlungen.", noHouse: "Die Integration Luftwächter wurde nicht gefunden. Einstellungen → Geräte & Dienste → Integration hinzufügen → Luftwächter.", legend: "Punkte: CO₂ · Feinstaub · Temperatur · Luftfeuchte", avgT: "Ø im Haus", ventStart: "Lüftungs-Timer starten ({n} min)", ventRun: "Lüften läuft", ventDone: "Zeit ist um: Fenster jetzt schließen", ventStop: "Abbrechen", fs: "Vollbild", fsExit: "Vollbild beenden", copyAll: "Hausstatus kopieren", trendUp: "Steigend", trendDown: "Fallend", onlyProblems: "Nur Probleme", rank: "CO₂ im Vergleich", rotate: "Räume automatisch durchschalten", csv: "CSV", shortcuts: "Tastatur: ← → Raum wechseln · Esc zurück · / suchen · S sortieren · P anheften · O nur Probleme · V Listenansicht · M Menü · R durchschalten · F Vollbild · H Hilfe", search: "Raum suchen…", noMatch: "Kein Raum gefunden.", listView: "Listenansicht", tileView: "Kachelansicht", soundOn: "Signalton bei Ablauf: an", soundOff: "Signalton bei Ablauf: aus", copyLink: "Link kopieren", mold: "Schimmelgefahr", dew: "Taupunkt", more: "Mehr", refreshNow: "Jetzt aktualisieren", cbMode: "Farbenblind-Modus (Symbole)", sinceFor: "{l} seit {t}", sortCo2: "Höchstes CO₂ zuerst", pin: "Oben anheften", unpin: "Nicht mehr anheften", pinned: "Angeheftet", copy: "Status kopieren", copied: "Kopiert", r6h: "6 h", r24h: "24 h", r7d: "7 Tage", a6h: "vor 6 h", a24h: "vor 24 h", a7d: "vor 7 Tagen", dayU: "Tg", hourU: "h",
    coffee: "☕ Gefällt dir Luftwächter? Spendiere dem Entwickler einen Kaffee (freiwillig)", helpTitle: "Was bedeuten die Messwerte?", causes: "Mögliche Ursachen", todo: "Was hilft",
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
    attention: "Do now", nothing: "Nothing to do, all good.", rooms_n: "{a} of {n} rooms need attention", stale: "Data may be outdated (last update {n} min ago).", silent: "Sensor has gone quiet: {r}", mold: "Mold risk (high humidity): {r}", avg: "Avg {c} ppm · {t} °C · {h} %", kAlerts: "Browser alerts on / off", kCb: "Colour-blind mode", kSize: "Text size", kCsv: "Save history as CSV", kLang: "Switch language", kEnds: "First / last room",
    alerts: "Browser alerts", alertsOn: "Browser alerts: on", alertsDenied: "Browser alerts are blocked in the browser", alertBody: "{r}: {l}", kiosk: "Kiosk mode", kioskOff: "Leave kiosk mode", langOpt: "Language", langAuto: "automatic", resetView: "Reset view settings", goodOf: "{g} of {n} rooms have good air", print: "Print / save as PDF", kTitle: "Keyboard shortcuts", kRoom: "Switch room", kNum: "Jump to room 1–9", kRange: "Chart range (6 h, 24 h, 7 d)", kBack: "Back", kSearch: "Search", kSort: "Sort", kPin: "Pin room", kOnly: "Only problems", kList: "List view", kCopy: "Copy house summary", kMenu: "Menu", kRot: "Rotate rooms", kFs: "Full screen", kHelp: "Help", swiped: "Swipe to change room", size: "Text size", onbTitle: "How rooms get into the panel", onb1: "Assign CO₂, fine dust, temperature or humidity sensors to an area (Settings → Areas).", onb2: "The room appears automatically as soon as a sensor reports values.", onb3: "Optional: give a window sensor the device class \"window\" to get ventilation advice.", noHouse: "The Luftwächter integration was not found. Settings → Devices & services → Add integration → Luftwächter.", legend: "Dots: CO₂ · fine dust · temperature · humidity", avgT: "House average", ventStart: "Start ventilation timer ({n} min)", ventRun: "Ventilating", ventDone: "Time is up: close the window now", ventStop: "Cancel", fs: "Full screen", fsExit: "Exit full screen", copyAll: "Copy house status", trendUp: "Rising", trendDown: "Falling", onlyProblems: "Only problems", rank: "CO₂ compared", rotate: "Rotate through rooms automatically", csv: "CSV", shortcuts: "Keyboard: ← → switch room · Esc back · / search · S sort · P pin · O only problems · V list view · M menu · R rotate · F full screen · H help", search: "Find a room…", noMatch: "No room found.", listView: "List view", tileView: "Tile view", soundOn: "Sound when time is up: on", soundOff: "Sound when time is up: off", copyLink: "Copy link", mold: "Mold risk", dew: "Dew point", more: "More", refreshNow: "Refresh now", cbMode: "Color-blind mode (symbols)", sinceFor: "{l} for {t}", sortCo2: "Highest CO₂ first", pin: "Pin to top", unpin: "Unpin", pinned: "Pinned", copy: "Copy status", copied: "Copied", r6h: "6 h", r24h: "24 h", r7d: "7 days", a6h: "6 h ago", a24h: "24 h ago", a7d: "7 days ago", dayU: "d", hourU: "h",
    coffee: "☕ Like Luftwächter? Buy the developer a coffee (optional)", helpTitle: "What do the readings mean?", causes: "Possible causes", todo: "What helps",
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
const rooms_ok = (el) => el._rooms().length > 1;
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const mem = {}; // fallback when the browser blocks localStorage (private window, kiosk profile): settings then last until the page closes
const store = {
  get(k) { try { const v = localStorage.getItem(k); if (v !== null) return v; } catch (e) { /* use memory */ } return k in mem ? mem[k] : null; },
  set(k, v) { mem[k] = v; try { localStorage.setItem(k, v); } catch (e) { /* memory only */ } },
  remove(k) { delete mem[k]; try { localStorage.removeItem(k); } catch (e) { /* ignore */ } },
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
    this._range = store.get("lw_range") || "24h";
    this._size = parseInt(store.get("lw_size") || "1", 10);
    this._alerts = store.get("lw_alerts") === "1"; this._kiosk = store.get("lw_kiosk") === "1" || /kiosk/.test(location.hash);
    this._only = store.get("lw_only") === "1";
    this._list = store.get("lw_list") === "1"; this._snd = store.get("lw_snd") === "1"; this._q = ""; this._cb = store.get("lw_cb") === "1"; try { this._pins = JSON.parse(store.get("lw_pins") || "[]"); } catch (e) { this._pins = []; } if (!Array.isArray(this._pins)) this._pins = []; this._menu = false;
    this._help = false;
    this._hist = {};
    try { const m = /[#&]room=([^&]+)/.exec(location.hash); if (m) this._sel = decodeURIComponent(m[1]); } catch (e) { /* ignore */ }
    try { const v = JSON.parse(store.get("lw_vent") || "null"); this._vent = v && v.end > Date.now() - 600000 ? v : null; } catch (e) { this._vent = null; }
    this._rot = false; this._rotTimer = null; this._wl = null;
    this._onFs = () => { this._wakelock(); this._render(); };
    this.shadowRoot.addEventListener("pointerdown", (ev) => { if (this._menu && !ev.composedPath().some((n) => n.id === "menuwrap")) this._toggleMenu(false); if (this._rot && !ev.composedPath().some((n) => n.id === "rot")) this._rotStop(false); }, true);
    this._onKey = (ev) => this._key(ev);
  }
  connectedCallback() {
    window.addEventListener("keydown", this._onKey);
    document.addEventListener("fullscreenchange", this._onFs);
    this._vtick = setInterval(() => this._ventTick(), 1000);
    this._tick = setInterval(() => { const e = this._house(), el = this.shadowRoot.querySelector(".upd"); if (e && el) { el.textContent = this._age(e, this._t()); this._staleCheck(); } }, 30000);
  }
  disconnectedCallback() { window.removeEventListener("keydown", this._onKey); document.removeEventListener("fullscreenchange", this._onFs); clearInterval(this._tick); clearInterval(this._vtick); clearInterval(this._rotTimer); try { this._wl && this._wl.release(); } catch (e) { /* ignore */ } }
  async _wakelock() { try { if (document.fullscreenElement && navigator.wakeLock) this._wl = await navigator.wakeLock.request("screen"); else if (this._wl) { await this._wl.release(); this._wl = null; } } catch (e) { /* ignore */ } }
  _rotStep() { const rs = this._rooms(); if (!rs.length) return; const i = rs.findIndex((r) => r.key === this._sel); this._select(rs[(i + 1) % rs.length].key); }
  _rotToggle() { if (this._rot) { this._rotStop(); return; } this._rot = true; this._rotTimer = setInterval(() => this._rotStep(), 12000); this._render(); }
  _rotStop(render = true) { if (!this._rot) return; this._rot = false; clearInterval(this._rotTimer); if (render) this._render(); }
  _closeHelp() { this._help = false; this._refocus = true; this._render(); }
  _ventLeft() { return this._vent ? Math.round((this._vent.end - Date.now()) / 1000) : null; }
  _fmtT(sec) { const m = Math.floor(Math.max(0, sec) / 60), r = Math.max(0, sec) % 60; return `${m}:${String(r).padStart(2, "0")}`; }
  _ventTick() {
    if (!this._vent) return;
    const left = this._ventLeft(), root = this.shadowRoot;
    if (left <= 0 && !this._vent.done) { this._vent.done = true; store.set("lw_vent", JSON.stringify(this._vent)); try { navigator.vibrate && navigator.vibrate([200, 100, 200]); } catch (e) { /* ignore */ } if (this._snd) this._beep(); this._render(); return; }
    root.querySelectorAll(".venttime").forEach((n) => { n.textContent = this._fmtT(left); });
  }
  _toggleMenu(open) {
    this._menu = open === undefined ? !this._menu : open;
    const m = this.shadowRoot.querySelector("#menu"), b = this.shadowRoot.querySelector("#more");
    if (m) m.hidden = !this._menu; if (b) b.setAttribute("aria-expanded", String(this._menu));
    if (this._menu && m) m.querySelector("button")?.focus(); else if (b && open === undefined) b.focus();
  }
  _menuItems(rooms, sel, t) {
    const b = (id, icon, label, pressed) => `<button class="mi" id="${id}"${pressed === undefined ? "" : ` aria-pressed="${pressed}"`}><span aria-hidden="true">${icon}</span> ${esc(label)}</button>`;
    const many = rooms.length > 1, ov = !sel, fs = document.fullscreenElement;
    return [ov && many ? b("only", "⚠", t.onlyProblems, this._only) : "", ov && many ? b("sort", "↕", this._sortLabel(t)) : "",
      ov && many ? b("dens", this._list ? "▦" : "☰", this._list ? t.tileView : t.listView) : "", many ? b("rot", "⟳", t.rotate, this._rot) : "",
      ov && rooms.length ? b("copyall", "⧉", t.copyAll) : "", document.fullscreenEnabled ? b("fs", fs ? "🗗" : "⛶", fs ? t.fsExit : t.fs) : "",
      b("alerts", "🔔", this._alerts ? t.alertsOn : (this._alertDenied ? t.alertsDenied : t.alerts), this._alerts), b("kiosk", "▣", this._kiosk ? t.kioskOff : t.kiosk, this._kiosk), b("lang", "🌐", `${t.langOpt}: ${(store.get("lw_lang") || "").toUpperCase() || t.langAuto}`), b("reset", "↺", t.resetView), b("print", "🖨", t.print), b("size", "Aa", t.size), b("cb", "◐", t.cbMode, this._cb), b("refresh", "↻", t.refreshNow)].join("");
  }
  _cycleLang() { const o = store.get("lw_lang") || ""; const n = { "": "de", de: "en", en: "" }[o] ?? ""; store.set("lw_lang", n); this._render(); }
  _setKiosk(on) { this._kiosk = on; store.set("lw_kiosk", on ? "1" : "0"); if (on) { this._size = 2; if (!this._rot && this._rooms().length > 1) { this._rotToggle(); return; } } else { this._size = parseInt(store.get("lw_size") || "1", 10); this._rotStop(); return; } this._render(); }
  async _toggleAlerts() {
    if (this._alerts) { this._alerts = false; store.set("lw_alerts", "0"); this._render(); return; }
    try { const p = typeof Notification === "undefined" ? "denied" : (Notification.permission === "default" ? await Notification.requestPermission() : Notification.permission); this._alerts = p === "granted"; } catch (e) { this._alerts = false; }
    store.set("lw_alerts", this._alerts ? "1" : "0"); if (!this._alerts) this._alertDenied = true; this._render();
  }
  _resetView() { ["lw_size", "lw_sort", "lw_pins", "lw_only", "lw_list", "lw_cb", "lw_lang", "lw_alerts", "lw_kiosk", "lw_room"].forEach((k) => store.remove(k)); this._size = 1; this._sort = "worst"; this._pins = []; this._only = false; this._list = false; this._cb = false; this._alerts = false; this._kiosk = false; this._sel = null; this._menu = false; this._rotStop(); }
  _nextSort() { this._sort = { worst: "name", name: "co2" }[this._sort] || "worst"; store.set("lw_sort", this._sort); this._render(); }
  _pin(key) { const i = this._pins.indexOf(key); if (i < 0) this._pins.push(key); else this._pins.splice(i, 1); store.set("lw_pins", JSON.stringify(this._pins)); this._render(); }
  _sortLabel(t) { return this._sort === "worst" ? t.sortWorst : this._sort === "co2" ? t.sortCo2 : t.sortName; }
  _sym(i) { return ["✓", "!", "✕"][i] || "–"; }
  _dur(min) { return min < 60 ? `${min} min` : `${Math.floor(min / 60)} h ${min % 60} min`; }
  _spark(r) {
    const d = r.spark; if (!d || d.length < 3) return "";
    const mn = Math.min(...d), mx = Math.max(...d), rg = Math.max(mx - mn, 100), st = 100 / (d.length - 1);
    const pts = d.map((v, i) => `${(i * st).toFixed(1)},${(20 - ((v - mn) / rg) * 18).toFixed(1)}`).join(" ");
    return `<svg class="spark" viewBox="0 0 100 22" preserveAspectRatio="none" aria-hidden="true"><polyline points="${pts}" fill="none" stroke="${this._col(r.level)}" stroke-width="2" vector-effect="non-scaling-stroke" stroke-linejoin="round"/></svg>`;
  }
  _beep() {
    try {
      const C = window.AudioContext || window.webkitAudioContext; if (!C) return; const c = new C();
      [0, 0.3, 0.6].forEach((d) => { const o = c.createOscillator(), g = c.createGain(); o.frequency.value = 880; g.gain.value = 0.15; o.connect(g); g.connect(c.destination); o.start(c.currentTime + d); o.stop(c.currentTime + d + 0.2); });
      setTimeout(() => c.close(), 1500);
    } catch (e) { /* ignore */ }
  }
  _ventStart(key, min) { this._vent = { key, end: Date.now() + min * 60000, min }; store.set("lw_vent", JSON.stringify(this._vent)); this._render(); }
  _ventStop() { this._vent = null; store.set("lw_vent", ""); this._render(); }
  _sndBtn(t) { return `<button class="tool" id="snd" aria-pressed="${this._snd}" title="${esc(this._snd ? t.soundOn : t.soundOff)}" aria-label="${esc(this._snd ? t.soundOn : t.soundOff)}">${this._snd ? "🔔" : "🔕"}</button>`; }
  _ventCard(sel, t) {
    const v = this._vent;
    if (v && v.key === sel.key) return `<div class="card vent${v.done || this._ventLeft() <= 0 ? " done" : ""}" role="status"><b>⏱ ${esc(v.done || this._ventLeft() <= 0 ? t.ventDone : t.ventRun)}</b> <span class="venttime">${esc(this._fmtT(this._ventLeft()))}</span> <button class="tool" id="ventstop">${esc(t.ventStop)}</button> ${this._sndBtn(t)}</div>`;
    if (["open", "keep_open"].includes(sel.action)) { const n = sel.ventMin || 5; return `<div class="card vent"><button class="tool" id="ventstart" data-min="${n}">⏱ ${esc(t.ventStart.replace("{n}", n))}</button> ${this._sndBtn(t)}</div>`; }
    return "";
  }
  _houseText(rooms, a, t) { return `${t.title}\n` + rooms.map((r) => `${r.name}: ${t[r.level] || t.unknown} – ${r.headline}`).join("\n") + (a.outside ? `\n${t.outside}: ${a.outside.temp} °C, ${a.outside.cond}` : ""); }
  _stats(rooms, lang) {
    const avg = (k, d) => { const x = rooms.map((r) => (r.values.find((v) => v.key === k) || {}).raw).filter((v) => v != null); if (!x.length) return null; const m = x.reduce((p, c) => p + c, 0) / x.length; const s = m.toFixed(d).replace(/^-0(\.0+)?$/, "0"); return lang === "de" ? s.replace(".", ",") : s; };
    return [["co2", 0, "ppm"], ["pm25", 0, "µg/m³"], ["temperature", 1, "°C"], ["humidity", 0, "%"]].map(([k, d, u]) => [k, avg(k, d), u]).filter((x) => x[1] != null);
  }
  _avgLine() { const a = this._house(); const x = a && a.attributes; if (!x || x.co2_avg == null || x.temp_avg == null || x.rh_avg == null) return ""; return (UI[this._lang()] || UI.en).avg.replace("{c}", x.co2_avg).replace("{t}", x.temp_avg).replace("{h}", x.rh_avg); }
  _mold() { const a = this._house(); const s = a && a.attributes.mold_rooms; return Array.isArray(s) ? s : []; }
  _silent() { const a = this._house(); const s = a && a.attributes.silent_rooms; return Array.isArray(s) ? s : []; }
  _staleLimit() { const a = this._house(); return (a && a.attributes.stale_min) || 10; }
  _staleMin() { const e = this._house(); const u = e && e.attributes.updated; return u ? Math.round((Date.now() / 1000 - u) / 60) : 0; }
  _staleCheck() { const b = this.shadowRoot.querySelector("#stale"); const m = this._staleMin(); if (b) { b.hidden = m < this._staleLimit(); b.textContent = this._t().stale.replace("{n}", m); } }
  set hass(h) {
    this._hass = h;
    const e = this._house();
    const sig = e ? h.language + "|" + e.last_updated + "|" + Object.values(h.states).filter((s) => /^(light|switch|climate|cover)\./.test(s.entity_id)).map((s) => s.state + (s.attributes && s.attributes.current_position)).join(",") : "none";
    if (sig !== this._sig) { this._sig = sig; this._render(); }
  }
  set narrow(v) { this._narrow = v; }
  set panel(v) { /* unused */ }
  _house() {
    const st = this._hass && this._hass.states;
    if (!st) return null;
    return Object.values(st).find((s) => s.entity_id.startsWith("sensor.") && s.attributes && Array.isArray(s.attributes.rooms) && s.attributes.summary) || null;
  }
  _lang() { const ov = store.get("lw_lang"); if (ov && UI[ov]) return ov; const e = this._house(), srv = ((e && e.attributes.lang) || "en").slice(0, 2), mine = ((this._hass && this._hass.language) || "").slice(0, 2); return UI[mine] ? mine : (UI[srv] ? srv : "en"); }
  _attrs() { const e = this._house(); if (!e) return {}; const a = e.attributes, l = this._lang(); return l !== a.lang && a.alt && a.alt[l] ? Object.assign({}, a, a.alt[l], { lang: l }) : a; }
  _t() { return UI[this._lang()] || UI.en; }
  _lim(k) { const l = this._attrs().limits || {}; if (k === "co2" && l.co2) return `< ${l.co2[0]} / < ${l.co2[1]} ppm`; if (k === "pm25" && l.pm25) return `< ${l.pm25[0]} / < ${l.pm25[1]} µg/m³`; return LIM[k]; }
  _scale(k) {
    const l = this._attrs().limits || {};
    if (k === "co2" && l.co2) { const [g, f] = l.co2, mx = Math.max(2000, Math.round(f * 1.35)); return [400, mx, [[400, g, 0], [g, f, 1], [f, mx, 2]]]; }
    if (k === "pm25" && l.pm25) { const [g, f] = l.pm25, mx = Math.max(80, Math.round(f * 1.6)); return [0, mx, [[0, g, 0], [g, f, 1], [f, mx, 2]]]; }
    return SCALE[k];
  }
  _col(level) { const i = ["good", "fair", "poor"].indexOf(level); return i < 0 ? GREY : COL[i]; }
  _lcol(i) { return i == null ? GREY : COL[i] || GREY; }
  _rooms() {
    const e = this._house(); if (!e) return [];
    const rooms = this._attrs().rooms.slice();
    if (this._sort === "worst") {
      const rank = (r) => ({ poor: 0, fair: 1, good: 2 }[r.level] ?? 3);
      rooms.sort((a, b) => rank(a) - rank(b) || a.name.localeCompare(b.name));
    } else if (this._sort === "co2") {
      const co2 = (r) => { const v = r.values.find((x) => x.key === "co2"); return v && v.raw != null ? v.raw : -1; };
      rooms.sort((a, b) => co2(b) - co2(a) || a.name.localeCompare(b.name));
    } else rooms.sort((a, b) => a.name.localeCompare(b.name));
    const pin = (r) => (this._pins.includes(r.key) ? 0 : 1);
    rooms.sort((a, b) => pin(a) - pin(b));
    return rooms;
  }
  _select(key) { this._sel = key; store.set("lw_room", key || ""); try { history.replaceState(null, "", key ? "#room=" + encodeURIComponent(key) : location.pathname + location.search); } catch (e) { /* ignore */ } this._render(); }
  _key(ev) {
    if (this.offsetParent === null && !this.isConnected) return;
    if (ev.key === "Escape" && this._menu) { this._toggleMenu(false); this.shadowRoot.querySelector("#more")?.focus(); return; }
    if (ev.key === "Escape") { if (this._help) { this._closeHelp(); } else if (this._sel) this._select(null); return; }
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const tg = ev.composedPath && ev.composedPath()[0];
    if (tg && (/^(INPUT|TEXTAREA|SELECT)$/.test(tg.tagName) || tg.isContentEditable)) return;
    const k = (ev.key || "").toLowerCase();
    if (k === "h" || ev.key === "?") { if (this._help) this._closeHelp(); else { this._help = true; this._render(); this.shadowRoot.querySelector("#hclose")?.focus(); } return; }
    if (this._help && ev.key === "Tab") { ev.preventDefault(); this.shadowRoot.querySelector("#hclose")?.focus(); return; }
    if (!this._help) {
      if (k === "s" && !this._sel) { this._nextSort(); return; }
      if (k === "p" && this._sel) { this._pin(this._sel); return; }
      if (k === "o" && !this._sel) { this._only = !this._only; store.set("lw_only", this._only ? "1" : "0"); this._render(); return; }
      if (k === "/" && !this._sel) { const qi = this.shadowRoot.querySelector("#q"); if (qi) { ev.preventDefault(); qi.focus(); return; } }
      if (k === "k") { this._setKiosk(!this._kiosk); return; }
      if (k === "l") { this._cycleLang(); return; }
      if (k === "a") { this._toggleAlerts(); return; }
      if (k === "b") { this._cb = !this._cb; store.set("lw_cb", this._cb ? "1" : "0"); this._render(); return; }
      if (k === "e" && this._sel) { this.shadowRoot.querySelector("#csv")?.click(); return; }
      if (ev.key === "+" || ev.key === "=" || ev.key === "-") { this._size = Math.max(0, Math.min(2, this._size + (ev.key === "-" ? -1 : 1))); store.set("lw_size", String(this._size)); this._render(); return; }
      if (ev.key === "Home" || ev.key === "End") { const rs = this._rooms(), r = ev.key === "Home" ? rs[0] : rs[rs.length - 1]; if (r) { ev.preventDefault(); this._select(r.key); } return; }
      if (/^[1-9]$/.test(ev.key)) { const rs = this._rooms(), r = rs[Number(ev.key) - 1]; if (r) { this._select(r.key); } return; }
      if (k === "t" && this._sel) { const order = ["6h", "24h", "7d"]; this._range = order[(order.indexOf(this._range) + 1) % order.length]; store.set("lw_range", this._range); this._render(); return; }
      if (k === "c" && !this._sel) { this.shadowRoot.querySelector("#copyall")?.click(); return; }
      if (k === "m") { this._toggleMenu(); return; }
      if (k === "v" && !this._sel) { this._list = !this._list; store.set("lw_list", this._list ? "1" : "0"); this._render(); return; }
      if (k === "r" && rooms_ok(this)) { this._rotToggle(); return; }
      if (k === "f") { try { document.fullscreenElement ? document.exitFullscreen() : this.requestFullscreen(); } catch (e) { /* ignore */ } return; }
    }
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
  _histKey(room, key) { return room.key + "|" + key + "|" + this._range; }
  _hours() { return { "6h": 6, "24h": 24, "7d": 168 }[this._range] || 24; }
  async _loadHist(room, key) {
    const hk = this._histKey(room, key); const c = this._hist[hk];
    if (c && (c.loading || Date.now() - c.at < 300000)) return;
    const ids = (room.sources && room.sources[key === "pm25" ? "pm25" : key === "co2" ? "carbon_dioxide" : key]) || [];
    this._hist[hk] = { loading: true, at: Date.now() };
    if (!ids.length || !this._hass.callWS) { this._hist[hk] = { error: true, at: Date.now() }; return this._render(); }
    try {
      const hrs = this._hours(); const end = new Date(), start = new Date(end.getTime() - hrs * 3600 * 1000);
      const res = await this._hass.callWS({ type: "history/history_during_period", start_time: start.toISOString(), end_time: end.toISOString(), entity_ids: ids, minimal_response: true, no_attributes: true, significant_changes_only: false });
      const N = 96, t0 = start.getTime() / 1000, step = (hrs * 3600) / N;
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
      this._hist[hk] = { data: avg, at: Date.now(), step };
    } catch (e) { console.error("lw history", e); this._hist[hk] = { error: true, at: Date.now() }; }
    this._render();
  }
  _chart(room, t) {
    this._chartMeta = null;
    const key = this._chartKey, hk = this._histKey(room, key), h = this._hist[hk];
    const tabs = KEYS.map((k) => `<button class="chip ${k === key ? "sel" : ""}" data-chart="${k}" aria-pressed="${k === key}">${esc(t[k])}</button>`).join("") +
      `<span class="rsp"></span>` + ["6h", "24h", "7d"].map((r) => `<button class="chip ${r === this._range ? "sel" : ""}" data-range="${r}" aria-pressed="${r === this._range}">${esc(t["r" + r])}</button>`).join("") + `<button class="chip" id="csv" title="CSV" aria-label="CSV">⭳ ${esc(t.csv)}</button>`;
    let body;
    if (!h || h.loading) body = `<div class="muted">${esc(t.loading)}</div>`;
    else if (h.error || !h.data || !h.data.some((v) => v != null)) body = `<div class="muted">${esc(t.nohist)}</div>`;
    else {
      const d = h.data, sc = this._scale(key); const vals = d.filter((v) => v != null);
      const mn = Math.min(...vals), mx = Math.max(...vals);
      const lo = Math.min(sc[0], mn), hi = Math.max(sc[1] * (key === "co2" || key === "pm25" ? 0.6 : 1), mx);
      const W = 600, H = 150, X = (i) => (i / (d.length - 1)) * W, Y = (v) => H - ((v - lo) / (hi - lo)) * H;
      const bands = sc[2].map(([a, b, l]) => { const y1 = Math.max(0, Y(Math.min(b, hi))), y2 = Math.min(H, Y(Math.max(a, lo))); return y2 > y1 ? `<rect x="0" y="${y1.toFixed(1)}" width="${W}" height="${(y2 - y1).toFixed(1)}" fill="${COL[l]}" opacity=".13"/>` : ""; }).join("");
      let path = "", pen = false;
      d.forEach((v, i) => { if (v == null) { pen = false; return; } path += `${pen ? "L" : "M"}${X(i).toFixed(1)},${Y(v).toFixed(1)} `; pen = true; });
      const unit = room.values.find((v) => v.key === key)?.unit || "";
      const fv = (v) => (key === "temperature" ? v.toFixed(1) : String(Math.round(v)));
      body = `<div class="chartwrap"><svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" role="img" aria-label="${esc(t[key])} ${esc(t.history)}">${bands}<path d="${path}" fill="none" stroke="var(--primary-text-color,#222)" stroke-width="2" vector-effect="non-scaling-stroke"/><line id="cur" x1="0" x2="0" y1="0" y2="${H}" stroke="var(--primary-color,#03a9f4)" stroke-width="1.5" vector-effect="non-scaling-stroke" visibility="hidden"/></svg><span class="ylab" style="top:2px">${esc(fv(hi))}</span><span class="ylab" style="top:${H - 18}px">${esc(fv(lo))}</span><i class="nowdot" style="top:${(Y(d[d.length - 1] ?? lo) - 4).toFixed(0)}px" aria-hidden="true"></i>
        <div class="axis"><span>${esc(t["a" + this._range])}</span><span id="readout" aria-live="off">${esc(t.min)} ${mn.toFixed(key === "temperature" ? 1 : 0)} · ${esc(t.max)} ${mx.toFixed(key === "temperature" ? 1 : 0)} ${esc(unit)}</span><span>${esc(t.now_)}</span></div></div>`;
      this._chartMeta = { d, unit, key, mn, mx, t, step: h.step || 900, end: h.at, room: room.key };
    }
    return `<div class="card"><h3>${esc(t.history.replace("(24 h)", "").replace(/\s*$/, ""))}</h3><div class="chips">${tabs}</div>${body}</div>`;
  }
  _rank(rooms, t) {
    const rows = rooms.map((r) => [r, r.values.find((v) => v.key === "co2")]).filter(([, v]) => v && v.raw != null).sort((a, b) => b[1].raw - a[1].raw);
    if (rows.length < 2) return "";
    const sc = this._scale("co2"), span = sc[1] - sc[0];
    return `<div class="card rank"><h3>${esc(t.rank)}</h3>${rows.map(([r, v]) => `<button class="link rrow" data-room="${esc(r.key)}"><span>${esc(r.name)}</span><span class="rbar"><i style="width:${Math.max(3, Math.min(100, ((v.raw - sc[0]) / span) * 100)).toFixed(0)}%;background:${this._lcol(v.level)}"></i></span><b>${esc(v.value)} ppm</b></button>`).join("")}</div>`;
  }
  _gauge(v) {
    const sc = this._scale(v.key); if (!sc || v.raw == null) return "";
    const [a, b, segs] = sc; const pos = Math.max(0, Math.min(100, ((v.raw - a) / (b - a)) * 100));
    const parts = segs.map(([f, to, l]) => `<i style="left:${((f - a) / (b - a)) * 100}%;width:${((to - f) / (b - a)) * 100}%;background:${COL[l]}"></i>`).join("");
    return `<div class="gauge" aria-hidden="true">${parts}<b style="left:${pos}%"></b></div>`;
  }
  _problems(room, t) {
    const rows = room.values.filter((v) => v.level >= 1 && v.raw != null).sort((a, b) => b.level - a.level).map((v) => {
      const sc = this._scale(v.key); let dir = "";
      if (v.key === "temperature" || v.key === "humidity") dir = v.raw < (v.key === "temperature" ? 17 : 30) ? t.tooLow : t.tooHigh;
      return `<li><span style="color:${COL[v.level]}">${LVLICON[v.level]}</span> <b>${esc(t[v.key])}</b> ${esc(v.value)} ${esc(v.unit)} ${v.level === 2 ? esc(t.isPoor) : esc(t.isFair)}${dir ? " (" + esc(dir) + ")" : ""} <small>${esc(t.limit)} ${esc(this._lim(v.key))}</small></li>`;
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
  _keysTable(t) {
    const rows = [["← →", t.kRoom], ["1–9", t.kNum], ["+ −", t.kSize], ["A", t.kAlerts], ["B", t.kCb], ["E", t.kCsv], ["Home · End", t.kEnds], ["T", t.kRange], ["L", t.kLang], ["Esc", t.kBack], ["/", t.kSearch], ["S", t.kSort], ["P", t.kPin], ["O", t.kOnly], ["V", t.kList], ["C", t.kCopy], ["M", t.kMenu], ["R", t.kRot], ["F", t.kFs], ["H · ?", t.kHelp]];
    return `<section class="keys"><h3>${esc(t.kTitle)}</h3><table>${rows.map(([k, d]) => `<tr><th scope="row"><kbd>${esc(k)}</kbd></th><td>${esc(d)}</td></tr>`).join("")}</table></section>`;
  }
  _helpDlg(t) {
    if (!this._help) return "";
    return `<div class="ovl" id="ovl"><div class="dlg" role="dialog" aria-modal="true" aria-label="${esc(t.helpTitle)}"><div class="dh"><h2>${esc(t.helpTitle)}</h2><button class="x" id="hclose" aria-label="${esc(t.close)}">✕</button></div>
      ${KEYS.map((k) => `<section><h3>${esc(t[k])} <small>${esc(this._lim(k))}</small></h3><p>${esc(t[HELPKEY[k][0]])}</p><p><b>${esc(t.causes)}:</b> ${esc(t[HELPKEY[k][1]])}</p><p><b>${esc(t.todo)}:</b> ${esc(t[HELPKEY[k][2]])}</p></section>`).join("")}${this._keysTable(t)}<p style="margin-top:14px"><a style="color:var(--primary-color,#03a9f4);text-decoration:underline" href="https://buymeacoffee.com/dstasiak" target="_blank" rel="noopener noreferrer">${esc(t.coffee)}</a></p></div></div>`;
  }
  _age(e, t) {
    const u = e.attributes.updated; if (!u) return "";
    const m = Math.max(0, Math.round((Date.now() / 1000 - u) / 60));
    return `${t.updated}: ${m < 1 ? t.now : t.ago.replace("{n}", m)}`;
  }
  _render() {
    const t = this._t(), e = this._house(), root = this.shadowRoot;
    const css = `:host{display:block;min-height:100%;background:var(--primary-background-color,#fff);color:var(--primary-text-color,#222);font-family:var(--paper-font-body1_-_font-family,system-ui,sans-serif)}
*{box-sizing:border-box}.wrap{max-width:1000px;margin:0 auto;padding:16px;font-size:${[14, 16, 19][this._size] || 16}px}
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
.dots{display:flex;gap:5px;margin-top:10px}.dots i{width:18px;height:6px;border-radius:3px;display:block}
.sum{margin-top:0;margin-bottom:12px}.todo{list-style:none;margin:0 0 6px;padding:0;display:grid;gap:4px}.link{border:0;background:none;cursor:pointer;text-align:left;padding:4px 0}.link:hover{text-decoration:underline}
.rsp{flex:1}.stale{background:#b36b0022;border:1px solid #b36b00;border-radius:10px;padding:8px 12px;margin-bottom:12px;font-size:13px}
.warn{margin-top:10px;font-size:13px;color:#b36b00}.out{display:flex;gap:12px;align-items:center}
.ovl{position:fixed;inset:0;background:#0009;display:flex;align-items:center;justify-content:center;padding:16px;z-index:10}.dlg{background:var(--card-background-color,#fff);border-radius:16px;max-width:620px;max-height:90vh;overflow:auto;padding:18px;width:100%}
.dh{display:flex;justify-content:space-between;align-items:center}.dh h2{margin:0;font-size:18px}.x{border:0;background:none;font-size:20px;cursor:pointer}.dlg section{margin-top:14px}.dlg p{margin:4px 0;font-size:14px}
.tile{position:relative;display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-start}.tile>*{max-width:100%}.pill{position:absolute;top:10px;right:10px;border-radius:10px;padding:1px 8px;font-size:11px;color:#fff}.tile b{padding-right:62px}
.stats{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px}.stats span{background:var(--card-background-color,#f4f6f8);border-radius:14px;padding:4px 12px;font-size:13px}.stats em{font-style:normal;opacity:.7;margin-right:4px}
.legend{font-size:12px;margin:10px 2px 0}.vent{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.venttime{font-size:22px;font-variant-numeric:tabular-nums}.vent.done{border:2px solid #d9472b}
.tool[aria-pressed=true]{background:var(--primary-color,#03a9f4);color:#fff;border-color:transparent}
header{position:sticky;top:0;z-index:5;background:var(--primary-background-color,#fff);padding:8px 0;margin-bottom:6px}
.chartwrap{position:relative}.ylab{position:absolute;left:4px;font-size:11px;opacity:.7;pointer-events:none;background:var(--card-background-color,#f4f6f8);border-radius:4px;padding:0 3px}.nowdot{position:absolute;right:-4px;width:9px;height:9px;border-radius:50%;background:var(--primary-color,#03a9f4);border:2px solid var(--card-background-color,#fff);pointer-events:none}
.mini{opacity:.8;font-size:12px;margin-top:4px}.rank{margin-top:12px}.rrow{display:grid;grid-template-columns:minmax(70px,26%) 1fr auto;gap:10px;align-items:center;width:100%;padding:5px 0}.rbar{display:block;height:10px;border-radius:5px;background:#8882;overflow:hidden}.rbar i{display:block;height:100%;border-radius:5px}
.onb ol{margin:8px 0 0;padding-left:20px;display:grid;gap:6px}
.tiles.list{grid-template-columns:1fr}.tiles.list .tile{flex-direction:row;flex-wrap:wrap;align-items:center;gap:2px 14px}.tiles.list .tile b{padding-right:0;min-width:120px}.tiles.list .dots{margin:0 0 0 auto}.tiles.list .pill{position:static}
.search{width:100%;margin:0 0 10px;padding:8px 12px;border-radius:18px;border:1px solid var(--divider-color,#8884);background:var(--card-background-color,#f4f6f8);color:inherit;font:inherit}
.mold{color:#d9472b}
.menuwrap{position:relative}.menu{position:absolute;right:0;top:calc(100% + 6px);z-index:20;min-width:250px;background:var(--card-background-color,#fff);border:1px solid var(--divider-color,#8884);border-radius:14px;padding:6px;display:grid;gap:2px;box-shadow:0 8px 24px #0006}
.mi{border:0;background:none;text-align:left;padding:9px 12px;border-radius:10px;cursor:pointer;display:flex;gap:10px;align-items:center}.mi:hover{background:var(--secondary-background-color,#e8ebee)}.mi span{width:20px;text-align:center}.mi[aria-pressed=true]::after{content:"✓";margin-left:auto;color:var(--primary-color,#03a9f4)}
.spark{display:block;width:100%;height:22px;margin-top:6px}.tiles.list .spark{width:110px;margin:0}
.dots.cbd{gap:6px}.dots.cbd i{width:20px;height:20px;border-radius:6px;font-style:normal;font-size:12px;line-height:20px;text-align:center;color:#fff;font-weight:700}.val small .sym{font-weight:700;margin-right:4px}[hidden]{display:none!important}
@media (forced-colors:active){.tile{border:2px solid CanvasText!important}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
.keys table{border-collapse:collapse;width:100%}.keys th{text-align:left;white-space:nowrap;padding:3px 10px 3px 0;font-weight:400}.keys td{padding:3px 0}kbd{font:inherit;font-size:.85em;border:1px solid var(--divider-color,#8886);border-radius:5px;padding:1px 6px;background:var(--card-background-color,#f4f6f8)}
.kiosk header .tool{opacity:.3}.kiosk header .tool:hover,.kiosk header .tool:focus-visible{opacity:1}.kiosk #help,.kiosk #ventpill,.kiosk #q{display:none}
@media print{.menuwrap,.tool,.back,#ovl,.chips{display:none!important}.wrap{max-width:none}}
@media (prefers-reduced-motion:no-preference){.tile,.dev,.chip{transition:filter .15s}}`;
    if (!e) { const has = this._hass && this._hass.states && Object.keys(this._hass.states).length > 5; root.innerHTML = `<style>${css}</style><div class="wrap" role="main">${has ? `<div class="card">${esc(t.noHouse)}</div>` : "<p>…</p>"}</div>`; return; }
    const a = this._attrs(), rooms = this._rooms();
    const sel = rooms.find((r) => r.key === this._sel);
    let body = "";
    if (!rooms.length) body = `<div class="card onb"><h3>${esc(t.onbTitle)}</h3><p class="muted">${esc(t.none)}</p><ol><li>${esc(t.onb1)}</li><li>${esc(t.onb2)}</li><li>${esc(t.onb3)}</li></ol></div>`;
    else if (!sel) {
      const todo = rooms.filter((r) => ["open", "close", "wait", "keep_open"].includes(r.action) || r.level === "poor" || r.level === "fair");
      const attn = rooms.filter((r) => r.level === "poor" || r.level === "fair").length;
      const goodN = rooms.filter((r) => r.level === "good").length;
      const sum = `<div class="card sum"><h3>${esc(t.attention)}</h3>${rooms.length > 1 ? `<p class="muted goodof">${esc(t.goodOf.replace("{g}", goodN).replace("{n}", rooms.length))}</p>` : ""}${this._avgLine() ? `<p class="muted" id="avg">${esc(this._avgLine())}</p>` : ""}${todo.length ? `<ul class="todo">${todo.map((r) => `<li><button class="link" data-room="${esc(r.key)}"><span>${ICON[r.action] && r.action !== "keep_closed" ? ICON[r.action] : LVLICON[["good", "fair", "poor"].indexOf(r.level)] || "❔"}</span> <b>${esc(r.name)}</b>: ${esc(r.headline)}</button></li>`).join("")}</ul><p class="muted">${esc(t.rooms_n.replace("{a}", attn).replace("{n}", rooms.length))}</p>` : `<p class="muted">✅ ${esc(t.nothing)}</p>`}</div>`;
      const stats = this._stats(rooms, a.lang);
      const shown = this._only ? rooms.filter((r) => r.level !== "good") : rooms;
      body = sum + `<div class="stats" aria-label="${esc(t.avgT)}">${stats.map(([k, v, u]) => `<span><em>${esc(t[k])} Ø</em>${esc(v)} ${esc(u)}</span>`).join("")}</div>${shown.length ? "" : `<p class="muted">✅ ${esc(t.nothing)}</p>`}${rooms.length >= 6 ? `<input class="search" id="q" type="search" value="${esc(this._q)}" placeholder="${esc(t.search)}" aria-label="${esc(t.search)}">` : ""}<p class="muted" id="nomatch" hidden>${esc(t.noMatch)}</p><div class="tiles${this._list ? " list" : ""}">${shown.map((r) => {
        const bad = r.values.filter((v) => v.level >= 1 && v.raw != null).sort((x, y) => y.level - x.level)[0];
        const co2 = r.values.find((v) => v.key === "co2");
        return `<button class="tile" data-name="${esc(r.name.toLowerCase())}" data-room="${esc(r.key)}" style="border-color:${this._col(r.level)}" aria-label="${esc(r.name)}: ${esc(t[r.level] || t.unknown)}" title="${esc(r.headline)} · ${esc(r.detail)}">
          <b>${this._pins.includes(r.key) ? "★ " : ""}${esc(r.name)}</b><span class="pill" title="${r.since >= 2 ? esc(t.sinceFor.replace("{l}", t[r.level] || t.unknown).replace("{t}", this._dur(r.since))) : ""}" style="background:${this._col(r.level)}">${esc(t[r.level] || t.unknown)}</span><small>${LVLICON[["good", "fair", "poor"].indexOf(r.level)] || "❔"} ${esc(r.headline)}</small>
          ${bad ? `<small style="color:${COL[bad.level]}">${esc(t[bad.key])}: ${esc(bad.value)} ${esc(bad.unit)}</small>` : ""}<small class="mini">${r.values.filter((v) => v.raw != null).map((v) => esc(v.value) + "\u00a0" + esc(v.unit)).join(" · ")}</small>${r.trend === "up" || r.trend === "down" ? `<small>${r.trend === "up" ? "↗" : "↘"} ${esc(t[r.trend === "up" ? "trendUp" : "trendDown"])}</small>` : ""}${r.mold ? `<small class="mold">💧 ${esc(t.mold)}</small>` : ""}${this._spark(r)}<div class="dots${this._cb ? " cbd" : ""}" aria-hidden="true">${r.values.map((v) => `<i title="${esc(t[v.key])}: ${esc(v.value)} ${esc(v.unit)}" style="background:${this._lcol(v.level)}">${this._cb ? this._sym(v.level) : ""}</i>`).join("")}</div></button>`;
      }).join("")}</div><p class="muted legend">${esc(t.legend)}</p>${this._rank(rooms, t)}`;
    } else {
      const li = rooms.findIndex((r) => r.key === sel.key);
      body = `<div class="nav"><button class="back" id="back">← ${esc(t.back)}</button><span class="sp"></span><button class="tool" id="pin" aria-pressed="${this._pins.includes(sel.key)}" title="${esc(this._pins.includes(sel.key) ? t.unpin : t.pin)}">${this._pins.includes(sel.key) ? "★ " + esc(t.pinned) : "☆ " + esc(t.pin)}</button><button class="tool" id="link">${esc(t.copyLink)}</button><button class="tool" id="copy">${esc(t.copy)}</button><button class="tool" id="prev" aria-label="${esc(t.prev)}">‹</button><button class="tool" id="next" aria-label="${esc(t.next)}">›</button></div>
      <div class="card"><div class="head"><span class="big">${["keep_closed", "unknown"].includes(sel.action) && LVLICON[["good", "fair", "poor"].indexOf(sel.level)] ? LVLICON[["good", "fair", "poor"].indexOf(sel.level)] : ICON[sel.action] || ""}</span><div><h2>${esc(sel.name)} · ${esc(sel.headline)}<span class="badge" style="background:${this._col(sel.level)}">${esc(t[sel.level] || t.unknown)}</span></h2><p>${esc(sel.detail)}</p>${sel.trend === "up" || sel.trend === "down" ? `<p class="muted">${sel.trend === "up" ? "↗" : "↘"} ${esc(t[sel.trend === "up" ? "trendUp" : "trendDown"])}</p>` : ""}${sel.since >= 2 ? `<p class="muted">⏳ ${esc(t.sinceFor.replace("{l}", t[sel.level] || t.unknown).replace("{t}", this._dur(sel.since)))}</p>` : ""}</div></div>${sel.warn ? `<div class="warn">${esc(sel.warn)}</div>` : ""}</div>${this._ventCard(sel, t)}
      <div class="cols"><div><div class="card"><h3>${esc(t.problems)}</h3>${this._problems(sel, t)}</div>
        <div class="card"><h3>${esc(t.values)}</h3><div class="vals">${sel.values.map((v) => `<div class="val" style="border-color:${this._lcol(v.level)}" title="${esc(t.limits)}: ${esc(this._lim(v.key))}"><small>${this._cb ? `<span class="sym">${this._sym(v.level)}</span>` : ""}${esc(t[v.key])}</small><b>${esc(v.value)}</b> <i>${esc(v.unit)}</i>${this._gauge(v)}</div>`).join("")}</div>${sel.dew ? `<p class="muted" style="margin-top:8px">${esc(t.dew)}: ${esc(sel.dew)} °C${sel.mold ? ` · <span class="mold">💧 ${esc(t.mold)}</span>` : ""}</p>` : ""}</div></div>
        <div>${this._chart(sel, t)}${this._devices(sel, t)}</div></div>`;
      this._pendingHist = sel;
    }
    const o = a.outside;
    const out = o ? `<div class="card out"><span class="big">${esc(o.icon)}</span><div><b>${esc(t.outside)}: ${esc(o.temp)} °C, ${esc(o.cond)}</b><br><small>${esc(t.wind)} ${esc(o.wind)} km/h ${esc(o.windDir)}${o.hum && o.hum !== "–" ? " · " + esc(o.hum) + " %" : ""}</small><br><small>${esc(o.tip)}</small></div></div>` : "";
    root.innerHTML = `<style>${css}</style><div class="wrap" role="main"><header><span class="dot" style="background:${this._col(e.state)}"></span><h1 aria-live="polite">${esc(t.title)} · ${esc(t[e.state] || t.unknown)}</h1><span class="upd">${esc(this._age(e, t))}</span>
      ${this._vent && (!sel || sel.key !== this._vent.key) ? `<button class="tool" id="ventpill" data-room="${esc(this._vent.key)}">⏱ <span class="venttime">${esc(this._fmtT(this._ventLeft()))}</span></button>` : ""}<span class="menuwrap" id="menuwrap"><button class="tool" id="more" aria-haspopup="true" aria-expanded="${this._menu}">⋯ ${esc(t.more)}</button><div class="menu" id="menu" ${this._menu ? "" : "hidden"}>${this._menuItems(rooms, sel, t)}</div></span><button class="tool" id="help" aria-label="${esc(t.help)}">? ${esc(t.help)}</button></header><div class="stale" id="stale" role="status" ${this._staleMin() < this._staleLimit() ? "hidden" : ""}>${esc(t.stale.replace("{n}", this._staleMin()))}</div><div class="stale" id="silent" role="status" ${this._silent().length ? "" : "hidden"}>⚠ ${esc(t.silent.replace("{r}", this._silent().join(", ")))}</div><div class="stale" id="mold" role="status" ${this._mold().length ? "" : "hidden"}>💧 ${esc(t.mold.replace("{r}", this._mold().join(", ")))}</div>${body}${out}${this._helpDlg(t)}</div>`;
    const q = (s) => root.querySelector(s), qa = (s) => root.querySelectorAll(s);
    if (this._refocus) { this._refocus = false; q("#help")?.focus(); }
    qa(".tile").forEach((b) => b.addEventListener("click", () => this._select(b.dataset.room)));
    try { const n = a.attention || 0, tot = a.total || rooms.length; document.title = (this._sel && rooms.find((r) => r.key === this._sel)) ? `Luftwächter · ${rooms.find((r) => r.key === this._sel).name}` : rooms.length ? `Luftwächter · ${n ? (this._lang() === "de" ? `${n} von ${tot} brauchen Aufmerksamkeit` : `${n} of ${tot} need attention`) : (this._lang() === "de" ? "Alles gut" : "All good")}` : "Luftwächter"; } catch (er) { /* ignore */ }
    if (!this._live) { this._live = document.createElement("div"); this._live.setAttribute("aria-live", "polite"); this._live.setAttribute("role", "status"); this._live.style.cssText = "position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden"; }
    root.appendChild(this._live);
    const lv = {}; rooms.forEach((r) => { lv[r.key] = r.level; });
    if (this._lvPrev) { const ch = rooms.filter((r) => this._lvPrev[r.key] && this._lvPrev[r.key] !== r.level); if (ch.length) this._live.textContent = ch.map((r) => `${r.name}: ${t[r.level] || t.unknown}`).join(". "); }
    if (this._alerts && this._lvPrev && document.hidden && typeof Notification !== "undefined" && Notification.permission === "granted") {
      rooms.filter((r) => r.level === "poor" && this._lvPrev[r.key] && this._lvPrev[r.key] !== "poor").forEach((r) => { try { new Notification("Luftwächter", { body: t.alertBody.replace("{r}", r.name).replace("{l}", t.poor || "Poor"), tag: "lw-" + r.key }); } catch (er) { /* ignore */ } });
    }
    this._lvPrev = lv;
    this.shadowRoot.querySelector(".wrap")?.classList.toggle("kiosk", !!this._kiosk);
    const wrap = q(".wrap");
    if (wrap && sel && rooms.length > 1) {
      let x0 = null, y0 = 0;
      wrap.addEventListener("pointerdown", (ev) => { if (ev.pointerType === "touch") { x0 = ev.clientX; y0 = ev.clientY; } });
      wrap.addEventListener("pointerup", (ev) => { if (x0 === null) return; const dx = ev.clientX - x0, dy = ev.clientY - y0; x0 = null; if (Math.abs(dx) > 70 && Math.abs(dx) > 2 * Math.abs(dy)) { const rs = this._rooms(); const i = rs.findIndex((r) => r.key === this._sel); this._select(rs[(i + (dx < 0 ? 1 : rs.length - 1)) % rs.length].key); } });
    }
    q("#back")?.addEventListener("click", () => this._select(null));
    const step = (d) => { const rs = this._rooms(); const i = rs.findIndex((r) => r.key === this._sel); this._select(rs[(i + d + rs.length) % rs.length].key); };
    q("#prev")?.addEventListener("click", () => step(-1)); q("#next")?.addEventListener("click", () => step(1));
    q("#sort")?.addEventListener("click", () => this._nextSort());
    q("#pin")?.addEventListener("click", () => this._pin(sel.key));
    q("#only")?.addEventListener("click", () => { this._only = !this._only; store.set("lw_only", this._only ? "1" : "0"); this._render(); });
    q("#size")?.addEventListener("click", () => { this._size = (this._size + 1) % 3; store.set("lw_size", String(this._size)); this._render(); });
    q("#copy")?.addEventListener("click", async (ev) => { const r = sel; const txt = `${r.name}: ${r.headline}. ${r.detail}\n` + r.values.map((v) => `${t[v.key]} ${v.value} ${v.unit}`).join(", "); try { await navigator.clipboard.writeText(txt); ev.target.textContent = t.copied + " ✓"; } catch (e) { ev.target.textContent = "✗"; } });
    qa("[data-range]").forEach((b) => b.addEventListener("click", () => { this._range = b.dataset.range; store.set("lw_range", this._range); this._render(); }));
    qa(".link[data-room]").forEach((b) => b.addEventListener("click", () => this._select(b.dataset.room)));
    q("#ventstart")?.addEventListener("click", (ev) => this._ventStart(sel.key, parseInt(ev.currentTarget.dataset.min, 10) || 5));
    q("#ventstop")?.addEventListener("click", () => this._ventStop());
    q("#ventpill")?.addEventListener("click", (ev) => this._select(ev.currentTarget.dataset.room));
    q("#rot")?.addEventListener("click", () => this._rotToggle());
    q("#more")?.addEventListener("click", () => this._toggleMenu());
    q("#menu")?.addEventListener("click", () => { this._menu = false; }, true);
    q("#cb")?.addEventListener("click", () => { this._cb = !this._cb; store.set("lw_cb", this._cb ? "1" : "0"); this._render(); });
    q("#alerts")?.addEventListener("click", () => this._toggleAlerts());
    q("#kiosk")?.addEventListener("click", () => { this._toggleMenu(false); this._setKiosk(!this._kiosk); });
    q("#lang")?.addEventListener("click", () => this._cycleLang());
    q("#reset")?.addEventListener("click", () => { this._resetView(); this._render(); });
    q("#print")?.addEventListener("click", () => { this._toggleMenu(false); try { window.print(); } catch (e) { /* ignore */ } });
    q("#refresh")?.addEventListener("click", () => { try { this._hass.callService("luftwaechter", "refresh", {}); } catch (e) { /* ignore */ } });
    q("#dens")?.addEventListener("click", () => { this._list = !this._list; store.set("lw_list", this._list ? "1" : "0"); this._render(); });
    q("#snd")?.addEventListener("click", () => { this._snd = !this._snd; store.set("lw_snd", this._snd ? "1" : "0"); if (this._snd) this._beep(); this._render(); });
    q("#link")?.addEventListener("click", async (ev) => { const b = ev.currentTarget; try { await navigator.clipboard.writeText(location.origin + location.pathname + "#room=" + encodeURIComponent(sel.key)); b.textContent = t.copied + " ✓"; } catch (er) { b.textContent = "✗"; } });
    const filt = () => { const v = this._q.trim().toLowerCase(); let n = 0; qa(".tile").forEach((b) => { const hide = !!v && !b.dataset.name.includes(v); b.hidden = hide; if (!hide) n++; }); const nm = q("#nomatch"); if (nm) nm.hidden = n > 0 || !v; };
    q("#q")?.addEventListener("input", (ev) => { this._q = ev.target.value; filt(); }); filt();
    q("#csv")?.addEventListener("click", () => {
      const m = this._chartMeta; if (!m || !sel || m.room !== sel.key) return;
      const rows = ["time,value"].concat(m.d.map((v, i) => `${new Date(m.end - (m.d.length - 1 - i) * m.step * 1000).toISOString()},${v == null ? "" : v}`));
      const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([rows.join("\n")], { type: "text/csv" })); a.download = `luftwaechter-${sel.key}-${m.key}-${this._range}.csv`; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
    });
    q("#fs")?.addEventListener("click", () => { try { document.fullscreenElement ? document.exitFullscreen() : this.requestFullscreen(); } catch (e) { /* ignore */ } });
    q("#copyall")?.addEventListener("click", async (ev) => { const b = ev.currentTarget; try { await navigator.clipboard.writeText(this._houseText(rooms, a, t)); b.textContent = "✓"; } catch (er) { b.textContent = "✗"; } });
    q("#help")?.addEventListener("click", () => { this._help = true; this._render(); q("#hclose")?.focus(); });
    q("#hclose")?.addEventListener("click", () => { this._closeHelp(); });
    q("#ovl")?.addEventListener("click", (ev) => { if (ev.target.id === "ovl") { this._closeHelp(); } });
    qa(".chip[data-chart]").forEach((b) => b.addEventListener("click", () => { this._chartKey = b.dataset.chart; this._render(); }));
    qa(".dev[data-dom]").forEach((b) => b.addEventListener("click", () => this._toggle(b.dataset.ent, b.dataset.dom)));
    qa("[data-cov]").forEach((b) => b.addEventListener("click", () => this._call("cover", b.dataset.cov, b.dataset.ent)));
    const svg = q(".chartwrap svg");
    if (svg && this._chartMeta) {
      const m = this._chartMeta, cur = q("#cur"), ro = q("#readout");
      const mv = (ev) => {
        const r = svg.getBoundingClientRect(); const f = Math.max(0, Math.min(1, (ev.clientX - r.left) / r.width));
        const i = Math.round(f * (m.d.length - 1)); const v = m.d[i];
        cur.setAttribute("x1", f * 600); cur.setAttribute("x2", f * 600); cur.setAttribute("visibility", "visible");
        const hb = ((m.d.length - 1 - i) * m.step) / 3600;
        const when = hb >= 48 ? `${(hb / 24).toFixed(1)} ${m.t.dayU}` : `${hb.toFixed(1)} ${m.t.hourU}`;
        if (v != null) ro.textContent = `${v.toFixed(m.key === "temperature" ? 1 : 0)} ${m.unit} · -${when}`;
      };
      svg.addEventListener("pointermove", mv);
      svg.addEventListener("pointerleave", () => { cur.setAttribute("visibility", "hidden"); ro.textContent = `${m.t.min} ${m.mn.toFixed(m.key === "temperature" ? 1 : 0)} · ${m.t.max} ${m.mx.toFixed(m.key === "temperature" ? 1 : 0)} ${m.unit}`; });
    }
    if (sel && this._pendingHist) { const r = this._pendingHist; this._pendingHist = null; this._loadHist(r, this._chartKey); }
  }
}
customElements.define("luftwaechter-panel", LuftwaechterPanel);
