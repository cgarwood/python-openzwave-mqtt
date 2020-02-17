"""Python wrapper for OpenZWave's MQTT daemon - Root Manager object."""
import json
from collections import deque

from .base import ItemCollection, ZWaveBase
from .const import EMPTY_PAYLOAD
from .models.instance import OZWInstance
from .options import OZWOptions


class OZWManager(ZWaveBase):
    """Manager that holds the OZW instances connected to MQTT."""

    DIRECT_COLLECTION = "instance"
    DEFAULT_VALUE = None
    EVENT_CHANGED = None

    def __init__(self, options: OZWOptions):
        """Initialize class."""
        super().__init__(options, None, options.topic_prefix, None)

    def create_collections(self):
        """Create collections that the manager supports."""
        return {"instance": ItemCollection(OZWInstance)}

    def receive_message(self, topic: str, message: str):
        """Receive an MQTT message."""
        assert topic.startswith(self.options.topic_prefix)

        topic_parts_raw = topic[len(self.options.topic_prefix) :].split("/")
        if topic_parts_raw[-1] == "":
            topic_parts_raw.pop()
        topic_parts = deque(topic_parts_raw)

        if message == "":
            payload = EMPTY_PAYLOAD
        else:
            payload = json.loads(message)

        self.process_message(topic_parts, payload)
