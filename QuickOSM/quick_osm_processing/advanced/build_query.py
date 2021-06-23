"""Processing algorithm for building a query."""

from typing import Dict

from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProcessingAlgorithm,
    QgsProcessingOutputString,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterExtent,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProject,
)

from QuickOSM.core.query_factory import QueryFactory
from QuickOSM.core.query_preparation import QueryPreparation
from QuickOSM.core.utilities.tools import get_setting
from QuickOSM.definitions.osm import QueryLanguage, QueryType
from QuickOSM.definitions.overpass import OVERPASS_SERVERS
from QuickOSM.qgis_plugin_tools.tools.i18n import tr

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


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
    def group() -> str:
        return tr('Advanced')

    @staticmethod
    def groupId() -> str:
        return 'advanced'

    def shortHelpString(self) -> str:
        return self.tr(
            'This algorithm builds a query and then encode it into the '
            'Overpass API URL. The "Download File" algorithm might be used '
            'after that to fetch the result.')

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagHideFromToolbox

    def add_top_parameters(self):
        param = QgsProcessingParameterString(self.KEY, tr('Key, default to all keys'), optional=True)
        help_string = tr('The OSM key to use. It can be empty and it will default to all keys.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        param = QgsProcessingParameterString(self.VALUE, tr('Value, default to all values'), optional=True)
        help_string = tr('The OSM value to use. It can be empty and it will default to all values.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

    def add_bottom_parameters(self):
        param = QgsProcessingParameterNumber(
            self.TIMEOUT, tr('Timeout'), defaultValue=25, minValue=5)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        help_string = tr('The timeout to use for the Overpass API.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        server = get_setting('defaultOAPI', OVERPASS_SERVERS[0]) + 'interpreter'
        param = QgsProcessingParameterString(
            self.SERVER,
            tr('Overpass server'),
            optional=False,
            defaultValue=server)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        help_string = tr('The Overpass API server to use to build the encoded URL.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        output = QgsProcessingOutputString(self.OUTPUT_URL, tr('Query as encoded URL'))
        help_string = tr(
            'The query is generated and encoded with the Overpass API URL. This output should be used in the '
            'File Downloader algorithm.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            pass
            # output.setHelp(help_string)
        else:
            output.tooltip_3liz = help_string
        self.addOutput(output)

        output = QgsProcessingOutputString(self.OUTPUT_OQL_QUERY, tr('Raw query as OQL'))
        help_string = tr('The query is generated in the OQL format.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            pass
            # output.setHelp(help_string)
        else:
            output.tooltip_3liz = help_string
        self.addOutput(output)

    def fetch_based_parameters(self, parameters, context):
        self.key = self.parameterAsString(parameters, self.KEY, context)
        self.value = self.parameterAsString(parameters, self.VALUE, context)
        self.timeout = self.parameterAsInt(parameters, self.TIMEOUT, context)
        self.server = self.parameterAsString(parameters, self.SERVER, context)

    def build_query(self) -> Dict[str, str]:
        query_factory = QueryFactory(
            query_type=self.QUERY_TYPE,
            key=self.key,
            value=self.value,
            area=self.area,
            around_distance=self.distance,
            timeout=self.timeout)
        raw_query = query_factory.make(QueryLanguage.OQL)
        self.feedback.pushInfo(query_factory.friendly_message())
        query_preparation = QueryPreparation(
            raw_query,
            area=self.area,
            extent=self.extent,
            overpass=self.server
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
    def name() -> str:
        return 'buildquerybyattributeonly'

    @staticmethod
    def displayName() -> str:
        return tr('Build query by attribute only')

    def initAlgorithm(self, config=None):
        self.add_top_parameters()
        self.add_bottom_parameters()

    def processAlgorithm(self, parameters, context, feedback) -> Dict[str, str]:
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)
        return self.build_query()


class BuildQueryInAreaAlgorithm(BuildQueryBasedAlgorithm):

    QUERY_TYPE = QueryType.InArea
    AREA = 'AREA'

    @staticmethod
    def name() -> str:
        return 'buildqueryinsidearea'

    @staticmethod
    def displayName() -> str:
        return tr('Build query inside an area')

    def initAlgorithm(self, config=None):
        self.add_top_parameters()

        param = QgsProcessingParameterString(self.AREA, tr('Inside the area'), optional=False)
        help_string = tr(
            'The name of the area. This will make a first query to the Nominatim API to fetch the OSM ID.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        self.add_bottom_parameters()

    def processAlgorithm(self, parameters, context, feedback) -> Dict[str, str]:
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)
        self.area = self.parameterAsString(parameters, self.AREA, context)
        return self.build_query()


class BuildQueryAroundAreaAlgorithm(BuildQueryBasedAlgorithm):

    QUERY_TYPE = QueryType.AroundArea
    AREA = 'AREA'
    DISTANCE = 'DISTANCE'

    @staticmethod
    def name() -> str:
        return 'buildqueryaroundarea'

    @staticmethod
    def displayName() -> str:
        return tr('Build query around an area')

    def initAlgorithm(self, config=None):
        self.add_top_parameters()

        param = QgsProcessingParameterString(self.AREA, tr('Around the area'), optional=False)
        help_string = tr(
            'The name of a place, a first query to the Nominatim API will be executed to fetch the OSM ID. '
            'A WKT Point string is accepted as well.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        param = QgsProcessingParameterNumber(
            self.DISTANCE, tr('Distance (meters)'), defaultValue=1000, minValue=1)
        help_string = tr(
            'The distance to use when doing the buffering around the named area. The distance must be in '
            'meters.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        self.add_bottom_parameters()

    def processAlgorithm(self, parameters, context, feedback) -> Dict[str, str]:
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)
        self.area = self.parameterAsString(parameters, self.AREA, context)
        self.distance = self.parameterAsInt(parameters, self.DISTANCE, context)
        return self.build_query()


class BuildQueryExtentAlgorithm(BuildQueryBasedAlgorithm):

    QUERY_TYPE = QueryType.BBox
    EXTENT = 'EXTENT'

    @staticmethod
    def name() -> str:
        return 'buildqueryextent'

    @staticmethod
    def displayName() -> str:
        return tr('Build query inside an extent')

    def initAlgorithm(self, config=None):
        self.add_top_parameters()

        param = QgsProcessingParameterExtent(self.EXTENT, tr('Extent'), optional=False)
        help_string = tr('The extent as a rectangle to use when building the query.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        self.add_bottom_parameters()

    def processAlgorithm(self, parameters, context, feedback) -> Dict[str, str]:
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)

        extent = self.parameterAsExtent(parameters, self.EXTENT, context)
        crs = self.parameterAsExtentCrs(parameters, self.EXTENT, context)

        crs_4326 = QgsCoordinateReferenceSystem(4326)
        transform = QgsCoordinateTransform(
            crs, crs_4326, QgsProject.instance())
        self.extent = transform.transform(extent)

        return self.build_query()
