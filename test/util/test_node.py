"""Tests for node util submodule."""
from openzwavemqtt.const import ATTR_LABEL, ATTR_POSITION, ATTR_VALUE, ValueType
from openzwavemqtt.exceptions import InvalidValueError, NotFoundError, WrongTypeError
from openzwavemqtt.models.value import OZWValue
import pytest

from openzwavemqtt.util.node import (
    _set_bitset_config_parameter,
    _set_bool_config_parameter,
    _set_int_config_parameter,
    _set_list_config_parameter,
)


class MockValue(OZWValue):
    """Mock OZWValue."""

    def __init__(self, type: ValueType, value=None, min=None, max=None):
        self._type = type
        self._value = value
        self._min = min
        self._max = max

    @property
    def value(self):
        """Mock OZWValue.value."""
        return self._value

    @property
    def type(self):
        """Mock OZWValue.value."""
        return self._type

    @property
    def min(self):
        """Mock OZWValue.min."""
        return self._min

    @property
    def max(self):
        """Mock OZWValue.max."""
        return self._max

    def send_value(self, new_value):
        """Mock OZWValue.send_value()."""
        pass


def test_set_bool_config_parameter():
    """Test setting a ValueType.BOOL config parameter."""
    mock_value = MockValue(ValueType.BOOL)

    _set_bool_config_parameter(mock_value, True)
    _set_bool_config_parameter(mock_value, False)
    _set_bool_config_parameter(mock_value, "True")
    _set_bool_config_parameter(mock_value, "False")

    with pytest.raises(WrongTypeError):
        _set_bool_config_parameter(mock_value, "test")

    with pytest.raises(WrongTypeError):
        _set_bool_config_parameter(mock_value, 95)


def test_set_list_config_parameter():
    """Test setting a ValueType.LIST config parameter."""
    mock_value = MockValue(ValueType.LIST, {"List": [{"Label": "test", "Value": 0}]})

    _set_list_config_parameter(mock_value, "0")
    _set_list_config_parameter(mock_value, 0)
    _set_list_config_parameter(mock_value, "test")

    with pytest.raises(WrongTypeError):
        _set_list_config_parameter(mock_value, ["test"])


def test_set_bitset_config_parameter():
    """Test setting a ValueType.BITSET config parameter."""
    mock_value = MockValue(
        ValueType.BITSET, [{"Position": 1, "Label": "test", "Value": False}]
    )
    with pytest.raises(WrongTypeError):
        _set_bitset_config_parameter(
            mock_value, [{ATTR_POSITION: 1, ATTR_LABEL: "test", ATTR_VALUE: True}]
        )

    with pytest.raises(WrongTypeError):
        _set_bitset_config_parameter(mock_value, [{ATTR_VALUE: True}])

    with pytest.raises(WrongTypeError):
        _set_bitset_config_parameter(
            mock_value, [{ATTR_POSITION: "test", ATTR_VALUE: True}]
        )

    with pytest.raises(WrongTypeError):
        _set_bitset_config_parameter(mock_value, [{ATTR_LABEL: 1, ATTR_VALUE: True}])

    with pytest.raises(WrongTypeError):
        _set_bitset_config_parameter(mock_value, [{ATTR_POSITION: 1}])

    with pytest.raises(WrongTypeError):
        _set_bitset_config_parameter(mock_value, [{ATTR_POSITION: 1, ATTR_VALUE: 1}])

    with pytest.raises(NotFoundError):
        _set_bitset_config_parameter(mock_value, [{ATTR_POSITION: 2, ATTR_VALUE: True}])

    with pytest.raises(NotFoundError):
        _set_bitset_config_parameter(
            mock_value, [{ATTR_LABEL: "test not found", ATTR_VALUE: True}]
        )

    _set_bitset_config_parameter(mock_value, [{ATTR_LABEL: "test", ATTR_VALUE: True}])
    _set_bitset_config_parameter(mock_value, [{ATTR_POSITION: 1, ATTR_VALUE: True}])


def test_set_int_config_parameter():
    """Test setting a ValueType.INT config parameter."""
    mock_value = MockValue(ValueType.INT, value=1, min=0, max=10)

    with pytest.raises(WrongTypeError):
        _set_int_config_parameter(mock_value, "test")

    with pytest.raises(InvalidValueError):
        _set_int_config_parameter(mock_value, -1)

    with pytest.raises(InvalidValueError):
        _set_int_config_parameter(mock_value, 11)

    _set_int_config_parameter(mock_value, 1)
