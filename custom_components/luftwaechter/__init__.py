"""Luftwächter: room air quality, ventilation advice and a sidebar panel."""
from __future__ import annotations

from pathlib import Path

import voluptuous as vol
from homeassistant.components import panel_custom
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, PANEL_URL, STATIC_URL
from .coordinator import LuftwaechterCoordinator

PLATFORMS = ["sensor", "binary_sensor"]
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
_VERSION = "0.20.0"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    async def _refresh(call: ServiceCall) -> None:
        for coord in [v for v in hass.data.get(DOMAIN, {}).values() if hasattr(v, "async_request_refresh")]:
            await coord.async_request_refresh()

    def _coords():
        return [v for v in hass.data.get(DOMAIN, {}).values() if hasattr(v, "async_snooze")]

    async def _snooze(call: ServiceCall) -> None:
        for coord in _coords():
            await coord.async_snooze(call.data["entity_id"], call.data.get("minutes", 30))

    async def _skip(call: ServiceCall) -> None:
        for coord in _coords():
            await coord.async_skip_until_closed(call.data["entity_id"])

    async def _clear(call: ServiceCall) -> None:
        for coord in _coords():
            await coord.async_clear_snooze(call.data["entity_id"])

    ids = vol.Schema({vol.Required("entity_id"): cv.entity_ids})
    hass.services.async_register(DOMAIN, "refresh", _refresh)
    hass.services.async_register(DOMAIN, "snooze", _snooze, schema=ids.extend({vol.Optional("minutes", default=30): vol.All(vol.Coerce(float), vol.Range(min=1, max=1440))}))
    hass.services.async_register(DOMAIN, "skip_until_closed", _skip, schema=ids)
    hass.services.async_register(DOMAIN, "clear_snooze", _clear, schema=ids)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coord = LuftwaechterCoordinator(hass, entry)
    await coord.async_load_reminders()
    await coord.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coord

    if not hass.data[DOMAIN].get("panel"):
        await hass.http.async_register_static_paths(
            [StaticPathConfig(STATIC_URL, str(Path(__file__).parent / "frontend"), cache_headers=False)]
        )
        await panel_custom.async_register_panel(
            hass,
            webcomponent_name="luftwaechter-panel",
            frontend_url_path=PANEL_URL,
            module_url=f"{STATIC_URL}/luftwaechter-panel.js?v={_VERSION}",
            sidebar_title="Luftwächter",
            sidebar_icon="mdi:air-filter",
            require_admin=False,
            config={},
        )
        hass.data[DOMAIN]["panel"] = True

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_reload))
    return True


async def _reload(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return ok
