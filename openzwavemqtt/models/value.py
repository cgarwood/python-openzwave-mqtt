from ..base import ZWaveBase
from ..const import EVENT_VALUE_ADDED, EVENT_VALUE_CHANGED, EVENT_VALUE_REMOVED


class OZWValue(ZWaveBase):

    EVENT_ADDED = EVENT_VALUE_ADDED
    EVENT_CHANGED = EVENT_VALUE_CHANGED
    EVENT_REMOVED = EVENT_VALUE_REMOVED

    @property
    def value(self):
        return self.data.get("value")
