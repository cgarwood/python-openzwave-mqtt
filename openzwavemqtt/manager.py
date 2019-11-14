from collections import deque
import json

from .base import ZWaveBase, ItemCollection
from .const import EMPTY
from .options import OZWOptions
from .models.instance import OZWInstance


class OZWManager(ZWaveBase):

    EVENT_CHANGED = None

    def __init__(self, options: OZWOptions):
        super().__init__(options, None, None)

    def create_collections(self):
        """Create collections that the manager supports."""
        return {"instance": ItemCollection(self.options, self, OZWInstance)}

    def receive_message(self, topic: str, message: dict):
        """Receive an MQTT message."""
        assert topic.startswith(self.options.topic_prefix)
        topic_parts = deque(
            ["instance"] + topic[len(self.options.topic_prefix) :].split("/")
        )

        if message == "":
            payload = EMPTY
        else:
            payload = json.loads(message)

        self.process_message(topic_parts, payload)
