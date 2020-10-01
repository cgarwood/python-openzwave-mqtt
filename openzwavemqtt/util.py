"""Utility functions and classes for OpenZWave."""
from typing import Any, Dict, List

from .const import (
    ATTR_LABEL,
    ATTR_MAX,
    ATTR_MIN,
    ATTR_OPTIONS,
    ATTR_PARAMETER,
    ATTR_POSITION,
    ATTR_TYPE,
    ATTR_VALUE,
    CommandClass,
    ValueGenre,
    ValueType,
)
from .exceptions import InvalidValueError, NotFoundError, WrongTypeError
from .manager import OZWManager
from .models.node import OZWNode


def get_node_from_manager(
    manager: OZWManager, instance_id: int, node_id: int
) -> OZWNode:
    """Get OZWNode from OZWManager."""
    instance = manager.get_instance(instance_id)  # type: ignore
    if not instance:
        raise NotFoundError(f"OZW Instance {instance_id} not found")

    node = instance.get_node(node_id)
    if not node:
        raise NotFoundError(f"OZW Node {node_id} not found")

    return node  # type: ignore


def set_config_parameter(node: OZWNode, parameter: int, new_value: Any) -> Any:
    """Set config parameter to a node."""
    value = node.get_value(CommandClass.CONFIGURATION, parameter)
    if not value:
        raise NotFoundError(
            f"Configuration parameter {parameter} for OZW Node Instance not found"
        )

    # Bool can be passed in as string or bool
    if value.type == ValueType.BOOL:
        if isinstance(new_value, bool):
            value.send_value(new_value)  # type: ignore
            return new_value
        if isinstance(new_value, str):
            if new_value.lower() in ("true", "false"):
                payload = new_value.lower() == "true"
                value.send_value(payload)  # type: ignore
                return payload

            raise WrongTypeError("Configuration parameter value must be true or false")

        raise WrongTypeError(
            (
                f"Configuration parameter type {value.type} does not match "
                f"the value type {type(new_value)}"
            )
        )

    # List value can be passed in as string or int
    if value.type == ValueType.LIST:
        try:
            new_value = int(new_value)
        except ValueError:
            pass
        if not isinstance(new_value, str) and not isinstance(new_value, int):
            raise WrongTypeError(
                (
                    f"Configuration parameter type {value.type} does not match "
                    f"the value type {type(new_value)}"
                )
            )

        for option in value.value["List"]:  # type: ignore
            if new_value not in (option["Label"], option["Value"]):
                continue
            try:
                payload = int(option["Value"])
            except ValueError:
                payload = option["Value"]
            value.send_value(payload)  # type: ignore
            return payload

        raise WrongTypeError(
            (
                f"Configuration parameter type {value.type} does not match "
                f"the value type {type(new_value)}"
            )
        )

    # Bitset value is passed in as dict
    if value.type == ValueType.BITSET:
        try:
            if not isinstance(new_value, dict) or not any(
                [int(val) not in (0, 1) for val in new_value.values()]
            ):
                raise WrongTypeError(
                    (
                        "Configuration parameter value must be in the form of a "
                        "dict with keys being the label or position of a "
                        "particular bit and values being 0 or 1"
                    )
                )
        except ValueError:
            raise WrongTypeError(
                (
                    "Configuration parameter value must be in the form of a "
                    "dict with keys being the label or position of a "
                    "particular bit and values being 0 or 1"
                )
            )

        # Check that all keys in dictionary are a valid position or label
        if not any(
            any(key not in (int(bit["Position"]), bit["Label"]) for bit in value.value)  # type: ignore
            for key in new_value.keys()
        ):
            raise NotFoundError("Configuration parameter value has an invalid key")

        value.send_value(new_value)  # type: ignore
        return value

    # Int, Byte, Short are always passed as int, Decimal should be float
    if value.type in (ValueType.INT, ValueType.BYTE, ValueType.SHORT):
        try:
            new_value = int(new_value)
        except ValueError:
            raise WrongTypeError(
                (
                    f"Configuration parameter type {value.type} does not match "
                    f"the value type {type(new_value)}"
                )
            )
        if (value.max and new_value > value.max) or (
            value.min and new_value < value.min
        ):
            raise InvalidValueError(
                (
                    f"Value {new_value} out of range for parameter {parameter}"
                    f" (Range: {value.min}-{value.max})",
                )
            )
        value.send_value(new_value)  # type: ignore
        return new_value

    # This will catch BUTTON, STRING, and UNKNOWN ValueTypes
    raise WrongTypeError(
        f"Value type of {value.type} for parameter {parameter} not supported"
    )


def get_config_parameters(node: OZWNode) -> List[Dict[str, Any]]:
    """Get config parameter from a node."""
    values = []

    for value in node.values():
        value_to_return = {}
        # BUTTON types aren't supported yet, and STRING, RAW, SCHEDULE,
        # and UNKNOWN are not valid config parameter types
        if (
            value.read_only
            or value.genre != ValueGenre.CONFIG
            or value.type
            in (
                ValueType.BUTTON,
                ValueType.STRING,
                ValueType.RAW,
                ValueType.SCHEDULE,
                ValueType.UNKNOWN,
            )
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
            value_to_return[ATTR_VALUE] = value.value["Selected"]  # type: ignore
            value_to_return[ATTR_OPTIONS] = value.value["List"]  # type: ignore

        elif value.type == ValueType.BITSET:
            value_to_return[ATTR_VALUE] = [
                {
                    ATTR_LABEL: bit["Label"],  # type: ignore
                    ATTR_POSITION: int(bit["Position"]),  # type: ignore
                    ATTR_VALUE: int(bit["Value"]),  # type: ignore
                }
                for bit in value.value  # type: ignore
            ]

        elif value.type in (ValueType.INT, ValueType.BYTE, ValueType.SHORT):
            value_to_return[ATTR_VALUE] = int(value.value)
            value_to_return[ATTR_MAX] = value.max
            value_to_return[ATTR_MIN] = value.min

        values.append(value_to_return)

    return values
