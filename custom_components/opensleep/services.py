from __future__ import annotations

from homeassistant.core import HomeAssistant, ServiceCall

from .const import (
    TOPIC_ACT_SET_AWAY_MODE,
    TOPIC_ACT_SET_PRIME,
    TOPIC_ACT_SET_PROFILE,
    TOPIC_ACT_SET_PRESENCE,
)
from .mqtt_client import OpensleepMqtt

def register_services(hass: HomeAssistant, client: OpensleepMqtt) -> None:
    async def _calibrate(call: ServiceCall):
        await client.async_publish(f"{client.prefix}/actions/calibrate", "1")

    async def _set_away(call: ServiceCall):
        val = call.data.get("away")
        payload = "true" if bool(val) else "false"
        await client.async_publish(TOPIC_ACT_SET_AWAY_MODE.format(p=client.prefix), payload)

    async def _set_prime(call: ServiceCall):
        timestr = str(call.data.get("time"))
        await client.async_publish(TOPIC_ACT_SET_PRIME.format(p=client.prefix), timestr)

    async def _set_profile(call: ServiceCall):
        target = call.data.get("target_side")
        field = call.data.get("field")
        value = str(call.data.get("value"))
        payload = f"{target}.{field}={value}"
        await client.async_publish(TOPIC_ACT_SET_PROFILE.format(p=client.prefix), payload)

    async def _set_presence(call: ServiceCall):
        field = call.data.get("field")
        value = str(call.data.get("value"))
        payload = f"{field}={value}"
        await client.async_publish(TOPIC_ACT_SET_PRESENCE.format(p=client.prefix), payload)

    hass.services.async_register("opensleep", "calibrate", _calibrate)
    hass.services.async_register("opensleep", "set_away_mode", _set_away)
    hass.services.async_register("opensleep", "set_prime", _set_prime)
    hass.services.async_register("opensleep", "set_profile", _set_profile)
    hass.services.async_register("opensleep", "set_presence_config", _set_presence)
