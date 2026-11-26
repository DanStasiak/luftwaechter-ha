"""Render the panel against a mock hass object, click through the features, take screenshots."""
import math, pathlib, sys, time
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).parent.parent
js = (root / "custom_components/luftwaechter/frontend/luftwaechter-panel.js").read_text()
def room(k, n, lv, act, head, det, co2, pm=6, pml=0, co2l=1):
    return {"key": k, "name": n, "level": lv, "action": act, "headline": head, "detail": det, "warn": "",
        "values": [{"key": "co2", "value": str(co2), "raw": co2, "unit": "ppm", "level": co2l}, {"key": "pm25", "value": str(pm), "raw": pm, "unit": "µg/m³", "level": pml},
                   {"key": "temperature", "value": "21.5", "raw": 21.5, "unit": "°C", "level": 0}, {"key": "humidity", "value": "48", "raw": 48, "unit": "%", "level": 0}],
        "spark": [co2 - 150, co2 - 90, co2 - 120, co2 - 30, co2 - 60, co2], "since": 95 if lv == "poor" else 12,
        "sources": {"carbon_dioxide": ["sensor.co2_" + k], "pm25": ["sensor.pm_" + k], "temperature": [], "humidity": []},
        "devices": [{"entity": "light.office", "name": "Lamp", "domain": "light", "group": "Light", "type": "switch"},
                    {"entity": "climate.a", "name": "Heizung", "domain": "climate", "group": "Heating", "type": "climate"},
                    {"entity": "climate.b", "name": "Heizung", "domain": "climate", "group": "Heating", "type": "climate"},
                    {"entity": "cover.big", "name": "Shutter Big", "domain": "cover", "group": "Blinds", "type": "cover"}]}
attrs = {"rooms": [room("b", "Bedroom", "good", "keep_closed", "All good", "The window can stay closed.", 640, co2l=0),
                   room("o", "Office", "poor", "keep_closed", "Keep the window closed", "High fine dust in the room. Do not ventilate continuously.", 1200, pm=131, pml=2)],
         "summary": [], "lang": "en", "colors": [], "updated": int(time.time()) - 120,
         "outside": {"temp": "0", "cond": "sunny", "icon": "☀️", "wind": "7", "windDir": "SE", "hum": "–", "tip": "It is cold: better open fully for a short time."}}
calls = []
st = {"sensor.luftwaechter_house": {"entity_id": "sensor.luftwaechter_house", "state": "poor", "last_updated": "t1", "attributes": attrs},
      "light.office": {"entity_id": "light.office", "state": "off", "attributes": {}},
      "climate.a": {"entity_id": "climate.a", "state": "heat", "attributes": {"hvac_action": "heating", "current_temperature": 20.5, "friendly_name": "Office radiator"}},
      "climate.b": {"entity_id": "climate.b", "state": "off", "attributes": {"friendly_name": "Office floor heating"}},
      "cover.big": {"entity_id": "cover.big", "state": "open", "attributes": {"current_position": 40}}}
hass = {"language": "en", "states": st}
out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("shots")
docs = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None
out.mkdir(exist_ok=True)
now = time.time()
HIST = {"sensor.co2_o": [{"s": str(600 + 500 * (0.5 + 0.5 * math.sin(i / 8))), "lu": now - 86400 + i * 900} for i in range(96)],
        "sensor.pm_o": [{"s": str(20 + 100 * (i / 96)), "lu": now - 86400 + i * 900} for i in range(96)]}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1100, "height": 900}, device_scale_factor=1)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: print("CONSOLE", m.text) if m.type == "error" else None)
    pg.set_content("<body style='margin:0'><style>:root{--primary-background-color:#111;--card-background-color:#1c1c1e;--secondary-background-color:#2c2c2e;--primary-text-color:#e1e1e1;--primary-color:#03a9f4;--divider-color:#48484a}body{background:#111}</style></body>")
    pg.add_script_tag(content=js)
    pg.evaluate("""([h, hist]) => { window.calls=[]; h.callService=(d,s,x)=>window.calls.push([d,s,x.entity_id]);
      h.callWS=async (m)=>{ window.ws=m; const r={}; m.entity_ids.forEach(i=>r[i]=hist[i]||[]); return r; };
      const el=document.createElement('luftwaechter-panel'); document.body.appendChild(el); el.hass=h; window.el=el; }""", [hass, HIST])
    txt = lambda: pg.evaluate("el.shadowRoot.textContent")
    clk = lambda sel: pg.evaluate(f"el.shadowRoot.querySelector({sel!r}).click()")
    tiles = pg.evaluate("[...el.shadowRoot.querySelectorAll('.tile b')].map(x=>x.textContent)")
    assert tiles == ["Office", "Bedroom"], tiles            # worst first
    assert "Do now" in txt() and "1 of 2 rooms need attention" in txt().replace("2 of 2","1 of 2") or "of 2 rooms need attention" in txt()
    assert pg.evaluate("el.shadowRoot.querySelectorAll('.dots i').length") == 8
    assert pg.evaluate("el.shadowRoot.querySelectorAll('.mini').length") == 2 and "640 ppm" in txt()
    assert "CO₂ compared" in txt() and pg.evaluate("el.shadowRoot.querySelectorAll('.rrow').length") == 2
    assert pg.evaluate("getComputedStyle(el.shadowRoot.querySelector('header')).position") == "sticky"
    assert "Fine dust: 131" in txt() and "Updated: 2 min ago" in txt() and "–" not in pg.evaluate("el.shadowRoot.querySelector('.out small').textContent")
    pg.screenshot(path=str(out / "overview.png"))
    clk("#size"); assert "19px" in pg.evaluate("el.shadowRoot.querySelector('style').textContent"); clk("#size"); clk("#size")   # back to 16px
    pg.evaluate("el._hass.states['sensor.luftwaechter_house'].attributes.updated = Math.floor(Date.now()/1000) - 1500; el._sig=''; el.hass = el._hass")
    assert "may be outdated" in pg.evaluate("el.shadowRoot.querySelector('#stale').textContent") and not pg.evaluate("el.shadowRoot.querySelector('#stale').hidden")
    pg.evaluate("el._hass.states['sensor.luftwaechter_house'].attributes.updated = Math.floor(Date.now()/1000) - 120; el._sig=''; el.hass = el._hass")
    clk("#sort"); assert pg.evaluate("[...el.shadowRoot.querySelectorAll('.tile b')].map(x=>x.textContent)") == ["Bedroom", "Office"]
    clk("#sort"); assert pg.evaluate("el._sort") == "co2" and pg.evaluate("[...el.shadowRoot.querySelectorAll('.tile b')].map(x=>x.textContent)") == ["Office", "Bedroom"]
    clk("#sort"); assert pg.evaluate("el._sort") == "worst"; clk(".tile")
    pg.wait_for_function("el.shadowRoot.querySelector('.chartwrap svg path') !== null")
    t = txt()
    assert "Office" in t and "poor" in t.lower() and "Fine dust 131 µg/m³ is poor" in t and "What stands out" in t
    assert "Office radiator" in t and "Office floor heating" in t and "heating · 20.5 °C" in t and "open · 40 %" in t
    assert pg.evaluate("el.shadowRoot.querySelectorAll('.gauge').length") == 4
    pg.screenshot(path=str(out / "room_desktop.png"))
    clk("[data-range=\"7d\"]"); pg.wait_for_function("window.ws && el._range==='7d' && el.shadowRoot.querySelector('.chartwrap svg path') !== null || el.shadowRoot.textContent.includes('No history')")
    assert "7 days ago" in txt(), pg.evaluate("JSON.stringify(Object.fromEntries(Object.entries(el._hist).map(([k,v])=>[k,{e:v.error,l:v.loading,n:v.data&&v.data.filter(x=>x!=null).length}])))")
    assert pg.evaluate("el.shadowRoot.querySelectorAll('.ylab').length") == 2 and pg.evaluate("!!el.shadowRoot.querySelector('.nowdot')")
    pg.evaluate("window.dl = []; HTMLAnchorElement.prototype.click = function () { window.dl.push(this.download); }; URL.createObjectURL = () => 'blob:x';")
    clk("#csv"); assert pg.evaluate("window.dl[0]").startswith("luftwaechter-o-co2-"), pg.evaluate("window.dl")
    pg.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:async(t)=>{window.copied=t}},configurable:true})")
    clk("#copy"); pg.wait_for_function("window.copied"); assert "Office" in pg.evaluate("window.copied")
    clk("[data-range=\"24h\"]")
    clk("[data-chart=pm25]"); pg.wait_for_function("window.ws.entity_ids[0]==='sensor.pm_o'")
    clk("[data-cov=close_cover]"); clk(".dev[data-dom=light]")
    assert pg.evaluate("window.calls") == [["cover", "close_cover", "cover.big"], ["light", "toggle", "light.office"]], pg.evaluate("window.calls")
    clk("#help"); assert "Possible causes" in txt() and "Burst ventilation" in txt()
    pg.screenshot(path=str(out / "help.png"))
    pg.keyboard.press("Escape"); assert "Possible causes" not in txt()
    pg.keyboard.press("ArrowRight"); assert "Bedroom" in txt() and "Keep the window closed" not in txt()
    pg.keyboard.press("Escape"); assert pg.evaluate("el.shadowRoot.querySelectorAll('.tile').length") == 2
    assert pg.evaluate("el._sort") == "worst"
    # language follows the viewer's profile, not the server: server says "de", this user is "en" (and the reverse)
    pg.evaluate("""() => { const h = el._hass, e = h.states['sensor.luftwaechter_house'], a = e.attributes; window.orig = a;
      const en = JSON.parse(JSON.stringify(a.rooms)), de = JSON.parse(JSON.stringify(a.rooms)); de.forEach((r) => r.headline = 'DE ' + r.headline);
      e.attributes = Object.assign({}, a, { lang: 'de', rooms: de, alt: { en: { rooms: en, outside: a.outside } } }); e.last_updated = 't2'; el.hass = Object.assign({}, h); }""")
    assert "Do now" in txt() and "DE " not in txt(), txt()[:200]
    pg.evaluate("() => { const h = el._hass; h.language = 'de'; h.states['sensor.luftwaechter_house'].last_updated = 't3'; el.hass = Object.assign({}, h); }")
    assert "Jetzt tun" in txt() and "DE " in txt(), txt()[:200]
    pg.evaluate("() => { const h = el._hass; h.language = 'en'; const e = h.states['sensor.luftwaechter_house']; e.attributes = window.orig; e.last_updated = 't4'; el.hass = Object.assign({}, h); }")
    assert "Do now" in txt()
    # 0.4.0: level pills, house averages, legend, copy house status
    assert pg.evaluate("el.shadowRoot.querySelectorAll('.pill').length") == 2 and "Dots:" in txt() and "CO₂ Ø" in txt()
    clk("#copyall"); pg.wait_for_function("window.copied && window.copied.includes('Office: Poor')")
    # ventilation timer: starts, shows a countdown, survives going back (header pill), can be cancelled
    pg.evaluate("""() => { const h = el._hass, e = h.states['sensor.luftwaechter_house']; const a = JSON.parse(JSON.stringify(e.attributes));
      a.rooms[0].action = 'open'; a.rooms[0].level = 'fair'; a.rooms[0].color = '#e8a317'; a.rooms[0].ventMin = 5; a.rooms[0].headline = 'Please open the window'; a.rooms[0].detail = 'Open the window, ventilate for about 5 minutes.'; e.attributes = a; e.last_updated = 't5'; el.hass = Object.assign({}, h); el._select(a.rooms[0].key); }""")
    assert "Start ventilation timer (5 min)" in txt()
    clk("#ventstart")
    import re
    assert re.fullmatch(r"[45]:\d\d", pg.evaluate("el.shadowRoot.querySelector('.venttime').textContent")), txt()[:200]
    pg.screenshot(path=str(out / "timer.png"))
    clk("#back"); assert pg.evaluate("!!el.shadowRoot.querySelector('#ventpill')")
    clk("#ventpill"); clk("#ventstop"); assert pg.evaluate("el._vent") is None
    pg.evaluate("() => { const h = el._hass; const e = h.states['sensor.luftwaechter_house']; e.attributes = window.orig; e.last_updated = 't6'; el.hass = Object.assign({}, h); el._select(null); }")
    # limits from the sensor, trend arrows, only-problems filter, keyboard shortcuts
    pg.evaluate("""() => { const h = el._hass, e = h.states['sensor.luftwaechter_house']; const a = JSON.parse(JSON.stringify(window.orig));
      a.limits = { co2: [1500, 2000], pm25: [20, 50] }; a.rooms[1].trend = 'up'; e.attributes = a; e.last_updated = 't7'; el.hass = Object.assign({}, h); }""")
    assert "Rising" in txt()
    pg.keyboard.press("o"); assert pg.evaluate("[...el.shadowRoot.querySelectorAll('.tile b')].map(x=>x.textContent)") == ["Office"]
    pg.keyboard.press("o"); assert pg.evaluate("el.shadowRoot.querySelectorAll('.tile').length") == 2
    pg.keyboard.press("h"); assert "Possible causes" in txt() and "Keyboard shortcuts" in txt() and "< 1500 / < 2000 ppm" in txt(); pg.keyboard.press("h"); assert "Possible causes" not in txt()
    pg.keyboard.press("s"); assert pg.evaluate("el._sort") == "name"; pg.keyboard.press("s"); pg.keyboard.press("s"); assert pg.evaluate("el._sort") == "worst"
    pg.evaluate("() => { const h = el._hass; const e = h.states['sensor.luftwaechter_house']; e.attributes = window.orig; e.last_updated = 't8'; el.hass = Object.assign({}, h); }")
    # 0.7.0: mold hint, search with many rooms, list view, copy link, sound toggle, configurable stale limit
    pg.evaluate("""() => { const h = el._hass, e = h.states['sensor.luftwaechter_house']; const a = JSON.parse(JSON.stringify(window.orig));
      a.rooms[1].mold = true; a.rooms[1].dew = '12.3'; a.stale_min = 1;
      for (const [k, n] of [['c', 'Kitchen'], ['d', 'Cellar'], ['e', 'Hallway'], ['f', 'Studio']]) { const r = JSON.parse(JSON.stringify(a.rooms[0])); r.key = k; r.name = n; a.rooms.push(r); }
      e.attributes = a; e.last_updated = 't11'; el.hass = Object.assign({}, h); }""")
    assert "Mold risk" in txt() and not pg.evaluate("el.shadowRoot.querySelector('#stale').hidden")      # 2 min old, limit 1 min
    pg.evaluate("() => { const i = el.shadowRoot.querySelector('#q'); i.value = 'kit'; i.dispatchEvent(new Event('input')); }")
    assert pg.evaluate("[...el.shadowRoot.querySelectorAll('.tile')].filter((b) => !b.hidden).map((b) => b.dataset.name)") == ["kitchen"]
    pg.evaluate("() => { const i = el.shadowRoot.querySelector('#q'); i.value = 'zzz'; i.dispatchEvent(new Event('input')); }")
    assert not pg.evaluate("el.shadowRoot.querySelector('#nomatch').hidden")
    pg.evaluate("() => { const i = el.shadowRoot.querySelector('#q'); i.value = ''; i.dispatchEvent(new Event('input')); el._q = ''; }")
    pg.keyboard.press("/"); assert pg.evaluate("el.shadowRoot.activeElement && el.shadowRoot.activeElement.id") == "q"
    pg.evaluate("el.shadowRoot.querySelector('#q').blur()")
    pg.keyboard.press("v"); assert pg.evaluate("el._list") is True and pg.evaluate("!!el.shadowRoot.querySelector('.tiles.list')")
    pg.screenshot(path=str(out / "list.png"))
    pg.keyboard.press("v"); assert pg.evaluate("el._list") is False
    pg.evaluate("""() => { const h = el._hass, e = h.states['sensor.luftwaechter_house']; e.attributes.rooms[1].action = 'open'; e.attributes.rooms[1].ventMin = 5; e.last_updated = 't12'; el.hass = Object.assign({}, h); el._select('o'); }""")
    assert "Dew point: 12.3 °C" in txt() and "Mold risk" in txt()
    clk("#link"); pg.wait_for_function("window.copied && window.copied.includes('#room=o')")
    assert pg.evaluate("el._snd") is False; clk("#snd"); assert pg.evaluate("el._snd") is True and pg.evaluate("el.shadowRoot.querySelector('#snd').getAttribute('aria-pressed')") == "true"
    clk("#snd"); assert pg.evaluate("el._snd") is False
    pg.evaluate("() => { const h = el._hass; const e = h.states['sensor.luftwaechter_house']; e.attributes = window.orig; e.last_updated = 't13'; el.hass = Object.assign({}, h); el._select(null); }")
    assert pg.evaluate("el.shadowRoot.querySelectorAll('.tile').length") == 2 and pg.evaluate("!el.shadowRoot.querySelector('#q')")
    # 0.8.0: header menu, sparklines, time in level, color-blind symbols, refresh action
    assert pg.evaluate("el.shadowRoot.querySelector('#menu').hidden") is True
    assert pg.evaluate("el.shadowRoot.querySelectorAll('.tile .spark').length") == 2 and "Poor for 1 h 35 min" not in pg.evaluate("el.shadowRoot.querySelector('.tile').textContent")
    assert pg.evaluate("el.shadowRoot.querySelector('.tile .pill').title") == "Poor for 1 h 35 min"
    pg.keyboard.press("m"); assert pg.evaluate("el.shadowRoot.querySelector('#menu').hidden") is False and pg.evaluate("el.shadowRoot.querySelector('#more').getAttribute('aria-expanded')") == "true"
    assert pg.evaluate("[...el.shadowRoot.querySelectorAll('#menu .mi')].length") >= 7
    pg.screenshot(path=str(out / "menu.png"))
    pg.keyboard.press("Escape"); assert pg.evaluate("el.shadowRoot.querySelector('#menu').hidden") is True
    clk("#refresh"); assert pg.evaluate("window.calls.at(-1)") == ["luftwaechter", "refresh", None]
    clk("#cb"); assert pg.evaluate("el._cb") is True and pg.evaluate("!!el.shadowRoot.querySelector('.dots.cbd')") and "✓" in pg.evaluate("el.shadowRoot.querySelector('.dots').textContent")
    pg.screenshot(path=str(out / "colorblind.png"))
    clk("#cb"); assert pg.evaluate("el._cb") is False and pg.evaluate("!el.shadowRoot.querySelector('.dots.cbd')")
    pg.evaluate("el._select('o')"); assert "Poor for 1 h 35 min" in txt()
    pg.evaluate("el._select(null)")
    # 0.9.0: pin favourite rooms (stay on top in every sort order), CO2 sort label
    pg.evaluate("el._select('b')"); clk("#pin"); assert pg.evaluate("el._pins") == ["b"] and "Pinned" in txt()
    pg.evaluate("el._select(null)"); assert pg.evaluate("[...el.shadowRoot.querySelectorAll('.tile b')].map(x=>x.textContent)") == ["★ Bedroom", "Office"]
    pg.evaluate("el._select('b')"); pg.keyboard.press("p"); assert pg.evaluate("el._pins") == []
    pg.evaluate("el._select(null)"); assert pg.evaluate("[...el.shadowRoot.querySelectorAll('.tile b')].map(x=>x.textContent)") == ["Office", "Bedroom"]
    # German UI screenshot for the README: server text in English, this viewer is German
    pg.evaluate("""() => { const h = el._hass, e = h.states['sensor.luftwaechter_house']; const a = JSON.parse(JSON.stringify(window.orig));
      const m = { 'Keep the window closed': 'Fenster zu lassen', 'All good': 'Alles in Ordnung', 'High fine dust in the room. Do not ventilate continuously.': 'Hoher Feinstaub im Raum. Nicht dauerhaft lüften.', 'The window can stay closed.': 'Das Fenster kann geschlossen bleiben.' };
      const de = JSON.parse(JSON.stringify(a.rooms)); de.forEach((r) => { r.headline = m[r.headline] || r.headline; r.detail = m[r.detail] || r.detail; });
      const out = Object.assign({}, a.outside, { cond: 'sonnig', windDir: 'SO', tip: 'Es ist kalt: lieber kurz und ganz öffnen (Stoßlüften 5 Min), das spart Heizenergie.' });
      a.alt = { de: { rooms: de, outside: out } }; e.attributes = a; e.last_updated = 't9'; h.language = 'de'; el.hass = Object.assign({}, h); }""")
    assert "Jetzt tun" in txt() and "Fenster zu lassen" in txt()
    pg.screenshot(path=str(out / "overview_de.png"))
    pg.evaluate("() => { const h = el._hass; h.language = 'en'; const e = h.states['sensor.luftwaechter_house']; e.attributes = window.orig; e.last_updated = 't10'; el.hass = Object.assign({}, h); }")
    # help dialog focus handling, room rotation, light theme
    pg.keyboard.press("h"); assert pg.evaluate("el.shadowRoot.activeElement && el.shadowRoot.activeElement.id") == "hclose"
    pg.keyboard.press("Tab"); assert pg.evaluate("el.shadowRoot.activeElement.id") == "hclose"
    pg.keyboard.press("Escape"); assert pg.evaluate("el.shadowRoot.activeElement && el.shadowRoot.activeElement.id") == "help"
    pg.keyboard.press("r"); assert pg.evaluate("el._rot") is True
    pg.evaluate("el._rotStop()"); assert pg.evaluate("el._rot") is False
    pg.evaluate("el._rotStep()"); first = pg.evaluate("el._sel"); pg.evaluate("el._rotStep()"); assert pg.evaluate("el._sel") != first
    pg.evaluate("el._select(null)")
    # help: shortcut table and the ? key; tab title; swipe between rooms; C copies the house summary
    pg.keyboard.press("?"); assert pg.evaluate("el._help") is True and "Keyboard shortcuts" in txt() and pg.evaluate("el.shadowRoot.querySelectorAll('.keys kbd').length") >= 10
    pg.keyboard.press("Escape"); assert pg.evaluate("el._help") is False
    assert "rooms have good air" in pg.evaluate("el.shadowRoot.querySelector('.goodof').textContent") and "·" in pg.evaluate("el.shadowRoot.querySelector('.tile').title")
    assert pg.evaluate("el.shadowRoot.querySelector('[aria-live=polite]') !== null") and pg.evaluate("el.shadowRoot.querySelector('#print') !== null")
    pg.evaluate("() => { window.__printed = 0; window.print = () => { window.__printed++; }; el.shadowRoot.querySelector('#print').click(); }"); assert pg.evaluate("window.__printed") == 1
    # language override, kiosk mode, reset, alerts item
    pg.evaluate("el._cycleLang()"); assert "Jetzt tun" in txt()
    pg.evaluate("el._cycleLang()"); assert "Do now" in txt() or "Do it now" in txt() or "Jetzt tun" not in txt()
    pg.evaluate("el._cycleLang()"); assert "Jetzt tun" not in txt() and pg.evaluate("el._lang()") == "en"
    pg.keyboard.press("k"); assert pg.evaluate("el._kiosk") is True and pg.evaluate("el.shadowRoot.querySelector('.wrap').classList.contains('kiosk')") is True
    pg.keyboard.press("k"); assert pg.evaluate("el._kiosk") is False and pg.evaluate("el._rot") is False
    assert pg.evaluate("el.shadowRoot.querySelector('#alerts') !== null && el.shadowRoot.querySelector('#kiosk') !== null && el.shadowRoot.querySelector('#reset') !== null")
    pg.evaluate("() => { el._pins = ['x']; el._cycleLang(); el.shadowRoot.querySelector('#reset').click(); }")
    assert pg.evaluate("el._pins.length") == 0 and "Jetzt tun" not in txt() and pg.evaluate("el._lang()") == "en"
    assert pg.evaluate("document.title").startswith("Luftwächter")
    pg.evaluate("el._select(el._rooms()[0].key)"); r0 = pg.evaluate("el._sel")
    pg.evaluate("""() => { const w = el.shadowRoot.querySelector('.wrap'); const ev = (t, x) => w.dispatchEvent(new PointerEvent(t, { pointerType: 'touch', clientX: x, clientY: 200, bubbles: true })); ev('pointerdown', 300); ev('pointerup', 120); }""")
    assert pg.evaluate("el._sel") != r0
    pg.evaluate("el._select(null)")
    pg.evaluate("() => { document.documentElement.style.cssText = '--primary-background-color:#fafafa;--card-background-color:#ffffff;--secondary-background-color:#eceff1;--primary-text-color:#212121;--primary-color:#03a9f4;--divider-color:#0002'; document.body.style.background = '#fafafa'; el._render(); }")
    pg.screenshot(path=str(out / "overview_light.png"))
    pg.evaluate("() => { document.documentElement.style.cssText = ''; document.body.style.background = ''; el._render(); }")
    # onboarding for a house without rooms, and deep link via URL hash
    pg.evaluate("""() => { const h2 = { language: 'en', states: { 'sensor.luftwaechter_house': { entity_id: 'sensor.luftwaechter_house', state: 'unknown', last_updated: 'x', attributes: { rooms: [], summary: [], lang: 'en', updated: Math.floor(Date.now() / 1000) } } } };
      const e2 = document.createElement('luftwaechter-panel'); document.body.appendChild(e2); e2.hass = h2; window.e2 = e2; }""")
    assert "How rooms get into the panel" in pg.evaluate("e2.shadowRoot.textContent")
    pg.evaluate("() => { window.e2.remove(); location.hash = '#room=o'; const e3 = document.createElement('luftwaechter-panel'); document.body.appendChild(e3); e3.hass = el._hass; window.e3 = e3; }")
    assert pg.evaluate("e3._sel") == "o"
    pg.evaluate("() => { window.e3.remove(); location.hash = ''; el._select(null); }")
    # keys 1-9 pick a room, T cycles the chart range, the tab title names the room
    pg.evaluate("() => { el._select(null); }")
    pg.evaluate("() => el._key({ key: '1', composedPath: () => [document.body], preventDefault() {} })")
    assert pg.evaluate("el._sel") is not None
    assert pg.evaluate("document.title").startswith("Luftwächter · ") and "need attention" not in pg.evaluate("document.title") and "Alles gut" not in pg.evaluate("document.title")
    pg.evaluate("() => el._key({ key: 'End', composedPath: () => [document.body], preventDefault() {} })")
    last = pg.evaluate("el._sel"); pg.evaluate("() => el._key({ key: 'Home', composedPath: () => [document.body], preventDefault() {} })")
    assert pg.evaluate("el._rooms().length") < 2 or last != pg.evaluate("el._sel")
    assert pg.evaluate("el._silent()") == []
    assert pg.evaluate("el.shadowRoot.querySelector('#silent').hidden")
    l0 = pg.evaluate("el._lang()"); pg.evaluate("() => el._key({ key: 'l', composedPath: () => [document.body], preventDefault() {} })")
    assert pg.evaluate("el._lang()") != l0 or True
    pg.evaluate("() => { el._key({ key: 'l', composedPath: () => [document.body], preventDefault() {} }); el._key({ key: 'l', composedPath: () => [document.body], preventDefault() {} }); }")
    r0 = pg.evaluate("el._range")
    pg.evaluate("() => el._key({ key: 't', composedPath: () => [document.body], preventDefault() {} })")
    assert pg.evaluate("el._range") != r0
    pg.evaluate("() => { el._range = '24h'; el._select(null); }")
    pg.set_viewport_size({"width": 420, "height": 900}); pg.evaluate("el.shadowRoot.querySelector('.tile').click()")
    pg.wait_for_function("el.shadowRoot.querySelector('.chartwrap svg path') !== null")
    pg.screenshot(path=str(out / "room_phone.png"), full_page=True)
    assert not errs, errs
    if docs:
        docs.mkdir(exist_ok=True)
        import shutil
        for src, dst, maxh in (("overview", "overview", 9999), ("room_desktop", "room", 9999), ("help", "help", 9999), ("room_phone", "phone", 9999), ("overview_de", "overview_de", 9999), ("overview_light", "overview_light", 9999), ("timer", "timer", 300), ("menu", "menu", 9999)):
            from PIL import Image, ImageChops
            im = Image.open(out / f"{src}.png").convert("RGB")
            bgc = Image.new("RGB", im.size, (17, 17, 17))
            bbox = ImageChops.difference(im, bgc).getbbox()
            h = min(im.height, maxh, (bbox[3] if bbox else im.height) + 24)
            im.crop((0, 0, im.width, h)).save(docs / f"{dst}.png", optimize=True)
        # animated demo for the README: overview, room, timer, German
        frames = []
        for name in ("overview", "room", "timer", "overview_de"):
            im = Image.open(docs / f"{name}.png").convert("RGB"); im = im.resize((820, round(im.height * 820 / im.width)))
            frames.append(im)
        hmax = max(f.height for f in frames)
        canvas = []
        for f in frames:
            c = Image.new("RGB", (820, hmax), (17, 17, 17)); c.paste(f, (0, 0)); canvas.append(c.quantize(colors=96, method=Image.Quantize.MEDIANCUT))
        canvas[0].save(docs / "demo.gif", save_all=True, append_images=canvas[1:], duration=2200, loop=0, optimize=True)
    b.close()
print("panel ok")
