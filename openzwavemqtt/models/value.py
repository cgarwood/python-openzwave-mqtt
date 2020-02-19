"""Model for the Value."""
from typing import cast

from ..const import (EVENT_VALUE_ADDED, EVENT_VALUE_CHANGED,
                     EVENT_VALUE_REMOVED, CommandClass, ValueGenre, ValueType)
from .node_child_base import OZWNodeChildBase


class OZWValue(OZWNodeChildBase):
    """Representation of an OpenZWave Value object."""

    EVENT_ADDED = EVENT_VALUE_ADDED
    EVENT_CHANGED = EVENT_VALUE_CHANGED
    EVENT_REMOVED = EVENT_VALUE_REMOVED

    @property
    def label(self) -> str:
        """Return Label."""
        return self.data.get("Label")

    @property
    def value(self) -> int:
        """Return Value."""
        return self.data.get("Value")

    @property
    def units(self) -> str:
        """Return Units."""
        return self.data.get("Units")

    @property
    def min(self) -> int:
        """Return Min."""
        return self.data.get("Min")

    @property
    def max(self) -> int:
        """Return Max."""
        return self.data.get("Max")

    @property
    def type(self) -> ValueType:
        """Return Type."""
        try:
            return ValueType(self.data.get("Type"))
        except ValueError:
            return ValueType.UNKNOWN

    @property
    def instance(self) -> int:
        """Return Instance."""
        return self.data.get("Instance")

    @property
    def command_class(self) -> CommandClass:
        """Return CommandClass this value belongs to."""
        return self.parent.command_class_id

    @property
    def index(self) -> int:
        """Return Index."""
        return self.data.get("Index")

    @property
    def genre(self) -> ValueGenre:
        """Return Genre."""
        try:
            return ValueGenre(self.data.get("Genre"))
        except ValueError:
            return ValueGenre.UNKNOWN

    @property
    def help(self) -> str:
        """Return Help."""
        return self.data.get("Help")

    @property
    def value_id_key(self) -> int:
        """Return ValueIDKey."""
        return self.data.get("ValueIDKey")

    @property
    def read_only(self) -> bool:
        """Return ReadOnly."""
        return self.data.get("ReadOnly")

    @property
    def write_only(self) -> bool:
        """Return WriteOnly."""
        return self.data.get("WriteOnly")

    @property
    def value_set(self) -> bool:
        """Return ValueSet."""
        return self.data.get("ValueSet")

    @property
    def value_polled(self) -> bool:
        """Return ValuePolled."""
        return self.data.get("ValuePolled")

    @property
    def change_verified(self) -> bool:
        """Return ChangeVerified."""
        return self.data.get("ChangeVerified")

    @property
    def event(self) -> str:
        """Return Event."""
        return self.data.get("Event")

    @property
    def time_stamp(self) -> int:
        """Return TimeStamp."""
        return self.data.get("TimeStamp")

    @property
    def ozw_instance(self):
        """Return OZWInstance this value belongs to."""
        from .instance import OZWInstance

        parent = self.parent
        while parent is not None and not isinstance(parent, OZWInstance):
            parent = parent.parent

        if isinstance(parent, OZWInstance):
            return cast(OZWInstance, parent)

    def send_value(self, new_value):
        """Send an updated value to MQTT."""
        instance_id = self.ozw_instance.id
        full_topic = f"{self.options.topic_prefix}{instance_id}/command/setvalue/"
        payload = {"ValueIDKey": self.value_id_key, "Value": new_value}
        self.options.send_message(full_topic, payload)
