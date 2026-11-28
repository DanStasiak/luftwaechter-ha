import importlib.util
import pathlib
import sys

p = pathlib.Path(__file__).parent.parent / "custom_components/luftwaechter/engine.py"
spec = importlib.util.spec_from_file_location("engine", p)
engine = importlib.util.module_from_spec(spec); sys.modules["engine"] = engine; spec.loader.exec_module(engine)

NOW = 1_000_000.0

def ent(eid, dc, state, dom="sensor", name=None, age=0, changed=None):
    return {"entity_id": eid, "domain": dom, "name": name or eid, "state": str(state),
            "device_class": dc, "last_reported": NOW - age * 60, "last_changed": NOW - (age if changed is None else changed) * 60}

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

def test_silent_rooms_listed():
    ok = engine.build_model([area(co2=900)], set(), None, "", "en", NOW)
    assert ok["silent_rooms"] == []
    a = area(co2=900)
    a["entities"].append(ent("sensor.co2_old", "carbon_dioxide", 3000, age=120, name="Office old"))
    m = engine.build_model([a], set(), None, "", "en", NOW)
    assert m["silent_rooms"] == [m["rooms"][0]["name"]]

def test_ventilate_rooms_counted():
    m = engine.build_model([area(co2=900)], set(), None, "", "en", NOW)
    assert m["ventilate"] == len(m["ventilate_rooms"]) and m["ventilate"] in (0, 1)
    assert isinstance(m["ventilate_rooms"], list)


def test_co2_average_and_mold_rooms():
    a2 = area(co2=1000)
    a2["id"], a2["name"] = "a2", "Bedroom"
    for e in a2["entities"]:
        e["entity_id"] = e["entity_id"] + "_b"
    m = engine.build_model([area(co2=800), a2], set(), None, "", "en", NOW)
    assert m["co2_avg"] == 900 and m["mold"] == len(m["mold_rooms"])
    assert engine.build_model([area(t=21)], set(), None, "", "en", NOW)["co2_avg"] is None


def test_mold_limit_configurable():
    a = area(co2=800, h=65)
    assert engine.build_model([a], set(), None, "", "en", NOW)["mold"] == 0
    m = engine.build_model([a], set(), None, "", "en", NOW, {"mold_rh": 60})
    assert m["mold"] == 1 and m["mold_rh"] == 60
    assert engine.mold_limit({"mold_rh": 5}) == 70 and engine.mold_limit({"mold_rh": "x"}) == 70


def test_temperature_and_humidity_averages():
    a2 = area(co2=900, t=23, h=60)
    a2["id"], a2["name"] = "a2", "Bedroom"
    for e in a2["entities"]:
        e["entity_id"] = e["entity_id"] + "_b"
    m = engine.build_model([area(co2=800, t=21, h=40), a2], set(), None, "", "en", NOW)
    assert m["temp_avg"] == 22.0 and m["rh_avg"] == 50


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


def test_texts_in_every_language():
    m = engine.build_model([area(co2=1300, win="off")], set(), None, "", "de", NOW)
    assert m["lang"] == "de" and set(m["alt"]) == {"en"}
    assert m["rooms"][0]["headline"] != m["alt"]["en"]["rooms"][0]["headline"]
    assert m["alt"]["en"]["rooms"][0]["key"] == m["rooms"][0]["key"]


def test_custom_limits_change_the_rating():
    m = engine.build_model([area(co2=1300)], set(), None, "", "en", NOW, {"co2": (1500, 2000)})
    assert m["rooms"][0]["level"] == "good" and m["limits"]["co2"] == [1500, 2000]
    assert engine.build_model([area(co2=1300)], set(), None, "", "en", NOW)["rooms"][0]["level"] == "fair"


def test_invalid_limits_fall_back_to_defaults():
    m = engine.build_model([area(co2=1300)], set(), None, "", "en", NOW, {"co2": (2000, 1000), "pm25": (0, 5)})
    assert m["limits"] == {"co2": [1000, 1500], "pm25": [20, 50]}


def test_dew_point_and_mold_hint():
    assert abs(engine.dew_point(20, 50) - 9.3) < 0.2
    assert engine.dew_point(None, 50) is None and engine.dew_point(20, None) is None
    wet = room(co2=600, t=21, h=75)
    assert wet["mold"] is True and "mold" in wet["detail"].lower() and wet["dew"] != ""
    assert room(co2=600, t=21, h=75, lang="de")["detail"].count("Schimmel") == 1
    dry = room(co2=600, t=21, h=45)
    assert dry["mold"] is False and "mold" not in dry["detail"].lower()


def test_house_attention_summary():
    m = engine.build_model([area(co2=1600, win="off")], set(), None, "", "en", NOW)
    assert m["attention"] == 1 and m["attention_rooms"] == ["Office"] and m["worst_room"] == "Office"
    ok = engine.build_model([area(co2=600, pm=5, t=21, h=45)], set(), None, "", "en", NOW)
    assert ok["attention"] == 0 and ok["attention_rooms"] == []


def room_win(win_min, dc="window", name=None, **v):
    a = area(**v)
    a["entities"] = [e for e in a["entities"] if e["domain"] != "binary_sensor"]
    a["entities"].append(ent("binary_sensor.w", dc, "on", dom="binary_sensor", name=name, changed=win_min))
    return engine.build_model([a], set(), v.pop("weather", None), "", "en", NOW)["rooms"][0]


def test_close_window_when_air_good_and_cold_after_minutes():
    w = {"temperature": 2, "condition": "cloudy"}
    a = area(co2=850, t=21, h=45)
    a["entities"].append(ent("binary_sensor.w", "window", "on", dom="binary_sensor", changed=12))
    r = engine.build_model([a], set(), w, "", "en", NOW)["rooms"][0]
    assert r["action"] == "close" and r["openMin"] == 12 and "2 °C" in r["detail"] and "12 min" in r["detail"]
    a["entities"][-1] = ent("binary_sensor.w", "window", "on", dom="binary_sensor", changed=2)
    r = engine.build_model([a], set(), w, "", "en", NOW)["rooms"][0]
    assert r["action"] == "keep_open"


def test_close_window_when_raining_and_air_good():
    a = area(co2=800, t=21, h=45)
    a["entities"].append(ent("binary_sensor.w", "window", "on", dom="binary_sensor", changed=1))
    r = engine.build_model([a], set(), {"temperature": 14, "condition": "rainy"}, "", "en", NOW)["rooms"][0]
    assert r["action"] == "close" and "raining" in r["detail"]
    m = engine.build_model([a], set(), {"temperature": 14, "condition": "rainy"}, "", "en", NOW)
    assert m["close"] == 1 and m["close_rooms"] == ["Office"] and m["attention"] == 1


def test_stale_air_keeps_window_open_even_when_cold():
    a = area(co2=1200, t=21, h=45)
    a["entities"].append(ent("binary_sensor.w", "window", "on", dom="binary_sensor", changed=30))
    r = engine.build_model([a], set(), {"temperature": 0, "condition": "cloudy"}, "", "en", NOW)["rooms"][0]
    assert r["action"] == "keep_open" and "30 min" in r["detail"]


def test_door_contact_counts_as_window_only_when_named_so():
    assert engine.is_window(ent("binary_sensor.x", "door", "on", dom="binary_sensor", name="Door Window Sensor 6"))
    assert not engine.is_window(ent("binary_sensor.front", "door", "on", dom="binary_sensor", name="Front door"))
    assert engine.is_window(ent("binary_sensor.y", "opening", "on", dom="binary_sensor", name="Balkon"))


def test_rain_sensor_name_detection():
    assert engine.is_rain_sensor("binary_sensor.solar_rain_sensor_2", "Solar Rain Sensor #2 Rain")
    assert engine.is_rain_sensor("binary_sensor.regen", "Regen")
    assert not engine.is_rain_sensor("binary_sensor.x_cleaning_reminder", "Solar Rain Sensor #2 Cleaning reminder")
    assert not engine.is_rain_sensor("binary_sensor.garden_rain_confirmed", "Garden rain confirmed")


def test_rain_sensor_makes_closed_stale_room_wait():
    r = room(co2=1200, win="off", weather={"raining": True})
    assert r["action"] == "wait" and "rain" in r["detail"].lower()
    assert room(co2=1200, win="off", weather={"raining": False})["action"] == "open"
    assert room(co2=1800, win="off", weather={"raining": True})["action"] == "open"


def test_rain_sensor_closes_open_window_with_good_air():
    a = area(co2=800, t=21, h=45)
    a["entities"].append(ent("binary_sensor.w", "window", "on", dom="binary_sensor", changed=1))
    r = engine.build_model([a], set(), {"raining": True}, "", "de", NOW)["rooms"][0]
    assert r["action"] == "close" and "regnet" in r["detail"]


def _wa(opened_min_ago, name="Office window", state="on"):
    return [{"id": "a1", "name": "Office", "entities": [
        {"entity_id": "binary_sensor.ow", "domain": "binary_sensor", "name": name, "state": state,
         "device_class": "window", "last_reported": NOW, "last_changed": NOW - opened_min_ago * 60}]}]


def test_reminder_due_after_first_wait_and_repeats():
    w = engine.window_reminders(_wa(12), NOW, 12, None, 3.0, {})[0]
    assert w["eligible"] and w["fire"] and w["open_min"] == 12 and "12 min" in w["message"] and "3 °C" in w["message"]
    again = engine.window_reminders(_wa(12), NOW, 12, None, 3.0, {"last_fired": {"binary_sensor.ow": NOW - 120}})[0]
    assert again["eligible"] and not again["fire"]
    later = engine.window_reminders(_wa(17), NOW, 12, None, 3.0, {"last_fired": {"binary_sensor.ow": NOW - 301}})[0]
    assert later["fire"]


def test_reminder_gates():
    def f(**k):
        return engine.window_reminders(_wa(k.pop("age", 12)), NOW, k.pop("hour", 12), k.pop("cfg", None), k.pop("t", 3.0), k.pop("st", {}))[0]

    assert f(age=5)["reason"] == "early"
    assert f(t=15)["reason"] == "warm"
    assert f(hour=23)["reason"] == "hours" and f(hour=7)["reason"] == "hours"
    assert f(cfg={"muted": True})["reason"] == "muted"
    assert f(cfg={"ignore": ["binary_sensor.ow"]})["reason"] == "ignored"
    assert f(st={"snooze": {"binary_sensor.ow": NOW + 60}})["reason"] == "snoozed"
    assert f(st={"snooze": {"binary_sensor.ow": NOW - 60}})["eligible"]
    opened = NOW - 12 * 60
    assert f(st={"skip": {"binary_sensor.ow": opened}})["reason"] == "skipped"
    assert f(st={"skip": {"binary_sensor.ow": opened - 999}})["eligible"]
    assert f(t=None)["eligible"]


def test_closed_window_has_no_reminder_and_hours_wrap():
    assert engine.window_reminders(_wa(30, state="off"), NOW, 12, None, 3.0, {}) == []
    assert engine.in_hours(23, 22, 6) and engine.in_hours(3, 22, 6) and not engine.in_hours(12, 22, 6)


def test_shared_advice_vectors():
    import json
    vec = json.loads((pathlib.Path(__file__).parent / "vectors/advice.json").read_text(encoding="utf-8"))["vectors"]
    for v in vec:
        a = {"id": "a1", "name": "Office", "entities": []}
        if "co2" in v:
            a["entities"].append(ent("sensor.co2", "carbon_dioxide", v["co2"]))
        if "window" in v:
            a["entities"].append(ent("sensor.pm", "pm25", 5))
            a["entities"].append(ent("binary_sensor.w", "window", v["window"], dom="binary_sensor", changed=v.get("open_min", 0)))
        w = None
        if "outside" in v:
            w = {"temperature": v["outside"], "condition": v.get("condition", "")}
        if v.get("raining") is not None:
            w = {**(w or {}), "raining": v["raining"]}
        r = engine.build_model([a], set(), w, "", "en", NOW)["rooms"]
        assert r and r[0]["action"] == v["expect"], (v["name"], r and r[0]["action"])


def test_air_score_counts_time_per_day():
    days = {}
    engine.score_add(days, "2026-11-28", "good", 900)
    engine.score_add(days, "2026-11-28", "poor", 300)
    engine.score_add(days, "2026-11-28", "unknown", 5000)  # unknown levels are not counted
    engine.score_add(days, "2026-11-28", "fair", -10)  # negative spans are not counted
    assert days["2026-11-28"] == {"good": 900.0, "fair": 0.0, "poor": 300.0}
    assert engine.score_pct([days], ["2026-11-28"]) == 75


def test_air_score_needs_enough_time_and_sums_rooms_and_days():
    a, b = {}, {}
    engine.score_add(a, "d1", "good", 300)
    assert engine.score_pct([a], ["d1"]) is None  # under 10 minutes counted
    engine.score_add(a, "d2", "good", 600)
    engine.score_add(b, "d1", "poor", 900)
    assert engine.score_pct([a], ["d1", "d2"]) == 100
    assert engine.score_pct([a, b], ["d1", "d2"]) == 50  # 900 good of 1800


def test_air_score_prune_keeps_only_listed_days():
    days = {}
    for d in ("a", "b", "c"):
        engine.score_add(days, d, "good", 60)
    engine.score_prune(days, ["b", "c"])
    assert sorted(days) == ["b", "c"]
