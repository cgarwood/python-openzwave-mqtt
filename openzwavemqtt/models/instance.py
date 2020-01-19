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
        """Send command to the OZW instance"""
        topic_prefix = self.options.topic_prefix
        full_topic = f"{topic_prefix}{self.id}/command/{command}/"
        self.options.send_message(full_topic, payload)

    # Shortcut methods to some common used (global) controller commands
    # https://github.com/OpenZWave/qt-openzwave/blob/master/docs/MQTT.md#mqtt-commands

    def add_node(self, secure: bool = False):
        """Enter inclusion mode on the controller."""
        self.send_command("addnode", {"secure": secure})

    def remove_node(self):
        """Enter exclusion mode on the controller."""
        self.send_command("removenode")

    def refresh_node(self, node_id: int):
        """Force OZW to re-interview a device."""
        self.send_command("refreshnodeinfo", {"node": node_id})

    def remove_failed_node(self, node_id: int):
        """Remove a failed node from the controller."""
        self.send_command("removefailednode", {"node": node_id})

    def replace_failed_node(self, node_id: int):
        """Replace a failed node from the controller with a new device."""
        self.send_command("replacefailednode", {"node": node_id})

    def heal_node(self, node_id: int):
        """Asks a Node to recalculate its neighbors and routes to other devices.​"""
        self.send_command("healnetworknode", {"node": node_id})

    def cancel_controller_command(self):
        """Cancels in Controller Commands that are in progress."""
        self.send_command("cancelcontrollercommand")
