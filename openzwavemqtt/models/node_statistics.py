"""Model for Node Statistics."""
from ..base import ZWaveBase
from ..const import EVENT_NODE_ADDED, EVENT_NODE_STATISTICS_CHANGED, EVENT_NODE_REMOVED


class OZWNodeStatistics(ZWaveBase):

    EVENT_ADDED = EVENT_NODE_ADDED
    EVENT_CHANGED = EVENT_NODE_STATISTICS_CHANGED
    EVENT_REMOVED = EVENT_NODE_REMOVED

    @property
    def ack_channel(self):
        """Return ackChannel."""
        return self.data.get("ackChannel")

    @property
    def average_request_rtt(self):
        """Return averageRequestRTT."""
        return self.data.get("averageRequestRTT")

    @property
    def average_response_rtt(self):
        """Return averageResponseRTT."""
        return self.data.get("averageResponseRTT")

    @property
    def extended_tx_supported(self):
        """Return extendedTXSupported."""
        return self.data.get("extendedTXSupported")

    @property
    def hops(self):
        """Return hops."""
        return self.data.get("hops")

    @property
    def last_failed_link_from(self):
        """Return lastFailedLinkFrom."""
        return self.data.get("lastFailedLinkFrom")

    @property
    def last_failed_link_to(self):
        """Return lastFailedLinkTo."""
        return self.data.get("lastFailedLinkTo")

    @property
    def last_received_time_stamp(self):
        """Return lastRecievedTimeStamp."""
        return self.data.get("lastRecievedTimeStamp")

    @property
    def last_tx_channel(self):
        """Return lastTXChannel."""
        return self.data.get("lastTXChannel")

    @property
    def quality(self):
        """Return quality."""
        return self.data.get("quality")

    @property
    def received_dup_packets(self):
        """Return receivedDupPackets."""
        return self.data.get("receivedDupPackets")

    @property
    def received_packets(self):
        """Return recievedPackets."""
        return self.data.get("recievedPackets")

    @property
    def received_unsolicited(self):
        """Return receivedUnsolicited."""
        return self.data.get("receivedUnsolicited")

    @property
    def retries(self):
        """Return retries."""
        return self.data.get("retries")

    @property
    def route_scheme(self):
        """Return routeScheme."""
        return self.data.get("routeScheme")

    @property
    def route_speed(self):
        """Return routeSpeed."""
        return self.data.get("routeSpeed")

    @property
    def route_tries(self):
        """Return routeTries."""
        return self.data.get("routeTries")

    @property
    def route_used(self):
        """Return routeUsed."""
        return self.data.get("routeUsed")

    @property
    def routes(self):
        """Return routes."""
        return [
            self.data.get("route_1"),
            self.data.get("route_2"),
            self.data.get("route_3"),
            self.data.get("route_4"),
        ]

    @property
    def rssi(self):
        """Return rssi."""
        return [
            self.data.get("rssi_1"),
            self.data.get("rssi_2"),
            self.data.get("rssi_3"),
            self.data.get("rssi_4"),
            self.data.get("rssi_5"),
        ]

    @property
    def send_count(self):
        """Return sendCount."""
        return self.data.get("sendCount")

    @property
    def sent_failed(self):
        """Return sentFailed."""
        return self.data.get("sentFailed")

    @property
    def tx_time(self):
        """Return txTime."""
        return self.data.get("txTime")
