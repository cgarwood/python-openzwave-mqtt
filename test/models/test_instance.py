"""Tests for instance model."""
from openzwavemqtt.const import EVENT_INSTANCE_EVENT


def test_events(mgr):
    """Test firing events."""
    events = []
    mgr.options.listen(EVENT_INSTANCE_EVENT, events.append)

    mgr.mock_receive_json("OpenZWave/1", {})
    mgr.mock_receive_json(
        "OpenZWave/1/event/test-instance-event", {"data": "for-event"}
    )

    assert len(events) == 1
    assert events[0] == {"event": "test-instance-event", "data": {"data": "for-event"}}
