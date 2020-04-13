"""Options for the OZW MQTT Connection."""
from typing import TYPE_CHECKING, Callable, Dict, List, Union

if TYPE_CHECKING:
    from .base import ZWaveBase  # noqa: F401


class OZWOptions:
    """OZW Options class."""

    def __init__(
        self,
        send_message: Callable[[str, Union[str, dict]], None],
        topic_prefix: str = "OpenZWave/",
    ):
        """Initialize class."""
        self.send_message = send_message
        self.topic_prefix = topic_prefix
        self.listeners: Dict[str, List[Callable[[Union[dict, "ZWaveBase"]], None]]] = {}

        # Make sure topic prefix ends in a slash
        assert topic_prefix[-1] == "/"

    def listen(
        self, event: str, listener: Callable[[Union[dict, "ZWaveBase"]], None]
    ) -> None:
        """Attach listener for events."""
        self.listeners.setdefault(event, []).append(listener)

    def notify(self, event: str, data: Union[dict, "ZWaveBase"]) -> None:
        """Notify listeners of a new event."""
        for listener in self.listeners.get(event, []):
            listener(data)
