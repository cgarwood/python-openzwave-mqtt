"""Test Node Child Base model."""
import pytest

from openzwavemqtt.models.node import OZWNode
from openzwavemqtt.models.node_child_base import OZWNodeChildBase


class MockDescendant(OZWNodeChildBase):
    EVENT_CHANGED = "mock-changed"


def test_node():
    node = OZWNode(None, None, "mock-node-id", 1)

    child = MockDescendant(None, node, "mock-child-id", 12)
    assert child.node is node

    grandchild = MockDescendant(None, child, "mock-grandchild-id", 123)
    assert grandchild.node is node

    with pytest.raises(RuntimeError):
        MockDescendant(None, None, "", "").node
