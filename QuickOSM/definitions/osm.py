"""Definitions for OSM concepts."""

from enum import Enum, unique

from QuickOSM.qgis_plugin_tools.tools.i18n import tr

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


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
class QueryLanguage(Enum):
    """Language of query that QuickOSM can generate."""
    XML = "xml"
    OQL = "oql"


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


Osm_Layers = [
    LayerType.Points, LayerType.Lines,
    LayerType.Multilinestrings, LayerType.Multipolygons
]


@unique
class MultiType(Enum):
    """Type of combination of two queries"""
    AND = tr('And')
    OR = tr('Or')
