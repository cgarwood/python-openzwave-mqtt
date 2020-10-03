"""Model for the Node Assocations level."""
from typing import Optional

from ..const import (
    EVENT_NODE_ASSOCIATION_ADDED,
    EVENT_NODE_ASSOCIATION_CHANGED,
    EVENT_NODE_ASSOCIATION_REMOVED,
)
from .node_child_base import OZWNodeChildBase


class OZWNodeAssocation(OZWNodeChildBase):
    """Model for Node Assocations."""

    EVENT_ADDED = EVENT_NODE_ASSOCIATION_ADDED
    EVENT_CHANGED = EVENT_NODE_ASSOCIATION_CHANGED
    EVENT_REMOVED = EVENT_NODE_ASSOCIATION_REMOVED

    @property
    def name(self) -> Optional[str]:
        """Return Name."""
        return self.data.get("Name")

    @property
    def help(self) -> Optional[str]:
        """Return Help."""
        return self.data.get("Help")

    @property
    def max_associations(self) -> Optional[int]:
        """Return MaxAssociations."""
        return self.data.get("MaxAssociations")

    @property
    def members(self) -> Optional[list]:
        """Return Members."""
        return self.data.get("Members")

    @property
    def time_stamp(self) -> Optional[int]:
        """Return TimeStamp."""
        return self.data.get("TimeStamp")
