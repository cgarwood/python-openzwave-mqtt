"""Root Manager object."""
import json
from collections import deque
from typing import TYPE_CHECKING, Dict, Optional, Type, Union

from .base import ItemCollection, ZWaveBase
from .const import EMPTY_PAYLOAD
from .models.instance import OZWInstance
from .options import OZWOptions

if TYPE_CHECKING:
    from .base import DiscardMessages, EventMessages  # noqa: F401


class OZWManager(ZWaveBase):
    """Manager that holds the OZW instances connected to MQTT."""

    DIRECT_COLLECTION = "instance"
    DEFAULT_VALUE: Optional[dict] = None
    EVENT_CHANGED = "manager_placeholder_event"

    def __init__(self, options: OZWOptions):
        """Initialize class."""
        super().__init__(options, None, options.topic_prefix, None)

    def create_collections(
        self,
    ) -> Dict[
        str,
        Union[ItemCollection, Type["ZWaveBase"], "DiscardMessages", "EventMessages"],
    ]:
        """Create collections that the manager supports."""
        return {"instance": ItemCollection(OZWInstance)}

    def receive_message(self, topic: str, message: str) -> None:
        """Receive an MQTT message."""
        assert topic.startswith(self.options.topic_prefix)

        topic_parts_raw = topic[len(self.options.topic_prefix) :].split("/")
        instance_id = self.options.instance_id

        if instance_id is not None and topic_parts_raw[0] != instance_id:
            return

        if topic_parts_raw[-1] == "":
            topic_parts_raw.pop()
        topic_parts = deque(topic_parts_raw)

        if message == "":
            payload = EMPTY_PAYLOAD
        else:
            payload = json.loads(message)

        self.process_message(topic_parts, payload)
