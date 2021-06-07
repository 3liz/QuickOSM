"""Definitions for action visibilities."""

from enum import Enum, unique

__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


@unique
class Visibility(Enum):
    """Visibility of actions."""
    Canvas = 'Canvas'
    Feature = 'Feature'
    Field = 'Field'
    Layer = 'Layer'
