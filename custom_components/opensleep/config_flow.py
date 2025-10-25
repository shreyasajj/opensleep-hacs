from __future__ import annotations
from typing import Any
import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN, CONF_PREFIX, DEFAULT_PREFIX

DATA_SCHEMA = vol.Schema({vol.Optional(CONF_PREFIX, default=DEFAULT_PREFIX): str})

class OpensleepFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            for entry in self._async_current_entries():
                return self.async_abort(reason="single_instance_allowed")
            return self.async_create_entry(title="OpenSleep", data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)
