from typing import cast, TYPE_CHECKING

from ..base import ZWaveBase
from ..const import EVENT_VALUE_ADDED, EVENT_VALUE_CHANGED, EVENT_VALUE_REMOVED

if TYPE_CHECKING:
    from .node import OZWNode


class OZWValue(ZWaveBase):

    EVENT_ADDED = EVENT_VALUE_ADDED
    EVENT_CHANGED = EVENT_VALUE_CHANGED
    EVENT_REMOVED = EVENT_VALUE_REMOVED

    @property
    def value(self):
        """Return value."""
        return self.data.get("Value")

    @property
    def change_verified(self):
        """Return ChangeVerified."""
        return self.data.get("ChangeVerified")

    @property
    def command_class(self):
        """Return CommandClass."""
        return self.data.get("CommandClass")

    @property
    def event(self):
        """Return Event."""
        return self.data.get("Event")

    @property
    def genre(self):
        """Return Genre."""
        return self.data.get("Genre")

    @property
    def help(self):
        """Return Help."""
        return self.data.get("Help")

    @property
    def index(self):
        """Return Index."""
        return self.data.get("Index")

    @property
    def instance(self):
        """Return Instance."""
        return self.data.get("Instance")

    @property
    def label(self):
        """Return Label."""
        return self.data.get("Label")

    @property
    def max(self):
        """Return Max."""
        return self.data.get("Max")

    @property
    def min(self):
        """Return Min."""
        return self.data.get("Min")

    @property
    def node_id(self):
        """Return Node."""
        return self.data.get("Node")

    @property
    def read_only(self):
        """Return ReadOnly."""
        return self.data.get("ReadOnly")

    @property
    def type(self):
        """Return Type."""
        return self.data.get("Type")

    @property
    def units(self):
        """Return Units."""
        return self.data.get("Units")

    @property
    def value_id_key(self):
        """Return ValueIDKey."""
        return self.data.get("ValueIDKey")

    @property
    def value_polled(self):
        """Return ValuePolled."""
        return self.data.get("ValuePolled")

    @property
    def value_set(self):
        """Return ValueSet."""
        return self.data.get("ValueSet")

    @property
    def write_only(self):
        """Return WriteOnly."""
        return self.data.get("WriteOnly")

    @property
    def node(self) -> "OZWNode":
        """Return Node."""
        from .node import OZWNode

        return cast(OZWNode, self.parent)

    @property
    def time_stamp(self) -> int:
        """Return TimeStamp."""
        return self.data.get("TimeStamp")
