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
    QgsProcessingOutputString,
    QgsCoordinateTransform,
    QgsProject,
    QgsCoordinateReferenceSystem,
)

from QuickOSM.definitions.overpass import OVERPASS_SERVERS
from QuickOSM.core.query_preparation import QueryPreparation
from QuickOSM.core.utilities.tools import tr, get_setting


class RawQueryAlgorithm(QgisAlgorithm):

    SERVER = 'SERVER'
    QUERY = 'QUERY'
    EXTENT = 'EXTENT'
    AREA = 'AREA'
    OUTPUT_URL = 'OUTPUT_URL'
    OUTPUT_OQL_QUERY = 'OUTPUT_OQL_QUERY'

    @staticmethod
    def group():
        return tr('Advanced')

    @staticmethod
    def groupId():
        return 'advanced'

    @staticmethod
    def name():
        return 'buildrawquery'

    @staticmethod
    def displayName():
        return tr('Build raw query')

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagHideFromToolbox

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterString(
                self.QUERY, tr('Query'), optional=False, multiLine=True))

        self.addParameter(
            QgsProcessingParameterExtent(
                self.EXTENT, tr('Extent, if "{{bbox}}" in the query'), optional=True))

        server = get_setting('defaultOAPI', OVERPASS_SERVERS[0]) + 'interpreter'
        parameter = QgsProcessingParameterString(
            self.SERVER, tr('Overpass server'), optional=False, defaultValue=server)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterString(
            self.AREA,
            tr('Area (if you want to override {{geocodeArea}} in the query'),
            optional=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        self.addOutput(
            QgsProcessingOutputString(
                self.OUTPUT_URL, tr('Query as encoded URL')))

        self.addOutput(
            QgsProcessingOutputString(
                self.OUTPUT_OQL_QUERY, tr('Raw query as OQL')))

    def processAlgorithm(self, parameters, context, feedback):
        raw_query = self.parameterAsString(parameters, self.QUERY, context)
        server = self.parameterAsString(parameters, self.SERVER, context)
        nominatim = self.parameterAsString(parameters, self.AREA, context)
        extent = self.parameterAsExtent(parameters, self.EXTENT, context)
        crs = self.parameterAsExtentCrs(parameters, self.EXTENT, context)

        crs_4326 = QgsCoordinateReferenceSystem(4326)
        transform = QgsCoordinateTransform(
            crs, crs_4326, QgsProject.instance())
        extent = transform.transform(extent)

        query_preparation = QueryPreparation(
            raw_query, extent=extent, nominatim_place=nominatim, overpass=server
        )
        raw_query = query_preparation.prepare_query()
        url = query_preparation.prepare_url()

        outputs = {
            self.OUTPUT_URL: url,
            self.OUTPUT_OQL_QUERY: raw_query,
        }
        return outputs
