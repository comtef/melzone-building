from datetime import timedelta
import json
import logging

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo

from .api_client import APIClient
from .const import CONF_COLIBRI_URL, CONF_NUMBER_OF_ZONES, DOMAIN

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)

PLATFORMS = [Platform.CLIMATE, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Melzone Building component."""
    conf = entry.data

    devices = [
        MelzoneBuildingDevice(
            conf[CONF_COLIBRI_URL], zone_id, async_get_clientsession(hass)
        )
        for zone_id in range(conf[CONF_NUMBER_OF_ZONES])
    ]

    hass.data.setdefault(DOMAIN, {}).update({entry.entry_id: devices})
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )
    hass.data[DOMAIN].pop(config_entry.entry_id)
    if not hass.data[DOMAIN]:
        hass.data.pop(DOMAIN)
    return unload_ok


class MelzoneBuildingDevice:
    """Melzone Building Device instance."""

    def __init__(
        self, colibri_url: str, zone_id: int, session: aiohttp.ClientSession
    ) -> None:
        """Construct a device wrapper."""
        self._api = APIClient(colibri_url, zone_id, session)
        self._unique_id = f"{colibri_url}-{zone_id}"
        self._zone_id = zone_id
        self._available = True
        self._name = f"Zone {zone_id}"

    async def async_update(self, **kwargs):
        """Pull the latest data from Colibri."""
        resp = await self._api.get_device()
        self.operation_mode = resp["Mode"]
        self.power = resp["Power"] == 1
        self.room_temperature = resp["Temperature"]
        self.target_temperature = resp["Consigne"]
        self._available = True

    def get_properties(self) -> dict:
        return {
            "Mode": self.operation_mode,
            "Temperature": self.room_temperature,
            "Consigne": self.target_temperature,
            "Power": 1 if self.power else 0,
            "Fan": 0,
            "Window": 0,
            "Occupancy": 0,
        }

    def format_device_data(self, data) -> str:
        # Colibri API won't accept any whitespace in data
        return json.dumps(data, indent=None).replace(" ", "")

    async def turn_on(self):
        """Write state changes to Colibri."""
        properties = self.get_properties()
        properties["Power"] = 1
        await self._api.set_device(self.format_device_data(properties))

    async def turn_off(self):
        """Write state changes to Colibri."""
        properties = self.get_properties()
        properties["Power"] = 0
        await self._api.set_device(self.format_device_data(properties))

    async def set_mode(self, operation_mode):
        """Write state changes to Colibri."""
        properties = self.get_properties()
        properties["Mode"] = operation_mode
        properties["Power"] = 1
        await self._api.set_device(self.format_device_data(properties))

    async def set_temperature(self, temperature):
        """Write state changes to Colibri."""
        properties = self.get_properties()
        properties["Consigne"] = temperature
        await self._api.set_device(self.format_device_data(properties))

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def unique_id(self) -> bool:
        """Unique identifier."""
        return self._unique_id

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return DeviceInfo(
            identifiers={(DOMAIN, f"Zone-{self._zone_id}")},
            manufacturer="Mitsubishi Electric",
            model="Melzone Building",
            name=self._name,
        )
