"""Exceptions for OpenZWave MQTT."""


class BaseOZWError(Exception):
    """Base OpenZWave MQTT exception."""


class NotFoundError(BaseOZWError):
    """Exception that is raised when an entity can't be found."""


class NotSupportedError(BaseOZWError):
    """Exception that is raised when an action isn't supported."""


class WrongTypeError(NotSupportedError):
    """Exception that is raised when an input is the wrong type."""


class InvalidValueError(NotSupportedError):
    """Exception that is raised when an input value is invalid."""
