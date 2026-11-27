"""Pure rating and advice logic for Luftwächter (no Home Assistant imports).

Ported from the Windows widget so that the rooms, limits and advice are the
same everywhere: CO2 good < 1000 / fair < 1500 ppm, fine dust good < 20 / fair
< 50 ug/m3, temperature good 17-23 / fair 13-25 C, humidity good 30-60 /
fair 25-70 %.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Any

LEVELS = ("good", "fair", "poor")
COLORS = ("#2e9e5b", "#e8a317", "#d9472b")
GREY = "#7a8594"

AIR_CLASSES = ("carbon_dioxide", "pm25", "temperature", "humidity")
DEFAULT_LIMITS = {"co2": (1000, 1500), "pm25": (20, 50)}


def mold_limit(limits: dict | None) -> int:
    """Relative humidity (%) from which a room counts as mold risk; invalid values fall back to MOLD_RH."""
    try:
        v = int((limits or {}).get("mold_rh", MOLD_RH))
    except (TypeError, ValueError):
        return MOLD_RH
    return v if 50 <= v <= 90 else MOLD_RH


def norm_limits(limits: dict | None) -> dict:
    """Good/fair limits for CO2 and PM2.5; falls back to the defaults for anything missing or invalid."""
    out = dict(DEFAULT_LIMITS)
    for k, (g0, f0) in DEFAULT_LIMITS.items():
        g, f = (limits or {}).get(k, (g0, f0))
        out[k] = (g, f) if 0 < g < f else (g0, f0)
    return out
DEVICE_DOMAINS = ("light", "switch", "climate", "cover", "button")

_BAD_TEMP_NAME = re.compile(
    r"taupunkt|dew|device_temp|ger[aä]tetemp|chip|cpu|prozessor|battery|batterie"
)

CONDITIONS = {
    "de": {
        "clear-night": "klar", "cloudy": "bewölkt", "partlycloudy": "teils bewölkt",
        "sunny": "sonnig", "rainy": "Regen", "pouring": "Starkregen", "snowy": "Schnee",
        "snowy-rainy": "Schneeregen", "fog": "Nebel", "windy": "windig",
        "windy-variant": "windig", "hail": "Hagel", "lightning": "Gewitter",
        "lightning-rainy": "Gewitter", "exceptional": "Unwetter",
    },
    "en": {
        "clear-night": "clear", "cloudy": "cloudy", "partlycloudy": "partly cloudy",
        "sunny": "sunny", "rainy": "rain", "pouring": "heavy rain", "snowy": "snow",
        "snowy-rainy": "sleet", "fog": "fog", "windy": "windy",
        "windy-variant": "windy", "hail": "hail", "lightning": "thunderstorm",
        "lightning-rainy": "thunderstorm", "exceptional": "severe weather",
    },
}
ICONS = {
    "clear-night": "🌙", "cloudy": "☁️", "partlycloudy": "⛅", "sunny": "☀️",
    "rainy": "🌧️", "pouring": "🌧️", "snowy": "🌨️", "snowy-rainy": "🌨️",
    "fog": "🌫️", "windy": "💨", "windy-variant": "💨", "hail": "🌨️",
    "lightning": "⛈️", "lightning-rainy": "⛈️", "exceptional": "⚠️",
}
RAIN_CONDITIONS = (
    "rainy", "pouring", "lightning-rainy", "lightning", "snowy", "snowy-rainy", "hail",
)
BAD_OUTSIDE = ("pouring", "lightning", "lightning-rainy", "hail", "snowy-rainy", "exceptional")

TEXTS: dict[str, dict[str, str]] = {
    "de": {
        "no_data": "Keine Messwerte",
        "no_data_d": "Der Sensor meldet gerade nichts. Bitte später nochmal schauen.",
        "close": "Bitte Fenster schließen",
        "fresh": "Die Luft ist wieder frisch.",
        "cold_room": " Sonst wird es kalt im Zimmer.",
        "keep_open": "Fenster offen lassen",
        "getting_better": "Die Luft wird gerade besser.",
        "wait": "Jetzt noch nicht lüften",
        "wait_d": "Draußen ist {c}. Später lüften.",
        "severe": "Unwetter",
        "open_window": "Bitte Fenster öffnen",
        "ventilate": "Bitte lüften",
        "rain_soon": " Bald lüften: ab {t} Uhr kommt Regen.",
        "stale": " Die Luft ist verbraucht.",
        "keep_closed_w": "Fenster zu lassen",
        "no_cont": "Nicht dauerhaft lüften",
        "dust_d": "Viel Feinstaub im Raum. Nicht dauerhaft lüften.",
        "all_good": "Alles in Ordnung",
        "win_stay": "Das Fenster kann zu bleiben.",
        "air_fine": "Die Luft ist in Ordnung.",
        "how5": "Ganz öffnen, 5 Minuten lüften.",
        "how10": "Ganz öffnen, 10 Minuten lüften.",
        "how15": "Fenster öffnen, ca. 15 Minuten lüften.",
        "silent": "⚠ {n} meldet seit {m} min nichts",
        "ignored": "⚠ ignoriert (veraltet): {n}",
        "tip_good": "Gute Zeit zum Lüften.",
        "tip_rain": "Es regnet: Fenster nur kurz öffnen (Stoßlüften 3 Min) oder in einer Regenpause lüften.",
        "tip_rain_soon": "Gute Zeit zum Lüften, ab {t} Uhr kommt Regen.",
        "tip_cold": "Es ist kalt: lieber kurz und ganz öffnen (Stoßlüften 5 Min), das spart Heizenergie.",
        "tip_warm": "Es ist warm draußen: morgens oder abends lüften, tagsüber Fenster zu lassen.",
        "tip_humid": "Draußen ist es feucht: kurz lüften, nicht dauerhaft kippen.",
        "mold_d": " Hohe Luftfeuchtigkeit: Schimmelgefahr. Möbel nicht dicht an kalte Außenwände stellen.",
        "heating": "Heizung",
        "now": "Ist {t} °C",
        "heating_on": " · heizt",
        "heating_off": " · aus",
        "close_cold": "Die Luft ist in Ordnung und draußen sind {t} °C. Zu lassen spart Heizenergie.",
        "close_rain": " Es regnet draußen.",
        "open_for": " Fenster seit {m} min offen.",
        "open": "offen", "closed": "zu", "opening": "öffnet", "closing": "schließt",
        "dirs": "N,NO,O,SO,S,SW,W,NW",
        "g_light": "Licht", "g_power": "Strom", "g_heat": "Heizung", "g_cover": "Rollo",
    },
    "en": {
        "no_data": "No data",
        "no_data_d": "The sensor is not reporting right now. Please check again later.",
        "close": "Please close the window",
        "fresh": "The air is fresh again.",
        "cold_room": " Otherwise the room gets cold.",
        "keep_open": "Keep the window open",
        "getting_better": "The air is getting better.",
        "wait": "Do not ventilate yet",
        "wait_d": "Outside: {c}. Ventilate later.",
        "severe": "severe weather",
        "open_window": "Please open the window",
        "ventilate": "Please ventilate",
        "rain_soon": " Ventilate soon: rain from {t}.",
        "stale": " The air is stale.",
        "keep_closed_w": "Keep the window closed",
        "no_cont": "Do not ventilate continuously",
        "dust_d": "High fine dust in the room. Do not ventilate continuously.",
        "all_good": "All good",
        "win_stay": "The window can stay closed.",
        "air_fine": "The air is fine.",
        "how5": "Open fully, ventilate for 5 minutes.",
        "how10": "Open fully, ventilate for 10 minutes.",
        "how15": "Open the window, ventilate for about 15 minutes.",
        "silent": "⚠ {n} silent for {m} min",
        "ignored": "⚠ ignored (stale): {n}",
        "tip_good": "Good time to ventilate.",
        "tip_rain": "It is raining: open the window only briefly (3 min burst) or wait for a break in the rain.",
        "tip_rain_soon": "Good time to ventilate, rain from {t}.",
        "tip_cold": "It is cold: better open fully for a short time (5 min burst), it saves heating energy.",
        "tip_warm": "It is warm outside: ventilate in the morning or evening, keep windows closed during the day.",
        "tip_humid": "It is humid outside: ventilate briefly, do not leave the window tilted.",
        "mold_d": " High humidity: mold risk. Keep furniture off cold outer walls.",
        "heating": "Heating",
        "now": "Now {t} °C",
        "heating_on": " · heating",
        "heating_off": " · off",
        "close_cold": "The air is fine and it is {t} °C outside. Closing saves heating energy.",
        "close_rain": " It is raining outside.",
        "open_for": " Window open for {m} min.",
        "open": "open", "closed": "closed", "opening": "opening", "closing": "closing",
        "dirs": "N,NE,E,SE,S,SW,W,NW",
        "g_light": "Light", "g_power": "Power", "g_heat": "Heating", "g_cover": "Blinds",
    },
}


def tx(lang: str, key: str, **kw: Any) -> str:
    table = TEXTS.get(lang) or TEXTS["en"]
    s = table.get(key, key)
    return s.format(**kw) if kw else s


def num(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


def level_above(v: float | None, good: float, fair: float) -> int | None:
    if v is None:
        return None
    if v < good:
        return 0
    if v < fair:
        return 1
    return 2


def level_range(v: float | None, g1: float, g2: float, f1: float, f2: float) -> int | None:
    if v is None:
        return None
    if g1 <= v <= g2:
        return 0
    if f1 <= v <= f2:
        return 1
    return 2


def is_candidate(e: dict, dc: str) -> bool:
    v = num(e.get("state"))
    if v is None:
        return False
    t = f"{e.get('entity_id', '')} {e.get('name', '')}".lower()
    if dc == "temperature":
        if _BAD_TEMP_NAME.search(t):
            return False
        return -30 < v < 60
    if dc == "humidity":
        if "absolut" in t:
            return False
        return 0 <= v <= 100
    if dc == "carbon_dioxide":
        return 250 <= v <= 10000
    return 0 <= v <= 2000


def short_name(name: str, room: str) -> str:
    if room and name.lower().startswith(room.lower()):
        name = name[len(room):].lstrip(" -:·").strip()
    if len(name) > 34:
        name = name[:33] + "…"
    return name


@dataclass
class Picked:
    value: float
    count: int
    age_min: int
    skipped: list[str]
    name: str
    dc: str
    entity_ids: list[str] = field(default_factory=list)


def pick_val(ents: list[dict], dc: str, labelled: set[str], room: str, now: float) -> Picked | None:
    c = [e for e in ents if e["domain"] == "sensor" and e.get("device_class") == dc and is_candidate(e, dc)]
    if not c:
        return None
    lb = [e for e in c if e["entity_id"] in labelled]
    if lb:
        c = lb
    stamps = [e.get("last_reported") or 0 for e in c]
    mx = max(stamps)
    skipped: list[str] = []
    lim = 21600 if dc in ("temperature", "humidity") else 1800
    if mx > 0:
        fresh = [e for e in c if (e.get("last_reported") or 0) >= mx - lim]
        if fresh:
            skipped = [short_name(e["name"], room) for e in c if (e.get("last_reported") or 0) < mx - lim]
            c = fresh
    vals = [num(e["state"]) or 0.0 for e in c]
    age = int(max(0, (now - mx) / 60)) if mx > 0 else 0
    return Picked(
        value=sum(vals) / len(vals), count=len(c), age_min=age, skipped=skipped,
        name=short_name(c[0]["name"], room), dc=dc, entity_ids=[e["entity_id"] for e in c],
    )


@dataclass
class RoomEval:
    key: str
    name: str
    co2: float | None
    pm: float | None
    t: float | None
    h: float | None
    levels: list[int | None]
    worst: int | None
    has_air: bool
    warn: str
    nsrc: int
    sources: dict[str, list[str]]
    entities: list[dict]


def eval_room(area: dict, labelled: set[str], lang: str, now: float, limits: dict | None = None) -> RoomEval:
    lim_ = norm_limits(limits)
    ents = area["entities"]
    name = area["name"]
    picks = {dc: pick_val(ents, dc, labelled, name, now) for dc in AIR_CLASSES}
    co2, pm, tt, hh = (picks[c].value if picks[c] else None for c in AIR_CLASSES)
    warn = ""
    for pv in picks.values():
        if not pv or warn:
            continue
        lim = 360 if pv.dc in ("temperature", "humidity") else 20
        if pv.age_min >= lim:
            warn = tx(lang, "silent", n=pv.name, m=pv.age_min)
        elif pv.skipped:
            warn = tx(lang, "ignored", n=pv.skipped[0])
    has_air = any(e["domain"] == "sensor" and e.get("device_class") in ("carbon_dioxide", "pm25") for e in ents)
    levels = [
        level_above(co2, *lim_["co2"]),
        level_above(pm, *lim_["pm25"]),
        level_range(tt, 17, 23, 13, 25),
        level_range(hh, 30, 60, 25, 70),
    ]
    known = [lv for lv in levels if lv is not None]
    return RoomEval(
        key=area["id"], name=name, co2=co2, pm=pm, t=tt, h=hh, levels=levels,
        worst=max(known) if known else None, has_air=has_air, warn=warn,
        nsrc=sum(p.count for p in picks.values() if p),
        sources={dc: (picks[dc].entity_ids if picks[dc] else []) for dc in AIR_CLASSES},
        entities=ents,
    )


def fmt(v: float | None, digits: int, lang: str) -> str:
    if v is None:
        return "–"
    s = f"{v:.{digits}f}"
    if float(s) == 0:
        s = s.lstrip("-")
    return s.replace(".", ",") if lang == "de" else s


def first_rain_hour(forecast: list[dict], now_ts: float, parse_ts) -> float | None:
    """Return the timestamp of the first hour in the next 6 h with rain/snow/thunder."""
    for f in forecast or []:
        t = parse_ts(f.get("datetime"))
        if t is None or t <= now_ts:
            continue
        if (t - now_ts) / 3600 > 6:
            break
        pr = num(f.get("precipitation"))
        if f.get("condition") in RAIN_CONDITIONS or (pr is not None and pr >= 0.3):
            return t
    return None


def outside_view(weather: dict | None, rain_at: str, lang: str) -> dict | None:
    if not weather:
        return None
    ot = num(weather.get("temperature"))
    if ot is None:
        return None
    cond = str(weather.get("condition") or "")
    ws = num(weather.get("wind_speed"))
    unit = weather.get("wind_speed_unit")
    if ws is not None:
        if unit == "m/s":
            ws *= 3.6
        elif unit == "mph":
            ws *= 1.609344
        elif unit == "kn":
            ws *= 1.852
    dirs = tx(lang, "dirs").split(",")
    wb = num(weather.get("wind_bearing"))
    wind_dir = dirs[int(round(wb / 45.0)) % 8] if wb is not None else str(weather.get("wind_bearing") or "")
    oh = num(weather.get("humidity"))
    tip = tx(lang, "tip_good")
    if cond in ("rainy", "pouring"):
        tip = tx(lang, "tip_rain")
    elif rain_at:
        tip = tx(lang, "tip_rain_soon", t=rain_at)
    elif ot < 5:
        tip = tx(lang, "tip_cold")
    elif ot >= 25:
        tip = tx(lang, "tip_warm")
    elif oh is not None and oh > 90:
        tip = tx(lang, "tip_humid")
    return {
        "temp": fmt(ot, 0, lang), "cond": CONDITIONS[lang].get(cond, cond), "icon": ICONS.get(cond, ""),
        "wind": fmt(ws, 0, lang), "windDir": wind_dir, "hum": fmt(oh, 0, lang),
        "cloud": fmt(num(weather.get("cloud_coverage")), 0, lang), "press": fmt(num(weather.get("pressure")), 0, lang),
        "tip": tip, "raw_temp": ot, "raw_cond": cond,
    }


def devices_view(room: RoomEval, labelled: set[str], lang: str) -> list[dict]:
    groups = {
        "light": (tx(lang, "g_light"), "switch"), "switch": (tx(lang, "g_power"), "switch"),
        "climate": (tx(lang, "g_heat"), "climate"), "cover": (tx(lang, "g_cover"), "cover"),
        "button": (tx(lang, "g_power"), "button"),
    }
    use_lab = len(labelled) > 0
    out = []
    for e in room.entities:
        dom = e["domain"]
        if dom not in groups:
            continue
        if dom in ("button", "switch") and not use_lab:
            continue
        if use_lab and e["entity_id"] not in labelled:
            continue
        if e["state"] in ("unavailable", "unknown"):
            continue
        nm = e["name"]
        if nm.lower().startswith(room.name.lower() + " ") and len(nm) > len(room.name) + 1:
            nm = nm[len(room.name) + 1:]
        nm = re.sub(r"\s+-\s+(Schalter|Switch)$", "", nm)
        if dom == "climate" and nm.lower() == room.name.lower():
            nm = tx(lang, "heating")
        out.append({"entity": e["entity_id"], "name": nm, "group": groups[dom][0], "type": groups[dom][1], "domain": dom})
    return out


MOLD_RH = 70  # sustained relative humidity above this invites mold on cold surfaces


def dew_point(t: float | None, h: float | None) -> float | None:
    """Dew point in °C (Magnus formula); None when temperature or humidity is missing."""
    if t is None or h is None or h <= 0:
        return None
    a, b = 17.62, 243.12
    g = math.log(h / 100.0) + a * t / (b + t)
    return b * g / (a - g)


COLD_OUTSIDE = 10  # deg C: below this an open window with good air should be closed
CLOSE_AFTER_MIN = 5
_WINDOW_NAME = re.compile(r"fenster|window")


def is_window(e: dict) -> bool:
    """Window contact: device class window or opening; a door contact only when its name says window."""
    if e.get("domain") != "binary_sensor":
        return False
    dc = e.get("device_class")
    if dc in ("window", "opening"):
        return True
    return dc == "door" and bool(_WINDOW_NAME.search(f"{e.get('entity_id', '')} {e.get('name', '')}".lower()))


def advice(room: RoomEval, weather: dict | None, rain_at: str, lang: str, limits: dict | None = None, now: float = 0.0) -> dict:
    lim_ = norm_limits(limits)
    co2_good, co2_fair = lim_["co2"]
    pm_dust = sum(lim_["pm25"]) / 2
    co2, pm, tt, hh = room.co2, room.pm, room.t, room.h
    wins = [e for e in room.entities if is_window(e)]
    has_window = bool(wins)
    wst = "unknown"
    if has_window:
        if any(e["state"] == "on" for e in wins):
            wst = "open"
        elif all(e["state"] == "off" for e in wins):
            wst = "closed"
    open_min = 0
    if wst == "open" and now:
        stamps = [e.get("last_changed") or 0 for e in wins if e["state"] == "on"]
        stamps = [x for x in stamps if x]
        if stamps:
            open_min = int(max(0, (now - min(stamps)) / 60))
    ot = num(weather.get("temperature")) if weather else None
    cond = str(weather.get("condition") or "") if weather else ""
    bad_out = cond in BAD_OUTSIDE
    need_vent = (
        (co2 is not None and co2 >= co2_good)
        or (hh is not None and hh > 60)
        or (tt is not None and tt >= 25 and ot is not None and ot < tt - 2)
    )
    if ot is not None and ot < 5:
        how, how_m = tx(lang, "how5"), 5
    elif ot is not None and ot < 15:
        how, how_m = tx(lang, "how10"), 10
    else:
        how, how_m = tx(lang, "how15"), 15
    vent_min = 0
    if co2 is None and pm is None:
        action, head, detail = "unknown", tx(lang, "no_data"), tx(lang, "no_data_d")
    elif wst == "open":
        if co2 is not None and co2 < 700 and not (tt is not None and tt >= 25) and not (hh is not None and hh > 60):
            action, head, detail = "close", tx(lang, "close"), tx(lang, "fresh")
            if ot is not None and ot < 15:
                detail += tx(lang, "cold_room")
        elif co2 is not None and co2 < co2_good and not (tt is not None and tt >= 25) and not (hh is not None and hh > 60) and (
            (ot is not None and ot < COLD_OUTSIDE and open_min >= CLOSE_AFTER_MIN) or cond in RAIN_CONDITIONS
        ):
            action, head = "close", tx(lang, "close")
            detail = tx(lang, "close_cold", t=fmt(ot, 0, lang)) if ot is not None and ot < COLD_OUTSIDE else tx(lang, "fresh")
            if cond in RAIN_CONDITIONS:
                detail += tx(lang, "close_rain")
        else:
            action, head, detail, vent_min = "keep_open", tx(lang, "keep_open"), tx(lang, "getting_better"), how_m
    elif need_vent:
        if bad_out:
            cd = CONDITIONS[lang].get(cond) or tx(lang, "severe")
            action, head, detail = "wait", tx(lang, "wait"), tx(lang, "wait_d", c=cd)
        else:
            action = "open"
            head = tx(lang, "open_window") if has_window else tx(lang, "ventilate")
            detail = how
            if rain_at:
                detail += tx(lang, "rain_soon", t=rain_at)
            if co2 is not None and co2 >= co2_fair:
                detail += tx(lang, "stale")
    elif pm is not None and pm >= pm_dust:
        action = "keep_closed"
        head = tx(lang, "keep_closed_w") if has_window else tx(lang, "no_cont")
        detail = tx(lang, "dust_d")
    else:
        action, head = "keep_closed", tx(lang, "all_good")
        detail = tx(lang, "win_stay") if has_window else tx(lang, "air_fine")
    if wst == "open" and open_min >= CLOSE_AFTER_MIN and action in ("close", "keep_open"):
        detail += tx(lang, "open_for", m=open_min)
    mold = hh is not None and hh >= mold_limit(limits) and action != "unknown"
    if mold:
        detail += tx(lang, "mold_d")
    return {
        "action": action, "headline": head, "detail": detail, "window": wst, "hasWindow": has_window,
        "ventMin": vent_min, "openMin": open_min, "mold": mold, "dew": fmt(dew_point(tt, hh), 1, lang) if dew_point(tt, hh) is not None else "",
    }


def room_view(room: RoomEval, weather: dict | None, rain_at: str, labelled: set[str], lang: str, limits: dict | None = None, now: float = 0.0) -> dict:
    worst = room.worst
    adv = advice(room, weather, rain_at, lang, limits, now)
    keys = ("co2", "pm25", "temperature", "humidity")
    units = ("ppm", "µg/m³", "°C", "%")
    vals = (room.co2, room.pm, room.t, room.h)
    digits = (0, 0, 1, 0)
    values = [
        {"key": k, "value": fmt(v, d, lang), "raw": v, "unit": u, "level": lv}
        for k, v, d, u, lv in zip(keys, vals, digits, units, room.levels, strict=True)
    ]
    return {
        "key": room.key, "name": room.name,
        "level": LEVELS[worst] if worst is not None else "unknown",
        "color": COLORS[worst] if worst is not None else GREY,
        **adv,
        "values": values, "warn": room.warn, "nsrc": room.nsrc, "sources": room.sources,
        "devices": devices_view(room, labelled, lang), "trend": "",
    }


def _model_for(areas: list[dict], labelled: set[str], weather: dict | None, rain_at: str, lang: str, now: float, limits: dict | None = None) -> tuple[list[dict], dict | None]:
    evals = [eval_room(a, labelled, lang, now, limits) for a in areas]
    evals = sorted([e for e in evals if e.has_air], key=lambda e: e.name.lower())
    rooms = [room_view(e, weather, rain_at, labelled, lang, limits, now) for e in evals]
    return rooms, outside_view(weather, rain_at, lang)


def build_model(areas: list[dict], labelled: set[str], weather: dict | None, rain_at: str, lang: str, now: float, limits: dict | None = None) -> dict:
    lang = lang if lang in TEXTS else "en"
    rooms, outside = _model_for(areas, labelled, weather, rain_at, lang, now, limits)
    summary = [
        {"key": r["key"], "name": r["name"], "level": r["level"], "color": r["color"],
         "co2": "" if r["values"][0]["raw"] is None else str(round(r["values"][0]["raw"]))}
        for r in rooms
    ]
    worst = max((LEVELS.index(r["level"]) for r in rooms if r["level"] in LEVELS), default=None)
    # The same texts in every other language, so the panel can follow each user's own profile language.
    alt = {}
    for other in TEXTS:
        if other != lang:
            o_rooms, o_outside = _model_for(areas, labelled, weather, rain_at, other, now, limits)
            alt[other] = {"rooms": o_rooms, "outside": o_outside}
    attn = [r for r in rooms if r["level"] == "poor" or r["action"] in ("open", "wait", "keep_open", "close")]
    co2s = [r["values"][0]["raw"] for r in rooms if r["values"] and r["values"][0]["raw"] is not None]
    co2_avg = round(sum(co2s) / len(co2s)) if co2s else None
    temps = [r["values"][2]["raw"] for r in rooms if len(r["values"]) > 2 and r["values"][2]["raw"] is not None]
    hums = [r["values"][3]["raw"] for r in rooms if len(r["values"]) > 3 and r["values"][3]["raw"] is not None]
    temp_avg = round(sum(temps) / len(temps), 1) if temps else None
    rh_avg = round(sum(hums) / len(hums)) if hums else None
    worst_room = ""
    if worst is not None:
        worst_room = next((r["name"] for r in rooms if r["level"] == LEVELS[worst]), "")
    return {
        "rooms": rooms, "summary": summary,
        "good": sum(1 for r in rooms if r["level"] == "good"), "total": len(rooms),
        "attention": len(attn), "attention_rooms": [r["name"] for r in attn],
        "silent_rooms": [r["name"] for r in rooms if r.get("warn")],
        "co2_avg": co2_avg, "temp_avg": temp_avg, "rh_avg": rh_avg, "mold_rh": mold_limit(limits), "mold": sum(1 for r in rooms if r.get("mold")), "mold_rooms": [r["name"] for r in rooms if r.get("mold")],
        "ventilate": sum(1 for r in rooms if r["action"] == "open"),
        "ventilate_rooms": [r["name"] for r in rooms if r["action"] == "open"], "worst_room": worst_room,
        "close": sum(1 for r in rooms if r["action"] == "close"),
        "close_rooms": [r["name"] for r in rooms if r["action"] == "close"],
        "level": LEVELS[worst] if worst is not None else "unknown",
        "outside": outside, "lang": lang, "alt": alt,
        "limits": {k: list(v) for k, v in norm_limits(limits).items()}, "colors": list(COLORS),
        "updated": int(now),
    }
