DOMAIN = "opensleep"
PLATFORMS = ["sensor", "binary_sensor", "button"]
CONF_PREFIX = "prefix"
DEFAULT_PREFIX = "opensleep"

TOPIC_AVAILABILITY = "{p}/availability"
# Device info
TOPIC_DEVICE_NAME = "{p}/device/name"
TOPIC_DEVICE_VERSION = "{p}/device/version"
TOPIC_DEVICE_LABEL = "{p}/device/label"

# State: presence
TOPIC_PRESENCE_ANY = "{p}/state/presence/any"
TOPIC_PRESENCE_LEFT = "{p}/state/presence/left"
TOPIC_PRESENCE_RIGHT = "{p}/state/presence/right"

# State: sensor subsystem
TOPIC_SENSOR_MODE = "{p}/state/sensor/mode"
TOPIC_SENSOR_HWINFO = "{p}/state/sensor/hwinfo"
TOPIC_SENSOR_PIEZO = "{p}/state/sensor/piezo_ok"
TOPIC_SENSOR_VIBRATION = "{p}/state/sensor/vibration_enabled"
TOPIC_SENSOR_BED_TEMP = "{p}/state/sensor/bed_temp"
TOPIC_SENSOR_AMBIENT = "{p}/state/sensor/ambient_temp"
TOPIC_SENSOR_HUMIDITY = "{p}/state/sensor/humidity"
TOPIC_SENSOR_MCU_TEMP = "{p}/state/sensor/mcu_temp"

# State: frozen subsystem
TOPIC_FROZEN_MODE = "{p}/state/frozen/mode"
TOPIC_FROZEN_HWINFO = "{p}/state/frozen/hwinfo"
TOPIC_FROZEN_LEFT_TEMP = "{p}/state/frozen/left_temp"
TOPIC_FROZEN_RIGHT_TEMP = "{p}/state/frozen/right_temp"
TOPIC_FROZEN_HEATSINK = "{p}/state/frozen/heatsink_temp"
TOPIC_FROZEN_LEFT_TARGET = "{p}/state/frozen/left_target_temp"
TOPIC_FROZEN_RIGHT_TARGET = "{p}/state/frozen/right_target_temp"

# Config values (published from config.ron)
TOPIC_CFG_TIMEZONE = "{p}/state/config/timezone"
TOPIC_CFG_AWAY_MODE = "{p}/state/config/away_mode"
TOPIC_CFG_PRIME = "{p}/state/config/prime"
TOPIC_CFG_LED_IDLE = "{p}/state/config/led/idle"
TOPIC_CFG_LED_ACTIVE = "{p}/state/config/led/active"
TOPIC_CFG_LED_BAND = "{p}/state/config/led/band"
TOPIC_CFG_PROFILE_TYPE = "{p}/state/config/profile/type"
TOPIC_CFG_PROFILE_LEFT_SLEEP = "{p}/state/config/profile/left/sleep"
TOPIC_CFG_PROFILE_LEFT_WAKE = "{p}/state/config/profile/left/wake"
TOPIC_CFG_PROFILE_LEFT_TEMPS = "{p}/state/config/profile/left/temperatures"
TOPIC_CFG_PROFILE_LEFT_ALARM = "{p}/state/config/profile/left/alarm"
TOPIC_CFG_PROFILE_RIGHT_SLEEP = "{p}/state/config/profile/right/sleep"
TOPIC_CFG_PROFILE_RIGHT_WAKE = "{p}/state/config/profile/right/wake"
TOPIC_CFG_PROFILE_RIGHT_TEMPS = "{p}/state/config/profile/right/temperatures"
TOPIC_CFG_PROFILE_RIGHT_ALARM = "{p}/state/config/profile/right/alarm"
TOPIC_CFG_PRES_BASELINES = "{p}/state/config/presence/baselines"
TOPIC_CFG_PRES_THRESHOLD = "{p}/state/config/presence/threshold"
TOPIC_CFG_PRES_DEBOUNCE = "{p}/state/config/presence/debounce_count"

# Result
TOPIC_RESULT_ACTION = "{p}/result/action"
TOPIC_RESULT_STATUS = "{p}/result/status"
TOPIC_RESULT_MESSAGE = "{p}/result/message"

# Actions (publish-only)
TOPIC_ACT_CALIBRATE = "{p}/actions/calibrate"
TOPIC_ACT_SET_AWAY_MODE = "{p}/actions/set_away_mode"
TOPIC_ACT_SET_PRIME = "{p}/actions/set_prime"
TOPIC_ACT_SET_PROFILE = "{p}/actions/set_profile"
TOPIC_ACT_SET_PRESENCE = "{p}/actions/set_presence_config"

ATTR_DEVICE_NAME = "device_name"
ATTR_DEVICE_VERSION = "device_version"
ATTR_DEVICE_LABEL = "device_label"
