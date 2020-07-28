"""Model for a OZW Node."""
from typing import Iterable, List, Optional

from ..base import ItemCollection, ZWaveBase
from ..const import (
    EVENT_NODE_ADDED,
    EVENT_NODE_CHANGED,
    EVENT_NODE_REMOVED,
    CommandClass,
    ValueIndex,
)
from .command_class import OZWCommandClass
from .node_association import OZWNodeAssocation
from .node_instance import OZWNodeInstance
from .node_statistics import OZWNodeStatistics
from .value import OZWValue


class OZWNode(ZWaveBase):
    """Model for a Z-Wave Node."""

    EVENT_ADDED = EVENT_NODE_ADDED
    EVENT_CHANGED = EVENT_NODE_CHANGED
    EVENT_REMOVED = EVENT_NODE_REMOVED

    @property
    def node_id(self) -> int:
        """Return NodeID."""
        return self.data.get("NodeID")

    @property
    def node_query_stage(self) -> str:
        """Return NodeQueryStage."""
        return self.data.get("NodeQueryStage")

    @property
    def is_listening(self) -> bool:
        """Return isListening."""
        return self.data.get("isListening")

    @property
    def is_flirs(self) -> bool:
        """Return isFlirs."""
        return self.data.get("isFlirs")

    @property
    def is_beaming(self) -> bool:
        """Return isBeaming."""
        return self.data.get("isBeaming")

    @property
    def is_routing(self) -> bool:
        """Return isRouting."""
        return self.data.get("isRouting")

    @property
    def is_securityv1(self) -> bool:
        """Return isSecurityv1."""
        return self.data.get("isSecurityv1")

    @property
    def is_zwave_plus(self) -> bool:
        """Return isZWavePlus."""
        return self.data.get("isZWavePlus")

    @property
    def is_nif_recieved(self) -> bool:
        """Return isNIFRecieved."""
        return self.data.get("isNIFRecieved")

    @property
    def is_awake(self) -> bool:
        """Return isAwake."""
        return self.data.get("isAwake")

    @property
    def is_failed(self) -> bool:
        """Return isFailed."""
        return self.data.get("isFailed")

    @property
    def meta_data(self) -> dict:
        """Return MetaData."""
        return self.data.get("MetaData")

    @property
    def event(self) -> str:
        """Return Event."""
        return self.data.get("Event")

    @property
    def time_stamp(self) -> int:
        """Return TimeStamp."""
        return self.data.get("TimeStamp")

    @property
    def node_manufacturer_name(self) -> str:
        """Return NodeManufacturerName."""
        return self.data.get("NodeManufacturerName")

    @property
    def node_product_name(self) -> str:
        """Return NodeProductName."""
        return self.data.get("NodeProductName")

    @property
    def node_basic_string(self) -> str:
        """Return NodeBasicString."""
        return self.data.get("NodeBasicString")

    @property
    def node_basic(self) -> int:
        """Return NodeBasic."""
        return self.data.get("NodeBasic")

    @property
    def node_generic_string(self) -> str:
        """Return NodeGenericString."""
        return self.data.get("NodeGenericString")

    @property
    def node_generic(self) -> int:
        """Return NodeGeneric."""
        return self.data.get("NodeGeneric")

    @property
    def node_specific_string(self) -> int:
        """Return NodeSpecificString."""
        return self.data.get("NodeSpecificString")

    @property
    def node_specific(self) -> int:
        """Return NodeSpecific."""
        return self.data.get("NodeSpecific")

    @property
    def node_manufacturer_id(self) -> str:
        """Return NodeManufacturerID."""
        return self.data.get("NodeManufacturerID")

    @property
    def node_product_type(self) -> str:
        """Return NodeProductType."""
        return self.data.get("NodeProductType")

    @property
    def node_product_id(self) -> str:
        """Return NodeProductID."""
        return self.data.get("NodeProductID")

    @property
    def node_baud_rate(self) -> int:
        """Return NodeBaudRate."""
        return self.data.get("NodeBaudRate")

    @property
    def node_version(self) -> int:
        """Return NodeVersion."""
        return self.data.get("NodeVersion")

    @property
    def node_groups(self) -> int:
        """Return NodeGroups."""
        return self.data.get("NodeGroups")

    @property
    def node_name(self) -> str:
        """Return NodeName."""
        return self.data.get("NodeName")

    @property
    def node_location(self) -> str:
        """Return NodeLocation."""
        return self.data.get("NodeLocation")

    @property
    def node_device_type_string(self) -> str:
        """Return NodeDeviceTypeString."""
        return self.data.get("NodeDeviceTypeString")

    @property
    def node_device_type(self) -> int:
        """Return NodeDeviceType."""
        return self.data.get("NodeDeviceType")

    @property
    def node_role(self) -> int:
        """Return NodeRole."""
        return self.data.get("NodeRole")

    @property
    def node_role_string(self) -> str:
        """Return NodeRoleString."""
        return self.data.get("NodeRoleString")

    @property
    def node_plus_type(self) -> int:
        """Return NodePlusType."""
        return self.data.get("NodePlusType")

    @property
    def node_plus_type_string(self) -> str:
        """Return NodePlusTypeString."""
        return self.data.get("NodePlusTypeString")

    @property
    def neighbors(self) -> List[int]:
        """Return Neighbors."""
        return self.data.get("Neighbors")

    def values(self) -> Iterable["OZWValue"]:
        """Iterate over all OZWValue child items."""
        # pylint: disable=no-member
        return (
            value
            for instance in self.instances()
            for cc in instance.commandclasses()
            for value in cc.values()
        )

    def create_collections(self):
        """Create collections that Node supports."""
        return {
            "instance": ItemCollection(OZWNodeInstance),
            "association": ItemCollection(OZWNodeAssocation),
            "statistics": OZWNodeStatistics,
        }

    def get_command_class(
        self, command_class_id: CommandClass, instance_id: Optional[int] = None
    ) -> Optional[OZWCommandClass]:
        """Return a specific CommandClass on this node (if exists)."""
        # pylint: disable=no-member
        for instance in self.instances():
            if instance_id is not None and instance.instance != instance_id:
                continue
            return instance.get_command_class(command_class_id)
        return None

    def has_command_class(
        self, command_class_id: CommandClass, instance_id: Optional[int] = None
    ) -> bool:
        """Determine if the node has the given CommandClass."""
        return self.get_command_class(command_class_id, instance_id) is not None

    def get_value(
        self,
        command_class_id: CommandClass,
        value_index: ValueIndex,
        instance_id: Optional[int] = None,
    ) -> Optional[OZWValue]:
        """Return a specific OZWValue on this node (if exists)."""
        command_class = self.get_command_class(command_class_id, instance_id)
        return command_class.get_value_by_index(value_index) if command_class else None

    def has_value(
        self,
        command_class_id: CommandClass,
        value_index: ValueIndex,
        instance_id: Optional[int] = None,
    ) -> bool:
        """Determine if the node has the given Value."""
        return self.get_value(command_class_id, value_index, instance_id) is not None
