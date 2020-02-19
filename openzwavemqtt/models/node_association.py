"""Model for the Node Assocations level."""
from ..const import (EVENT_NODE_ASSOCIATION_ADDED,
                     EVENT_NODE_ASSOCIATION_CHANGED,
                     EVENT_NODE_ASSOCIATION_REMOVED)
from .node_child_base import OZWNodeChildBase


class OZWNodeAssocation(OZWNodeChildBase):
    """Model for Node Assocations."""

    EVENT_ADDED = EVENT_NODE_ASSOCIATION_ADDED
    EVENT_CHANGED = EVENT_NODE_ASSOCIATION_CHANGED
    EVENT_REMOVED = EVENT_NODE_ASSOCIATION_REMOVED

    @property
    def name(self) -> str:
        """Return Name."""
        return self.data.get("Name")

    @property
    def help(self) -> str:
        """Return Help."""
        return self.data.get("Help")

    @property
    def max_associations(self) -> int:
        """Return MaxAssociations."""
        return self.data.get("MaxAssociations")

    @property
    def members(self) -> list:
        """Return Members."""
        return self.data.get("Members")

    @property
    def time_stamp(self) -> int:
        """Return TimeStamp."""
        return self.data.get("TimeStamp")
