"""Definitions for GUI concepts."""

from enum import Enum, unique

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


@unique
class Panels(Enum):
    """Name of panels in the GUI."""
    QuickQuery = 'QuickQuery'
    Query = 'Query'
    File = 'File'
    Configuration = 'Configuration'
