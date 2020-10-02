"""Utility functions for OpenZWave nodes."""
from typing import cast, Dict, List, Union

from ..const import (
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
from ..exceptions import InvalidValueError, NotFoundError, WrongTypeError
from ..manager import OZWManager
from ..models.node import OZWNode
from ..models.value import OZWValue


def get_node_from_manager(
    manager: OZWManager, instance_id: int, node_id: int
) -> OZWNode:
    """Get OZWNode from OZWManager."""
    instance = manager.get_instance(instance_id)  # type: ignore
    if not instance:
        raise NotFoundError(f"OZW Instance {instance_id} not found")

    node = cast(OZWNode, instance.get_node(node_id))
    if not node:
        raise NotFoundError(f"OZW Node {node_id} not found")

    return node


def _set_bool_config_parameter(value: OZWValue, new_value: Union[bool, str]) -> bool:
    """Set a ValueType.BOOL config parameter."""
    if isinstance(new_value, bool):
        value.send_value(new_value)  # type: ignore
        return new_value

    if isinstance(new_value, str):
        new_value = new_value.lower()
        if new_value in ("true", "false"):
            payload = new_value == "true"
            value.send_value(payload)  # type: ignore
            return payload

        raise WrongTypeError("Configuration parameter value must be true or false")

    raise WrongTypeError(
        (
            f"Configuration parameter type {value.type} does not match "
            f"the value type {type(new_value)}"
        )
    )


def _set_list_config_parameter(value: OZWValue, new_value: Union[int, str]) -> int:
    """Set a ValueType.LIST config parameter."""
    try:
        new_value = int(new_value)
    except ValueError:
        pass

    if isinstance(new_value, (int, str)):
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


def _set_bitset_config_parameter(
    value: OZWValue, new_value: List[Dict[str, Union[int, str, bool]]]
) -> List[Dict[str, Union[int, str, bool]]]:
    """Set a ValueType.BITSET config parameter."""
    # Check that ATTR_VALUE is provided and is bool, check that exactly one of ATTR_POSITION
    # and ATTR_LABEL is provided, and that ATTR_POSITION is an int and ATTR_LABEL is a str
    if not isinstance(new_value, list) or any(
        [
            ATTR_VALUE not in bit
            or (ATTR_POSITION in bit and ATTR_LABEL in bit)
            or (ATTR_POSITION not in bit and ATTR_LABEL not in bit)
            or (ATTR_POSITION in bit and not isinstance(bit[ATTR_POSITION], int))
            or (ATTR_LABEL in bit and not isinstance(bit[ATTR_LABEL], str))
            or not isinstance(bit[ATTR_VALUE], bool)
            for bit in new_value
        ]
    ):
        raise WrongTypeError(
            (
                "Configuration parameter value must be in the form of a "
                f"list of dicts with the {ATTR_VALUE} key and either the "
                f"{ATTR_POSITION} or {ATTR_LABEL} keys defined. {ATTR_VALUE} "
                f"should be a bool, {ATTR_POSITION} should be an int, and "
                f"{ATTR_LABEL} should be a string."
            )
        )

    # Check that all keys in dictionary are a valid position or label
    if any(
        next(
            [
                (ATTR_POSITION in new_bit and new_bit[ATTR_POSITION] == int(bit["Position"]))  # type: ignore
                or (ATTR_LABEL in new_bit and new_bit[ATTR_LABEL] == int(bit["Label"]))  # type: ignore
                for bit in value.value  # type: ignore
            ],
            None,
        )
        is None
        for new_bit in new_value
    ):
        raise NotFoundError("Configuration parameter value has an invalid key")

    value.send_value(new_value)  # type: ignore
    return new_value


def _set_int_config_parameter(parameter: int, value: OZWValue, new_value: int) -> int:
    """Set a ValueType.BITSET config parameter."""
    try:
        new_value = int(new_value)
    except ValueError:
        raise WrongTypeError(
            (
                f"Configuration parameter type {value.type} does not match "
                f"the value type {type(new_value)}"
            )
        )
    if (value.max and new_value > value.max) or (value.min and new_value < value.min):
        raise InvalidValueError(
            (
                f"Value {new_value} out of range for parameter {parameter}"
                f" (Range: {value.min}-{value.max})",
            )
        )
    value.send_value(new_value)  # type: ignore
    return new_value


def set_config_parameter(
    node: OZWNode,
    parameter: int,
    new_value: Union[int, str, bool, List[Dict[str, Union[int, str, bool]]]],
) -> Union[int, str, bool, List[Dict[str, Union[int, str, bool]]]]:
    """Set config parameter to a node."""
    value = node.get_value(CommandClass.CONFIGURATION, parameter)
    if not value:
        raise NotFoundError(
            f"Configuration parameter {parameter} for OZW Node Instance not found"
        )

    # Bool can be passed in as string or bool
    if value.type == ValueType.BOOL:
        return _set_bool_config_parameter(value, new_value)  # type: ignore

    # List value can be passed in as string or int
    if value.type == ValueType.LIST:
        return _set_list_config_parameter(value, new_value)  # type: ignore

    # Bitset value is passed in as dict
    if value.type == ValueType.BITSET:
        return _set_bitset_config_parameter(value, new_value)  # type: ignore

    # Int, Byte, Short are always passed as int, Decimal should be float
    if value.type in (ValueType.INT, ValueType.BYTE, ValueType.SHORT):
        return _set_int_config_parameter(parameter, value, new_value)  # type: ignore

    # This will catch BUTTON, STRING, and UNKNOWN ValueTypes
    raise WrongTypeError(
        f"Value type of {value.type} for parameter {parameter} not supported"
    )


def get_config_parameters(
    node: OZWNode,
) -> List[Dict[str, Union[int, str, bool, List[Dict[str, Union[int, str, bool]]]]]]:
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
                    ATTR_VALUE: bool(bit["Value"]),  # type: ignore
                }
                for bit in value.value  # type: ignore
            ]

        elif value.type in (ValueType.INT, ValueType.BYTE, ValueType.SHORT):
            value_to_return[ATTR_VALUE] = int(value.value)  # type: ignore
            value_to_return[ATTR_MAX] = value.max
            value_to_return[ATTR_MIN] = value.min

        values.append(value_to_return)

    return values
