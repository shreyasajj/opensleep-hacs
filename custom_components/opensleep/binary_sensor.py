from __future__ import annotations
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN, CONF_PREFIX, DEFAULT_PREFIX,
    TOPIC_PRESENCE_ANY, TOPIC_PRESENCE_LEFT, TOPIC_PRESENCE_RIGHT, TOPIC_AVAILABILITY
)
from .mqtt_client import OpensleepMqtt

_LOGGER = logging.getLogger(__name__)

class PresenceBinary(BinarySensorEntity):
    _attr_device_class = "presence"
    _attr_has_entity_name = True

    def __init__(self, client: OpensleepMqtt, name: str, topic: str) -> None:
        self._client = client
        self._topic = topic
        self._attr_name = name
        self._attr_unique_id = f"{name.lower().replace(' ', '_')}_{topic.replace('/', '_')}"
        self._remove = None
        self._attr_available = True

    @property
    def is_on(self) -> bool | None:
        return self._attr_is_on

    async def async_added_to_hass(self) -> None:
        @callback
        def _listener(topic: str, payload: str) -> None:
            if topic == self._topic:
                val = payload.strip().lower()
                if val in ("1", "true", "on", "yes"): self._attr_is_on = True
                elif val in ("0", "false", "off", "no"): self._attr_is_on = False
                else:
                    try:
                        self._attr_is_on = bool(int(val))
                    except Exception:
                        _LOGGER.debug("Unknown presence payload on %s: %s", topic, payload)
                        return
                self.async_write_ha_state()

            if topic == TOPIC_AVAILABILITY.format(p=self._client.prefix):
                self._attr_available = payload.strip().lower() == "online"
                self.async_write_ha_state()

        self._remove = self._client.add_listener(_listener)

    async def async_will_remove_from_hass(self) -> None:
        if self._remove:
            self._remove()
            self._remove = None

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    client: OpensleepMqtt = hass.data[DOMAIN][entry.entry_id]
    prefix = entry.data.get(CONF_PREFIX, DEFAULT_PREFIX)
    entities = [
        PresenceBinary(client, "Presence Any", TOPIC_PRESENCE_ANY.format(p=prefix)),
        PresenceBinary(client, "Presence Left", TOPIC_PRESENCE_LEFT.format(p=prefix)),
        PresenceBinary(client, "Presence Right", TOPIC_PRESENCE_RIGHT.format(p=prefix)),
    ]
    async_add_entities(entities)
