from ..base import ZWaveBase, ItemCollection
from ..const import (
    EVENT_INSTANCE_STATUS_CHANGED,
    EVENT_INSTANCE_ADDED,
    EVENT_INSTANCE_CHANGED,
    EVENT_INSTANCE_REMOVED,
)

from .node import OZWNode
from .instance_statistics import OZWInstanceStatistics


class OZWInstanceStatus(ZWaveBase):

    EVENT_CHANGED = EVENT_INSTANCE_STATUS_CHANGED

    @property
    def status(self):
        return self.data.get("Status")

    @property
    def home_id(self):
        return self.data.get("homeID")

    @property
    def manufacturer_db_ready(self):
        return self.data.get("ManufacturerSpecificDBReady")


class OZWInstance(ZWaveBase):
    DEFAULT_VALUE = None

    EVENT_ADDED = EVENT_INSTANCE_ADDED
    EVENT_CHANGED = EVENT_INSTANCE_CHANGED
    EVENT_REMOVED = EVENT_INSTANCE_REMOVED

    def create_collections(self):
        """Create collections that Node supports."""
        return {
            "node": ItemCollection(self.options, self, OZWNode),
            "status": OZWInstanceStatus(self.options, self, None),
            "statistics": OZWInstanceStatistics(self.options, self, None),
        }
