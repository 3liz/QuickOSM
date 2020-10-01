"""Generate a raw query."""

from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from qgis.core import (
    Qgis,
    QgsProcessingAlgorithm,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterString,
    QgsProcessingParameterExtent,
    QgsProcessingOutputString,
    QgsCoordinateTransform,
    QgsProject,
    QgsCoordinateReferenceSystem,
)

from ...core.query_preparation import QueryPreparation
from ...core.utilities.tools import get_setting
from ...definitions.overpass import OVERPASS_SERVERS
from ...qgis_plugin_tools.tools.i18n import tr

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


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

    def shortHelpString(self):
        return 'A XML or OQL query to send to a Overpass API server.'

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagHideFromToolbox

    def initAlgorithm(self, config=None):
        param = QgsProcessingParameterString(self.QUERY, tr('Query'), optional=False, multiLine=True)
        help_string = tr('A XML or OQL query to be send to the Overpass API. It can contains some {{}} tokens.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        param = QgsProcessingParameterExtent(self.EXTENT, tr('Extent, if "{{bbox}}" in the query'), optional=True)
        help_string = tr('If the query has a {{bbox}} token, this extent will be used for replacement.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        server = get_setting(
            'defaultOAPI', OVERPASS_SERVERS[0]) + 'interpreter'
        param = QgsProcessingParameterString(
            self.SERVER,
            tr('Overpass server'),
            optional=False,
            defaultValue=server)
        param.setFlags(
            param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        help_string = tr('The Overpass API server to use to build the encoded URL.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        param = QgsProcessingParameterString(
            self.AREA,
            tr('Area (if you want to override {{geocodeArea}} in the query)'),
            optional=True)
        param.setFlags(
            param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        help_string = tr('{{geocodeArea}} can be overridden on runtime.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        output = QgsProcessingOutputString(self.OUTPUT_URL, tr('Query as encoded URL'))
        help_string = tr(
            'The query is generated and encoded with the Overpass API URL. This output should be used in the File '
            'Downloader algorithm.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            pass
            # param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addOutput(output)

        output = QgsProcessingOutputString(self.OUTPUT_OQL_QUERY, tr('Raw query as OQL'))
        help_string = tr('The query is generated in the OQL format.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            pass
            # param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addOutput(output)

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
            raw_query,
            extent=extent,
            area=nominatim,
            overpass=server
        )
        raw_query = query_preparation.prepare_query()
        url = query_preparation.prepare_url()

        outputs = {
            self.OUTPUT_URL: url,
            self.OUTPUT_OQL_QUERY: raw_query,
        }
        return outputs
