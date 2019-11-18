from ..base import ZWaveBase, ItemCollection
from ..const import (
    EVENT_NODE_INSTANCE_ADDED,
    EVENT_NODE_INSTANCE_CHANGED,
    EVENT_NODE_INSTANCE_REMOVED,
)

from .command_class import OZWCommandClass


class OZWNodeInstance(ZWaveBase):

    EVENT_ADDED = EVENT_NODE_INSTANCE_ADDED
    EVENT_CHANGED = EVENT_NODE_INSTANCE_CHANGED
    EVENT_REMOVED = EVENT_NODE_INSTANCE_REMOVED

    def create_collections(self):
        """Create collections that Node supports."""
        return {"commandclass": ItemCollection(self.options, self, OZWCommandClass)}
