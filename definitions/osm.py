"""Definitions for OSM concepts."""

from enum import Enum, unique, auto


class AutoEnum(Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        return name


@unique
class QueryType(AutoEnum):
    """Type of query that QuickOSM can generate."""
    NotSpatial = auto()
    BBox = auto()
    InArea = auto()
    AroundArea = auto()


@unique
class OsmType(AutoEnum):
    """OSM objects."""
    Node = auto()
    Way = auto()
    Relation = auto()


@unique
class LayerType(AutoEnum):
    """Layers that ogr2ogr can generate from an OSM file which are readable."""
    Points = auto()
    Lines = auto()
    Multilinestrings = auto()
    MultiPolygons = auto()
