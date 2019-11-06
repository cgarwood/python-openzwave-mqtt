from typing import Callable, Dict
import attr


@attr.s
class OZWOptions:

    sent_message: Callable[[str, dict], None] = attr.ib()
    topic_prefix: str = attr.ib(default="/openzwave/")
    listeners: Dict[str, Callable] = attr.ib(factory=dict)

    def listen(self, event, listener):
        self.listeners.setdefault(event, []).append(listener)

    def notify(self, event, data):
        for listener in self.listeners.get(event, []):
            listener(data)
