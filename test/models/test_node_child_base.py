"""Test Node Child Base model."""
import pytest

from openzwavemqtt.models.node import OZWNode
from openzwavemqtt.models.node_child_base import OZWNodeChildBase


class MockDescendant(OZWNodeChildBase):
    """Mock a descendant."""

    EVENT_CHANGED = "mock-changed"


def test_node():
    """Test a node."""
    node = OZWNode(None, None, "mock-node-id", 1)

    child = MockDescendant(None, node, "mock-child-id", 12)
    assert child.node is node

    grandchild = MockDescendant(None, child, "mock-grandchild-id", 123)
    assert grandchild.node is node

    assert str(grandchild) == "<MockDescendant 123 (node: 1)>"

    no_node_parent = MockDescendant(None, None, "", "")

    with pytest.raises(RuntimeError):
        # test access node property without valid parent (node)
        no_node_parent.node  # pylint: disable=pointless-statement

    assert str(no_node_parent) == "<MockDescendant (node: <missing> (bad!))>"
