"""Platform for climate integration."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MelzoneBuildingDevice
from .const import DOMAIN, OPERATION_MODE_AUTO, OPERATION_MODE_COOL, OPERATION_MODE_HEAT

SCAN_INTERVAL = timedelta(seconds=10)


HVAC_MODE_LOOKUP = {
    OPERATION_MODE_AUTO: HVACMode.AUTO,
    OPERATION_MODE_HEAT: HVACMode.HEAT,
    OPERATION_MODE_COOL: HVACMode.COOL,
}
HVAC_MODE_REVERSE_LOOKUP = {v: k for k, v in HVAC_MODE_LOOKUP.items()}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Melzone Building device climate based on config_entry."""
    devices = hass.data[DOMAIN][entry.entry_id]
    entities: list[MelzoneBuildingClimate] = [
        MelzoneBuildingClimate(device) for device in devices
    ]
    async_add_entities(
        entities,
        True,
    )


class MelzoneBuildingClimate(ClimateEntity):
    """Base climate device."""

    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_has_entity_name = True
    _attr_name = None
    _enable_turn_on_off_backwards_compatibility = False

    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE

    def __init__(self, device: MelzoneBuildingDevice) -> None:
        """Initialize the climate."""
        self.device = device
        self._attr_unique_id = self.device.unique_id
        self._attr_device_info = self.device.device_info

    async def async_update(self) -> None:
        """Update state from Colibri."""
        await self.device.async_update()

    @property
    def target_temperature_step(self) -> float | None:
        """Return the supported step of target temperature."""
        return 1.0

    @property
    def hvac_mode(self) -> HVACMode | None:
        """Return hvac operation ie. heat, cool mode."""
        mode = HVAC_MODE_LOOKUP.get(self.device.operation_mode)
        if not self.device.power or mode is None:
            return HVACMode.OFF
        return mode

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        if hvac_mode == HVACMode.OFF:
            await self.device.turn_off()
        else:
            operation_mode = HVAC_MODE_REVERSE_LOOKUP.get(hvac_mode)
            if operation_mode is None:
                raise ValueError(f"Invalid hvac_mode [{hvac_mode}]")
            await self.device.set_mode(operation_mode)

    @property
    def hvac_modes(self) -> list[HVACMode]:
        """Return the list of available hvac operation modes."""
        return [HVACMode.OFF, HVACMode.AUTO, HVACMode.HEAT, HVACMode.COOL]

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        return self.device.room_temperature

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature we try to reach."""
        return self.device.target_temperature

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if ATTR_TEMPERATURE in kwargs:
            await self.device.set_temperature(kwargs.get(ATTR_TEMPERATURE))

    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        await self.device.turn_on()

    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        await self.device.turn_off()
