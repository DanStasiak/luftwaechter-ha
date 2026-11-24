"""Collects rooms from Home Assistant and builds the Luftwächter model."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import label_registry as lr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from . import engine
from .const import CONF_WEATHER, DOMAIN, LABEL, SCAN_SECONDS

_LOGGER = logging.getLogger(__name__)


class LuftwaechterCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass, _LOGGER, name=DOMAIN, config_entry=entry,
            update_interval=timedelta(seconds=SCAN_SECONDS),
        )
        self.entry = entry
        self.lang = "en"

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

    async def _async_update_data(self) -> dict:
        self.lang = (self.hass.config.language or "en").split("-")[0]
        areas, labelled = self._collect_areas()
        weather, rain_at = await self._weather()
        return engine.build_model(areas, labelled, weather, rain_at, self.lang, dt_util.utcnow().timestamp())
