from ..base import ZWaveBase, ItemCollection
from ..const import EVENT_NODE_ADDED, EVENT_NODE_STATISTICS_CHANGED, EVENT_NODE_REMOVED

from .value import OZWValue


class OZWNodeStatistics(ZWaveBase):

    EVENT_ADDED = EVENT_NODE_ADDED
    EVENT_CHANGED = EVENT_NODE_STATISTICS_CHANGED
    EVENT_REMOVED = EVENT_NODE_REMOVED

    @property
    def ack_channel(self):
        return self.data.get("ackChannel")

    @property
    def average_request_rtt(self):
        return self.data.get("averageRequestRTT")

    @property
    def average_response_rtt(self):
        return self.data.get("averageResponseRTT")

    @property
    def extended_tx_supported(self):
        return self.data.get("extendedTXSupported")

    @property
    def hops(self):
        return self.data.get("hops")

    @property
    def last_failed_link_from(self):
        return self.data.get("lastFailedLinkFrom")

    @property
    def last_failed_link_to(self):
        return self.data.get("lastFailedLinkTo")

    @property
    def last_received_time_stamp(self):
        return self.data.get("lastRecievedTimeStamp")

    @property
    def last_tx_channel(self):
        return self.data.get("lastTXChannel")

    @property
    def quality(self):
        return self.data.get("quality")

    @property
    def received_dup_packets(self):
        return self.data.get("receivedDupPackets")

    @property
    def received_packets(self):
        return self.data.get("recievedPackets")

    @property
    def received_unsolicited(self):
        return self.data.get("receivedUnsolicited")

    @property
    def retries(self):
        return self.data.get("retries")

    @property
    def route_scheme(self):
        return self.data.get("routeScheme")

    @property
    def route_speed(self):
        return self.data.get("routeSpeed")

    @property
    def route_tries(self):
        return self.data.get("routeTries")

    @property
    def route_used(self):
        return self.data.get("routeUsed")

    @property
    def routes(self):
        return [
            self.data.get("route_1"),
            self.data.get("route_2"),
            self.data.get("route_3"),
            self.data.get("route_4"),
        ]

    @property
    def rssi(self):
        return [
            self.data.get("rssi_1"),
            self.data.get("rssi_2"),
            self.data.get("rssi_3"),
            self.data.get("rssi_4"),
            self.data.get("rssi_5"),
        ]

    @property
    def send_count(self):
        return self.data.get("sendCount")

    @property
    def sent_failed(self):
        return self.data.get("sentFailed")

    @property
    def tx_time(self):
        return self.data.get("txTime")

