from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_PREFIX, DEFAULT_PREFIX, TOPIC_AVAILABILITY
from .mqtt_client import OpensleepMqtt

class CalibrateButton(ButtonEntity):
    _attr_name = "Calibrate Presence"
    _attr_has_entity_name = True
    _attr_entity_category = "config"  # shows under "Controls" on device page
    _remove = None

    def __init__(self, client: OpensleepMqtt):
        self._client = client
        self._attr_unique_id = f"opensleep_calibrate_{client.prefix}"

    @property
    def device_info(self):
        # Match the same device grouping as sensors/binary_sensors
        label = self._client.state.device_label or "opensleep"
        return {
            "identifiers": {(DOMAIN, label)},
            "manufacturer": "OpenSleep",
            "name": self._client.state.device_name or "OpenSleep",
            "sw_version": self._client.state.device_version or None,
        }

    async def async_added_to_hass(self) -> None:
        # Optional: track availability so the button grays out when device is offline
        def _listener(topic: str, payload: str) -> None:
            if topic == TOPIC_AVAILABILITY.format(p=self._client.prefix):
                self._attr_available = payload.strip().lower() == "online"
                self.async_write_ha_state()

        self._remove = self._client.add_listener(_listener)

    async def async_will_remove_from_hass(self) -> None:
        if self._remove:
            self._remove()
            self._remove = None

    async def async_press(self) -> None:
        await self._client.async_publish(f"{self._client.prefix}/actions/calibrate", "1")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    client: OpensleepMqtt = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CalibrateButton(client)])
