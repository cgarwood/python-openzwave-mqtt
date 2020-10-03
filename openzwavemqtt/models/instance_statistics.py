"""Model for the Instance statistics."""
from typing import Optional

from ..const import EVENT_INSTANCE_STATISTICS_CHANGED
from .node_child_base import OZWNodeChildBase


class OZWInstanceStatistics(OZWNodeChildBase):
    """Model for OZW Instance statistics."""

    EVENT_CHANGED = EVENT_INSTANCE_STATISTICS_CHANGED

    @property
    def sof_cnt(self) -> Optional[int]:
        """Return SOFCnt."""
        return self.data.get("SOFCnt")

    @property
    def ack_waiting(self) -> Optional[int]:
        """Return ACKWaiting."""
        return self.data.get("ACKWaiting")

    @property
    def read_aborts(self) -> Optional[int]:
        """Return readAborts."""
        return self.data.get("readAborts")

    @property
    def bad_checksum(self) -> Optional[int]:
        """Return badChecksum."""
        return self.data.get("badChecksum")

    @property
    def read_cnt(self) -> Optional[int]:
        """Return readCnt."""
        return self.data.get("readCnt")

    @property
    def write_cnt(self) -> Optional[int]:
        """Return writeCnt."""
        return self.data.get("writeCnt")

    @property
    def can_cnt(self) -> Optional[int]:
        """Return CANCnt."""
        return self.data.get("CANCnt")

    @property
    def nak_cnt(self) -> Optional[int]:
        """Return NAKCnt."""
        return self.data.get("NAKCnt")

    @property
    def ack_cnt(self) -> Optional[int]:
        """Return ACKCnt."""
        return self.data.get("ACKCnt")

    @property
    def oof_cnt(self) -> Optional[int]:
        """Return OOFCnt."""
        return self.data.get("OOFCnt")

    @property
    def dropped(self) -> Optional[int]:
        """Return dropped."""
        return self.data.get("dropped")

    @property
    def retries(self) -> Optional[int]:
        """Return retries."""
        return self.data.get("retries")

    @property
    def callbacks(self) -> Optional[int]:
        """Return callbacks."""
        return self.data.get("callbacks")

    @property
    def badroutes(self) -> Optional[int]:
        """Return badroutes."""
        return self.data.get("badroutes")

    @property
    def noack(self) -> Optional[int]:
        """Return noack."""
        return self.data.get("noack")

    @property
    def netbusy(self) -> Optional[int]:
        """Return netbusy."""
        return self.data.get("netbusy")

    @property
    def notidle(self) -> Optional[int]:
        """Return notidle."""
        return self.data.get("notidle")

    @property
    def txverified(self) -> Optional[int]:
        """Return txverified."""
        return self.data.get("txverified")

    @property
    def nondelivery(self) -> Optional[int]:
        """Return nondelivery."""
        return self.data.get("nondelivery")

    @property
    def routedbusy(self) -> Optional[int]:
        """Return routedbusy."""
        return self.data.get("routedbusy")

    @property
    def broadcast_read_cnt(self) -> Optional[int]:
        """Return broadcastReadCnt."""
        return self.data.get("broadcastReadCnt")

    @property
    def broadcast_write_cnt(self) -> Optional[int]:
        """Return broadcastWriteCnt."""
        return self.data.get("broadcastWriteCnt")
