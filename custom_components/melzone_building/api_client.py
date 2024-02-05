import asyncio
from http import HTTPStatus

import aiohttp
import async_timeout


class APIClient:

    def __init__(
        self, colibri_url: str, zone_id: int, session: aiohttp.ClientSession
    ) -> None:
        """Initialize API Client."""
        self._colibri_url = colibri_url
        self._zone_id = zone_id
        self._session = session

    async def get_device(self, timeout=10):
        """Read device data

        This method is a coroutine.
        """
        try:
            with async_timeout.timeout(timeout):
                request = await self._session.request(
                    "get",
                    f"{self._colibri_url}/Temps_Reel/Zone/{self._zone_id}/Thermostat.json",
                    timeout=None,
                )

                if request.status != HTTPStatus.OK:
                    raise ApiError(
                        f"Error calling API, got HTTP status {request.status}"
                    )

                resp = await request.json(content_type=None)
                return resp

        except asyncio.TimeoutError:
            raise ApiError("Timeout on API request")

    async def set_device(self, data, timeout=10):
        """Set device data

        This method is a coroutine.
        """
        try:
            with async_timeout.timeout(timeout):
                response = await self._session.post(
                    f"{self._colibri_url}/Temps_Reel/Zone/{self._zone_id}/Thermostat.json",
                    data=data,
                )

                if response.status != HTTPStatus.OK:
                    raise ApiError(
                        f"Error calling API, got HTTP status {response.status}"
                    )

                resp = await response.json(content_type=None)
                return resp

        except asyncio.TimeoutError:
            raise ApiError("Timeout on API request")


class ApiError(Exception):
    """Represents an API error."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        super().__init__(message)
