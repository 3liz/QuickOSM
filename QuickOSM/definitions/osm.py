"""Definitions for OSM concepts."""

from enum import Enum, unique

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


# Wait for python 3.6 minimum version
# class AutoEnum(Enum):
#     # noinspection PyMethodParameters
#     def _generate_next_value_(name, start, count, last_values):
#         return name


@unique
class QueryType(Enum):
    """Type of query that QuickOSM can generate."""
    NotSpatial = 'NotSpatial'
    BBox = 'BBox'
    InArea = 'InArea'
    AroundArea = 'AroundArea'


@unique
class OsmType(Enum):
    """OSM objects."""
    Node = 'Node'
    Way = 'Way'
    Relation = 'Relation'


@unique
class LayerType(Enum):
    """Layers that ogr2ogr can generate from an OSM file which are readable."""
    Points = 'Points'
    Lines = 'Lines'
    Multilinestrings = 'Multilinestrings'
    Multipolygons = 'Multipolygons'
