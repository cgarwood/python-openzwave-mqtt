"""Model for Node Instance."""
from ..base import ItemCollection
from ..const import (
    EVENT_NODE_INSTANCE_ADDED,
    EVENT_NODE_INSTANCE_CHANGED,
    EVENT_NODE_INSTANCE_REMOVED,
)

from .command_class import OZWCommandClass
from .node_child_base import OZWNodeChildBase


class OZWNodeInstance(OZWNodeChildBase):

    EVENT_ADDED = EVENT_NODE_INSTANCE_ADDED
    EVENT_CHANGED = EVENT_NODE_INSTANCE_CHANGED
    EVENT_REMOVED = EVENT_NODE_INSTANCE_REMOVED

    @property
    def instance(self) -> int:
        """Return Instance."""
        return self.data.get("Instance")

    @property
    def time_stamp(self) -> int:
        """Return TimeStamp."""
        return self.data.get("TimeStamp")

    def create_collections(self):
        """Create collections that Node supports."""
        return {"commandclass": ItemCollection(self.options, self, OZWCommandClass)}
