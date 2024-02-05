"""Support for Melzone Building device sensors."""

from __future__ import annotations

from collections.abc import Callable
import dataclasses
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MelzoneBuildingDevice
from .const import DOMAIN


@dataclasses.dataclass(frozen=True)
class MelzoneBuildingRequiredKeysMixin:
    """Mixin for required keys."""

    value_fn: Callable[[Any], float]


@dataclasses.dataclass(frozen=True)
class MelzoneBuildingSensorEntityDescription(
    SensorEntityDescription, MelzoneBuildingRequiredKeysMixin
):
    """Describes Melzone Building sensor entity."""


MELZONE_BUILDING_SENSORS: tuple[MelzoneBuildingSensorEntityDescription, ...] = (
    MelzoneBuildingSensorEntityDescription(
        key="room_temperature",
        translation_key="room_temperature",
        name="Room temperature",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda device: device.room_temperature,
    ),
    MelzoneBuildingSensorEntityDescription(
        key="target_temperature",
        translation_key="target_temperature",
        name="Target temperature",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda device: device.target_temperature,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Melzone Building device sensors based on config_entry."""
    devices = hass.data[DOMAIN].get(entry.entry_id)

    entities: list[MelzoneBuildingDeviceSensor] = [
        MelzoneBuildingDeviceSensor(device, description)
        for description in MELZONE_BUILDING_SENSORS
        for device in devices
    ]
    async_add_entities(entities, True)


class MelzoneBuildingDeviceSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        device: MelzoneBuildingDevice,
        description: MelzoneBuildingSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self.device = device
        self.entity_description = description

        self._attr_unique_id = f"{device.unique_id}-{description.key}"
        self._attr_device_info = device.device_info

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.device)

    async def async_update(self) -> None:
        """Retrieve latest state."""
        await self.device.async_update()
