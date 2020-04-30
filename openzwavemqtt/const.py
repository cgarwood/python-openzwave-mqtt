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
    BASIC = "Basic"
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
    """Enum with all (known/used) Value indexes."""

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
    SENSOR_MULTILEVEL_AIR_TEMPERATURE = 1
    SENSOR_MULTILEVEL_GENERAL_PURPOSE = 2
    SENSOR_MULTILEVEL_ILLUMINANCE = 3
    SENSOR_MULTILEVEL_POWER = 4
    SENSOR_MULTILEVEL_HUMIDITY = 5
    SENSOR_MULTILEVEL_VELOCITY = 6
    SENSOR_MULTILEVEL_DIRECTION = 7
    SENSOR_MULTILEVEL_ATMOSPHERIC_PRESSURE = 8
    SENSOR_MULTILEVEL_BAROMETIC_PRESSURE = 9
    SENSOR_MULTILEVEL_SOLAR_RADIATION = 10
    SENSOR_MULTILEVEL_DEW_POINT = 11
    SENSOR_MULTILEVEL_RAIN_RATE = 12
    SENSOR_MULTILEVEL_TIDE_LEVEL = 13
    SENSOR_MULTILEVEL_WEIGHT = 14
    SENSOR_MULTILEVEL_VOLTAGE = 15
    SENSOR_MULTILEVEL_CURRENT = 16
    SENSOR_MULTILEVEL_CARBON_DIOXIDE = 17
    SENSOR_MULTILEVEL_AIR_FLOW = 18
    SENSOR_MULTILEVEL_TANK_CAPACITY = 19
    SENSOR_MULTILEVEL_DISTANCE = 20
    SENSOR_MULTILEVEL_ANGLE_POSITION = 21
    SENSOR_MULTILEVEL_ROTATION = 22
    SENSOR_MULTILEVEL_WATER_TEMPERATURE = 23
    SENSOR_MULTILEVEL_SOIL_TEMPERATURE = 24
    SENSOR_MULTILEVEL_SEISMIC_INTENSITY = 25
    SENSOR_MULTILEVEL_SEISMIC_MAGNITUDE = 26
    SENSOR_MULTILEVEL_ULTRAVIOLET = 27
    SENSOR_MULTILEVEL_ELECTRICAL_RESISTIVITY = 28
    SENSOR_MULTILEVEL_ELECTRICAL_CONDUCTIVITY = 29
    SENSOR_MULTILEVEL_LOUDNESS = 30
    SENSOR_MULTILEVEL_MOISTURE = 31
    SENSOR_MULTILEVEL_FREQUENCY = 32
    SENSOR_MULTILEVEL_TIME = 33
    SENSOR_MULTILEVEL_TARGET_TEMPERATURE = 34
    SENSOR_MULTILEVEL_PARTICULATE_MATTER = 35
    SENSOR_MULTILEVEL_FORMALDEHYDE_CH20_LEVEL = 36
    SENSOR_MULTILEVEL_RADON_CONCENTRATION = 37
    SENSOR_MULTILEVEL_METHANE_DENSITY = 38
    SENSOR_MULTILEVEL_VOLATILE_ORGANIC_COMPOUND = 39
    SENSOR_MULTILEVEL_CARBON_MONOXIDE = 40
    SENSOR_MULTILEVEL_SOIL_HUMIDITY = 41
    SENSOR_MULTILEVEL_SOIL_REACTIVITY = 42
    SENSOR_MULTILEVEL_SOIL_SALINITY = 43
    SENSOR_MULTILEVEL_HEART_RATE = 44
    SENSOR_MULTILEVEL_BLOOD_PRESSURE = 45
    SENSOR_MULTILEVEL_MUSCLE_MASS = 46
    SENSOR_MULTILEVEL_FAT_MASS = 47
    SENSOR_MULTILEVEL_BONE_MASS = 48
    SENSOR_MULTILEVEL_TOTAL_BODY_WATER = 49
    SENSOR_MULTILEVEL_BASIC_METABOLIC_RATE = 50
    SENSOR_MULTILEVEL_BODY_MASS_INDEX = 51
    SENSOR_MULTILEVEL_X_AXIS_ACCELERATION = 52
    SENSOR_MULTILEVEL_Y_AXIS_ACCELERATION = 53
    SENSOR_MULTILEVEL_Z_AXIS_ACCELERATION = 54
    SENSOR_MULTILEVEL_SMOKE_DENSITY = 55
    SENSOR_MULTILEVEL_WATER_FLOW = 56
    SENSOR_MULTILEVEL_WATER_PRESSURE = 57
    SENSOR_MULTILEVEL_RF_SIGNAL_STRENGTH = 58
    SENSOR_MULTILEVEL_PARTICULATE_MATTER = 59
    SENSOR_MULTILEVEL_RESPIRATORY_RATE = 60
    SENSOR_MULTILEVEL_RELATIVE_MODULATION = 61
    SENSOR_MULTILEVEL_BOILER_WATER_TEMPERATURE = 62
    SENSOR_MULTILEVEL_DOMESTIC_HOT_WATER_TEMPERATURE = 63
    SENSOR_MULTILEVEL_OUTSIDE_TEMPERATURE = 64
    SENSOR_MULTILEVEL_EXHAUST_TEMPERATURE = 65
    SENSOR_MULTILEVEL_WATER_CHLORINE = 66
    SENSOR_MULTILEVEL_WATER_ACIDITY = 67
    SENSOR_MULTILEVEL_WATER_OXIDATION_REDUCTION_POTENTIAL = 68
    SENSOR_MULTILEVEL_HEART_RATE_LF_HF_RATIO = 69
    SENSOR_MULTILEVEL_MOTION_DIRECTION = 70
    SENSOR_MULTILEVEL_APPLIED_FORCE = 71
    SENSOR_MULTILEVEL_RETURN_AIR_TEMPERATURE = 72
    SENSOR_MULTILEVEL_SUPPLY_AIR_TEMPERATURE = 73
    SENSOR_MULTILEVEL_CONDENSER_COIL_TEMPERATURE = 74
    SENSOR_MULTILEVEL_EVAPORATOR_COIL_TEMPERATURE = 75
    SENSOR_MULTILEVEL_LIQUID_LINE_TEMPERATURE = 76
    SENSOR_MULTILEVEL_DISCHARGE_LINE_TEMPERATURE = 77
    SENSOR_MULTILEVEL_SUCTION = 78
    SENSOR_MULTILEVEL_DISCHARGE = 79
    SENSOR_MULTILEVEL_DEFROST_TEMPERATURE = 80
    SENSOR_MULTILEVEL_OZONE = 81
    SENSOR_MULTILEVEL_SULFUR_DIOXIDE = 82
    SENSOR_MULTILEVEL_NITROGEN_DIOXIDE = 83
    SENSOR_MULTILEVEL_AMMONIA = 84
    SENSOR_MULTILEVEL_LEAD = 85
    SENSOR_MULTILEVEL_PARTICULATE_MATTER = 86
    # Color
    SWITCH_COLOR_COLOR = 0
    SWITCH_COLOR_CHANNELS = 2
    # SwitchMultilevel
    SWITCH_MULTILEVEL_LEVEL = 0
    SWITCH_MULTILEVEL_BRIGHT = 1
    SWITCH_MULTILEVEL_DIM = 2
    SWITCH_MULTILEVEL_DURATION = 5
    # Notification
    NOTIFICATION_SMOKE_ALARM = 1
    NOTIFICATION_CARBON_MONOOXIDE = 2
    NOTIFICATION_CARBON_DIOXIDE = 3
    NOTIFICATION_HEAT = 4
    NOTIFICATION_WATER = 5
    NOTIFICATION_ACCESS_CONTROL = 6
    NOTIFICATION_HOME_SECURITY = 7
    NOTIFICATION_POWER_MANAGEMENT = 8
    NOTIFICATION_SYSTEM = 9
    NOTIFICATION_EMERGENCY = 10
    NOTIFICATION_CLOCK = 11
    NOTIFICATION_APPLIANCE = 12
    NOTIFICATION_HOME_HEALTH = 13
    NOTIFICATION_SIREN = 14
    NOTIFICATION_WATER_VALVE = 15
    NOTIFICATION_WEATHER = 16
    NOTIFICATION_IRRIGATION = 17
    NOTIFICATION_GAS = 18
    UNKNOWN = 999


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


# DeviceTypes Generic/Specific

GENERIC_TYPE_AV_CONTROL_POINT = 3
SPECIFIC_TYPE_DOORBELL = 18
SPECIFIC_TYPE_SATELLITE_RECEIVER = 4
SPECIFIC_TYPE_SATELLITE_RECEIVER_V2 = 17

GENERIC_TYPE_DISPLAY = 4
SPECIFIC_TYPE_SIMPLE_DISPLAY = 1

GENERIC_TYPE_ENTRY_CONTROL = 64
SPECIFIC_TYPE_DOOR_LOCK = 1
SPECIFIC_TYPE_ADVANCED_DOOR_LOCK = 2
SPECIFIC_TYPE_SECURE_KEYPAD_DOOR_LOCK = 3
SPECIFIC_TYPE_SECURE_KEYPAD_DOOR_LOCK_DEADBOLT = 4
SPECIFIC_TYPE_SECURE_DOOR = 5
SPECIFIC_TYPE_SECURE_GATE = 6
SPECIFIC_TYPE_SECURE_BARRIER_ADDON = 7
SPECIFIC_TYPE_SECURE_BARRIER_OPEN_ONLY = 8
SPECIFIC_TYPE_SECURE_BARRIER_CLOSE_ONLY = 9
SPECIFIC_TYPE_SECURE_LOCKBOX = 10
SPECIFIC_TYPE_SECURE_KEYPAD = 11

GENERIC_TYPE_GENERIC_CONTROLLER = 1
SPECIFIC_TYPE_PORTABLE_CONTROLLER = 1
SPECIFIC_TYPE_PORTABLE_SCENE_CONTROLLER = 2
SPECIFIC_TYPE_PORTABLE_INSTALLER_TOOL = 3
SPECIFIC_TYPE_REMOTE_CONTROL_AV = 4
SPECIFIC_TYPE_REMOTE_CONTROL_SIMPLE = 6

GENERIC_TYPE_METER = 49
SPECIFIC_TYPE_SIMPLE_METER = 1
SPECIFIC_TYPE_ADV_ENERGY_CONTROL = 2
SPECIFIC_TYPE_WHOLE_HOME_METER_SIMPLE = 3

GENERIC_TYPE_METER_PULSE = 48

GENERIC_TYPE_NON_INTEROPERABLE = 255

GENERIC_TYPE_REPEATER_SLAVE = 15
SPECIFIC_TYPE_REPEATER_SLAVE = 1
SPECIFIC_TYPE_VIRTUAL_NODE = 2

GENERIC_TYPE_SECURITY_PANEL = 23
SPECIFIC_TYPE_ZONED_SECURITY_PANEL = 1

GENERIC_TYPE_SEMI_INTEROPERABLE = 80
SPECIFIC_TYPE_ENERGY_PRODUCTION = 1

GENERIC_TYPE_SENSOR_ALARM = 161
SPECIFIC_TYPE_ADV_ZENSOR_NET_ALARM_SENSOR = 5
SPECIFIC_TYPE_ADV_ZENSOR_NET_SMOKE_SENSOR = 10
SPECIFIC_TYPE_BASIC_ROUTING_ALARM_SENSOR = 1
SPECIFIC_TYPE_BASIC_ROUTING_SMOKE_SENSOR = 6
SPECIFIC_TYPE_BASIC_ZENSOR_NET_ALARM_SENSOR = 3
SPECIFIC_TYPE_BASIC_ZENSOR_NET_SMOKE_SENSOR = 8
SPECIFIC_TYPE_ROUTING_ALARM_SENSOR = 2
SPECIFIC_TYPE_ROUTING_SMOKE_SENSOR = 7
SPECIFIC_TYPE_ZENSOR_NET_ALARM_SENSOR = 4
SPECIFIC_TYPE_ZENSOR_NET_SMOKE_SENSOR = 9
SPECIFIC_TYPE_ALARM_SENSOR = 11

GENERIC_TYPE_SENSOR_BINARY = 32
SPECIFIC_TYPE_ROUTING_SENSOR_BINARY = 1

GENERIC_TYPE_SENSOR_MULTILEVEL = 33
SPECIFIC_TYPE_ROUTING_SENSOR_MULTILEVEL = 1
SPECIFIC_TYPE_CHIMNEY_FAN = 2

GENERIC_TYPE_STATIC_CONTROLLER = 2
SPECIFIC_TYPE_PC_CONTROLLER = 1
SPECIFIC_TYPE_SCENE_CONTROLLER = 2
SPECIFIC_TYPE_STATIC_INSTALLER_TOOL = 3
SPECIFIC_TYPE_SET_TOP_BOX = 4
SPECIFIC_TYPE_SUB_SYSTEM_CONTROLLER = 5
SPECIFIC_TYPE_TV = 6
SPECIFIC_TYPE_GATEWAY = 7

GENERIC_TYPE_SWITCH_BINARY = 16
SPECIFIC_TYPE_POWER_SWITCH_BINARY = 1
SPECIFIC_TYPE_SCENE_SWITCH_BINARY = 3
SPECIFIC_TYPE_POWER_STRIP = 4
SPECIFIC_TYPE_SIREN = 5
SPECIFIC_TYPE_VALVE_OPEN_CLOSE = 6
SPECIFIC_TYPE_COLOR_TUNABLE_BINARY = 2
SPECIFIC_TYPE_IRRIGATION_CONTROLLER = 7

GENERIC_TYPE_SWITCH_MULTILEVEL = 17
SPECIFIC_TYPE_CLASS_A_MOTOR_CONTROL = 5
SPECIFIC_TYPE_CLASS_B_MOTOR_CONTROL = 6
SPECIFIC_TYPE_CLASS_C_MOTOR_CONTROL = 7
SPECIFIC_TYPE_MOTOR_MULTIPOSITION = 3
SPECIFIC_TYPE_POWER_SWITCH_MULTILEVEL = 1
SPECIFIC_TYPE_SCENE_SWITCH_MULTILEVEL = 4
SPECIFIC_TYPE_FAN_SWITCH = 8
SPECIFIC_TYPE_COLOR_TUNABLE_MULTILEVEL = 2

GENERIC_TYPE_SWITCH_REMOTE = 18
SPECIFIC_TYPE_REMOTE_BINARY = 1
SPECIFIC_TYPE_REMOTE_MULTILEVEL = 2
SPECIFIC_TYPE_REMOTE_TOGGLE_BINARY = 3
SPECIFIC_TYPE_REMOTE_TOGGLE_MULTILEVEL = 4

GENERIC_TYPE_SWITCH_TOGGLE = 19
SPECIFIC_TYPE_SWITCH_TOGGLE_BINARY = 1
SPECIFIC_TYPE_SWITCH_TOGGLE_MULTILEVEL = 2

GENERIC_TYPE_THERMOSTAT = 8
SPECIFIC_TYPE_SETBACK_SCHEDULE_THERMOSTAT = 3
SPECIFIC_TYPE_SETBACK_THERMOSTAT = 5
SPECIFIC_TYPE_SETPOINT_THERMOSTAT = 4
SPECIFIC_TYPE_THERMOSTAT_GENERAL = 2
SPECIFIC_TYPE_THERMOSTAT_GENERAL_V2 = 6
SPECIFIC_TYPE_THERMOSTAT_HEATING = 1

GENERIC_TYPE_VENTILATION = 22
SPECIFIC_TYPE_RESIDENTIAL_HRV = 1

GENERIC_TYPE_WINDOWS_COVERING = 9
SPECIFIC_TYPE_SIMPLE_WINDOW_COVERING = 1

GENERIC_TYPE_ZIP_NODE = 21
SPECIFIC_TYPE_ZIP_ADV_NODE = 2
SPECIFIC_TYPE_ZIP_TUN_NODE = 1

GENERIC_TYPE_WALL_CONTROLLER = 24
SPECIFIC_TYPE_BASIC_WALL_CONTROLLER = 1

GENERIC_TYPE_NETWORK_EXTENDER = 5
SPECIFIC_TYPE_SECURE_EXTENDER = 1

GENERIC_TYPE_APPLIANCE = 6
SPECIFIC_TYPE_GENERAL_APPLIANCE = 1
SPECIFIC_TYPE_KITCHEN_APPLIANCE = 2
SPECIFIC_TYPE_LAUNDRY_APPLIANCE = 3

GENERIC_TYPE_SENSOR_NOTIFICATION = 7
SPECIFIC_TYPE_NOTIFICATION_SENSOR = 1
