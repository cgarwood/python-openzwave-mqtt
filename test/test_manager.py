from openzwavemqtt import manager


def test_receive_message(mgr):
    """Test receive message processing."""

    def mock_process_message(topic_parts, payload):
        """Test data comes in ok."""
        assert list(topic_parts) == ["1", "node", "2", "value", "3"]
        assert payload == {"mock": "payload"}

    mgr.process_message = mock_process_message

    mgr.receive_message("openzwave/1/node/2/value/3/", '{"mock":"payload"}')
