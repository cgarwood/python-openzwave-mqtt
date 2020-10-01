"""Exceptions for OpenZWave MQTT."""


class BaseOZWError(Exception):
    """Base OpenZWave MQTT exception."""


class NotFoundError(BaseOZWError):
    """Exception that is raised when an entity can't be found."""


class WrongTypeError(BaseOZWError):
    """Exception that gets raised when an input is the wrong type."""


class InvalidValueError(BaseOZWError):
    """Exception that gets raised when an input value is invalid."""
