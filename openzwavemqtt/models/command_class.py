"""Model for the CommandClass."""
from typing import Optional

from ..base import ItemCollection
from ..const import (
    EVENT_COMMAND_CLASS_ADDED,
    EVENT_COMMAND_CLASS_CHANGED,
    EVENT_COMMAND_CLASS_REMOVED,
    LOGGER,
    CommandClass,
    ValueIndex,
)
from .node_child_base import OZWNodeChildBase
from .value import OZWValue


class OZWCommandClass(OZWNodeChildBase):
    """Model for the OZW CommandClass."""

    EVENT_ADDED = EVENT_COMMAND_CLASS_ADDED
    EVENT_CHANGED = EVENT_COMMAND_CLASS_CHANGED
    EVENT_REMOVED = EVENT_COMMAND_CLASS_REMOVED

    PLURAL_NAME = "commandclasses"

    @property
    def instance(self) -> int:
        """Return Instance."""
        return self.data.get("Instance")

    @property
    def command_class_id(self) -> CommandClass:
        """Return CommandClassId as CommandClass Enum."""
        try:
            return CommandClass(self.data.get("CommandClassId"))
        except ValueError:
            LOGGER.warning(
                "Unknown CommandClass found: %s", self.data.get("CommandClassId")
            )
            return CommandClass.UNKNOWN

    @property
    def command_class(self) -> str:
        """Return string/label representation of this CommandClass."""
        # TODO: This needs changing to a better name once fixed upstream in the daemon
        return self.data.get("CommandClass")

    @property
    def time_stamp(self) -> int:
        """Return TimeStamp."""
        return self.data.get("TimeStamp")

    def create_collections(self):
        """Create collections that Node supports."""
        return {"value": ItemCollection(OZWValue)}

    def get_value(self, value_index: ValueIndex) -> Optional[OZWValue]:
        """Return a specific OZWValue on this CommandClass (if exists)."""
        # pylint: disable=no-member
        for value in self.values():
            if value.index == value_index:
                return value
        return None

    def has_value(self, value_index: ValueIndex) -> bool:
        """Determine if the CommandClass has the given ValueIndex."""
        return self.get_value(value_index) is not None
