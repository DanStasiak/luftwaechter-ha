"""Binary sensor: on while at least one room needs attention (for automations)."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import LuftwaechterCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coord: LuftwaechterCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AttentionSensor(coord, entry), SensorProblemSensor(coord, entry)])
    known: set[str] = set()

    @callback
    def _add() -> None:
        new = []
        for room in (coord.data or {}).get("rooms", []):
            if room["key"] not in known:
                known.add(room["key"])
                new.append(RoomVentilateSensor(coord, entry, room["key"]))
        if new:
            async_add_entities(new)

    _add()
    entry.async_on_unload(coord.async_add_listener(_add))


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


class SensorProblemSensor(CoordinatorEntity[LuftwaechterCoordinator], BinarySensorEntity):
    """On while a room's air sensor has stopped reporting or was ignored as stale."""

    _attr_has_entity_name = False
    _attr_name = "Luftwächter Sensor problem"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coord: LuftwaechterCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coord)
        self._attr_unique_id = f"{entry.entry_id}_sensor_problem"
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, entry.entry_id)}, name="Luftwächter", manufacturer="Dan Stasiak")

    @property
    def is_on(self) -> bool:
        return bool((self.coordinator.data or {}).get("silent_rooms"))

    @property
    def extra_state_attributes(self) -> dict:
        rooms = (self.coordinator.data or {}).get("silent_rooms", [])
        return {"count": len(rooms), "rooms": rooms}


class RoomVentilateSensor(CoordinatorEntity[LuftwaechterCoordinator], BinarySensorEntity):
    """On while Luftwächter advises opening a window in this room (one per room, for automations)."""

    _attr_has_entity_name = False

    def __init__(self, coord: LuftwaechterCoordinator, entry: ConfigEntry, key: str) -> None:
        super().__init__(coord)
        self._key = key
        self._attr_unique_id = f"{entry.entry_id}_ventilate_{key}"
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, entry.entry_id)}, name="Luftwächter", manufacturer="Dan Stasiak")

    def _room(self) -> dict | None:
        return next((r for r in (self.coordinator.data or {}).get("rooms", []) if r["key"] == self._key), None)

    @property
    def name(self) -> str:
        room = self._room()
        return f"Luftwächter {room['name'] if room else self._key} ventilate"

    @property
    def available(self) -> bool:
        return super().available and self._room() is not None

    @property
    def is_on(self) -> bool:
        room = self._room()
        return bool(room and room["action"] == "open")

    @property
    def extra_state_attributes(self) -> dict:
        room = self._room() or {}
        return {"room": room.get("name", ""), "headline": room.get("headline", ""), "level": room.get("level", "unknown")}
