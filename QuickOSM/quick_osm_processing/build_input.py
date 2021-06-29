"""Set up the parameters for the processing algorithms."""

from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from qgis.core import (
    Qgis,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterExtent,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
)

__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

from QuickOSM.core.utilities.tools import get_setting
from QuickOSM.definitions.osm import QueryType
from QuickOSM.definitions.overpass import OVERPASS_SERVERS
from QuickOSM.qgis_plugin_tools.tools.i18n import tr


class BuildBased(QgisAlgorithm):
    """Set up the parameters."""

    TIMEOUT = 'TIMEOUT'
    SERVER = 'SERVER'

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.feedback = None
        self.area = None
        self.extent = None
        self.server = None
        self.timeout = None

    def fetch_based_parameters(self, parameters, context):
        """Get the parameters."""
        self.server = self.parameterAsString(parameters, self.SERVER, context)
        self.timeout = self.parameterAsInt(parameters, self.TIMEOUT, context)

    def add_top_parameters(self):
        """Set up the parameters."""
        pass

    def add_bottom_parameters(self):
        """Set up the advanced parameters."""
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


class BuildRaw(BuildBased):
    """Set up the parameters for a raw query input."""

    QUERY = 'QUERY'
    EXTENT = 'EXTENT'
    AREA = 'AREA'

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.query = None
        self.crs = None

    def fetch_based_parameters(self, parameters, context):
        """Get the parameters."""
        super().fetch_based_parameters(parameters, context)
        self.query = self.parameterAsString(parameters, self.QUERY, context)
        self.extent = self.parameterAsExtent(parameters, self.EXTENT, context)
        self.crs = self.parameterAsExtentCrs(parameters, self.EXTENT, context)
        self.area = self.parameterAsString(parameters, self.AREA, context)

    def add_top_parameters(self):
        """Set up the parameters."""
        super().add_top_parameters()

        param = QgsProcessingParameterString(
            self.QUERY, tr('Query'), optional=False, multiLine=True
        )
        help_string = tr(
            'A XML or OQL query to be send to the Overpass API. It can contains some {{}} tokens.'
        )
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

    def add_bottom_parameters(self):
        """Set up the advanced parameters."""
        super().add_bottom_parameters()

        param = QgsProcessingParameterExtent(
            self.EXTENT, tr('Extent, if "{{bbox}}" in the query'),
            defaultValue='0,1,0,1 []', optional=True
        )
        param.setFlags(
            param.flags() | QgsProcessingParameterDefinition.FlagAdvanced
        )
        help_string = tr(
            'If the query has a {{bbox}} token, this extent will be used for replacement.'
        )
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        param = QgsProcessingParameterString(
            self.AREA,
            tr('Area (if {{geocodeArea}} in the query)'),
            optional=True
        )
        param.setFlags(
            param.flags() | QgsProcessingParameterDefinition.FlagAdvanced
        )
        help_string = tr('If the query has a {{geocodeArea}} token, this place will be used.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)


class BuildBasedQuery(BuildBased):
    """Set up the parameters for a query input."""

    KEY = 'KEY'
    VALUE = 'VALUE'

    def __init__(self):
        super().__init__()
        self.key = None
        self.value = None
        self.distance = None

    def fetch_based_parameters(self, parameters, context):
        """Get the parameters."""
        super().fetch_based_parameters(parameters, context)
        self.key = self.parameterAsString(parameters, self.KEY, context)
        self.value = self.parameterAsString(parameters, self.VALUE, context)

    def add_top_parameters(self):
        """Set up the parameters."""
        super().add_top_parameters()

        param = QgsProcessingParameterString(
            self.KEY, tr('Key, default to all keys'), optional=True
        )
        help_string = tr(
            'The OSM key to use. It can be empty and it will default to all keys. '
            'Multiple keys can be be ask by adding the separator \',\' between each key.'
            'In this case make sure the number of keys match the number of values'
        )
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        param = QgsProcessingParameterString(
            self.VALUE, tr('Value, default to all values'), optional=True
        )
        help_string = tr(
            'The OSM value to use. It can be empty and it will default to all values.'
            'Multiple values can be be ask by adding the separator \',\' between each value.'
            'In this case make sure the number of values match the number of keys'
        )
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)


class BuildBasedNotSpatialQuery(BuildBasedQuery):
    """Set up the parameters for a not spatial query."""

    QUERY_TYPE = QueryType.NotSpatial


class BuildBasedInAreaQuery(BuildBasedQuery):
    """Set up the parameters for a 'in area' query."""

    QUERY_TYPE = QueryType.InArea
    AREA = 'AREA'

    def fetch_based_parameters(self, parameters, context):
        """Get the parameters."""
        super().fetch_based_parameters(parameters, context)
        self.area = self.parameterAsString(parameters, self.AREA, context)

    def add_top_parameters(self):
        """Set up the parameter."""
        super().add_top_parameters()

        param = QgsProcessingParameterString(self.AREA, tr('Inside the area'), optional=False)
        help_string = tr(
            'The name of the area. '
            'This will make a first query to the Nominatim API to fetch the OSM ID.'
        )
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)


class BuildBasedAroundAreaQuery(BuildBasedInAreaQuery):
    """Set up the parameters for an 'around area' query."""

    QUERY_TYPE = QueryType.AroundArea
    DISTANCE = 'DISTANCE'

    def __init__(self):
        super().__init__()
        self.distance = None

    def fetch_based_parameters(self, parameters, context):
        """Get the parameters."""
        super().fetch_based_parameters(parameters, context)
        self.distance = self.parameterAsInt(parameters, self.DISTANCE, context)

    def add_top_parameters(self):
        """Set up the parameter."""
        super().add_top_parameters()

        param = QgsProcessingParameterNumber(
            self.DISTANCE, tr('Distance (meters)'), defaultValue=1000, minValue=1)
        help_string = tr(
            'The distance to use when doing the buffering around the named area. '
            'The distance must be in meters.'
        )
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)


class BuildBasedExtentQuery(BuildBasedQuery):
    """Set up the parameters for an 'around area' query."""

    QUERY_TYPE = QueryType.BBox
    EXTENT = 'EXTENT'

    def fetch_based_parameters(self, parameters, context):
        """Get the parameters."""
        super().fetch_based_parameters(parameters, context)
        self.extent = self.parameterAsExtent(parameters, self.EXTENT, context)

    def add_top_parameters(self):
        """Set up the parameter."""
        super().add_top_parameters()

        param = QgsProcessingParameterExtent(self.EXTENT, tr('Extent'), optional=False)
        help_string = tr('The extent as a rectangle to use when building the query.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)
