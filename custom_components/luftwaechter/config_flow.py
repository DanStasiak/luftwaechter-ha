"""Config flow for Luftwächter."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import CONF_WEATHER, DOMAIN

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


class LuftwaechterOptionsFlow(OptionsFlow):
    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            return self.async_create_entry(data=user_input)
        cur = self.config_entry.options.get(CONF_WEATHER, self.config_entry.data.get(CONF_WEATHER))
        schema = vol.Schema(
            {
                vol.Optional(CONF_WEATHER, description={"suggested_value": cur}): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="weather")
                )
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
