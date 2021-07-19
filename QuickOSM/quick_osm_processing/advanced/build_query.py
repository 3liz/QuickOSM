"""Processing algorithm for building a query."""

from typing import Dict

from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProcessingAlgorithm,
    QgsProcessingOutputString,
    QgsProject,
)

from QuickOSM.core.query_factory import QueryFactory
from QuickOSM.core.query_preparation import QueryPreparation
from QuickOSM.definitions.osm import QueryLanguage
from QuickOSM.qgis_plugin_tools.tools.i18n import tr

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

from QuickOSM.quick_osm_processing.build_input import (
    BuildBasedAroundAreaQuery,
    BuildBasedExtentQuery,
    BuildBasedInAreaQuery,
    BuildBasedNotSpatialQuery,
)


class BuildQueryBasedAlgorithm(QgisAlgorithm):
    """Processing algorithm for building a query."""

    OUTPUT_URL = 'OUTPUT_URL'
    OUTPUT_OQL_QUERY = 'OUTPUT_OQL_QUERY'

    def __init__(self):
        super().__init__()

    @staticmethod
    def group() -> str:
        """Return the group of the algorithm."""
        return tr('Advanced')

    @staticmethod
    def groupId() -> str:
        """Return the id of the group."""
        return 'advanced'

    def shortHelpString(self) -> str:
        """Return an helper for the algorithm."""
        return self.tr(
            'This algorithm builds a query and then encode it into the '
            'Overpass API URL. The "Download File" algorithm might be used '
            'after that to fetch the result.')

    def flags(self):
        """Return the flags."""
        return super().flags() | QgsProcessingAlgorithm.FlagHideFromToolbox

    def add_outputs(self):
        """Set up the advanced parameters."""
        output = QgsProcessingOutputString(self.OUTPUT_URL, tr('Query as encoded URL'))
        help_string = tr(
            'The query is generated and encoded with the Overpass API URL. '
            'This output should be used in the File Downloader algorithm.'
        )
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

    def initAlgorithm(self, config=None):
        """Set up of the algorithm."""
        self.add_top_parameters()
        self.add_bottom_parameters()
        self.add_outputs()

    def build_query(self) -> Dict[str, str]:
        """Build the query requested."""
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


class BuildQueryNotSpatialAlgorithm(BuildBasedNotSpatialQuery, BuildQueryBasedAlgorithm):
    """Processing algorithm for building a 'not spatial' query."""

    @staticmethod
    def name() -> str:
        """Return the name of the algorithm."""
        return 'buildquerybyattributeonly'

    @staticmethod
    def displayName() -> str:
        """Return the display name of the algorithm."""
        return tr('Build query by attribute only')

    def processAlgorithm(self, parameters, context, feedback) -> Dict[str, str]:
        """Run the algorithm."""
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)
        return self.build_query()


class BuildQueryInAreaAlgorithm(BuildBasedInAreaQuery, BuildQueryBasedAlgorithm):
    """Processing algorithm for building a 'in area' query."""

    @staticmethod
    def name() -> str:
        """Return the name of the algorithm."""
        return 'buildqueryinsidearea'

    @staticmethod
    def displayName() -> str:
        """Return the display name of the algorithm."""
        return tr('Build query inside an area')

    def processAlgorithm(self, parameters, context, feedback) -> Dict[str, str]:
        """Run the algorithm."""
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)
        return self.build_query()


class BuildQueryAroundAreaAlgorithm(BuildQueryBasedAlgorithm, BuildBasedAroundAreaQuery):
    """Processing algorithm for building a 'around' query."""

    @staticmethod
    def name() -> str:
        """Return the name of the algorithm."""
        return 'buildqueryaroundarea'

    @staticmethod
    def displayName() -> str:
        """Return the display name of the algorithm."""
        return tr('Build query around an area')

    def processAlgorithm(self, parameters, context, feedback) -> Dict[str, str]:
        """Run the algorithm."""
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)
        return self.build_query()


class BuildQueryExtentAlgorithm(BuildQueryBasedAlgorithm, BuildBasedExtentQuery):
    """Processing algorithm for building a 'extent' query."""

    @staticmethod
    def name() -> str:
        """Return the name of the algorithm."""
        return 'buildqueryextent'

    @staticmethod
    def displayName() -> str:
        """Return the display name of the algorithm."""
        return tr('Build query inside an extent')

    def processAlgorithm(self, parameters, context, feedback) -> Dict[str, str]:
        """Run the algorithm."""
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)

        crs = self.parameterAsExtentCrs(parameters, self.EXTENT, context)

        crs_4326 = QgsCoordinateReferenceSystem(4326)
        transform = QgsCoordinateTransform(
            crs, crs_4326, QgsProject.instance())
        self.extent = transform.transform(self.extent)

        return self.build_query()
