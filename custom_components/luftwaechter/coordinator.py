"""Collects rooms from Home Assistant and builds the Luftwächter model."""
from __future__ import annotations

import logging
from collections import deque
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import issue_registry as ir
from homeassistant.helpers import label_registry as lr
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from . import engine
from .const import (
    CONF_CO2_FAIR,
    CONF_CO2_GOOD,
    CONF_EXCLUDE,
    CONF_IGNORE,
    CONF_MOLD_RH,
    CONF_MUTE,
    CONF_OUTSIDE_TEMP,
    CONF_PM_FAIR,
    CONF_PM_GOOD,
    CONF_RAIN,
    CONF_REM_BELOW,
    CONF_REM_FIRST,
    CONF_REM_FROM,
    CONF_REM_REPEAT,
    CONF_REM_TO,
    CONF_STALE,
    CONF_WEATHER,
    DEFAULT_STALE,
    DOMAIN,
    EMPTY_BEFORE_ISSUE,
    EVENT_LEVEL_CHANGED,
    EVENT_REMINDER,
    ISSUE_NO_ROOMS,
    LABEL,
    SCAN_SECONDS,
    STORE_KEY,
)

_LOGGER = logging.getLogger(__name__)


class LuftwaechterCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass, _LOGGER, name=DOMAIN, config_entry=entry,
            update_interval=timedelta(seconds=SCAN_SECONDS),
        )
        self.entry = entry
        self.lang = "en"
        self._samples: dict[str, deque] = {}
        self._levels: dict[str, str] | None = None
        self._since: dict[str, tuple[str, float]] = {}
        self._empty = 0
        self._store: Store = Store(hass, 1, f"{STORE_KEY}.{entry.entry_id}")
        self._rem: dict[str, dict] = {"snooze": {}, "skip": {}}
        self._fired: dict[str, float] = {}
        self._score: dict[str, dict[str, dict[str, float]]] = {}
        self._score_ts: float | None = None
        self._score_saved = 0.0

    async def async_load_reminders(self) -> None:
        data = await self._store.async_load() or {}
        self._rem = {"snooze": dict(data.get("snooze", {})), "skip": dict(data.get("skip", {}))}
        score = data.get("score")
        if isinstance(score, dict):
            for room, days in score.items():
                if isinstance(days, dict):
                    self._score[str(room)] = {
                        str(d): {k: float(v.get(k, 0.0)) for k in ("good", "fair", "poor")}
                        for d, v in days.items() if isinstance(v, dict)
                    }

    async def _save_reminders(self) -> None:
        now = dt_util.utcnow().timestamp()
        self._rem["snooze"] = {k: v for k, v in self._rem["snooze"].items() if v > now}
        await self._store.async_save({**self._rem, "score": self._score})

    def _track_score(self, model: dict, now: float) -> None:
        """Count how long each room spent in good, fair and poor air today and over the last 7 days (kept across restarts)."""
        local = dt_util.as_local(dt_util.utc_from_timestamp(now)).date()
        today = local.isoformat()
        keys = [(local - timedelta(days=i)).isoformat() for i in range(engine.SCORE_DAYS)]
        span = 0.0
        if self._score_ts is not None:
            span = min(max(now - self._score_ts, 0.0), SCAN_SECONDS * 3)  # a gap (restart, outage) is not counted
        self._score_ts = now
        for r in model["rooms"]:
            days = self._score.setdefault(r["key"], {})
            engine.score_add(days, today, r["level"], span)
            engine.score_prune(days, keys)
        week_keys = [k for k in keys]
        rooms_days = [self._score.get(r["key"], {}) for r in model["rooms"]]
        house = {"today": engine.score_pct(rooms_days, [today]), "week": engine.score_pct(rooms_days, week_keys)}
        per_room = {
            r["key"]: {
                "today": engine.score_pct([self._score.get(r["key"], {})], [today]),
                "week": engine.score_pct([self._score.get(r["key"], {})], week_keys),
            }
            for r in model["rooms"]
        }
        model["score_today"], model["score_week"] = house["today"], house["week"]
        for rooms in [model["rooms"]] + [a["rooms"] for a in model.get("alt", {}).values()]:
            for r in rooms:
                r["score"] = per_room.get(r["key"], {"today": None, "week": None})
        if now - self._score_saved >= 300:
            self._score_saved = now
            self.hass.async_create_task(self._save_reminders())

    async def async_snooze(self, entity_ids: list[str], minutes: float) -> None:
        until = dt_util.utcnow().timestamp() + float(minutes) * 60
        for eid in entity_ids:
            self._rem["snooze"][eid] = until
            self._fired.pop(eid, None)
        await self._save_reminders()
        await self.async_request_refresh()

    async def async_skip_until_closed(self, entity_ids: list[str]) -> None:
        for eid in entity_ids:
            st = self.hass.states.get(eid)
            if st is not None and st.state == "on":
                self._rem["skip"][eid] = st.last_changed.timestamp()
        await self._save_reminders()
        await self.async_request_refresh()

    def fire_test_reminder(self, room: str | None = None, message: str | None = None) -> None:
        """Fire one sample reminder event so the phone/speaker automation can be tested without opening a window."""
        de = self.lang == "de"
        room = room or ("Testraum" if de else "Test room")
        message = message or ("Das ist ein Test: Das Fenster ist seit 10 Minuten offen." if de else "This is a test: the window has been open for 10 minutes.")
        self.hass.bus.async_fire(EVENT_REMINDER, {
            "room": room, "room_key": "test", "window": "Test window", "entity_id": "binary_sensor.luftwaechter_test_window",
            "minutes_open": 10, "outside_temp": None, "message": message, "test": True,
        })

    async def async_clear_snooze(self, entity_ids: list[str]) -> None:
        for eid in entity_ids:
            self._rem["snooze"].pop(eid, None)
            self._rem["skip"].pop(eid, None)
        await self._save_reminders()
        await self.async_request_refresh()

    def _reminders(self, areas: list[dict], outside_t: float | None, now: float) -> list[dict]:
        o = self.entry.options
        muted = any((s := self.hass.states.get(e)) is not None and s.state == "on" for e in (o.get(CONF_MUTE) or []))
        cfg = {
            "first": o.get(CONF_REM_FIRST, 10), "repeat": o.get(CONF_REM_REPEAT, 5), "below": o.get(CONF_REM_BELOW, 10),
            "from": o.get(CONF_REM_FROM, 8), "to": o.get(CONF_REM_TO, 22),
            "ignore": set(o.get(CONF_IGNORE) or []), "muted": muted,
        }
        hour = dt_util.as_local(dt_util.utc_from_timestamp(now)).hour
        wins = engine.window_reminders(
            areas, now, hour, cfg, outside_t, {**self._rem, "last_fired": self._fired}, self.lang if self.lang in engine.TEXTS else "en"
        )
        open_ids = {w["entity_id"] for w in wins}
        for eid in [k for k in self._fired if k not in open_ids]:
            self._fired.pop(eid, None)
        for eid in [k for k in self._rem["skip"] if k not in open_ids]:
            self._rem["skip"].pop(eid, None)
        for w in wins:
            if w["fire"]:
                self._fired[w["entity_id"]] = now
                self.hass.bus.async_fire(EVENT_REMINDER, {
                    "room": w["room"], "room_key": w["room_key"], "window": w["window"], "entity_id": w["entity_id"],
                    "minutes_open": w["open_min"], "outside_temp": outside_t, "message": w["message"],
                })
        return wins

    @property
    def weather_entity(self) -> str | None:
        return self.entry.options.get(CONF_WEATHER) or self.entry.data.get(CONF_WEATHER)

    def _collect_areas(self) -> tuple[list[dict], set[str]]:
        areas_reg = ar.async_get(self.hass)
        ent_reg = er.async_get(self.hass)
        dev_reg = dr.async_get(self.hass)
        lab_reg = lr.async_get(self.hass)
        label_ids = {lb.label_id for lb in lab_reg.async_list_labels() if lb.name.lower() == LABEL or lb.label_id == LABEL}
        labelled: set[str] = set()
        by_area: dict[str, list[dict]] = {}
        for ent in ent_reg.entities.values():
            if ent.disabled_by or ent.hidden_by:
                continue
            if ent.entity_category is not None:  # config / diagnostic entities are not controls
                continue
            area_id = ent.area_id
            if not area_id and ent.device_id:
                dev = dev_reg.async_get(ent.device_id)
                area_id = dev.area_id if dev else None
            if not area_id:
                continue
            st = self.hass.states.get(ent.entity_id)
            if st is None:
                continue
            if label_ids & set(ent.labels):
                labelled.add(ent.entity_id)
            by_area.setdefault(area_id, []).append(
                {
                    "entity_id": ent.entity_id,
                    "domain": ent.domain,
                    "name": st.name or ent.name or ent.original_name or ent.entity_id,
                    "state": st.state,
                    "device_class": st.attributes.get("device_class") or ent.original_device_class,
                    "last_reported": st.last_reported.timestamp() if st.last_reported else 0,
                    "last_changed": st.last_changed.timestamp() if st.last_changed else 0,
                }
            )
        areas = []
        for area_id, ents in by_area.items():
            area = areas_reg.async_get_area(area_id)
            if area:
                areas.append({"id": area_id, "name": area.name, "entities": ents})
        return areas, labelled

    async def _weather(self) -> tuple[dict | None, str]:
        eid = self.weather_entity
        if not eid:
            return None, ""
        st = self.hass.states.get(eid)
        if st is None or st.state in ("unavailable", "unknown"):
            return None, ""
        weather = {**st.attributes, "condition": st.state}
        weather.setdefault("temperature", st.attributes.get("temperature"))
        rain_at = ""
        try:
            resp = await self.hass.services.async_call(
                "weather", "get_forecasts", {"entity_id": eid, "type": "hourly"},
                blocking=True, return_response=True,
            )
            fc = (resp or {}).get(eid, {}).get("forecast", [])
            now = dt_util.utcnow().timestamp()
            ts = engine.first_rain_hour(
                fc, now, lambda s: dt_util.parse_datetime(s).timestamp() if s and dt_util.parse_datetime(s) else None
            )
            if ts:
                rain_at = dt_util.as_local(dt_util.utc_from_timestamp(ts)).strftime("%H:%M")
        except Exception:  # forecast is optional
            _LOGGER.debug("No hourly forecast for %s", eid)
        return weather, rain_at

    def _outside_temp(self) -> float | None:
        eid = self.entry.options.get(CONF_OUTSIDE_TEMP)
        st = self.hass.states.get(eid) if eid else None
        if st is None:
            return None
        v = engine.num(st.state)
        return v if v is not None and -60 < v < 60 else None

    def _rain_now(self) -> bool | None:
        """State of the rain sensor: the one picked in the options, else a binary sensor named rain / Regen. None when there is none."""
        eid = self.entry.options.get(CONF_RAIN)
        st = self.hass.states.get(eid) if eid else None
        if st is None:
            for cand in self.hass.states.async_all("binary_sensor"):
                if engine.is_rain_sensor(cand.entity_id, cand.name):
                    st = cand
                    break
        if st is None or st.state not in ("on", "off"):
            return None
        return st.state == "on"

    def _limits(self) -> dict:
        o = self.entry.options
        return {
            "co2": (o.get(CONF_CO2_GOOD, 1000), o.get(CONF_CO2_FAIR, 1500)),
            "pm25": (o.get(CONF_PM_GOOD, 20), o.get(CONF_PM_FAIR, 50)),
            "mold_rh": o.get(CONF_MOLD_RH, 70),
        }

    def _annotate(self, model: dict) -> None:
        """Add a rising/falling trend per room and fire an event when a room's level changes."""
        now = model["updated"]
        trends: dict[str, str] = {}
        sparks: dict[str, list[int]] = {}
        sinces: dict[str, int] = {}
        for r in model["rooms"]:
            co2 = next((v["raw"] for v in r["values"] if v["key"] == "co2"), None)
            pm = next((v["raw"] for v in r["values"] if v["key"] == "pm25"), None)
            kind, val, step = ("co2", co2, 40) if co2 is not None else ("pm25", pm, 4)
            q = self._samples.setdefault(r["key"], deque(maxlen=60))
            trend = ""
            if val is not None:
                old = [s for s in q if s[1] == kind and 480 <= now - s[0] <= 1800]
                if old:
                    ref = min(old, key=lambda s: abs((now - s[0]) - 900))
                    diff = val - ref[2]
                    trend = "up" if diff > step else "down" if diff < -step else "flat"
                q.append((now, kind, val))
            trends[r["key"]] = trend
            spark = [round(s[2]) for s in q if s[1] == kind][-30:]
            sparks[r["key"]] = spark if len(spark) >= 3 else []
            prev = self._since.get(r["key"])
            if prev is None or prev[0] != r["level"]:
                self._since[r["key"]] = (r["level"], now)
            sinces[r["key"]] = int((now - self._since[r["key"]][1]) // 60)
        for rooms in [model["rooms"]] + [a["rooms"] for a in model.get("alt", {}).values()]:
            for r in rooms:
                r["trend"] = trends.get(r["key"], "")
                r["spark"] = sparks.get(r["key"], [])
                r["since"] = sinces.get(r["key"], 0)
        levels = {r["key"]: r["level"] for r in model["rooms"]}
        if self._levels is not None:
            for r in model["rooms"]:
                old = self._levels.get(r["key"])
                if old is not None and old != r["level"]:
                    self.hass.bus.async_fire(
                        EVENT_LEVEL_CHANGED,
                        {"room": r["name"], "room_key": r["key"], "from": old, "to": r["level"], "headline": r["headline"]},
                    )
        self._levels = levels

    def _check_rooms(self, model: dict) -> None:
        """Raise a repair issue when no room has been found for a while (about 5 minutes), clear it once rooms appear."""
        self._empty = 0 if model["rooms"] else self._empty + 1
        if self._empty >= EMPTY_BEFORE_ISSUE:
            ir.async_create_issue(
                self.hass, DOMAIN, ISSUE_NO_ROOMS, is_fixable=False, severity=ir.IssueSeverity.WARNING, translation_key=ISSUE_NO_ROOMS
            )
        elif model["rooms"]:
            ir.async_delete_issue(self.hass, DOMAIN, ISSUE_NO_ROOMS)

    async def _async_update_data(self) -> dict:
        self.lang = (self.hass.config.language or "en").split("-")[0]
        areas, labelled = self._collect_areas()
        excluded = set(self.entry.options.get(CONF_EXCLUDE) or [])
        areas = [a for a in areas if a["id"] not in excluded]
        weather, rain_at = await self._weather()
        outside_sensor = self._outside_temp()
        if outside_sensor is not None:
            weather = {**(weather or {}), "temperature": outside_sensor}
        raining = self._rain_now()
        if raining is not None:
            weather = {**(weather or {}), "raining": raining}
        model = engine.build_model(areas, labelled, weather, rain_at, self.lang, dt_util.utcnow().timestamp(), self._limits())
        outside_t = engine.num((weather or {}).get("temperature"))
        wins = self._reminders(areas, outside_t, dt_util.utcnow().timestamp())
        model["windows"] = wins
        model["reminders_due"] = sum(1 for w in wins if w["eligible"])
        model["window_areas"] = [
            {"key": a["id"], "name": a["name"]} for a in areas if any(engine.is_window(e) for e in a["entities"])
        ]
        for r in model["rooms"]:
            r["windowReminder"] = any(w["eligible"] and w["room_key"] == r["key"] for w in wins)
        self._annotate(model)
        self._track_score(model, dt_util.utcnow().timestamp())
        self._check_rooms(model)
        model["stale_min"] = int(self.entry.options.get(CONF_STALE, DEFAULT_STALE) or DEFAULT_STALE)
        return model
