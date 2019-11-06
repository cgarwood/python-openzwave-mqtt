"""Python listener implementation of the OpenZWave MQTT Server."""

from abc import ABC
from collections import deque
from typing import Callable, Dict, Deque
import json
import logging

import attr

from .const import (
    EVENT_PLACEHOLDER,
    EVENT_INSTANCE_ADDED,
    EVENT_INSTANCE_CHANGED,
    EVENT_INSTANCE_REMOVED,
    EVENT_INSTANCE_STATISTICS_CHANGED,
    EVENT_INSTANCE_STATUS_CHANGED,
    EVENT_NODE_ADDED,
    EVENT_NODE_CHANGED,
    EVENT_NODE_REMOVED,
    EVENT_VALUE_ADDED,
    EVENT_VALUE_CHANGED,
    EVENT_VALUE_REMOVED,
)

EMPTY = {}

_LOGGER = logging.getLogger(__name__)


@attr.s
class ZWaveOptions:

    sent_message: Callable[[str, dict], None] = attr.ib()
    topic_prefix: str = attr.ib(default="/openzwave/")
    listeners: Dict[str, Callable] = attr.ib(factory=dict)

    def listen(self, event, listener):
        self.listeners.setdefault(event, []).append(listener)

    def notify(self, event, data):
        for listener in self.listeners.get(event, []):
            listener(data)


class ItemCollection:
    def __init__(
        self,
        options: ZWaveOptions,
        item_class: Callable[[ZWaveOptions, str], "ZwaveBase"],
        event_added: str,
        event_removed: str,
    ):
        self.options = options
        self.item_class = item_class
        self.event_added = event_added
        self.event_removed = event_removed
        self.collection = {}

    def get(self, item_id: str):
        """Return item in collection."""
        return self.collection.get(item_id)

    def process_message(self, topic: Deque[str], message: dict):
        """Process a new message."""
        item_id = topic.popleft()
        item = self.collection.get(item_id)
        added = False

        if item is None and message is EMPTY:
            return

        elif item is None:
            item = self.collection[item_id] = self.item_class(self.options, item_id)
            added = True

        if len(topic) == 0 and message is EMPTY:
            self.remove_and_notify(item_id)
            return

        item.process_message(topic, message)

        # Only notify after we process the message.
        if added:
            self.options.notify(self.event_added, item)

    def remove_and_notify(self, item_id):
        """Remove item from collection and fire remove events for all child objects."""
        item = self.collection.pop(item_id)
        self.options.notify(self.event_removed, item)

        for collection in item.collections.values():
            if not isinstance(collection, ItemCollection):
                continue

            for item in list(collection):
                collection.remove_and_notify(item.id)

    def __iter__(self):
        """Return iterator over all items in this collection."""
        return iter(self.collection.values())


class ZWaveBase(ABC):

    EVENT_CHANGED = EVENT_PLACEHOLDER

    def __init__(self, options: ZWaveOptions, item_id: str):
        self.options = options
        self.id = item_id
        self.collections = self.create_collections()
        self.data = EMPTY
        assert self.EVENT_CHANGED != EVENT_PLACEHOLDER

        # Create helpers
        for item_type, collection in self.collections.items():
            setattr(self, f"get_{item_type}", collection.get)

    def get(self):
        """Get helper to work with collection helpers."""
        return self

    def create_collections(self):
        """Create collections that this type supports.
        Each collection is either an instance of ZWaveBase or ItemCollection.
        """
        return {}

    def process_message(self, topic: Deque[str], message: dict):
        """Process a new message."""
        if len(topic) > 0 and topic[-1] == "":
            topic.pop()

        if len(topic) == 0:
            should_notify = self.data is not EMPTY
            self.data = message
            if should_notify:
                self.options.notify(self.EVENT_CHANGED, self)

        elif topic[0] in self.collections:
            collection_type = topic.popleft()
            self.collections[collection_type].process_message(topic, message)
        else:
            self._warn_cannot_handle(topic, message)

    def _warn_cannot_handle(self, topic: Deque[str], message: dict):
        _LOGGER.warning(
            "%s cannot process message %s: %s",
            type(self).__name__,
            "/".join(topic),
            message,
        )


class OZWValue(ZWaveBase):

    EVENT_CHANGED = EVENT_VALUE_CHANGED

    @property
    def value(self):
        return self.data.get("value")


class OZWNode(ZWaveBase):

    EVENT_CHANGED = EVENT_NODE_CHANGED

    def create_collections(self):
        """Create collections that Node supports."""
        return {
            "values": ItemCollection(
                self.options, OZWValue, EVENT_VALUE_ADDED, EVENT_VALUE_REMOVED
            )
        }


class OZWInstanceStatistics(ZWaveBase):

    EVENT_CHANGED = EVENT_INSTANCE_STATISTICS_CHANGED

    @property
    def some_stat(self):
        return self.data.get("some_stat")


class OZWInstanceStatus(ZWaveBase):

    EVENT_CHANGED = EVENT_INSTANCE_STATUS_CHANGED

    @property
    def status(self):
        return self.data.get("Status")

    @property
    def home_id(self):
        return self.data.get("homeID")

    @property
    def manufacturer_db_ready(self):
        return self.data.get("ManufacturerSpecificDBReady")


class OZWInstance(ZWaveBase):

    EVENT_CHANGED = EVENT_INSTANCE_CHANGED

    def create_collections(self):
        """Create collections that Node supports."""
        return {
            "node": ItemCollection(
                self.options, OZWNode, EVENT_NODE_ADDED, EVENT_NODE_REMOVED
            ),
            "statistics": OZWInstanceStatistics(self.options, None),
            "status": OZWInstanceStatus(self.options, None),
        }


class ZWaveManager(ZWaveBase):

    EVENT_CHANGED = None

    def __init__(self, options: ZWaveOptions):
        super().__init__(options, None)

    def create_collections(self):
        """Create collections that Node supports."""
        return {
            "instance": ItemCollection(
                self.options, OZWInstance, EVENT_INSTANCE_ADDED, EVENT_INSTANCE_REMOVED
            )
        }

    def receive_message(self, topic: str, message: dict):
        """Receive a message.
        We split the topic based on the parts that matter for
        """
        assert topic.startswith(self.options.topic_prefix)
        topic_parts = deque(
            ["instance"] + topic[len(self.options.topic_prefix) :].split("/")
        )
        self.process_message(topic_parts, json.loads(message))


if __name__ == "__main__":
    options = ZWaveOptions(None)
    manager = ZWaveManager(options)

    # Statistics
    manager.receive_message("/openzwave/1/statistics/", {"some_stat": "some-stat-data"})
    print("Stat via helper", manager.get_instance("1").get_statistics().some_stat)

    # Listen for value added
    options.listen(
        EVENT_VALUE_ADDED, lambda value: print("Value added", value.id, value.value)
    )
    manager.receive_message("/openzwave/1/node/2/value/3/", {"value": "yo"})

    # Listen for value changed
    options.listen(
        EVENT_VALUE_CHANGED, lambda value: print("Value updated", value.id, value.value)
    )
    manager.receive_message("/openzwave/1/node/2/value/3", {"value": "yo2"})

    # Show how to use collection helpers
    print(
        "Get value with helpers",
        manager.get_instance("1").get_node("2").get_value("3").value,
    )

    # Listen for value removed
    options.listen(EVENT_VALUE_REMOVED, lambda value: print("Value removed", value.id))
    manager.receive_message("/openzwave/1/node/2/value/3", EMPTY)

    # Removing instance should also notify that Node is removed
    options.listen(EVENT_NODE_REMOVED, lambda value: print("Node removed", value.id))
    manager.receive_message("/openzwave/1", EMPTY)
