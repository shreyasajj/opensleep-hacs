
from __future__ import annotations
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_PREFIX,
    DEFAULT_PREFIX,
    TOPIC_AVAILABILITY,
    TOPIC_CFG_AWAY_MODE,
    TOPIC_ACT_SET_AWAY_MODE,
)
from .mqtt_client import OpensleepMqtt

_LOGGER = logging.getLogger(__name__)

class AwayModeSwitch(SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = "Away Mode"
    _attr_should_poll = False

    def __init__(self, client: OpensleepMqtt, prefix: str) -> None:
        self._client = client
        self._prefix = prefix
        self._attr_unique_id = f"opensleep_away_mode_{prefix}"
        self._remove = None
        self._attr_available = True
        self._attr_is_on = False  # make visible in HA UI


    @property
    def device_info(self):
        label = self._client.state.device_label or "opensleep"
        return {
            "identifiers": {(DOMAIN, label)},
            "manufacturer": "OpenSleep",
            "name": self._client.state.device_name or "OpenSleep",
            "sw_version": self._client.state.device_version or None,
        }

    async def async_added_to_hass(self) -> None:
        cfg_topic = TOPIC_CFG_AWAY_MODE.format(p=self._prefix)
        avail_topic = TOPIC_AVAILABILITY.format(p=self._prefix)

        @callback
        def _listener(topic: str, payload: str) -> None:
            t = topic
            p = payload.strip().lower()
            if t == cfg_topic:
                if p in ("1", "true", "on", "yes"):
                    self._attr_is_on = True
                elif p in ("0", "false", "off", "no"):
                    self._attr_is_on = False
                else:
                    try:
                        self._attr_is_on = bool(int(p))
                    except Exception:
                        _LOGGER.debug("Unknown away_mode payload on %s: %s", t, payload)
                        return
                self.async_write_ha_state()

            elif t == avail_topic:
                self._attr_available = (p == "online")
                self.async_write_ha_state()

        self._remove = self._client.add_listener(_listener)

    async def async_will_remove_from_hass(self) -> None:
        if self._remove:
            self._remove()
            self._remove = None

    async def async_turn_on(self, **kwargs) -> None:
        await self._client.async_publish(TOPIC_ACT_SET_AWAY_MODE.format(p=self._prefix), "true")
        # Optimistic; device will publish new state on config topic
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        await self._client.async_publish(TOPIC_ACT_SET_AWAY_MODE.format(p=self._prefix), "false")
        self._attr_is_on = False
        self.async_write_ha_state()

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    client: OpensleepMqtt = hass.data[DOMAIN][entry.entry_id]
    prefix = entry.data.get(CONF_PREFIX, DEFAULT_PREFIX)
    async_add_entities([AwayModeSwitch(client, prefix)])
