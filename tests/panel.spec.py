"""Render the panel against a mock hass object and take screenshots."""
import json, pathlib, sys
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).parent.parent
js = (root / "custom_components/luftwaechter/frontend/luftwaechter-panel.js").read_text()
room = lambda k, n, lv, act, head, det, co2: {
    "key": k, "name": n, "level": lv, "action": act, "headline": head, "detail": det, "warn": "",
    "values": [{"key": "co2", "value": str(co2), "raw": co2, "unit": "ppm", "level": 1}, {"key": "pm25", "value": "6", "raw": 6, "unit": "µg/m³", "level": 0},
               {"key": "temperature", "value": "21.5", "raw": 21.5, "unit": "°C", "level": 0}, {"key": "humidity", "value": "48", "raw": 48, "unit": "%", "level": 0}],
    "devices": [{"entity": "light.office", "name": "Lamp", "domain": "light", "group": "Light", "type": "switch"}]}
attrs = {"rooms": [room("o", "Office", "fair", "open", "Please open the window", "Open fully, ventilate for 10 minutes.", 1200),
                   room("b", "Bedroom", "good", "keep_closed", "All good", "The window can stay closed.", 640)],
         "summary": [], "lang": "en", "colors": [],
         "outside": {"temp": "9", "cond": "cloudy", "icon": "☁️", "wind": "12", "windDir": "SW", "hum": "80", "tip": "Good time to ventilate."}}
calls = []
hass = {"language": "en", "states": {"sensor.luftwaechter_house": {"entity_id": "sensor.luftwaechter_house", "state": "fair", "last_updated": "t1", "attributes": attrs},
                                    "light.office": {"entity_id": "light.office", "state": "off", "attributes": {}}}}
out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("shots")
out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 420, "height": 800}, device_scale_factor=2)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.set_content("<body></body>")
    pg.add_script_tag(content=js)
    pg.evaluate("""(h) => { window.calls=[]; h.callService=(d,s,x)=>window.calls.push([d,s,x.entity_id]);
      const el=document.createElement('luftwaechter-panel'); document.body.appendChild(el); el.hass=h; window.el=el; }""", hass)
    assert "Fair" in pg.inner_text("luftwaechter-panel") or pg.evaluate("el.shadowRoot.textContent").count("Fair")
    pg.screenshot(path=str(out / "overview.png"))
    pg.evaluate("el.shadowRoot.querySelector('.tile').click()")
    txt = pg.evaluate("el.shadowRoot.textContent")
    assert "Please open the window" in txt and "1200" in txt, txt
    pg.screenshot(path=str(out / "room.png"))
    pg.evaluate("el.shadowRoot.querySelector('.dev').click()")
    assert pg.evaluate("window.calls") == [["light", "toggle", "light.office"]]
    pg.evaluate("el.hass={...el._hass, language:'de'}")
    pg.evaluate("el.shadowRoot.getElementById('back').click()")
    assert "Gut" in pg.evaluate("el.shadowRoot.textContent") or "Mittel" in pg.evaluate("el.shadowRoot.textContent")
    assert not errs, errs
    b.close()
print("panel ok")
