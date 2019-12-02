"""Options class."""
from typing import Callable


class OZWOptions:
    def __init__(
        self,
        send_message: Callable[[str, dict], None],
        topic_prefix: str = "OpenZWave/",
    ):
        self.send_message = send_message
        self.topic_prefix = topic_prefix
        self.listeners = {}

        # Make sure topic prefix ends in a slash
        assert topic_prefix[-1] == "/"

    def listen(self, event, listener):
        self.listeners.setdefault(event, []).append(listener)

    def notify(self, event, data):
        for listener in self.listeners.get(event, []):
            listener(data)
