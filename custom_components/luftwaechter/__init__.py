"""Luftwächter: room air quality, ventilation advice and a sidebar panel."""
from __future__ import annotations

from pathlib import Path

from homeassistant.components import panel_custom
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PANEL_URL, STATIC_URL
from .coordinator import LuftwaechterCoordinator

PLATFORMS = ["sensor"]
_VERSION = "0.3.0"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coord = LuftwaechterCoordinator(hass, entry)
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
