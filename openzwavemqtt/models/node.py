from ..base import ZWaveBase, ItemCollection
from ..const import EVENT_NODE_ADDED, EVENT_NODE_CHANGED, EVENT_NODE_REMOVED

from .value import OZWValue
from .node_statistics import OZWNodeStatistics


class OZWNode(ZWaveBase):

    EVENT_ADDED = EVENT_NODE_ADDED
    EVENT_CHANGED = EVENT_NODE_CHANGED
    EVENT_REMOVED = EVENT_NODE_REMOVED

    def create_collections(self):
        """Create collections that Node supports."""
        return {
            "value": ItemCollection(self.options, OZWValue),
            "statistics": OZWNodeStatistics(self.options, OZWNodeStatistics),
        }
