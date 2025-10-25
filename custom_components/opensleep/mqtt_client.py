from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional
import logging

from homeassistant.core import HomeAssistant, callback
from homeassistant.components import mqtt

_LOGGER = logging.getLogger(__name__)

MessageCallback = Callable[[str, str], None]

@dataclass
class OpensleepState:
    available: bool = False
    device_name: Optional[str] = None
    device_version: Optional[str] = None
    device_label: Optional[str] = None
    last_action: Optional[str] = None
    last_status: Optional[str] = None
    last_message: Optional[str] = None
    values: Dict[str, Any] = field(default_factory=dict)

class OpensleepMqtt:
    def __init__(self, hass: HomeAssistant, prefix: str) -> None:
        self.hass = hass
        self.prefix = prefix
        self._unsubs: list[Callable[[], None]] = []
        self.state = OpensleepState()
        self._listeners: list[MessageCallback] = []

    async def async_subscribe(self, topic: str) -> None:
        async def _cb(msg):
            payload = msg.payload
            t = msg.topic
            self.state.values[t] = payload
            for l in list(self._listeners):
                try:
                    l(t, payload)
                except Exception:
                    _LOGGER.exception("Listener error for %s", t)
        unsub = await mqtt.async_subscribe(self.hass, topic, _cb, qos=0)
        self._unsubs.append(unsub)

    async def async_subscribe_many(self, topics: list[str]) -> None:
        for t in topics:
            await self.async_subscribe(t)

    @callback
    def add_listener(self, cb: MessageCallback) -> Callable[[], None]:
        self._listeners.append(cb)
        def _remove():
            if cb in self._listeners:
                self._listeners.remove(cb)
        return _remove

    async def async_publish(self, topic: str, payload: str) -> None:
        await mqtt.async_publish(self.hass, topic, payload, qos=0, retain=False)

    async def async_setup_core_subscriptions(self) -> None:
        p = self.prefix
        await self.async_subscribe(f"{p}/#")

    async def async_unload(self) -> None:
        while self._unsubs:
            self._unsubs.pop()()
