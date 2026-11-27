"""Config flow for Luftwächter."""
from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers import selector

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
)

SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_WEATHER): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="weather")
        )
    }
)


class LuftwaechterConfigFlow(ConfigFlow, domain=DOMAIN):
    """Single-step setup: optional weather entity."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if user_input is not None:
            return self.async_create_entry(title="Luftwächter", data=user_input)
        return self.async_show_form(step_id="user", data_schema=SCHEMA)

    @staticmethod
    @callback
    def async_get_options_flow(entry: ConfigEntry) -> OptionsFlow:
        return LuftwaechterOptionsFlow()


def _num(lo: float, hi: float, unit: str) -> selector.NumberSelector:
    return selector.NumberSelector(
        selector.NumberSelectorConfig(min=lo, max=hi, step=1, mode=selector.NumberSelectorMode.BOX, unit_of_measurement=unit)
    )


class LuftwaechterOptionsFlow(OptionsFlow):
    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}
        if user_input is not None:
            if user_input[CONF_CO2_GOOD] >= user_input[CONF_CO2_FAIR] or user_input[CONF_PM_GOOD] >= user_input[CONF_PM_FAIR]:
                errors["base"] = "limits_order"
            else:
                return self.async_create_entry(data=user_input)
        o, d = self.config_entry.options, self.config_entry.data
        cur = (user_input or {}).get(CONF_WEATHER, o.get(CONF_WEATHER, d.get(CONF_WEATHER)))
        schema = vol.Schema(
            {
                vol.Optional(CONF_WEATHER, description={"suggested_value": cur}): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="weather")
                ),
                vol.Optional(CONF_RAIN, description={"suggested_value": o.get(CONF_RAIN)}): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="binary_sensor")
                ),
                vol.Optional(CONF_OUTSIDE_TEMP, description={"suggested_value": o.get(CONF_OUTSIDE_TEMP)}): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", device_class="temperature")
                ),
                vol.Required(CONF_REM_FIRST, default=o.get(CONF_REM_FIRST, 10)): _num(1, 240, "min"),
                vol.Required(CONF_REM_REPEAT, default=o.get(CONF_REM_REPEAT, 5)): _num(1, 240, "min"),
                vol.Required(CONF_REM_BELOW, default=o.get(CONF_REM_BELOW, 10)): _num(-30, 40, "°C"),
                vol.Required(CONF_REM_FROM, default=o.get(CONF_REM_FROM, 8)): _num(0, 23, "h"),
                vol.Required(CONF_REM_TO, default=o.get(CONF_REM_TO, 22)): _num(0, 23, "h"),
                vol.Optional(CONF_MUTE, description={"suggested_value": o.get(CONF_MUTE, [])}): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain=["binary_sensor", "input_boolean", "switch"], multiple=True)
                ),
                vol.Optional(CONF_IGNORE, description={"suggested_value": o.get(CONF_IGNORE, [])}): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="binary_sensor", multiple=True)
                ),
                vol.Optional(CONF_EXCLUDE, description={"suggested_value": o.get(CONF_EXCLUDE, [])}): selector.AreaSelector(
                    selector.AreaSelectorConfig(multiple=True)
                ),
                vol.Required(CONF_CO2_GOOD, default=o.get(CONF_CO2_GOOD, 1000)): _num(400, 5000, "ppm"),
                vol.Required(CONF_CO2_FAIR, default=o.get(CONF_CO2_FAIR, 1500)): _num(400, 5000, "ppm"),
                vol.Required(CONF_PM_GOOD, default=o.get(CONF_PM_GOOD, 20)): _num(1, 500, "µg/m³"),
                vol.Required(CONF_PM_FAIR, default=o.get(CONF_PM_FAIR, 50)): _num(1, 500, "µg/m³"),
                vol.Required(CONF_MOLD_RH, default=o.get(CONF_MOLD_RH, 70)): _num(50, 90, "%"),
                vol.Required(CONF_STALE, default=o.get(CONF_STALE, DEFAULT_STALE)): _num(2, 120, "min"),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)
