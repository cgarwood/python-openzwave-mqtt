"""Model of OZW instance statistics."""
from ..const import EVENT_INSTANCE_STATISTICS_CHANGED
from .node_child_base import OZWNodeChildBase


class OZWInstanceStatistics(OZWNodeChildBase):
    EVENT_CHANGED = EVENT_INSTANCE_STATISTICS_CHANGED

    @property
    def sof_count(self):
        """Return SOFCnt."""
        return self.data.get("SOFCnt")

    @property
    def ack_waiting(self):
        """Return ACKWaiting."""
        return self.data.get("ACKWaiting")

    @property
    def read_aborts(self):
        """Return readAborts."""
        return self.data.get("readAborts")

    @property
    def bad_checksum(self):
        """Return badChecksum."""
        return self.data.get("badChecksum")

    @property
    def read_count(self):
        """Return readCnt."""
        return self.data.get("readCnt")

    @property
    def write_count(self):
        """Return writeCnt."""
        return self.data.get("writeCnt")

    @property
    def can_count(self):
        """Return CANCnt."""
        return self.data.get("CANCnt")

    @property
    def nak_count(self):
        """Return NAKCnt."""
        return self.data.get("NAKCnt")

    @property
    def ack_count(self):
        """Return ACKCnt."""
        return self.data.get("ACKCnt")

    @property
    def oof_count(self):
        """Return OOFCnt."""
        return self.data.get("OOFCnt")

    @property
    def dropped(self):
        """Return dropped."""
        return self.data.get("dropped")

    @property
    def retries(self):
        """Return retries."""
        return self.data.get("retries")

    @property
    def callbacks(self):
        """Return callbacks."""
        return self.data.get("callbacks")

    @property
    def badroutes(self):
        """Return badroutes."""
        return self.data.get("badroutes")

    @property
    def no_ack(self):
        """Return noack."""
        return self.data.get("noack")

    @property
    def net_busy(self):
        """Return netbusy."""
        return self.data.get("netbusy")

    @property
    def not_idle(self):
        """Return notidle."""
        return self.data.get("notidle")

    @property
    def tx_verified(self):
        """Return txverified."""
        return self.data.get("txverified")

    @property
    def non_delivery(self):
        """Return nondelivery."""
        return self.data.get("nondelivery")

    @property
    def routed_busy(self):
        """Return routedbusy."""
        return self.data.get("routedbusy")

    @property
    def broadcast_read_count(self):
        """Return broadcast_read_count."""
        return self.data.get("broadcast_read_count")

    @property
    def broadcast_write_count(self):
        """Return broadcast_write_count."""
        return self.data.get("broadcast_write_count")
