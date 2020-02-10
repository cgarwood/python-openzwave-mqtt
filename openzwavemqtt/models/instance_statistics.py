"""Model of OZW instance statistics."""
from ..const import EVENT_INSTANCE_STATISTICS_CHANGED
from .node_child_base import OZWNodeChildBase


class OZWInstanceStatistics(OZWNodeChildBase):
    EVENT_CHANGED = EVENT_INSTANCE_STATISTICS_CHANGED

    @property
    def sof_cnt(self) -> int:
        """Return SOFCnt."""
        return self.data.get("SOFCnt")

    @property
    def ack_waiting(self) -> int:
        """Return ACKWaiting."""
        return self.data.get("ACKWaiting")

    @property
    def read_aborts(self) -> int:
        """Return readAborts."""
        return self.data.get("readAborts")

    @property
    def bad_checksum(self) -> int:
        """Return badChecksum."""
        return self.data.get("badChecksum")

    @property
    def read_cnt(self) -> int:
        """Return readCnt."""
        return self.data.get("readCnt")

    @property
    def write_cnt(self) -> int:
        """Return writeCnt."""
        return self.data.get("writeCnt")

    @property
    def can_cnt(self) -> int:
        """Return CANCnt."""
        return self.data.get("CANCnt")

    @property
    def nak_cnt(self) -> int:
        """Return NAKCnt."""
        return self.data.get("NAKCnt")

    @property
    def ack_cnt(self) -> int:
        """Return ACKCnt."""
        return self.data.get("ACKCnt")

    @property
    def oof_cnt(self) -> int:
        """Return OOFCnt."""
        return self.data.get("OOFCnt")

    @property
    def dropped(self) -> int:
        """Return dropped."""
        return self.data.get("dropped")

    @property
    def retries(self) -> int:
        """Return retries."""
        return self.data.get("retries")

    @property
    def callbacks(self) -> int:
        """Return callbacks."""
        return self.data.get("callbacks")

    @property
    def badroutes(self) -> int:
        """Return badroutes."""
        return self.data.get("badroutes")

    @property
    def noack(self) -> int:
        """Return noack."""
        return self.data.get("noack")

    @property
    def netbusy(self) -> int:
        """Return netbusy."""
        return self.data.get("netbusy")

    @property
    def notidle(self) -> int:
        """Return notidle."""
        return self.data.get("notidle")

    @property
    def txverified(self) -> int:
        """Return txverified."""
        return self.data.get("txverified")

    @property
    def nondelivery(self) -> int:
        """Return nondelivery."""
        return self.data.get("nondelivery")

    @property
    def routedbusy(self) -> int:
        """Return routedbusy."""
        return self.data.get("routedbusy")

    @property
    def broadcast_read_cnt(self) -> int:
        """Return broadcastReadCnt."""
        return self.data.get("broadcastReadCnt")

    @property
    def broadcast_write_cnt(self) -> int:
        """Return broadcastWriteCnt."""
        return self.data.get("broadcastWriteCnt")
