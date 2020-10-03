"""Tests for node util submodule."""
from unittest.mock import Mock, patch

import pytest

from openzwavemqtt.const import ATTR_LABEL, ATTR_POSITION, ATTR_VALUE, ValueType
from openzwavemqtt.exceptions import InvalidValueError, NotFoundError, WrongTypeError
from openzwavemqtt.models.node import OZWNode
from openzwavemqtt.models.value import OZWValue
from openzwavemqtt.util.node import set_config_parameter


@pytest.fixture(name="node")
def mock_node_fixture(options):
    """Mock OZWNode."""
    return OZWNode(options, None, "test", None)


@pytest.fixture(name="mock_value")
def mock_value_fixture():
    """Mock OZWValue."""
    return Mock(spec=OZWValue)


@pytest.fixture(name="mock_get_value")
def mock_get_value_fixture(mock_value):
    """Patch get_value."""
    with patch("openzwavemqtt.util.node.OZWNode.get_value", return_value=mock_value):
        yield


def test_set_bool_config_parameter(node, mock_value, mock_get_value):
    """Test setting a ValueType.BOOL config parameter."""
    mock_value.type = ValueType.BOOL

    assert set_config_parameter(node, 1, True)
    assert not set_config_parameter(node, 1, False)
    assert set_config_parameter(node, 1, "True")
    assert not set_config_parameter(node, 1, "False")

    with pytest.raises(WrongTypeError):
        set_config_parameter(node, 1, "test")

    with pytest.raises(WrongTypeError):
        set_config_parameter(node, 1, 95)


def test_set_list_config_parameter(node, mock_value, mock_get_value):
    """Test setting a ValueType.LIST config parameter."""
    mock_value.type = ValueType.LIST
    mock_value.value = {"List": [{"Label": "test", "Value": 0}]}

    assert set_config_parameter(node, 1, "0") == 0
    assert set_config_parameter(node, 1, 0) == 0
    assert set_config_parameter(node, 1, "test") == 0

    with pytest.raises(NotFoundError):
        set_config_parameter(node, 1, 1)

    with pytest.raises(WrongTypeError):
        set_config_parameter(node, 1, ["test"])

    mock_value.value = {"List": [{"Label": "test", "Value": "test"}]}
    assert set_config_parameter(node, 1, "test") == "test"


def test_set_bitset_config_parameter(node, mock_value, mock_get_value):
    """Test setting a ValueType.BITSET config parameter."""
    mock_value.type = ValueType.BITSET
    mock_value.value = [{"Position": 1, "Label": "test", "Value": False}]

    with pytest.raises(WrongTypeError):
        set_config_parameter(
            node, 1, [{ATTR_POSITION: 1, ATTR_LABEL: "test", ATTR_VALUE: True}]
        )

    with pytest.raises(WrongTypeError):
        set_config_parameter(node, 1, [{ATTR_VALUE: True}])

    with pytest.raises(WrongTypeError):
        set_config_parameter(node, 1, [{ATTR_POSITION: "test", ATTR_VALUE: True}])

    with pytest.raises(WrongTypeError):
        set_config_parameter(node, 1, [{ATTR_LABEL: 1, ATTR_VALUE: True}])

    with pytest.raises(WrongTypeError):
        set_config_parameter(node, 1, [{ATTR_POSITION: 1}])

    with pytest.raises(WrongTypeError):
        set_config_parameter(node, 1, [{ATTR_POSITION: 1, ATTR_VALUE: 1}])

    with pytest.raises(NotFoundError):
        set_config_parameter(node, 1, [{ATTR_POSITION: 2, ATTR_VALUE: True}])

    with pytest.raises(NotFoundError):
        set_config_parameter(
            node, 1, [{ATTR_LABEL: "test not found", ATTR_VALUE: True}]
        )

    assert set_config_parameter(node, 1, [{ATTR_LABEL: "test", ATTR_VALUE: True}]) == [
        {ATTR_LABEL: "test", ATTR_VALUE: True}
    ]
    assert set_config_parameter(node, 1, [{ATTR_POSITION: 1, ATTR_VALUE: True}]) == [
        {ATTR_POSITION: 1, ATTR_VALUE: True}
    ]


def test_set_int_config_parameter(node, mock_value, mock_get_value):
    """Test setting a ValueType.INT config parameter."""
    mock_value.type = ValueType.INT
    mock_value.value = 1
    mock_value.min = 0
    mock_value.max = 10

    with pytest.raises(WrongTypeError):
        set_config_parameter(node, 1, "test")

    with pytest.raises(InvalidValueError):
        set_config_parameter(node, 1, -1)

    with pytest.raises(InvalidValueError):
        set_config_parameter(node, 1, 11)

    assert set_config_parameter(node, 1, 1) == 1
    assert set_config_parameter(node, 1, "1") == 1


def test_invalid_config_parameter_types(node, mock_value, mock_get_value):
    """Test invalid config parameter types."""
    for value_type in (
        ValueType.DECIMAL,
        ValueType.RAW,
        ValueType.SCHEDULE,
        ValueType.UNKNOWN,
    ):
        mock_value.type = value_type
        with pytest.raises(WrongTypeError):
            set_config_parameter(node, 1, True)


def test_config_parameter_not_found(node):
    """Test config parameter can't be found."""
    with patch("openzwavemqtt.util.node.OZWNode.get_value", return_value=None):
        with pytest.raises(NotFoundError):
            set_config_parameter(node, 1, True)
