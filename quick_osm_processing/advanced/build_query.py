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
    QgsProcessingParameterDefinition,
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


class BuildQueryBasedAlgorithm(QgisAlgorithm):

    SERVER = 'SERVER'
    KEY = 'KEY'
    VALUE = 'VALUE'
    TIMEOUT = 'TIMEOUT'
    OUTPUT_URL = 'OUTPUT_URL'
    OUTPUT_OQL_QUERY = 'OUTPUT_OQL_QUERY'

    def __init__(self):
        super(BuildQueryBasedAlgorithm, self).__init__()
        self.feedback = None
        self.key = None
        self.value = None
        self.area = None
        self.extent = None
        self.distance = None
        self.timeout = None
        self.server = None

    @staticmethod
    def group():
        return tr('Advanced')

    @staticmethod
    def groupId():
        return 'advanced'

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
        parameter = QgsProcessingParameterNumber(
            self.TIMEOUT, tr('Timeout'), defaultValue=25, minValue=5)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        server = get_setting('defaultOAPI') + 'interpreter'
        parameter = QgsProcessingParameterString(
            self.SERVER, tr('Overpass server'), optional=False, defaultValue=server)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        self.addOutput(
            QgsProcessingOutputString(
                self.OUTPUT_URL, tr('Query as encoded URL')))

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
            area=self.area,
            around_distance=self.distance,
            timeout=self.timeout)
        raw_query = query_factory.make()
        query_preparation = QueryPreparation(
            raw_query, nominatim_place=self.area, extent=self.extent, overpass=self.server
        )
        raw_query = query_preparation.prepare_query()
        url = query_preparation.prepare_url()

        outputs = {
            self.OUTPUT_URL: url,
            self.OUTPUT_OQL_QUERY: raw_query,
        }
        return outputs


class BuildQueryNotSpatialAlgorithm(BuildQueryBasedAlgorithm):

    QUERY_TYPE = QueryType.NotSpatial

    @staticmethod
    def name():
        return 'buildquerybyattributeonly'

    @staticmethod
    def displayName():
        return tr('Build query by attribute only')

    def initAlgorithm(self, config=None):
        self.add_top_parameters()
        self.add_bottom_parameters()

    def processAlgorithm(self, parameters, context, feedback):
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)
        return self.build_query()


class BuildQueryInAreaAlgorithm(BuildQueryBasedAlgorithm):

    QUERY_TYPE = QueryType.InArea
    AREA = 'AREA'

    @staticmethod
    def name():
        return 'buildqueryinsidearea'

    @staticmethod
    def displayName():
        return tr('Build query inside an area')

    def initAlgorithm(self, config=None):
        self.add_top_parameters()
        self.addParameter(
            QgsProcessingParameterString(
                self.AREA, tr('Inside the area'), optional=False))
        self.add_bottom_parameters()

    def processAlgorithm(self, parameters, context, feedback):
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)
        self.area = self.parameterAsString(parameters, self.AREA, context)
        return self.build_query()


class BuildQueryAroundAreaAlgorithm(BuildQueryBasedAlgorithm):

    QUERY_TYPE = QueryType.AroundArea
    AREA = 'AREA'
    DISTANCE = 'DISTANCE'

    @staticmethod
    def name():
        return 'buildqueryaroundarea'

    @staticmethod
    def displayName():
        return tr('Build query around an area')

    def initAlgorithm(self, config=None):
        self.add_top_parameters()
        self.addParameter(
            QgsProcessingParameterString(
                self.AREA, tr('Around the area (Point WKT accepted)'), optional=False))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DISTANCE, tr('Distance (meters)'), defaultValue=1000, minValue=1))
        self.add_bottom_parameters()

    def processAlgorithm(self, parameters, context, feedback):
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)
        self.area = self.parameterAsString(parameters, self.AREA, context)
        self.distance = self.parameterAsInt(parameters, self.DISTANCE, context)
        return self.build_query()


class BuildQueryExtentAlgorithm(BuildQueryBasedAlgorithm):

    QUERY_TYPE = QueryType.BBox
    EXTENT = 'EXTENT'

    @staticmethod
    def name():
        return 'buildqueryextent'

    @staticmethod
    def displayName():
        return tr('Build query inside an extent')

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
