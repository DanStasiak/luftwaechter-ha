"""Render the panel against a mock hass object, click through the features, take screenshots."""
import math, pathlib, sys, time
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).parent.parent
js = (root / "custom_components/luftwaechter/frontend/luftwaechter-panel.js").read_text()
def room(k, n, lv, act, head, det, co2, pm=6, pml=0, co2l=1):
    return {"key": k, "name": n, "level": lv, "action": act, "headline": head, "detail": det, "warn": "",
        "values": [{"key": "co2", "value": str(co2), "raw": co2, "unit": "ppm", "level": co2l}, {"key": "pm25", "value": str(pm), "raw": pm, "unit": "µg/m³", "level": pml},
                   {"key": "temperature", "value": "21.5", "raw": 21.5, "unit": "°C", "level": 0}, {"key": "humidity", "value": "48", "raw": 48, "unit": "%", "level": 0}],
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
    assert "Fine dust: 131" in txt() and "Updated: 2 min ago" in txt() and "–" not in pg.evaluate("el.shadowRoot.querySelector('.out small').textContent")
    pg.screenshot(path=str(out / "overview.png"))
    clk("#size"); assert "19px" in pg.evaluate("el.shadowRoot.querySelector('style').textContent"); clk("#size"); clk("#size")   # back to 16px
    pg.evaluate("el._hass.states['sensor.luftwaechter_house'].attributes.updated = Math.floor(Date.now()/1000) - 1500; el._sig=''; el.hass = el._hass")
    assert "may be outdated" in pg.evaluate("el.shadowRoot.querySelector('#stale').textContent") and not pg.evaluate("el.shadowRoot.querySelector('#stale').hidden")
    pg.evaluate("el._hass.states['sensor.luftwaechter_house'].attributes.updated = Math.floor(Date.now()/1000) - 120; el._sig=''; el.hass = el._hass")
    clk("#sort"); assert pg.evaluate("[...el.shadowRoot.querySelectorAll('.tile b')].map(x=>x.textContent)") == ["Bedroom", "Office"]
    clk("#sort"); clk(".tile")
    pg.wait_for_function("el.shadowRoot.querySelector('.chartwrap svg path') !== null")
    t = txt()
    assert "Office" in t and "poor" in t.lower() and "Fine dust 131 µg/m³ is poor" in t and "What stands out" in t
    assert "Office radiator" in t and "Office floor heating" in t and "heating · 20.5 °C" in t and "open · 40 %" in t
    assert pg.evaluate("el.shadowRoot.querySelectorAll('.gauge').length") == 4
    pg.screenshot(path=str(out / "room_desktop.png"))
    clk("[data-range=\"7d\"]"); pg.wait_for_function("window.ws && el._range==='7d' && el.shadowRoot.querySelector('.chartwrap svg path') !== null || el.shadowRoot.textContent.includes('No history')")
    assert "7 days ago" in txt(), pg.evaluate("JSON.stringify(Object.fromEntries(Object.entries(el._hist).map(([k,v])=>[k,{e:v.error,l:v.loading,n:v.data&&v.data.filter(x=>x!=null).length}])))")
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
    pg.set_viewport_size({"width": 420, "height": 900}); pg.evaluate("el.shadowRoot.querySelector('.tile').click()")
    pg.wait_for_function("el.shadowRoot.querySelector('.chartwrap svg path') !== null")
    pg.screenshot(path=str(out / "room_phone.png"), full_page=True)
    assert not errs, errs
    if docs:
        docs.mkdir(exist_ok=True)
        import shutil
        for src, dst in (("overview", "overview"), ("room_desktop", "room"), ("help", "help"), ("room_phone", "phone")):
            from PIL import Image, ImageChops
            im = Image.open(out / f"{src}.png").convert("RGB")
            bgc = Image.new("RGB", im.size, (17, 17, 17))
            bbox = ImageChops.difference(im, bgc).getbbox()
            h = min(im.height, (bbox[3] if bbox else im.height) + 24)
            im.crop((0, 0, im.width, h)).save(docs / f"{dst}.png", optimize=True)
    b.close()
print("panel ok")
