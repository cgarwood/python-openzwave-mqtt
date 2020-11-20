"""Provide tests for the manager."""


def test_receive_message(mgr):
    """Test receive message processing."""

    messages = 0

    def mock_process_message(topic_parts, payload):
        """Test data comes in ok."""
        nonlocal messages
        messages += 1
        assert list(topic_parts) == ["1", "node", "2", "value", "3"]
        assert payload == {"mock": "payload"}

    mgr.process_message = mock_process_message

    mgr.receive_message("OpenZWave/1/node/2/value/3/", '{"mock":"payload"}')

    assert messages == 1

    # Assert that we can filter messages with incorrect instance id.
    mgr.options.instance_id = 1
    mgr.receive_message("OpenZWave/2/node/2/value/3/", '{"mock":"payload"}')

    assert messages == 1

    mgr.receive_message("OpenZWave/1/node/2/value/3/", '{"mock":"payload"}')

    assert messages == 2
