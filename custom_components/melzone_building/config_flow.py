import logging

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

from .const import CONF_COLIBRI_URL, CONF_NUMBER_OF_ZONES, DOMAIN

_LOGGER = logging.getLogger(__name__)


class FlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        user_form = vol.Schema(
            {
                vol.Required(
                    CONF_COLIBRI_URL,
                ): str,
                vol.Required(
                    CONF_NUMBER_OF_ZONES,
                    default=3,
                ): int,
            }
        )

        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=user_form)

        # Validate input
        await self.async_set_unique_id(f"{DOMAIN}_{user_input[CONF_COLIBRI_URL]}")
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"{DOMAIN}_{user_input[CONF_COLIBRI_URL]}", data=user_input
        )
