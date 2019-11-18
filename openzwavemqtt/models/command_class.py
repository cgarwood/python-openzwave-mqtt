from ..base import ZWaveBase, ItemCollection
from ..const import (
    EVENT_COMMAND_CLASS_ADDED,
    EVENT_COMMAND_CLASS_CHANGED,
    EVENT_COMMAND_CLASS_REMOVED,
)

from .value import OZWValue


class OZWCommandClass(ZWaveBase):

    EVENT_ADDED = EVENT_COMMAND_CLASS_ADDED
    EVENT_CHANGED = EVENT_COMMAND_CLASS_CHANGED
    EVENT_REMOVED = EVENT_COMMAND_CLASS_REMOVED

    def create_collections(self):
        """Create collections that Node supports."""
        return {"value": ItemCollection(self.options, self, OZWValue)}
