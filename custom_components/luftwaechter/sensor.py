"""Sensors: one per room plus a house summary that feeds the panel."""
from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import DOMAIN
from .coordinator import LuftwaechterCoordinator

LEVEL_OPTIONS = ["good", "fair", "poor", "unknown"]


def _device(entry: ConfigEntry) -> DeviceInfo:
    return DeviceInfo(identifiers={(DOMAIN, entry.entry_id)}, name="Luftwächter", manufacturer="Dan Stasiak")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coord: LuftwaechterCoordinator = hass.data[DOMAIN][entry.entry_id]
    known: set[str] = set()

    @callback
    def _add() -> None:
        new = []
        for room in (coord.data or {}).get("rooms", []):
            if room["key"] not in known:
                known.add(room["key"])
                new.append(RoomSensor(coord, entry, room["key"], slugify(room["name"])))
        if new:
            async_add_entities(new)

    async_add_entities([HouseSensor(coord, entry)])
    _add()
    entry.async_on_unload(coord.async_add_listener(_add))


class HouseSensor(CoordinatorEntity[LuftwaechterCoordinator], SensorEntity):
    """Whole-house model; the sidebar panel reads this entity."""

    _attr_has_entity_name = False
    _attr_name = "Luftwächter House"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = LEVEL_OPTIONS
    _unrecorded_attributes = frozenset({"rooms", "summary", "outside", "colors"})

    def __init__(self, coord: LuftwaechterCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coord)
        self._attr_unique_id = f"{entry.entry_id}_house"
        self._attr_device_info = _device(entry)

    @property
    def suggested_object_id(self) -> str:
        return "luftwaechter_house"

    @property
    def native_value(self) -> str:
        return (self.coordinator.data or {}).get("level", "unknown")

    @property
    def extra_state_attributes(self) -> dict:
        d = self.coordinator.data or {}
        return {k: d.get(k) for k in ("rooms", "summary", "outside", "lang", "colors")}


class RoomSensor(CoordinatorEntity[LuftwaechterCoordinator], SensorEntity):
    _attr_has_entity_name = False
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = LEVEL_OPTIONS
    _unrecorded_attributes = frozenset({"devices", "sources", "values"})

    def __init__(self, coord: LuftwaechterCoordinator, entry: ConfigEntry, key: str, room_name: str) -> None:
        super().__init__(coord)
        self._key = key
        self._attr_unique_id = f"{entry.entry_id}_room_{key}"
        self._slug = f"luftwaechter_{room_name}"
        self._attr_device_info = _device(entry)

    @property
    def suggested_object_id(self) -> str:
        return self._slug

    def _room(self) -> dict | None:
        for r in (self.coordinator.data or {}).get("rooms", []):
            if r["key"] == self._key:
                return r
        return None

    @property
    def available(self) -> bool:
        return super().available and self._room() is not None

    @property
    def name(self) -> str:
        r = self._room()
        return f"Luftwächter {r['name']}" if r else self._key

    @property
    def native_value(self) -> str:
        r = self._room()
        return r["level"] if r else "unknown"

    @property
    def extra_state_attributes(self) -> dict:
        r = self._room() or {}
        return {k: r.get(k) for k in ("action", "headline", "detail", "window", "ventMin", "warn", "values", "devices", "sources")}
