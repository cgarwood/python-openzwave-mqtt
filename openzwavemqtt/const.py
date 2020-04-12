"""All constants and common types."""
import logging
from enum import Enum, IntEnum

LOGGER = logging.getLogger("openzwavemqtt")

# OZW Events
EVENT_PLACEHOLDER = "missing"
EVENT_COMMAND_CLASS_ADDED = "command_class_added"
EVENT_COMMAND_CLASS_CHANGED = "command_class_changed"
EVENT_COMMAND_CLASS_REMOVED = "command_class_removed"
EVENT_INSTANCE_ADDED = "instance_added"
EVENT_INSTANCE_CHANGED = "instance_changed"
EVENT_INSTANCE_REMOVED = "instance_removed"
EVENT_INSTANCE_EVENT = "instance_event"
EVENT_INSTANCE_STATISTICS_CHANGED = "instance_statistics_changed"
EVENT_INSTANCE_STATUS_CHANGED = "instance_status_changed"
EVENT_NODE_ADDED = "node_added"
EVENT_NODE_CHANGED = "node_changed"
EVENT_NODE_REMOVED = "node_removed"
EVENT_NODE_INSTANCE_ADDED = "node_instance_added"
EVENT_NODE_INSTANCE_CHANGED = "node_instance_changed"
EVENT_NODE_INSTANCE_REMOVED = "node_instance_removed"
EVENT_NODE_ASSOCIATION_ADDED = "node_association_added"
EVENT_NODE_ASSOCIATION_CHANGED = "node_association_changed"
EVENT_NODE_ASSOCIATION_REMOVED = "node_association_removed"
EVENT_NODE_STATISTICS_CHANGED = "node_statistics_changed"
EVENT_VALUE_ADDED = "value_added"
EVENT_VALUE_CHANGED = "value_changed"
EVENT_VALUE_REMOVED = "value_removed"

# Default/empty payload on MQTT messages
EMPTY_PAYLOAD: dict = {}


class ValueGenre(Enum):
    """Enum with all diferent Value genres."""

    USER = "User"
    SYSTEM = "System"
    UNKNOWN = None


class ValueType(Enum):
    """Enum with all diferent Value types."""

    BOOL = "Bool"
    LIST = "List"
    STRING = "String"
    DECIMAL = "Decimal"
    BYTE = "Byte"
    INT = "Int"
    BUTTON = "Button"
    UNKNOWN = None


class ValueIndex(IntEnum):
    """Enum with all (known) Value indexes."""

    # Alarm
    ALARM_TYPE = 0
    ALARM_LEVEL = 1
    ALARM_ACCESS_CONTROL = 9
    # BarrierOperator
    BARRIER_OPERATOR_LABEL = 1
    # DoorLock
    DOOR_LOCK_LOCK = 0
    # Meter
    METER_POWER = 2
    METER_RESET = 257
    # SensorMultilevel
    SENSOR_MULTILEVEL_TEMPERATURE = 1
    SENSOR_MULTILEVEL_POWER = 4
    # Color
    SWITCH_COLOR_COLOR = 0
    SWITCH_COLOR_CHANNELS = 2
    # SwitchMultilevel
    SWITCH_MULTILEVEL_LEVEL = 0
    SWITCH_MULTILEVEL_BRIGHT = 1
    SWITCH_MULTILEVEL_DIM = 2
    SWITCH_MULTILEVEL_DURATION = 5


class CommandClass(IntEnum):
    """Enum with all known CommandClasses."""

    ALARM = 113
    SENSOR_ALARM = 156
    SILENCE_ALARM = 157
    SWITCH_ALL = 39
    ANTITHEFT = 93
    ANTITHEFT_UNLOCK = 126
    APPLICATION_CAPABILITY = 87
    APPLICATION_STATUS = 34
    ASSOCIATION = 133
    ASSOCIATION_COMMAND_CONFIGURATION = 155
    ASSOCIATION_GRP_INFO = 89
    AUTHENTICATION = 161
    AUTHENTICATION_MEDIA_WRITE = 162
    BARRIER_OPERATOR = 102
    BASIC = 32
    BASIC_TARIFF_INFO = 54
    BASIC_WINDOW_COVERING = 80
    BATTERY = 128
    SENSOR_BINARY = 48
    SWITCH_BINARY = 37
    SWITCH_TOGGLE_BINARY = 40
    CLIMATE_CONTROL_SCHEDULE = 70
    CENTRAL_SCENE = 91
    CLOCK = 129
    SWITCH_COLOR = 51
    CONFIGURATION = 112
    CONTROLLER_REPLICATION = 33
    CRC_16_ENCAP = 86
    DCP_CONFIG = 58
    DCP_MONITOR = 59
    DEVICE_RESET_LOCALLY = 90
    DOOR_LOCK = 98
    DOOR_LOCK_LOGGING = 76
    ENERGY_PRODUCTION = 144
    ENTRY_CONTROL = 111
    FIRMWARE_UPDATE_MD = 122
    GENERIC_SCHEDULE = 163
    GEOGRAPHIC_LOCATION = 140
    GROUPING_NAME = 123
    HAIL = 130
    HRV_STATUS = 55
    HRV_CONTROL = 57
    HUMIDITY_CONTROL_MODE = 109
    HUMIDITY_CONTROL_OPERATING_STATE = 110
    HUMIDITY_CONTROL_SETPOINT = 100
    INCLUSION_CONTROLLER = 116
    INDICATOR = 135
    IP_ASSOCIATION = 92
    IP_CONFIGURATION = 154
    IR_REPEATER = 160
    IRRIGATION = 107
    LANGUAGE = 137
    LOCK = 118
    MAILBOX = 105
    MANUFACTURER_PROPRIETARY = 145
    MANUFACTURER_SPECIFIC = 114
    MARK = 239
    METER = 50
    METER_TBL_CONFIG = 60
    METER_TBL_MONITOR = 61
    METER_TBL_PUSH = 62
    MTP_WINDOW_COVERING = 81
    MULTI_CHANNEL = 96
    MULTI_CHANNEL_ASSOCIATION = 142
    MULTI_CMD = 143
    SENSOR_MULTILEVEL = 49
    SWITCH_MULTILEVEL = 38
    SWITCH_TOGGLE_MULTILEVEL = 41
    NETWORK_MANAGEMENT_BASIC = 77
    NETWORK_MANAGEMENT_INCLUSION = 52
    NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE = 103
    NETWORK_MANAGEMENT_PRIMARY = 84
    NETWORK_MANAGEMENT_PROXY = 82
    NO_OPERATION = 0
    NODE_NAMING = 119
    NODE_PROVISIONING = 120
    NOTIFICATION = 113
    POWERLEVEL = 115
    PREPAYMENT = 63
    PREPAYMENT_ENCAPSULATION = 65
    PROPRIETARY = 136
    PROTECTION = 117
    METER_PULSE = 53
    RATE_TBL_CONFIG = 72
    RATE_TBL_MONITOR = 73
    REMOTE_ASSOCIATION_ACTIVATE = 124
    REMOTE_ASSOCIATION = 125
    SCENE_ACTIVATION = 43
    SCENE_ACTUATOR_CONF = 44
    SCENE_CONTROLLER_CONF = 45
    SCHEDULE = 83
    SCHEDULE_ENTRY_LOCK = 78
    SCREEN_ATTRIBUTES = 147
    SCREEN_MD = 146
    SECURITY = 152
    SECURITY_2 = 159
    SECURITY_SCHEME0_MARK = 61696
    SENSOR_CONFIGURATION = 158
    SIMPLE_AV_CONTROL = 148
    SOUND_SWITCH = 121
    SUPERVISION = 108
    TARIFF_CONFIG = 74
    TARIFF_TBL_MONITOR = 75
    THERMOSTAT_FAN_MODE = 68
    THERMOSTAT_FAN_STATE = 69
    THERMOSTAT_MODE = 64
    THERMOSTAT_OPERATING_STATE = 66
    THERMOSTAT_SETBACK = 71
    THERMOSTAT_SETPOINT = 67
    TIME = 138
    TIME_PARAMETERS = 139
    TRANSPORT_SERVICE = 85
    USER_CODE = 99
    VERSION = 134
    WAKE_UP = 132
    WINDOW_COVERING = 106
    ZIP = 35
    ZIP_6LOWPAN = 79
    ZIP_GATEWAY = 95
    ZIP_NAMING = 104
    ZIP_ND = 88
    ZIP_PORTAL = 97
    ZWAVEPLUS_INFO = 94
    UNKNOWN = 0
