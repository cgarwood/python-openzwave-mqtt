"""Model for Node Statistics."""
from typing import List

from ..base import ZWaveBase
from ..const import EVENT_NODE_ADDED, EVENT_NODE_REMOVED, EVENT_NODE_STATISTICS_CHANGED


class OZWNodeStatistics(ZWaveBase):
    """Model for Node Statistics."""

    EVENT_ADDED = EVENT_NODE_ADDED
    EVENT_CHANGED = EVENT_NODE_STATISTICS_CHANGED
    EVENT_REMOVED = EVENT_NODE_REMOVED

    @property
    def send_count(self) -> int:
        """Return sendCount."""
        return self.data.get("sendCount")

    @property
    def sent_failed(self) -> int:
        """Return sentFailed."""
        return self.data.get("sentFailed")

    @property
    def retries(self) -> int:
        """Return retries."""
        return self.data.get("retries")

    @property
    def received_packets(self) -> int:
        """Return receivedPackets."""
        return self.data.get("receivedPackets")

    @property
    def received_dup_packets(self) -> int:
        """Return receivedDupPackets."""
        return self.data.get("receivedDupPackets")

    @property
    def received_unsolicited(self) -> int:
        """Return receivedUnsolicited."""
        return self.data.get("receivedUnsolicited")

    @property
    def last_sent_time_stamp(self) -> int:
        """Return lastSentTimeStamp."""
        return self.data.get("lastSentTimeStamp")

    @property
    def last_received_time_stamp(self) -> int:
        """Return lastReceivedTimeStamp."""
        return self.data.get("lastReceivedTimeStamp")

    @property
    def last_request_rtt(self) -> int:
        """Return lastRequestRTT."""
        return self.data.get("lastRequestRTT")

    @property
    def average_request_rtt(self) -> int:
        """Return averageRequestRTT."""
        return self.data.get("averageRequestRTT")

    @property
    def last_response_rtt(self) -> int:
        """Return lastResponseRTT."""
        return self.data.get("lastResponseRTT")

    @property
    def average_response_rtt(self) -> int:
        """Return averageResponseRTT."""
        return self.data.get("averageResponseRTT")

    @property
    def quality(self) -> int:
        """Return quality."""
        return self.data.get("quality")

    @property
    def extended_tx_supported(self) -> bool:
        """Return extendedTXSupported."""
        return self.data.get("extendedTXSupported")

    @property
    def tx_time(self) -> int:
        """Return txTime."""
        return self.data.get("txTime")

    @property
    def hops(self) -> int:
        """Return hops."""
        return self.data.get("hops")

    @property
    def rssi1(self) -> str:
        """Return rssi_1."""
        return self.data.get("rssi_1")

    @property
    def rssi2(self) -> str:
        """Return rssi_2."""
        return self.data.get("rssi_2")

    @property
    def rssi3(self) -> str:
        """Return rssi_3."""
        return self.data.get("rssi_3")

    @property
    def rssi4(self) -> str:
        """Return rssi_4."""
        return self.data.get("rssi_4")

    @property
    def rssi5(self) -> str:
        """Return rssi_5."""
        return self.data.get("rssi_5")

    @property
    def route1(self) -> int:
        """Return route_1."""
        return self.data.get("route_1")

    @property
    def route2(self) -> int:
        """Return route_2."""
        return self.data.get("route_2")

    @property
    def route3(self) -> int:
        """Return route_3."""
        return self.data.get("route_3")

    @property
    def route4(self) -> int:
        """Return route_4."""
        return self.data.get("route_4")

    @property
    def ack_channel(self) -> int:
        """Return ackChannel."""
        return self.data.get("ackChannel")

    @property
    def last_tx_channel(self) -> int:
        """Return lastTXChannel."""
        return self.data.get("lastTXChannel")

    @property
    def route_scheme(self) -> str:
        """Return routeScheme."""
        return self.data.get("routeScheme")

    @property
    def route_used(self) -> str:
        """Return routeUsed."""
        return self.data.get("routeUsed")

    @property
    def route_speed(self) -> str:
        """Return routeSpeed."""
        return self.data.get("routeSpeed")

    @property
    def route_tries(self) -> int:
        """Return routeTries."""
        return self.data.get("routeTries")

    @property
    def last_failed_link_from(self) -> int:
        """Return lastFailedLinkFrom."""
        return self.data.get("lastFailedLinkFrom")

    @property
    def last_failed_link_to(self) -> int:
        """Return lastFailedLinkTo."""
        return self.data.get("lastFailedLinkTo")

    @property
    def routes(self) -> List[int]:
        """Return routes."""
        return [
            self.data.get("route_1"),
            self.data.get("route_2"),
            self.data.get("route_3"),
            self.data.get("route_4"),
        ]

    @property
    def rssi(self) -> List[int]:
        """Return rssi."""
        return [
            self.data.get("rssi_1"),
            self.data.get("rssi_2"),
            self.data.get("rssi_3"),
            self.data.get("rssi_4"),
            self.data.get("rssi_5"),
        ]
