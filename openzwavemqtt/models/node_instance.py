"""Model for the Node instance level."""
from ..base import ItemCollection
from ..const import (
    EVENT_NODE_INSTANCE_ADDED,
    EVENT_NODE_INSTANCE_CHANGED,
    EVENT_NODE_INSTANCE_REMOVED,
    CommandClass,
    ValueIndex,
)
from .command_class import OZWCommandClass
from .node_child_base import OZWNodeChildBase


class OZWNodeInstance(OZWNodeChildBase):
    """Model for Node Instance."""

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
        return {"commandclass": ItemCollection(OZWCommandClass)}

    def get_command_class(self, command_class_id: CommandClass) -> bool:
        """Helper method to get a specific CommandClass on this NodeInstance."""
        # pylint: disable=no-member
        for command_class in self.commandclasses():
            if command_class.command_class_id == command_class_id:
                return command_class
        return None

    def has_command_class(self, command_class_id: CommandClass) -> bool:
        """Helper method to determine if the node has the given CommandClass."""
        return self.get_command_class(command_class_id) is not None

    def get_value(
        self, command_class_id: CommandClass, value_index: ValueIndex
    ) -> bool:
        """Helper method to get a specific OZWValue on this node."""
        command_class = self.get_command_class(command_class_id)
        return command_class.get_value(value_index) if command_class else None

    def has_value(
        self, command_class_id: CommandClass, value_index: ValueIndex
    ) -> bool:
        """Helper method to determine if this NodeInstance has the given OZWValue."""
        return self.get_value(command_class_id, value_index) is not None
