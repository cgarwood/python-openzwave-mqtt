from openzwavemqtt.const import (
    EVENT_VALUE_REMOVED,
    EVENT_NODE_REMOVED,
    EVENT_INSTANCE_REMOVED,
)


def test_statistics(mgr):
    mgr.mock_receive_json("/openzwave/1/statistics/", {"some_stat": "some-stat-data"})
    assert mgr.get_instance("1").get_statistics().some_stat == "some-stat-data"


def test_recursive_remove(mgr):
    events = []
    mgr.options.listen(EVENT_VALUE_REMOVED, events.append)
    mgr.options.listen(EVENT_NODE_REMOVED, events.append)
    mgr.options.listen(EVENT_INSTANCE_REMOVED, events.append)

    # Instantiate instance, node, value
    mgr.mock_receive_json("/openzwave/1/node/2/value/3/", {"value": "yo"})

    mgr.receive_message("/openzwave/1", "")

    assert len(events) == 3
    assert events[0].id == "3", events  # value
    assert events[1].id == "2", events  # node
    assert events[2].id == "1", events  # instance
