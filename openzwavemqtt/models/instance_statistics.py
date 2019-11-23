from ..base import ZWaveBase
from ..const import EVENT_INSTANCE_STATISTICS_CHANGED


class OZWInstanceStatistics(ZWaveBase):
    EVENT_CHANGED = EVENT_INSTANCE_STATISTICS_CHANGED

    @property
    def sof_count(self):
        return self.data.get("SOFCnt")

    @property
    def ack_waiting(self):
        return self.data.get("ACKWaiting")

    @property
    def read_aborts(self):
        return self.data.get("readAborts")

    @property
    def bad_checksum(self):
        return self.data.get("badChecksum")

    @property
    def read_count(self):
        return self.data.get("readCnt")

    @property
    def write_count(self):
        return self.data.get("writeCnt")

    @property
    def can_count(self):
        return self.data.get("CANCnt")

    @property
    def nak_count(self):
        return self.data.get("NAKCnt")

    @property
    def ack_count(self):
        return self.data.get("ACKCnt")

    @property
    def oof_count(self):
        return self.data.get("OOFCnt")

    @property
    def dropped(self):
        return self.data.get("dropped")

    @property
    def retries(self):
        return self.data.get("retries")

    @property
    def callbacks(self):
        return self.data.get("callbacks")

    @property
    def badroutes(self):
        return self.data.get("badroutes")

    @property
    def no_ack(self):
        return self.data.get("noack")

    @property
    def net_busy(self):
        return self.data.get("netbusy")

    @property
    def not_idle(self):
        return self.data.get("notidle")

    @property
    def tx_verified(self):
        return self.data.get("txverified")

    @property
    def non_delivery(self):
        return self.data.get("nondelivery")

    @property
    def routed_busy(self):
        return self.data.get("routedbusy")

    @property
    def broadcast_read_count(self):
        return self.data.get("broadcast_read_count")

    @property
    def broadcast_write_count(self):
        return self.data.get("broadcast_write_count")
