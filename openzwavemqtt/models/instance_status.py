"""Python wrapper for OpenZWave's MQTT daemon - Model for OZW Instance Status."""
from .. import base
from ..const import EVENT_INSTANCE_STATUS_CHANGED


class OZWInstanceStatus(base.ZWaveBase):
    """Model for OZW Instance Status."""

    EVENT_CHANGED = EVENT_INSTANCE_STATUS_CHANGED

    @property
    def status(self):
        """Return current status of this OZW Instance."""
        return self.data.get("Status")

    @property
    def home_id(self):
        """Return the homeID of this OZW Instance."""
        return self.data.get("homeID")

    @property
    def manufacturer_specific_db_ready(self) -> bool:
        """Return ManufacturerSpecificDBReady."""
        return self.data.get("ManufacturerSpecificDBReady")

    @property
    def time_stamp(self) -> int:
        """Return TimeStamp."""
        return self.data.get("TimeStamp")

    @property
    def openzwave_version(self) -> str:
        """Return OpenZWave_Version."""
        return self.data.get("OpenZWave_Version")

    @property
    def ozw_deamon_version(self) -> str:
        """Return OZWDeamon_Version."""
        return self.data.get("OZWDeamon_Version")

    @property
    def qt_openzwave_version(self) -> str:
        """Return QTOpenZWave_Version."""
        return self.data.get("QTOpenZWave_Version")

    @property
    def qt_version(self) -> str:
        """Return QT_Version."""
        return self.data.get("QT_Version")

    @property
    def get_controller_node_id(self) -> int:
        """Return getControllerNodeId."""
        return self.data.get("getControllerNodeId")

    @property
    def get_suc_node_id(self) -> int:
        """Return getSUCNodeId."""
        return self.data.get("getSUCNodeId")

    @property
    def is_primary_controller(self) -> bool:
        """Return isPrimaryController."""
        return self.data.get("isPrimaryController")

    @property
    def is_bridge_controller(self) -> bool:
        """Return isBridgeController."""
        return self.data.get("isBridgeController")

    @property
    def has_extended_tx_statistics(self) -> bool:
        """Return hasExtendedTXStatistics."""
        return self.data.get("hasExtendedTXStatistics")

    @property
    def get_controller_library_version(self) -> str:
        """Return getControllerLibraryVersion."""
        return self.data.get("getControllerLibraryVersion")

    @property
    def get_controller_library_type(self) -> str:
        """Return getControllerLibraryType."""
        return self.data.get("getControllerLibraryType")

    @property
    def get_controller_path(self) -> str:
        """Return getControllerPath."""
        return self.data.get("getControllerPath")
