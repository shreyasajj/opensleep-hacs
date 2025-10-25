from __future__ import annotations
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS, CONF_PREFIX, DEFAULT_PREFIX
from .mqtt_client import OpensleepMqtt

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    prefix = entry.data.get(CONF_PREFIX, DEFAULT_PREFIX)
    client = OpensleepMqtt(hass, prefix)
    await client.async_setup_core_subscriptions()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = client

    # Register services
    from .services import register_services
    register_services(hass, client)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("opensleep entry set up for prefix %s", prefix)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    client: OpensleepMqtt = hass.data[DOMAIN].pop(entry.entry_id)
    await client.async_unload()
    return unload_ok
