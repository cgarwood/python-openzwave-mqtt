from abc import ABC
from typing import Dict, Deque, Optional, Union, Type, Callable

from .const import EVENT_PLACEHOLDER, EMPTY, LOGGER
from .options import OZWOptions


class ItemCollection:
    """Initialize an item collection."""

    def __init__(
        self, item_class: Type["ZWaveBase"],
    ):
        self.parent: Optional["ZWaveBase"] = None
        self.topic_part: Optional[str] = None
        self.item_class = item_class
        self.collection: Dict[str, "ZWaveBase"] = {}

        assert item_class.EVENT_ADDED != EVENT_PLACEHOLDER
        assert item_class.EVENT_REMOVED != EVENT_PLACEHOLDER

    def adopt(self, parent: "ZWaveBase", topic_part: Optional[str]):
        """Adopt the item collection."""
        assert self.parent is None
        self.parent = parent
        self.topic_part = topic_part

    def get(self, item_id: str):
        """Return item in collection."""
        return self.collection.get(item_id)

    def process_message(self, topic: Deque[str], message: dict):
        """Process a new message."""
        item_id = int(topic.popleft())
        item = self.collection.get(item_id)
        added = False

        if item is None and message is EMPTY:
            return

        if item is None:
            topic_part = item_id

            if self.topic_part is not None:
                topic_part = f"{self.topic_part}/{topic_part}"

            item = self.collection[item_id] = self.item_class(
                self.parent.options, self.parent, topic_part, item_id
            )
            added = True

        if len(topic) == 0 and message is EMPTY:
            self.remove_and_notify(item_id)
            return

        item.process_message(topic, message)

        # Only notify after we process the message.
        if added:
            self.parent.options.notify(self.item_class.EVENT_ADDED, item)

    def remove_and_notify(self, item_id):
        """Remove item from collection and fire remove events for all child objects."""
        item = self.collection[item_id]

        for collection in item.collections.values():
            if not isinstance(collection, ItemCollection):
                continue

            for item in list(collection):
                collection.remove_and_notify(item.id)

        self.parent.options.notify(
            self.item_class.EVENT_REMOVED, self.collection.pop(item_id)
        )

    def __iter__(self):
        """Return iterator over all items in this collection."""
        return iter(self.collection.values())


class ZWaveBase(ABC):
    """A base class for all models."""

    # Name the direct collection that lives underneath this object
    # but is not named in the topic. A message to /openzwave/1 will
    # be interpreted as if sent to /openzwave/<DIRECT_COLLECTION>/1
    DIRECT_COLLECTION = None

    # Default value of this object. If untouched, all messages for child objects
    # will be held until information for this object has been received.
    DEFAULT_VALUE = EMPTY

    # Use in case there is a special plural name of this class.
    PLURAL_NAME = None

    EVENT_ADDED = EVENT_PLACEHOLDER
    EVENT_CHANGED = EVENT_PLACEHOLDER
    EVENT_REMOVED = EVENT_PLACEHOLDER

    def __init__(
        self,
        options: OZWOptions,
        parent: Optional["ZWaveBase"],
        topic_part: str,
        item_id: Optional[int],
    ):
        """Initialize the model."""
        # Runtime options
        self.options = options

        # Parent object
        self.parent = parent

        # Part of the topic that instantiated this object.
        self.topic_part = topic_part

        # Identifier of this object
        self.id = item_id

        # Models that live under this model
        self.collections: Dict[str, Union[ItemCollection, "ZWaveBase"]] = {}

        # The data this object olds
        self.data = self.DEFAULT_VALUE

        # Messages for children that are held until data is received
        self.pending_messages: Optional[list] = None

        assert self.EVENT_CHANGED != EVENT_PLACEHOLDER

        # Process collections
        for item_type, collection in self.create_collections().items():
            if isinstance(collection, type):  # OZWBase
                self.collections[item_type] = collection(
                    self.options, self, item_type, None
                )
                setattr(
                    self, f"get_{item_type}", create_getter(self.collections[item_type])
                )
                continue

            if not isinstance(collection, ItemCollection):
                self.collections[item_type] = collection
                continue

            setattr(self, f"get_{item_type}", collection.get)

            plural_name = collection.item_class.PLURAL_NAME or f"{item_type}s"
            if hasattr(self, plural_name):
                raise RuntimeError(
                    f"Cannot add {plural_name} function to {type(self).__name__}. Already exists."
                )
            setattr(self, plural_name, collection.collection.values)

            if item_type == self.DIRECT_COLLECTION:
                coll_topic_part: Optional[str] = None
            else:
                coll_topic_part = item_type

            collection.adopt(self, coll_topic_part)
            self.collections[item_type] = collection

    @property
    def topic(self):
        """Return topic of this object."""
        if self.parent is None:
            # Cut off the trailing slash
            return self.options.topic_prefix[:-1]

        return f"{self.parent.topic}/{self.topic_part}"

    @staticmethod
    def create_collections() -> Dict[
        str, Union[ItemCollection, Type["ZWaveBase"]],
    ]:
        """Create collections that this type supports.

        Each collection is either ItemCollection or a class derived from ZWaveBase.
        """
        return {}

    def process_message(self, topic: Deque[str], message: dict):
        """Process a new message."""
        if len(topic) == 0:
            is_init_msg = self.data is EMPTY
            self.data = message

            if not is_init_msg:
                self.options.notify(self.EVENT_CHANGED, self)
                return

            # Process all messages for the children.
            if self.pending_messages is not None:
                for pend_topic, pend_message in self.pending_messages:
                    self.process_message(pend_topic, pend_message)
                self.pending_messages = None

            return

        # If this object has not been initialized, queue up messages.
        if self.data is EMPTY:
            if self.pending_messages is None:
                self.pending_messages = []
            self.pending_messages.append((topic, message))
            return

        if topic[0] in self.collections:
            collection_type = topic.popleft()

        elif self.DIRECT_COLLECTION and topic[0].isnumeric():
            collection_type = self.DIRECT_COLLECTION

        else:
            self._warn_cannot_handle(topic, message)
            return

        self.collections[collection_type].process_message(topic, message)

    def _warn_cannot_handle(self, topic: Deque[str], message: dict):
        LOGGER.warning(
            "%s cannot process message %s: %s",
            type(self).__name__,
            f"{self.topic}/{'/'.join(topic)}",
            message,
        )


class DiscardMessages:
    """Class that discards all messages sent to it."""

    def process_message(self, topic: Deque[str], message: dict):
        """Process incoming message."""
        pass


class EventMessages:
    """Class that converts messages to events."""

    def __init__(
        self,
        options: OZWOptions,
        event: str,
        type_extractor: Callable[[Deque[str], dict], str],
    ):
        """Initialize EventMessages."""
        self.options = options
        self.event = event
        self.type_extractor = type_extractor

    def process_message(self, topic: Deque[str], message: dict):
        """Process incoming message."""
        event_type = self.type_extractor(topic, message)
        self.options.notify(self.event, {"event": event_type, "data": message})


def create_getter(obj):
    """Return a function that returns an object.

    Workaround for not being able to create lambdas that refer to variables in the
    current iteration of the loop.
    """
    return lambda: obj
