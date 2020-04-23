"""Provide tests for the model base."""
from collections import deque
from unittest.mock import patch

import pytest

from openzwavemqtt import base


class Level3(base.ZWaveBase):
    """Represent a level 3 descendant."""

    EVENT_ADDED = "level3_added"
    EVENT_CHANGED = "level3_change"
    EVENT_REMOVED = "level3_removed"

    @property
    def hello(self):
        """Return hello data."""
        return self.data.get("hello")


class Level2(base.ZWaveBase):
    """Represent a level 2 descendant."""

    DIRECT_COLLECTION = "level3"
    EVENT_ADDED = "level2_added"
    EVENT_CHANGED = "level2_change"
    EVENT_REMOVED = "level2_removed"

    PLURAL_NAME = "level_twos"

    def create_collections(self):
        """Create collections."""
        return {"level3": base.ItemCollection(Level3)}


class Level1(base.ZWaveBase):
    """Represent a level 1 descendant."""

    DIRECT_COLLECTION = "level2"
    EVENT_ADDED = "level1_added"
    EVENT_CHANGED = "level1_change"
    EVENT_REMOVED = "level1_removed"

    def create_collections(self):
        """Create collections."""
        return {"level2": base.ItemCollection(Level2)}


@pytest.fixture(name="level1")
def level1_fixture(options):
    """Return a level 1 descendant."""
    return Level1(options, None, None, None)


def test_direct_collection(level1, caplog):
    """Test direct collection."""
    level1.process_message(deque(), {"info": 1})
    level1.process_message(deque(["2"]), {"info": 1})
    level1.process_message(deque(["2", "3"]), {"hello": 1})
    assert level1.get_level2(2).get_level3(3).hello == 1

    # Only works on numbers
    level1.process_message(deque(["2", "a"]), {"hello": 1})
    assert level1.get_level2(2).get_level3("a") is None
    assert "cannot process message" in caplog.text


def test_pending_messages(level1, options):
    """Test pending messages."""
    events = []
    options.notify = lambda event, data: events.append(event)

    # Only message for level3 has been received, level2 is none
    level1.process_message(deque(["2", "3"]), {"hello": 1})
    assert level1.get_level2(2) is None
    assert events == []

    # Message for level2, level3 received, level1 still None
    level1.process_message(deque(["2"]), {"hello": 1})
    assert level1.get_level2(2) is None
    assert events == []

    # Level 1 receives data, process all child messages.
    level1.process_message(deque(), {"info": 1})
    assert level1.get_level2(2).get_level3(3).hello == 1
    assert events == ["level2_added", "level3_added"]


def test_recursive_remove(level1, options):
    """Test recursive remove."""
    events = []

    level1.process_message(deque(), {"info": 1})
    level1.process_message(deque(["2"]), {"info": 1})
    level1.process_message(deque(["2", "3"]), {"hello": 1})

    options.notify = lambda event, data: events.append(event)
    level1.process_message(deque(["2"]), base.EMPTY_PAYLOAD)

    assert events == ["level3_removed", "level2_removed"]


def test_topic(options):
    """Test topic property."""

    class Level4(base.ZWaveBase):
        """Represent a level 4 descendant."""

        EVENT_ADDED = "level4_added"
        EVENT_CHANGED = "level4_change"
        EVENT_REMOVED = "level4_removed"

    class Level3Statistics(base.ZWaveBase):
        """Represent level 3 statistics."""

        EVENT_CHANGED = "level3statistics_change"

    # Patch in a non-direct collection
    with patch.object(
        Level3,
        "create_collections",
        lambda _: {
            "level4": base.ItemCollection(Level4),
            "statistics": Level3Statistics,
        },
    ):
        level1 = Level1(options, None, None, None)
        level1.process_message(deque(), {"info": 1})
        level1.process_message(deque(["2"]), {"info": 1})
        level1.process_message(deque(["2", "3"]), {"hello": 1})
        level1.process_message(deque(["2", "3", "level4", "4"]), {"hello": 1})
        level1.process_message(deque(["2", "3", "statistics"]), {"hello": 1})

    assert (
        level1.get_level2(2)  # pylint: disable=no-member
        .get_level3(3)
        .get_level4(4)
        .topic
        == "OpenZWave/2/3/level4/4"
    )
    assert (
        level1.get_level2(2)  # pylint: disable=no-member
        .get_level3(3)
        .get_statistics()
        .topic
        == "OpenZWave/2/3/statistics"
    )


def test_automatic_collections(level1):
    """Test automatic collections."""
    level1.process_message(deque(), {"info": 1})
    level1.process_message(deque(["2"]), {"info": 1})
    level1.process_message(deque(["2", "3"]), {"hello": 1})

    # Test overridden using PLURAL_NAME
    assert list(level1.level_twos()) == [level1.get_level2(2)]

    # Test default name
    assert list(level1.get_level2(2).level3s()) == [level1.get_level2(2).get_level3(3)]


def test_warn_unhandled(level1, caplog):
    """Test warn unhandled."""
    level1.process_message(deque(), {"info": 1})
    level1.process_message(deque(["2"]), {"info": 1})
    level1.process_message(deque(["2", "something"]), {"info": 1})

    assert (
        "Level2 cannot process message OpenZWave/2/something: {'info': 1}"
        in caplog.text
    )


def test_discarder(level1, options, caplog):
    """Test we can discard messages."""
    with patch.object(
        Level1, "create_collections", lambda _: {"command": base.DiscardMessages()}
    ):
        level1 = Level1(options, None, None, None)
        level1.process_message(deque(), {"info": 1})
        level1.process_message(deque(["command"]), {"info": 1})

    assert "cannot process message" not in caplog.text


def test_events(level1, options):
    """Test we can fire events messages."""
    events = []
    options.notify = lambda event, data: events.append((event, data))

    with patch.object(
        Level1,
        "create_collections",
        lambda _: {
            "event": base.EventMessages(
                options, "super_event", lambda topic, msg: topic[0]
            )
        },
    ):
        level1 = Level1(options, None, None, None)
        level1.process_message(deque(), {"info": 1})
        level1.process_message(
            deque(["event", "test-event-type"]), {"data": "for-event"}
        )

    assert len(events) == 1
    event, data = events[0]
    assert event == "super_event"
    assert data == {"event": "test-event-type", "data": {"data": "for-event"}}


def test_repr():
    """Test repr function."""

    class TestNode(base.ZWaveBase):
        """Represent a test node."""

        EVENT_CHANGED = "bla"

    inst = TestNode(None, None, "mock-topic-part", "mock-id")
    assert str(inst) == "<TestNode mock-id>"
