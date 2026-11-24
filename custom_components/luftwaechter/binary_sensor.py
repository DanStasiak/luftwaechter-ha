"""Binary sensor: on while at least one room needs attention (for automations)."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import LuftwaechterCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_add_entities([AttentionSensor(hass.data[DOMAIN][entry.entry_id], entry)])


class AttentionSensor(CoordinatorEntity[LuftwaechterCoordinator], BinarySensorEntity):
    """On when a room is poor or advises opening / waiting for a window."""

    _attr_has_entity_name = False
    _attr_name = "Luftwächter Attention"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _unrecorded_attributes = frozenset({"rooms"})

    def __init__(self, coord: LuftwaechterCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coord)
        self._attr_unique_id = f"{entry.entry_id}_attention"
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, entry.entry_id)}, name="Luftwächter", manufacturer="Dan Stasiak")

    @property
    def is_on(self) -> bool:
        return bool((self.coordinator.data or {}).get("attention", 0))

    @property
    def extra_state_attributes(self) -> dict:
        d = self.coordinator.data or {}
        return {"count": d.get("attention", 0), "rooms": d.get("attention_rooms", []), "worst_room": d.get("worst_room", "")}
