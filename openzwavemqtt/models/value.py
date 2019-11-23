from ..base import ZWaveBase
from ..const import EVENT_VALUE_ADDED, EVENT_VALUE_CHANGED, EVENT_VALUE_REMOVED


class OZWValue(ZWaveBase):

    EVENT_ADDED = EVENT_VALUE_ADDED
    EVENT_CHANGED = EVENT_VALUE_CHANGED
    EVENT_REMOVED = EVENT_VALUE_REMOVED

    @property
    def value(self):
        return self.data.get("Value")

    @property
    def change_verified(self):
        return self.data.get("ChangeVerified")

    @property
    def command_class(self):
        return self.data.get("CommandClass")

    @property
    def event(self):
        return self.data.get("Event")

    @property
    def genre(self):
        return self.data.get("Genre")

    @property
    def help(self):
        return self.data.get("Help")

    @property
    def index(self):
        return self.data.get("Index")

    @property
    def instance(self):
        return self.data.get("Instance")

    @property
    def label(self):
        return self.data.get("Label")

    @property
    def max(self):
        return self.data.get("Max")

    @property
    def min(self):
        return self.data.get("Min")

    @property
    def node_id(self):
        return self.data.get("Node")

    @property
    def read_only(self):
        return self.data.get("ReadOnly")

    @property
    def type(self):
        return self.data.get("Type")

    @property
    def units(self):
        return self.data.get("Units")

    @property
    def value_id(self):
        return self.data.get("ValueIDKey")

    @property
    def value_polled(self):
        return self.data.get("ValuePolled")

    @property
    def value_set(self):
        return self.data.get("ValueSet")

    @property
    def write_only(self):
        return self.data.get("WriteOnly")
