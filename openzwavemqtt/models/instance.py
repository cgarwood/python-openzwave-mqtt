from ..base import ZWaveBase, ItemCollection
from ..const import (
    EVENT_INSTANCE_STATISTICS_CHANGED,
    EVENT_INSTANCE_STATUS_CHANGED,
    EVENT_INSTANCE_ADDED,
    EVENT_INSTANCE_CHANGED,
    EVENT_INSTANCE_REMOVED,
)

from .node import OZWNode


class OZWInstanceStatistics(ZWaveBase):

    EVENT_CHANGED = EVENT_INSTANCE_STATISTICS_CHANGED

    @property
    def some_stat(self):
        return self.data.get("some_stat")


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

    EVENT_ADDED = EVENT_INSTANCE_ADDED
    EVENT_CHANGED = EVENT_INSTANCE_CHANGED
    EVENT_REMOVED = EVENT_INSTANCE_REMOVED

    def create_collections(self):
        """Create collections that Node supports."""
        return {
            "node": ItemCollection(self.options, OZWNode),
            "statistics": OZWInstanceStatistics(self.options, None),
            "status": OZWInstanceStatus(self.options, None),
        }
