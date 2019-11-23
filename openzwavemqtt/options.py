from typing import Callable, Dict


class OZWOptions:
    def __init__(
        self,
        sent_message: Callable[[str, dict], None],
        topic_prefix: str = "OpenZWave/",
    ):
        self.sent_message = sent_message
        self.topic_prefix = topic_prefix
        self.listeners = {}

    def listen(self, event, listener):
        self.listeners.setdefault(event, []).append(listener)

    def notify(self, event, data):
        for listener in self.listeners.get(event, []):
            listener(data)
