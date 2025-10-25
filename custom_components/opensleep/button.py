from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .mqtt_client import OpensleepMqtt

class CalibrateButton(ButtonEntity):
    _attr_name = "Calibrate Presence"
    _attr_has_entity_name = True

    def __init__(self, client: OpensleepMqtt):
        self._client = client
        self._attr_unique_id = f"opensleep_calibrate_{client.prefix}"

    async def async_press(self) -> None:
        await self._client.async_publish(f"{self._client.prefix}/actions/calibrate", "1")

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    client: OpensleepMqtt = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CalibrateButton(client)])
