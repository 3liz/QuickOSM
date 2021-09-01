"""Definitions for action visibilities."""

from enum import Enum, unique

__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


@unique
class Visibility(Enum):
    """Visibility of actions."""
    Canvas = 'Canvas'
    """Canvas"""

    Feature = 'Feature'
    """Feature"""

    Field = 'Field'
    """Field"""

    Layer = 'Layer'
    """Field"""


@unique
class SaveType(Enum):
    """Type of save for saving a query."""
    New = 'Create new'
    """Create a new query"""

    Existing = 'Add existing'
    """Edit an existing one"""
