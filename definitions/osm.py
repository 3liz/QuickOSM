"""Definitions for OSM concepts."""

from enum import Enum


class QueryType(Enum):
    NotSpatial = 'NotSpatial'
    BBox = 'Bbox'
    InNominatimPlace = 'InNominatimPlace'
    AroundNominatimPlace = 'AroundNominatimPlace'


class OsmType(Enum):
    Node = 'node'
    Way = 'way'
    Relation = 'relation'


class LayerType(Enum):
    Points = 'points'
    Lines = 'lines'
    Multilinestrings = 'multilinestrings'
    MultiPolygons = 'multipolygons'


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
