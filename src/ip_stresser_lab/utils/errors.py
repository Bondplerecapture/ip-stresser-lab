"""Custom exception hierarchy for ip-stresser-lab."""
from __future__ import annotations


class StresserError(Exception):
    """Base class for all ip-stresser-lab errors."""


class PluginLoadError(StresserError):
    """Raised when a plugin manifest or entry module cannot be loaded."""


class ConfigError(StresserError):
    """Raised when config.yaml is malformed or missing required keys."""


class TargetError(StresserError):
    """Raised when a target fails validation or resolution."""