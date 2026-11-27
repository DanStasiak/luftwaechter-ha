"""System health info for Luftwächter (Settings → System → Repairs → three dots → System information)."""
from __future__ import annotations

from typing import Any

from homeassistant.components import system_health
from homeassistant.core import HomeAssistant, callback

from . import _VERSION
from .const import DOMAIN


@callback
def async_register(hass: HomeAssistant, register: system_health.SystemHealthRegistration) -> None:
    register.async_register_info(system_info)


async def system_info(hass: HomeAssistant) -> dict[str, Any]:
    coords = [v for v in hass.data.get(DOMAIN, {}).values() if hasattr(v, "async_snooze")]
    info: dict[str, Any] = {"version": _VERSION}
    if coords:
        model = coords[0].data or {}
        info["rooms"] = model.get("total", 0)
        info["rooms_good"] = model.get("good", 0)
        info["last_update_ok"] = coords[0].last_update_success
    return info
