"""Diagnostics for Luftwächter: what the integration sees, for bug reports."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    coord = hass.data[DOMAIN][entry.entry_id]
    model = coord.data or {}
    return {
        "entry": {"data": dict(entry.data), "options": dict(entry.options)},
        "language": coord.lang,
        "rooms": [
            {
                "key": r["key"], "level": r["level"], "action": r["action"],
                "values": {v["key"]: v["raw"] for v in r["values"]},
                "sources": r["sources"], "warn": r["warn"],
                "devices": [d["entity"] for d in r["devices"]],
            }
            for r in model.get("rooms", [])
        ],
        "level": model.get("level"),
        "outside": model.get("outside"),
        "updated": model.get("updated"),
    }
