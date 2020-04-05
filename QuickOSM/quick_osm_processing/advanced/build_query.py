"""Processing algorithm for building a query."""

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

from ...core.query_factory import QueryFactory
from ...core.query_preparation import QueryPreparation
from ...core.utilities.tools import get_setting
from ...definitions.osm import QueryType
from ...definitions.overpass import OVERPASS_SERVERS
from ...qgis_plugin_tools.tools.i18n import tr

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


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

    def shortHelpString(self):
        return self.tr(
            'This algorithm builds a query and then encode it into the '
            'Overpass API URL. The "Download File" algorithm might be used '
            'after that to fetch the result.')

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
        parameter.setFlags(
            parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        server = get_setting(
            'defaultOAPI', OVERPASS_SERVERS[0]) + 'interpreter'
        parameter = QgsProcessingParameterString(
            self.SERVER,
            tr('Overpass server'),
            optional=False,
            defaultValue=server)
        parameter.setFlags(
            parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
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
                self.AREA,
                tr('Around the area (Point WKT accepted)'),
                optional=False))
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DISTANCE,
                tr('Distance (meters)'),
                defaultValue=1000,
                minValue=1))
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
        transform = QgsCoordinateTransform(
            crs, crs_4326, QgsProject.instance())
        self.extent = transform.transform(extent)

        return self.build_query()
