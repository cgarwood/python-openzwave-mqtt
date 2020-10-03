"""Tests for node util submodule."""
from unittest.mock import Mock, patch

import pytest

from openzwavemqtt.const import ATTR_LABEL, ATTR_POSITION, ATTR_VALUE, ValueType
from openzwavemqtt.exceptions import InvalidValueError, NotFoundError, WrongTypeError
from openzwavemqtt.models.node import OZWNode
from openzwavemqtt.models.value import OZWValue
from openzwavemqtt.util.node import set_config_parameter


def test_set_bool_config_parameter(options):
    """Test setting a ValueType.BOOL config parameter."""
    mock_value = Mock(spec=OZWValue)
    mock_value.type = ValueType.BOOL

    node = OZWNode(options, None, "test", None)

    with patch("openzwavemqtt.util.node.OZWNode.get_value", return_value=mock_value):
        assert set_config_parameter(node, 1, True)
        assert not set_config_parameter(node, 1, False)
        assert set_config_parameter(node, 1, "True")
        assert not set_config_parameter(node, 1, "False")

        with pytest.raises(WrongTypeError):
            set_config_parameter(node, 1, "test")

        with pytest.raises(WrongTypeError):
            set_config_parameter(node, 1, 95)


def test_set_list_config_parameter(options):
    """Test setting a ValueType.LIST config parameter."""
    mock_value = Mock(spec=OZWValue)
    mock_value.type = ValueType.LIST
    mock_value.value = {"List": [{"Label": "test", "Value": 0}]}

    node = OZWNode(options, None, "test", None)

    with patch("openzwavemqtt.util.node.OZWNode.get_value", return_value=mock_value):
        assert set_config_parameter(node, 1, "0") == 0
        assert set_config_parameter(node, 1, 0) == 0
        assert set_config_parameter(node, 1, "test") == 0

        with pytest.raises(NotFoundError):
            set_config_parameter(node, 1, 1)

        with pytest.raises(WrongTypeError):
            set_config_parameter(node, 1, ["test"])

    mock_value.value = {"List": [{"Label": "test", "Value": "test"}]}
    with patch("openzwavemqtt.util.node.OZWNode.get_value", return_value=mock_value):
        assert set_config_parameter(node, 1, "test") == "test"


def test_set_bitset_config_parameter(options):
    """Test setting a ValueType.BITSET config parameter."""
    mock_value = Mock(spec=OZWValue)
    mock_value.type = ValueType.BITSET
    mock_value.value = [{"Position": 1, "Label": "test", "Value": False}]

    node = OZWNode(options, None, "test", None)

    with patch("openzwavemqtt.util.node.OZWNode.get_value", return_value=mock_value):
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

        assert set_config_parameter(
            node, 1, [{ATTR_LABEL: "test", ATTR_VALUE: True}]
        ) == [{ATTR_LABEL: "test", ATTR_VALUE: True}]
        assert set_config_parameter(
            node, 1, [{ATTR_POSITION: 1, ATTR_VALUE: True}]
        ) == [{ATTR_POSITION: 1, ATTR_VALUE: True}]


def test_set_int_config_parameter(options):
    """Test setting a ValueType.INT config parameter."""
    mock_value = Mock(spec=OZWValue)
    mock_value.type = ValueType.INT
    mock_value.value = 1
    mock_value.min = 0
    mock_value.max = 10

    node = OZWNode(options, None, "test", None)

    with patch("openzwavemqtt.util.node.OZWNode.get_value", return_value=mock_value):
        with pytest.raises(WrongTypeError):
            set_config_parameter(node, 1, "test")

        with pytest.raises(InvalidValueError):
            set_config_parameter(node, 1, -1)

        with pytest.raises(InvalidValueError):
            set_config_parameter(node, 1, 11)

        assert set_config_parameter(node, 1, 1) == 1
        assert set_config_parameter(node, 1, "1") == 1


def test_invalid_config_parameter_types(options):
    """Test invalid config parameter types."""
    mock_value = Mock(spec=OZWValue)

    node = OZWNode(options, None, "test", None)

    for value_type in (
        ValueType.DECIMAL,
        ValueType.RAW,
        ValueType.SCHEDULE,
        ValueType.UNKNOWN,
    ):
        mock_value.type = value_type
        with patch(
            "openzwavemqtt.util.node.OZWNode.get_value", return_value=mock_value
        ):
            with pytest.raises(WrongTypeError):
                set_config_parameter(node, 1, True)


def test_config_parameter_not_found(options):
    """Test config parameter can't be found."""
    node = OZWNode(options, None, "test", None)
    with patch("openzwavemqtt.util.node.OZWNode.get_value", return_value=None):
        with pytest.raises(NotFoundError):
            set_config_parameter(node, 1, True)
