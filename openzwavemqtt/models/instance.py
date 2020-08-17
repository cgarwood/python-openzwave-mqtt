"""Model for the OZW instance level."""
from typing import Dict, Optional, Type, Union

from .. import base
from ..const import (
    EVENT_INSTANCE_ADDED,
    EVENT_INSTANCE_CHANGED,
    EVENT_INSTANCE_EVENT,
    EVENT_INSTANCE_REMOVED,
)
from .instance_statistics import OZWInstanceStatistics
from .instance_status import OZWInstanceStatus
from .node import OZWNode


class OZWInstance(base.ZWaveBase):
    """Model for the OZW instance level."""

    DEFAULT_VALUE: Optional[dict] = None

    EVENT_ADDED = EVENT_INSTANCE_ADDED
    EVENT_CHANGED = EVENT_INSTANCE_CHANGED
    EVENT_REMOVED = EVENT_INSTANCE_REMOVED

    def create_collections(
        self,
    ) -> Dict[
        str,
        Union[
            base.ItemCollection,
            Type[base.ZWaveBase],
            base.DiscardMessages,
            base.EventMessages,
        ],
    ]:
        """Create collections that Node supports."""
        return {
            "node": base.ItemCollection(OZWNode),
            "status": OZWInstanceStatus,
            "statistics": OZWInstanceStatistics,
            "command": base.DiscardMessages(),
            "event": base.EventMessages(
                self.options, EVENT_INSTANCE_EVENT, lambda topic, data: topic[0]
            ),
        }

    def send_command(self, command: str, payload: Optional[dict] = None) -> None:
        """Send command to the OZW instance."""
        if payload is None:
            payload = {}
        topic_prefix = self.options.topic_prefix
        full_topic = f"{topic_prefix}{self.id}/command/{command}/"
        self.options.send_message(full_topic, payload)

    # Shortcut methods to some common used (global) controller commands
    # https://github.com/OpenZWave/qt-openzwave/blob/master/docs/MQTT.md#mqtt-commands

    def add_node(self, secure: bool = False) -> None:
        """Enter inclusion mode on the controller."""
        self.send_command("addnode", {"secure": secure})

    def remove_node(self) -> None:
        """Enter exclusion mode on the controller."""
        self.send_command("removenode")

    def refresh_node(self, node_id: int) -> None:
        """Force OZW to re-interview a device."""
        self.send_command("refreshnodeinfo", {"node": node_id})

    def remove_failed_node(self, node_id: int) -> None:
        """Remove a failed node from the controller."""
        self.send_command("removefailednode", {"node": node_id})

    def replace_failed_node(self, node_id: int) -> None:
        """Replace a failed node from the controller with a new device."""
        self.send_command("replacefailednode", {"node": node_id})

    def heal_node(self, node_id: int) -> None:
        """Ask a Node to recalculate its neighbors and routes to other devices."""
        self.send_command("healnetworknode", {"node": node_id})

    def cancel_controller_command(self) -> None:
        """Cancel in Controller Commands that are in progress."""
        self.send_command("cancelcontrollercommand")

    def check_node_failed(self, node_id: int) -> None:
        """Force OZW to test communication with a node."""
        self.send_command("hasnodefailed", {"node": node_id})

    def refresh_value(self, value_id: int) -> None:
        """Refresh a specific value."""
        self.send_command("refreshvalue", {"ValueIDKey": value_id})

    def refresh_values(self, node_id: int) -> None:
        """Refresh dynamic and static values for a node."""
        self.send_command("requestnodestate", {"node": node_id})

    def refresh_dynamic_values(self, node_id: int) -> None:
        """Refresh dynamic values for a node."""
        self.send_command("requestnodedynamic", {"node": node_id})
