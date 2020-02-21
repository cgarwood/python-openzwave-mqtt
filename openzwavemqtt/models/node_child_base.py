"""Base class with Node specific helpers."""

from typing import cast

from ..base import ZWaveBase


class OZWNodeChildBase(ZWaveBase):
    """Base class for objects that are descendants of a Node object."""

    @property
    def node(self):
        """Return the node that this child belongs to."""
        from .node import OZWNode

        parent = self.parent

        while parent is not None and not isinstance(parent, OZWNode):
            parent = parent.parent

        if isinstance(parent, OZWNode):
            return cast(OZWNode, parent)

        raise RuntimeError("Object is not a descendant of a Node")

    def __repr__(self):
        """Return a representation of this object."""
        iden = f" {self.id}" if self.id else ""

        try:
            node = self.node.id
        except RuntimeError:
            node = "<missing> (bad!)"

        return f"<{type(self).__name__}{iden} (node: {node})>"
