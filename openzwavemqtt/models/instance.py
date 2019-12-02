"""Model for OZW Instance."""
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
    def manufacturer_specific_db_ready(self) -> bool:
        """Return ManufacturerSpecificDBReady."""
        return self.data.get("ManufacturerSpecificDBReady")

    @property
    def time_stamp(self) -> int:
        """Return TimeStamp."""
        return self.data.get("TimeStamp")


class OZWInstance(ZWaveBase):
    DEFAULT_VALUE = None

    EVENT_ADDED = EVENT_INSTANCE_ADDED
    EVENT_CHANGED = EVENT_INSTANCE_CHANGED
    EVENT_REMOVED = EVENT_INSTANCE_REMOVED

    def create_collections(self):
        """Create collections that Node supports."""
        return {
            "node": ItemCollection(OZWNode),
            "status": OZWInstanceStatus,
            "statistics": OZWInstanceStatistics,
        }

    def send_command(self, command: str, payload: str = ""):
        topic_prefix = self.options.topic_prefix
        full_topic = f"{topic_prefix}{self.id}/command/{command}/"
        self.options.send_command(full_topic, payload)

    def add_node(self, secure=False):
        self.send_command("addnode", {"secure": secure})

    def cancel_controller_command(self):
        self.send_command("cancelcontrollercommand")
