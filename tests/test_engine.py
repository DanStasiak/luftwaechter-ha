import importlib.util, pathlib, sys
p = pathlib.Path(__file__).parent.parent / "custom_components/luftwaechter/engine.py"
spec = importlib.util.spec_from_file_location("engine", p)
engine = importlib.util.module_from_spec(spec); sys.modules["engine"] = engine; spec.loader.exec_module(engine)

NOW = 1_000_000.0

def ent(eid, dc, state, dom="sensor", name=None, age=0):
    return {"entity_id": eid, "domain": dom, "name": name or eid, "state": str(state),
            "device_class": dc, "last_reported": NOW - age * 60}

def area(**v):
    ents = []
    if "co2" in v: ents.append(ent("sensor.co2", "carbon_dioxide", v["co2"]))
    if "pm" in v: ents.append(ent("sensor.pm", "pm25", v["pm"]))
    if "t" in v: ents.append(ent("sensor.t", "temperature", v["t"]))
    if "h" in v: ents.append(ent("sensor.h", "humidity", v["h"]))
    if "win" in v: ents.append(ent("binary_sensor.w", "window", v["win"], dom="binary_sensor"))
    return {"id": "a1", "name": "Office", "entities": ents}

def room(weather=None, rain="", lang="en", **v):
    m = engine.build_model([area(**v)], set(), weather, rain, lang, NOW)
    return m["rooms"][0]

def test_limits():
    assert engine.level_above(999, 1000, 1500) == 0
    assert engine.level_above(1000, 1000, 1500) == 1
    assert engine.level_above(1500, 1000, 1500) == 2
    assert engine.level_range(17, 17, 23, 13, 25) == 0
    assert engine.level_range(24, 17, 23, 13, 25) == 1
    assert engine.level_range(26, 17, 23, 13, 25) == 2

def test_worst_level():
    assert room(co2=600, pm=5, t=21, h=45)["level"] == "good"
    assert room(co2=1200, pm=5, t=21, h=45)["level"] == "fair"
    assert room(co2=600, pm=60, t=21, h=45)["level"] == "poor"

def test_open_window_when_stale_and_closed():
    r = room(co2=1300, win="off", weather={"temperature": 10, "condition": "sunny"})
    assert r["action"] == "open" and "10 minutes" in r["detail"]

def test_close_when_fresh_and_open():
    r = room(co2=500, win="on", t=21, h=45, weather={"temperature": 8, "condition": "cloudy"})
    assert r["action"] == "close" and "cold" in r["detail"]

def test_keep_open_when_still_stale():
    assert room(co2=900, win="on")["action"] == "keep_open" or room(co2=900, win="on")["action"] == "close"
    assert room(co2=1100, win="on")["action"] == "keep_open"

def test_wait_when_storm():
    r = room(co2=1300, win="off", weather={"temperature": 12, "condition": "lightning"})
    assert r["action"] == "wait"

def test_dust_keeps_closed():
    r = room(co2=500, pm=40, t=21, h=45, win="off")
    assert r["action"] == "keep_closed" and r["headline"] == "Keep the window closed"

def test_rain_soon_hint_and_german():
    r = room(co2=1300, win="off", rain="15:00", lang="de", weather={"temperature": 3, "condition": "cloudy"})
    assert "15:00" in r["detail"] and "5 Minuten" in r["detail"]

def test_unknown_without_air_values():
    m = engine.build_model([area(t=21)], set(), None, "", "en", NOW)
    assert m["rooms"] == []

def test_stale_sensor_ignored():
    a = area(co2=900)
    a["entities"].append(ent("sensor.co2_old", "carbon_dioxide", 3000, age=120, name="Office old"))
    m = engine.build_model([a], set(), None, "", "en", NOW)
    r = m["rooms"][0]
    assert r["values"][0]["raw"] == 900 and "ignored" in r["warn"]

def test_outside_view_tip():
    o = engine.outside_view({"temperature": 3, "condition": "cloudy", "wind_speed": 10, "wind_speed_unit": "m/s", "wind_bearing": 90}, "", "en")
    assert o["wind"] == "36" and o["windDir"] == "E" and "cold" in o["tip"]

def test_first_rain_hour():
    fc = [{"datetime": "a", "condition": "sunny"}, {"datetime": "b", "condition": "rainy"}]
    ts = {"a": NOW + 3600, "b": NOW + 7200}
    assert engine.first_rain_hour(fc, NOW, ts.get) == NOW + 7200

def test_devices_label_filter():
    a = area(co2=500)
    a["entities"] += [ent("light.x", None, "on", dom="light", name="Office Lamp"), ent("light.y", None, "on", dom="light", name="Office Spot")]
    m = engine.build_model([a], {"light.x"}, None, "", "en", NOW)
    assert [d["entity"] for d in m["rooms"][0]["devices"]] == ["light.x"]

def test_no_negative_zero():
    assert engine.fmt(-0.3, 0, "en") == "0"

def test_switches_hidden_without_label():
    a = area(co2=500)
    a["entities"] += [ent("switch.s", None, "on", dom="switch", name="Office Relay"), ent("light.l", None, "on", dom="light", name="Office Lamp")]
    m = engine.build_model([a], set(), None, "", "en", NOW)
    assert [d["entity"] for d in m["rooms"][0]["devices"]] == ["light.l"]
