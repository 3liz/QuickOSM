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
