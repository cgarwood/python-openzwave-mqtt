"""Options for the OZW MQTT Connection."""
from typing import Callable


class OZWOptions:
    """OZW Options class."""

    def __init__(
        self,
        send_message: Callable[[str, dict], None],
        topic_prefix: str = "OpenZWave/",
    ):
        """Initialize class."""
        self.send_message = send_message
        self.topic_prefix = topic_prefix
        self.listeners = {}

        # Make sure topic prefix ends in a slash
        assert topic_prefix[-1] == "/"

    def listen(self, event, listener):
        """Attach listener for events."""
        self.listeners.setdefault(event, []).append(listener)

    def notify(self, event, data):
        """Notify listeners of a new event."""
        for listener in self.listeners.get(event, []):
            listener(data)
