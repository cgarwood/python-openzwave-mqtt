"""Provide pytest fixtures."""
import json
import pytest

from openzwavemqtt import OZWOptions, OZWManager


class MockOptions(OZWOptions):
    """Class with test options that keeps track of sent messages."""

    def __init__(self):
        """Initialize mock options instance."""
        self.mock_sent = []
        super().__init__(lambda topic, msg: self.mock_sent.append((topic, msg)))


class MockManager(OZWManager):
    """Represent a mock manager."""

    def __init__(self, options=None):
        """Initialize mock manager instance."""
        super().__init__(options or MockOptions())

    def mock_receive_json(self, topic, json_payload):
        """Receive JSON payloads directly."""
        self.receive_message(topic, json.dumps(json_payload))


@pytest.fixture(name="options")
def options_fixture():
    """Fixture for a manager."""
    return MockOptions()


@pytest.fixture(name="mgr")
def mgr_fixture(options):
    """Fixture for a manager."""
    return MockManager(options)
