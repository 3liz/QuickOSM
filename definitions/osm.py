"""Definitions for OSM concepts."""

from enum import Enum


class QueryType(Enum):
    NotSpatial = 'NotSpatial'
    BBox = 'Bbox'
    InArea = 'InNominatimPlace'
    AroundArea = 'AroundNominatimPlace'


class OsmType(Enum):
    Node = 'node'
    Way = 'way'
    Relation = 'relation'


class LayerType(Enum):
    Points = 'points'
    Lines = 'lines'
    Multilinestrings = 'multilinestrings'
    MultiPolygons = 'multipolygons'


ALL_QUERY_TYPES = [
    QueryType.AroundArea,
    QueryType.InArea,
    QueryType.NotSpatial,
    QueryType.BBox,
]

ALL_LAYER_TYPES = [
    LayerType.Points,
    LayerType.Lines,
    LayerType.Multilinestrings,
    LayerType.MultiPolygons
]

ALL_OSM_TYPES = [
    OsmType.Node,
    OsmType.Way,
    OsmType.Relation
]
