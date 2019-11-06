from openzwavemqtt.const import (
    EVENT_VALUE_ADDED,
    EVENT_VALUE_CHANGED,
    EVENT_VALUE_REMOVED,
)


def test_value_events(mgr):
    events = []

    # Listen for value added
    mgr.options.listen(EVENT_VALUE_ADDED, events.append)
    mgr.mock_receive_json("/openzwave/1/node/2/values/3/", {"value": "yo"})
    assert len(events) == 1
    assert events[0].id == "3"
    assert events[0].value == "yo"

    # Listen for value changed
    mgr.options.listen(EVENT_VALUE_CHANGED, events.append)
    mgr.mock_receive_json("/openzwave/1/node/2/values/3", {"value": "yo2"})
    assert len(events) == 2
    assert events[0].id == "3"
    assert events[0].value == "yo2"

    # Show how to use collection helpers
    assert mgr.get_instance("1").get_node("2").get_values("3").value == "yo2"

    # Listen for value removed
    mgr.options.listen(EVENT_VALUE_REMOVED, events.append)
    mgr.receive_message("/openzwave/1/node/2/values/3", "")
    assert len(events) == 3
    assert events[0].id == "3"
