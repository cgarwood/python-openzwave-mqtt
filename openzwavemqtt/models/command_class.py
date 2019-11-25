from ..base import ItemCollection
from ..const import (
    EVENT_COMMAND_CLASS_ADDED,
    EVENT_COMMAND_CLASS_CHANGED,
    EVENT_COMMAND_CLASS_REMOVED,
)

from .value import OZWValue
from .node_child_base import OZWNodeChildBase


class OZWCommandClass(OZWNodeChildBase):

    EVENT_ADDED = EVENT_COMMAND_CLASS_ADDED
    EVENT_CHANGED = EVENT_COMMAND_CLASS_CHANGED
    EVENT_REMOVED = EVENT_COMMAND_CLASS_REMOVED

    @property
    def instance(self) -> int:
        """Return Instance."""
        return self.data.get("Instance")

    @property
    def command_class_id(self) -> int:
        """Return CommandClassId."""
        return self.data.get("CommandClassId")

    @property
    def command_class(self) -> str:
        """Return CommandClass."""
        return self.data.get("CommandClass")

    @property
    def time_stamp(self) -> int:
        """Return TimeStamp."""
        return self.data.get("TimeStamp")

    def create_collections(self):
        """Create collections that Node supports."""
        return {"value": ItemCollection(self.options, self, OZWValue)}
