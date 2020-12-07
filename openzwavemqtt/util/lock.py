"""Utility functions for OpenZWave locks."""
from typing import Dict, List, Union

from ..const import (
    ATTR_CODE_SLOT,
    ATTR_IN_USE,
    ATTR_NAME,
    ATTR_USERCODE,
    CommandClass,
    ValueGenre,
    ValueIndex,
)
from ..exceptions import InvalidValueError, NotFoundError, NotSupportedError
from ..models.node import OZWNode


def get_code_slots(node: OZWNode) -> List[Dict[str, Union[int, bool, str]]]:
    """Get all code slots on the lock and whether or not they are used."""
    command_class = node.get_command_class(CommandClass.USER_CODE)

    if not command_class:
        raise NotSupportedError("Node doesn't have code slots")

    return [
        {
            ATTR_CODE_SLOT: value.index.value,
            ATTR_NAME: value.label,
            ATTR_IN_USE: value.value_set,
        }
        for value in command_class.values()  # type: ignore
        if value.genre == ValueGenre.USER
    ]


def set_usercode(node: OZWNode, code_slot: int, usercode: str) -> None:
    """Set the usercode to index X on the lock."""
    value = node.get_value(CommandClass.USER_CODE, code_slot)

    if not value:
        raise NotFoundError(f"Code slot {code_slot} not found")

    if len(str(usercode)) < 4:
        raise InvalidValueError("User code must be at least 4 digits")

    value.send_value(usercode)  # type: ignore


def clear_usercode(node: OZWNode, code_slot: int) -> None:
    """Clear usercode in slot X on the lock."""
    value = node.get_value(CommandClass.USER_CODE, ValueIndex.CLEAR_USER_CODE)

    if not value:
        raise NotSupportedError("Node is not capable of clearing user codes")

    value.send_value(code_slot)  # type: ignore
    # Sending twice because the first time it doesn't take
    value.send_value(code_slot)  # type: ignore


def get_usercodes(node: OZWNode) -> List[Dict[str, Union[int, bool, str]]]:
    """Get all code slots and usercodes on the lock."""
    command_class = node.get_command_class(CommandClass.USER_CODE)

    if not command_class:
        raise NotSupportedError("Node doesn't have code slots")

    return [
        {
            ATTR_CODE_SLOT: value.index.value,
            ATTR_NAME: value.label,
            ATTR_IN_USE: value.value_set,
            ATTR_USERCODE: value.value if value.value_set else None,
        }
        for value in command_class.values()  # type: ignore
        if value.genre == ValueGenre.USER
    ]


def get_usercode(
    node: OZWNode, code_slot: int
) -> List[Dict[str, Union[int, bool, str]]]:
    """Get usercode from slot X on the lock."""
    value = node.get_value(CommandClass.USER_CODE, code_slot)

    if not value:
        raise NotFoundError(f"Code slot {code_slot} not found")

    return value.value if value.value_set else None
