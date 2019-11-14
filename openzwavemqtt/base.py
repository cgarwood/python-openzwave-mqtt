from abc import ABC
from typing import Callable, Deque

from .const import EVENT_PLACEHOLDER, EMPTY, LOGGER
from .options import OZWOptions


class ItemCollection:
    def __init__(
        self, options: OZWOptions, item_class: Callable[[OZWOptions, str], "ZwaveBase"]
    ):
        self.options = options
        self.item_class = item_class
        self.collection = {}

        assert item_class.EVENT_ADDED != EVENT_PLACEHOLDER
        assert item_class.EVENT_REMOVED != EVENT_PLACEHOLDER

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
            self.options.notify(self.item_class.EVENT_ADDED, item)

    def remove_and_notify(self, item_id):
        """Remove item from collection and fire remove events for all child objects."""
        item = self.collection[item_id]

        for collection in item.collections.values():
            if not isinstance(collection, ItemCollection):
                continue

            for item in list(collection):
                collection.remove_and_notify(item.id)

        self.options.notify(self.item_class.EVENT_REMOVED, self.collection.pop(item_id))

    def __iter__(self):
        """Return iterator over all items in this collection."""
        return iter(self.collection.values())


class ZWaveBase(ABC):

    # Name the direct collection that lives underneath this object
    # but is not named in the topic. A message to /openzwave/1 will
    # be interpreted as if sent to /openzwave/<DIRECT_COLLECTION>/1
    DIRECT_COLLECTION = None

    EVENT_ADDED = EVENT_PLACEHOLDER
    EVENT_CHANGED = EVENT_PLACEHOLDER
    EVENT_REMOVED = EVENT_PLACEHOLDER

    def __init__(self, options: OZWOptions, item_id: str):
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
        if len(topic) == 0:
            should_notify = self.data is not EMPTY
            self.data = message
            if should_notify:
                self.options.notify(self.EVENT_CHANGED, self)
            return

        if topic[0] in self.collections:
            collection_type = topic.popleft()

        elif topic[0].isnumeric():
            collection_type = self.DIRECT_COLLECTION

        else:
            collection_type = None

        if collection_type is not None:
            self.collections[collection_type].process_message(topic, message)
            return

        self._warn_cannot_handle(topic, message)

    def _warn_cannot_handle(self, topic: Deque[str], message: dict):
        LOGGER.warning(
            "%s cannot process message %s: %s",
            type(self).__name__,
            "/".join(topic),
            message,
        )
