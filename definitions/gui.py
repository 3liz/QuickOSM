"""Definitions for GUI concepts."""

from enum import Enum, unique


@unique
class Panels(Enum):
    """Name of panels in the GUI."""
    QuickQuery = 'QuickQuery'
    Query = 'Query'
    File = 'File'
