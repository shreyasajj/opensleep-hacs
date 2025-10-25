
# 💤 OpenSleep (MQTT) — Home Assistant Integration

This **custom HACS integration** connects your OpenSleep device to **Home Assistant** via **MQTT**, allowing you to view presence, bed temperature, water temperature, humidity, and other telemetry directly from the `opensleep/` MQTT topics.  
It also provides Home Assistant **services and UI buttons** to send commands to the `opensleep/actions/*` topics (e.g., calibrate, set away mode, change profile times).

---

## 🌟 Features

✅ Reads all `opensleep/` MQTT topics automatically (wildcard subscription)  
✅ Exposes **sensors** for temperatures, humidity, and configuration values  
✅ Exposes **binary sensors** for presence detection (`any`, `left`, `right`)  
✅ Includes **button entity** to trigger calibration  
✅ Registers **Home Assistant services** to modify configuration values  
✅ Displays **device info** (name, version, label) dynamically from MQTT  
✅ Fully **HACS-compliant** and uses Home Assistant’s config flow UI  

---

## 🧠 Requirements

- Home Assistant `2024.6.0` or newer  
- The **MQTT integration** must already be configured and connected to your broker  
- Your OpenSleep device must publish topics following this structure:
  ```
  opensleep/
    availability
    device/
    state/
    actions/
    result/
  ```

---

## 📦 Installation (via HACS)

1. In **HACS → Integrations → 3-dot menu → Custom repositories**
2. Add your GitHub repo URL (e.g. `https://github.com/yourname/opensleep-hacs`)  
   - Category: **Integration**
3. Click **Download** once it appears in HACS.
4. **Restart Home Assistant**
5. Go to **Settings → Devices & Services → + Add Integration → OpenSleep (MQTT)**  
6. Set the **MQTT topic prefix** (default: `opensleep`) and finish setup.

---

## 🧩 Entities

### **Binary Sensors**
| Entity | Topic | Description |
|--------|--------|-------------|
| `presence_any` | `state/presence/any` | True if anyone detected |
| `presence_left` | `state/presence/left` | True if left side occupied |
| `presence_right` | `state/presence/right` | True if right side occupied |

### **Sensors**
Includes dozens of automatically registered sensors:
- Bed, ambient, MCU, and heatsink temperatures (°C)
- Humidity (%)
- Frozen subsystem values (water temps, targets)
- Config values (timezone, away mode, LED patterns, profile times)
- Result info (last action, status, message)

> Temperatures published as centidegrees (e.g., `2325`) are automatically converted to °C (e.g., `23.25`).

### **Button**
- **Calibrate Presence** → publishes `1` to `opensleep/actions/calibrate`

---

## ⚙️ Services

| Service | Description | Example |
|----------|--------------|----------|
| `opensleep.calibrate` | Starts presence calibration | — |
| `opensleep.set_away_mode` | Sets away mode | `away: true` |
| `opensleep.set_prime` | Sets prime time | `time: "06:30"` |
| `opensleep.set_profile` | Updates sleep/wake/alarm config | `target_side: left` `field: sleep` `value: "22:00"` |
| `opensleep.set_presence_config` | Updates presence thresholds | `field: threshold` `value: 45` |

---

## 🧱 Folder Structure

```
custom_components/opensleep/
├── __init__.py
├── binary_sensor.py
├── button.py
├── config_flow.py
├── const.py
├── manifest.json
├── mqtt_client.py
├── sensor.py
├── services.py
├── services.yaml
├── strings.json
├── translations/en.json
└── README.md
```

---

## 🛠️ Development Notes

- The integration subscribes to `{prefix}/#` (default: `opensleep/#`) and updates entities in real time.
- No polling or external APIs are used — pure local MQTT communication.
- You can extend sensors easily by adding entries in `SENSOR_SPECS` inside `sensor.py`.

---

## 🧾 License

[MIT License](./LICENSE)
