# OpenSleep (MQTT) — Custom Integration

This integration reads all relevant `opensleep/` MQTT topics and exposes them as entities in Home Assistant.
It also publishes to `opensleep/actions/*` via services.

## Install (HACS)
1. In HACS → Integrations → 3-dot menu → **Custom repositories** → Add this repo URL as **Integration**.
2. Click **Download**.
3. Restart Home Assistant.
4. Settings → Devices & Services → **+ Add Integration** → **OpenSleep (MQTT)**.
5. Set *MQTT topic prefix* to `opensleep` (or your custom prefix) and submit.

> Requires the built-in MQTT integration to already be configured and connected to your broker.

## Entities

### Binary sensors
- `Presence Any`, `Presence Left`, `Presence Right` — driven by `state/presence/*`.
- Availability is tracked via `availability` (online/offline).

### Sensors
- Sensor subsystem values: mode, hwinfo, piezo_ok, vibration_enabled, bed/ambient/mcu temps, humidity.
- Frozen subsystem values: mode, hwinfo, left/right/heatsink temps, left/right target temps.
- Config echo sensors: timezone, away_mode, prime, LED patterns/band, profile (type, left/right sleep/wake/temperatures/alarm), presence baselines/threshold/debounce.
- Result sensors: last action/status/message from `result/*`.

> Temperatures published as `centidegrees_celcius` are converted to °C (value/100).

### Button
- `Calibrate Presence` — publishes `1` to `actions/calibrate`.

## Services
- `opensleep.calibrate`
- `opensleep.set_away_mode` (boolean `away`)
- `opensleep.set_prime` (text `time`, e.g., `06:30`)
- `opensleep.set_profile` (`target_side`: both|left|right, `field`: sleep|wake|temperatures|alarm, `value`: string)
- `opensleep.set_presence_config` (`field`: baselines|threshold|debounce_count, `value`: string)

## Notes
- Wildcard subscription to `{prefix}/#`; no polling.
- Device info comes from `device/name`, `device/version`, `device/label` when published.
- Extend by adding new `SensorDef`s in `sensor.py`.
