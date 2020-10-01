"""Utility functions and classes for OpenZWave."""
from .const import (
    CommandClass,
    ValueGenre,
    ValueType,
    ATTR_LABEL,
    ATTR_MAX,
    ATTR_MIN,
    ATTR_OPTIONS,
    ATTR_PARAMETER,
    ATTR_TYPE,
    ATTR_VALUE,
)


class OZWValidationResponse:
    """Class to hold response for validating an action."""

    def __init__(self, success, *args, payload=None, err_msg=None):
        """Initialize OZWValidationResponse."""
        self.success = success
        self.payload = payload
        self.err_msg = err_msg
        self.err_args = args

    @classmethod
    def process_fail(cls, err_msg, *args):
        """Process an invalid request."""
        return cls(False, err_msg=err_msg, *args)

    @classmethod
    def process_fail_on_type(cls, value, new_value):
        """Process an invalid request that fails type validation."""
        return cls.process_fail(
            "Configuration parameter type {} does not match the value type {}",
            value.type,
            type(new_value),
        )

    @classmethod
    def process_success(cls, payload):
        """Process a valid request."""
        return cls(True, payload=payload)


def set_config_parameter(node, parameter, new_value):
    """Set config parameter to a node."""
    value = node.get_value(CommandClass.CONFIGURATION, parameter)
    if not value:
        return OZWValidationResponse.process_fail(
            "Configuration parameter {} for OZW Node Instance not found", parameter,
        )

    # Bool can be passed in as string or bool
    if value.type == ValueType.BOOL:
        if isinstance(new_value, bool):
            value.send_value(new_value)
            return OZWValidationResponse.process_success(new_value)
        if isinstance(new_value, str):
            if new_value.lower() in ("true", "false"):
                payload = new_value.lower() == "true"
                value.send_value(payload)
                return OZWValidationResponse.process_success(payload)

            return OZWValidationResponse.process_fail(
                "Configuration parameter value must be true or false",
            )

        return OZWValidationResponse.process_fail_on_type(value, new_value)

    # List value can be passed in as string or int
    if value.type == ValueType.LIST:
        try:
            new_value = int(new_value)
        except ValueError:
            pass
        if not isinstance(new_value, str) and not isinstance(new_value, int):
            return OZWValidationResponse.process_fail_on_type(value, new_value)

        for option in value.value["List"]:
            if new_value not in (option["Label"], option["Value"]):
                continue
            try:
                payload = int(option["Value"])
            except ValueError:
                payload = option["Value"]
            value.send_value(payload)
            return OZWValidationResponse.process_success(payload)

        return OZWValidationResponse.process_fail(
            "Invalid value {} for parameter {}", new_value, parameter,
        )

    # Int, Byte, Short are always passed as int, Decimal should be float
    if value.type in (ValueType.INT, ValueType.BYTE, ValueType.SHORT,):
        try:
            new_value = int(new_value)
        except ValueError:
            return OZWValidationResponse.process_fail_on_type(value, new_value)
        if (value.max and new_value > value.max) or (
            value.min and new_value < value.min
        ):
            return OZWValidationResponse.process_fail(
                "Value {} out of range for parameter {} (Min: {} Max: {})",
                new_value,
                parameter,
                value.min,
                value.max,
            )
        value.send_value(new_value)
        return OZWValidationResponse.process_success(new_value)

    # This will catch BUTTON, STRING, and UNKNOWN ValueTypes
    return OZWValidationResponse.process_fail(
        "Value type of {} for parameter {} not supported", value.type, parameter,
    )


def get_config_parameters(node):
    """Get config parameter from a node."""
    values = []

    for value in node.values():
        value_to_return = {}
        # BUTTON types aren't supported yet, and STRING and UNKNOWN
        # are not valid config parameter types
        if (
            value.read_only
            or value.genre != ValueGenre.CONFIG
            or value.type in (ValueType.BUTTON, ValueType.STRING, ValueType.UNKNOWN)
        ):
            continue

        value_to_return = {
            ATTR_LABEL: value.label,
            ATTR_TYPE: value.type.value,
            ATTR_PARAMETER: value.index.value,
        }

        if value.type == ValueType.BOOL:
            value_to_return[ATTR_VALUE] = value.value

        elif value.type == ValueType.LIST:
            value_to_return[ATTR_VALUE] = value.value["Selected"]
            value_to_return[ATTR_OPTIONS] = value.value["List"]

        elif value.type in (ValueType.INT, ValueType.BYTE, ValueType.SHORT,):
            value_to_return[ATTR_VALUE] = int(value.value)
            value_to_return[ATTR_MAX] = value.max
            value_to_return[ATTR_MIN] = value.min

        values.append(value_to_return)

    return OZWValidationResponse.process_success(values)
