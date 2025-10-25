from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature, PERCENTAGE
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN, CONF_PREFIX, DEFAULT_PREFIX,
    TOPIC_DEVICE_NAME, TOPIC_DEVICE_VERSION, TOPIC_DEVICE_LABEL,
    TOPIC_SENSOR_MODE, TOPIC_SENSOR_HWINFO, TOPIC_SENSOR_BED_TEMP, TOPIC_SENSOR_AMBIENT,
    TOPIC_SENSOR_HUMIDITY, TOPIC_SENSOR_MCU_TEMP,
    TOPIC_FROZEN_MODE, TOPIC_FROZEN_HWINFO, TOPIC_FROZEN_LEFT_TEMP, TOPIC_FROZEN_RIGHT_TEMP,
    TOPIC_FROZEN_HEATSINK, TOPIC_FROZEN_LEFT_TARGET, TOPIC_FROZEN_RIGHT_TARGET,
    TOPIC_CFG_TIMEZONE, TOPIC_CFG_AWAY_MODE, TOPIC_CFG_PRIME, TOPIC_CFG_LED_IDLE,
    TOPIC_CFG_LED_ACTIVE, TOPIC_CFG_LED_BAND, TOPIC_CFG_PROFILE_TYPE,
    TOPIC_CFG_PROFILE_LEFT_SLEEP, TOPIC_CFG_PROFILE_LEFT_WAKE, TOPIC_CFG_PROFILE_LEFT_TEMPS,
    TOPIC_CFG_PROFILE_LEFT_ALARM, TOPIC_CFG_PROFILE_RIGHT_SLEEP, TOPIC_CFG_PROFILE_RIGHT_WAKE,
    TOPIC_CFG_PROFILE_RIGHT_TEMPS, TOPIC_CFG_PROFILE_RIGHT_ALARM,
    TOPIC_CFG_PRES_BASELINES, TOPIC_CFG_PRES_THRESHOLD, TOPIC_CFG_PRES_DEBOUNCE,
    TOPIC_RESULT_ACTION, TOPIC_RESULT_STATUS, TOPIC_RESULT_MESSAGE
)
from .mqtt_client import OpensleepMqtt

_LOGGER = logging.getLogger(__name__)
CENTI = 100.0

@dataclass
class SensorDef:
    name: str
    topic_tpl: str
    unit: Optional[str] = None
    device_class: Optional[str] = None
    state_class: Optional[str] = None
    value_fn: Optional[Callable[[str], float | str]] = None
    def topic(self, prefix: str) -> str:
        return self.topic_tpl.format(p=prefix)

def as_celsius_from_centi(payload: str) -> float:
    return round(int(payload) / CENTI, 2)

SENSOR_SPECS: list[SensorDef] = [
    SensorDef("Sensor Mode", TOPIC_SENSOR_MODE),
    SensorDef("Sensor HW Info", TOPIC_SENSOR_HWINFO),
    SensorDef("Bed Temp (°C)", TOPIC_SENSOR_BED_TEMP, UnitOfTemperature.CELSIUS, value_fn=as_celsius_from_centi),
    SensorDef("Ambient Temp (°C)", TOPIC_SENSOR_AMBIENT, UnitOfTemperature.CELSIUS, value_fn=as_celsius_from_centi),
    SensorDef("MCU Temp (°C)", TOPIC_SENSOR_MCU_TEMP, UnitOfTemperature.CELSIUS, value_fn=as_celsius_from_centi),
    SensorDef("Humidity (%)", TOPIC_SENSOR_HUMIDITY, PERCENTAGE, value_fn=lambda s: int(s)),
    SensorDef("Frozen Mode", TOPIC_FROZEN_MODE),
    SensorDef("Frozen HW Info", TOPIC_FROZEN_HWINFO),
    SensorDef("Left Water Temp (°C)", TOPIC_FROZEN_LEFT_TEMP, UnitOfTemperature.CELSIUS, value_fn=as_celsius_from_centi),
    SensorDef("Right Water Temp (°C)", TOPIC_FROZEN_RIGHT_TEMP, UnitOfTemperature.CELSIUS, value_fn=as_celsius_from_centi),
    SensorDef("Heatsink Temp (°C)", TOPIC_FROZEN_HEATSINK, UnitOfTemperature.CELSIUS, value_fn=as_celsius_from_centi),
    SensorDef("Left Target (°C/disabled)", TOPIC_FROZEN_LEFT_TARGET, UnitOfTemperature.CELSIUS, value_fn=as_celsius_from_centi),
    SensorDef("Right Target (°C/disabled)", TOPIC_FROZEN_RIGHT_TARGET, UnitOfTemperature.CELSIUS, value_fn=as_celsius_from_centi),
    SensorDef("Timezone", TOPIC_CFG_TIMEZONE),
    SensorDef("Away Mode (cfg)", TOPIC_CFG_AWAY_MODE),
    SensorDef("Prime Time", TOPIC_CFG_PRIME),
    SensorDef("LED Idle", TOPIC_CFG_LED_IDLE),
    SensorDef("LED Active", TOPIC_CFG_LED_ACTIVE),
    SensorDef("LED Band", TOPIC_CFG_LED_BAND),
    SensorDef("Profile Type", TOPIC_CFG_PROFILE_TYPE),
    SensorDef("Left Sleep", TOPIC_CFG_PROFILE_LEFT_SLEEP),
    SensorDef("Left Wake", TOPIC_CFG_PROFILE_LEFT_WAKE),
    SensorDef("Left Temps", TOPIC_CFG_PROFILE_LEFT_TEMPS),
    SensorDef("Left Alarm", TOPIC_CFG_PROFILE_LEFT_ALARM),
    SensorDef("Right Sleep", TOPIC_CFG_PROFILE_RIGHT_SLEEP),
    SensorDef("Right Wake", TOPIC_CFG_PROFILE_RIGHT_WAKE),
    SensorDef("Right Temps", TOPIC_CFG_PROFILE_RIGHT_TEMPS),
    SensorDef("Right Alarm", TOPIC_CFG_PROFILE_RIGHT_ALARM),
    SensorDef("Presence Baselines", TOPIC_CFG_PRES_BASELINES),
    SensorDef("Presence Threshold", TOPIC_CFG_PRES_THRESHOLD),
    SensorDef("Presence Debounce", TOPIC_CFG_PRES_DEBOUNCE),
    SensorDef("Last Action", TOPIC_RESULT_ACTION),
    SensorDef("Last Status", TOPIC_RESULT_STATUS),
    SensorDef("Last Message", TOPIC_RESULT_MESSAGE),
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    client: OpensleepMqtt = hass.data[DOMAIN][entry.entry_id]
    prefix = entry.data.get(CONF_PREFIX, DEFAULT_PREFIX)

    entities: list[OpensleepSensor] = []

    for spec in SENSOR_SPECS:
        entities.append(OpensleepSensor(client, spec, prefix))

    entities.append(OpensleepSensor(client, SensorDef("Device Name", TOPIC_DEVICE_NAME), prefix))
    entities.append(OpensleepSensor(client, SensorDef("Device Version", TOPIC_DEVICE_VERSION), prefix))
    entities.append(OpensleepSensor(client, SensorDef("Device Label", TOPIC_DEVICE_LABEL), prefix))

    async_add_entities(entities)

class OpensleepSensor(SensorEntity):
    _attr_has_entity_name = True
    def __init__(self, client: OpensleepMqtt, spec: SensorDef, prefix: str) -> None:
        self._client = client
        self._spec = spec
        self._topic = spec.topic(prefix)
        self._attr_unique_id = f"opensleep_{self._topic.replace('/', '_')}"
        self._remove = None
        self._attr_native_unit_of_measurement = spec.unit

    @property
    def name(self) -> str | None:
        return self._spec.name

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
        @callback
        def _handle(topic: str, payload: str) -> None:
            if topic == self._topic:
                val = payload
                if self._spec.value_fn:
                    try:
                        val = self._spec.value_fn(payload)
                    except Exception:
                        logging.getLogger(__name__).exception("Bad payload on %s: %s", topic, payload)
                        return
                self._attr_native_value = val
                self.async_write_ha_state()

            p = self._client.prefix
            if topic == TOPIC_DEVICE_NAME.format(p=p):
                self._client.state.device_name = payload
            elif topic == TOPIC_DEVICE_VERSION.format(p=p):
                self._client.state.device_version = payload
            elif topic == TOPIC_DEVICE_LABEL.format(p=p):
                self._client.state.device_label = payload

        self._remove = self._client.add_listener(_handle)

    async def async_will_remove_from_hass(self) -> None:
        if self._remove:
            self._remove()
            self._remove = None
