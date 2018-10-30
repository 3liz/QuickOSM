"""
/***************************************************************************
        QuickOSM QGIS plugin
        OSM Overpass API frontend
                             -------------------
        begin                : 2017-11-11
        copyright            : (C) 2017 by Etienne Trimaille
        email                : etienne dot trimaille at gmail dot com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterString,
    QgsProcessingParameterExtent,
    QgsProcessingParameterNumber,
    QgsProcessingOutputString,
    QgsCoordinateTransform,
    QgsProject,
    QgsCoordinateReferenceSystem,
)


from QuickOSM.definitions.osm import ALL_QUERY_TYPES, QueryType, ALL_OSM_TYPES, OsmType
from QuickOSM.core.query_factory import QueryFactory
from QuickOSM.core.query_preparation import QueryPreparation
from QuickOSM.core.utilities.tools import tr, get_setting


class QueryFactoryBasedAlgorithm(QgisAlgorithm):

    SERVER = 'SERVER'
    KEY = 'KEY'
    VALUE = 'VALUE'
    TIMEOUT = 'TIMEOUT'
    OUTPUT_URL = 'OUTPUT_URL'
    OUTPUT_OQL_QUERY = 'OUTPUT_OQL_QUERY'

    def __init__(self):
        super(QueryFactoryBasedAlgorithm, self).__init__()
        self.feedback = None
        self.key = None
        self.value = None
        self.nominatim = None
        self.extent = None
        self.distance = None
        self.timeout = None
        self.server = None

    @staticmethod
    def group():
        return tr('Advanced')

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagHideFromToolbox

    def add_top_parameters(self):
        self.addParameter(
            QgsProcessingParameterString(
                self.KEY, tr('Key, default to all keys'), optional=True))

        self.addParameter(
            QgsProcessingParameterString(
                self.VALUE, tr('Value, default to all values'), optional=True))

    def add_bottom_parameters(self):
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TIMEOUT, tr('Timeout'), defaultValue=25, minValue=5))

        server = get_setting('defaultOAPI') + 'interpreter'
        self.addParameter(
            QgsProcessingParameterString(
                self.SERVER, tr('Overpass server'), optional=False, defaultValue=server))

        self.addOutput(
            QgsProcessingOutputString(
                self.OUTPUT_URL, tr('Query as URL')))

        self.addOutput(
            QgsProcessingOutputString(
                self.OUTPUT_OQL_QUERY, tr('Raw query as OQL')))

    def fetch_based_parameters(self, parameters, context):
        self.key = self.parameterAsString(parameters, self.KEY, context)
        self.value = self.parameterAsString(parameters, self.VALUE, context)
        self.timeout = self.parameterAsInt(parameters, self.TIMEOUT, context)
        self.server = self.parameterAsString(parameters, self.SERVER, context)

    def build_query(self):
        query_factory = QueryFactory(
            query_type=self.QUERY_TYPE,
            key=self.key,
            value=self.value,
            nominatim_place=self.nominatim,
            around_distance=self.distance,
            timeout=self.timeout)
        raw_query = query_factory.make()
        query_preparation = QueryPreparation(
            raw_query, nominatim_place=self.nominatim, extent=self.extent, overpass=self.server
        )
        raw_query = query_preparation.prepare_query()
        url = query_preparation.prepare_url()

        outputs = {
            self.OUTPUT_URL: url,
            self.OUTPUT_OQL_QUERY: raw_query,
        }
        return outputs


class QueryFactoryNotSpatialAlgorithm(QueryFactoryBasedAlgorithm):

    QUERY_TYPE = QueryType.NotSpatial

    @staticmethod
    def name():
        return 'query_factory_not_spatial'

    @staticmethod
    def displayName():
        return tr('Query factory by attribute only')

    def initAlgorithm(self, config=None):
        self.add_top_parameters()
        self.add_bottom_parameters()

    def processAlgorithm(self, parameters, context, feedback):
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)
        return self.build_query()


class QueryFactoryInNominatimAlgorithm(QueryFactoryBasedAlgorithm):

    QUERY_TYPE = QueryType.InNominatimPlace
    NOMINATIM = 'NOMINATIM'

    @staticmethod
    def name():
        return 'query_factory_in_nominatim'

    @staticmethod
    def displayName():
        return tr('Query factory in a place')

    def initAlgorithm(self, config=None):
        self.add_top_parameters()
        self.addParameter(
            QgsProcessingParameterString(
                self.NOMINATIM, tr('In'), optional=False))
        self.add_bottom_parameters()

    def processAlgorithm(self, parameters, context, feedback):
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)
        self.nominatim = self.parameterAsString(parameters, self.NOMINATIM, context)
        return self.build_query()


class QueryFactoryAroundNominatimAlgorithm(QueryFactoryBasedAlgorithm):

    QUERY_TYPE = QueryType.AroundNominatimPlace
    NOMINATIM = 'NOMINATIM'
    DISTANCE = 'DISTANCE'

    @staticmethod
    def name():
        return 'query_factory_around_nominatim'

    @staticmethod
    def displayName():
        return tr('Query factory around a place')

    def initAlgorithm(self, config=None):
        self.add_top_parameters()
        self.addParameter(
            QgsProcessingParameterString(
                self.NOMINATIM, tr('Around'), optional=False))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DISTANCE, tr('Distance'), defaultValue=1000, minValue=1))
        self.add_bottom_parameters()

    def processAlgorithm(self, parameters, context, feedback):
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)
        self.nominatim = self.parameterAsString(parameters, self.NOMINATIM, context)
        self.distance = self.parameterAsInt(parameters, self.DISTANCE, context)
        return self.build_query()


class QueryFactoryExtentAlgorithm(QueryFactoryBasedAlgorithm):

    QUERY_TYPE = QueryType.BBox
    EXTENT = 'EXTENT'

    @staticmethod
    def name():
        return 'query_factory_extent'

    @staticmethod
    def displayName():
        return tr('Query factory in an extent')

    def initAlgorithm(self, config=None):
        self.add_top_parameters()
        self.addParameter(
            QgsProcessingParameterExtent(
                self.EXTENT, tr('Extent'), optional=False))
        self.add_bottom_parameters()

    def processAlgorithm(self, parameters, context, feedback):
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)

        extent = self.parameterAsExtent(parameters, self.EXTENT, context)
        crs = self.parameterAsExtentCrs(parameters, self.EXTENT, context)

        crs_4326 = QgsCoordinateReferenceSystem(4326)
        transform = QgsCoordinateTransform(crs, crs_4326, QgsProject.instance())
        self.extent = transform.transform(extent)

        return self.build_query()
