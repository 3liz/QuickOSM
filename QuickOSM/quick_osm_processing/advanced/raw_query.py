"""Generate a raw query."""

from typing import Dict

from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProcessingAlgorithm,
    QgsProcessingOutputString,
    QgsProject,
)

from QuickOSM.core.query_preparation import QueryPreparation
from QuickOSM.qgis_plugin_tools.tools.i18n import tr

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

from QuickOSM.quick_osm_processing.build_input import BuildRaw


class RawQueryAlgorithm(BuildRaw):
    """Processing algorithm to generate a raw query."""

    OUTPUT_URL = 'OUTPUT_URL'
    OUTPUT_OQL_QUERY = 'OUTPUT_OQL_QUERY'

    @staticmethod
    def group() -> str:
        """Return the group of the algorithm."""
        return tr('Advanced')

    @staticmethod
    def groupId() -> str:
        """Return the id of the group."""
        return 'advanced'

    @staticmethod
    def name() -> str:
        """Return the name of the algorithm."""
        return 'buildrawquery'

    @staticmethod
    def displayName() -> str:
        """Return the display name of the algorithm."""
        return tr('Build raw query')

    def shortHelpString(self) -> str:
        """Return an helper for the algorithm."""
        return 'A XML or OQL query to send to a Overpass API server.'

    def flags(self):
        """Return the flags."""
        return super().flags() | QgsProcessingAlgorithm.FlagHideFromToolbox

    def initAlgorithm(self, config=None):
        """Set up of the algorithm."""
        self.add_top_parameters()
        self.add_bottom_parameters()

        output = QgsProcessingOutputString(self.OUTPUT_URL, tr('Query as encoded URL'))
        help_string = tr(
            'The query is generated and encoded with the Overpass API URL. '
            'This output should be used in the File Downloader algorithm.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            pass
            # param.setHelp(help_string)
        else:
            output.tooltip_3liz = help_string
        self.addOutput(output)

        output = QgsProcessingOutputString(self.OUTPUT_OQL_QUERY, tr('Raw query as OQL'))
        help_string = tr('The query is generated in the OQL format.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            pass
            # param.setHelp(help_string)
        else:
            output.tooltip_3liz = help_string
        self.addOutput(output)

    def processAlgorithm(self, parameters, context, feedback) -> Dict[str, str]:
        """Run the algorithm."""
        self.feedback = feedback
        self.fetch_based_parameters(parameters, context)

        crs_4326 = QgsCoordinateReferenceSystem(4326)
        transform = QgsCoordinateTransform(
            self.crs, crs_4326, QgsProject.instance())
        self.extent = transform.transform(self.extent)

        self.feedback.pushInfo('Prepare the url.')

        query_preparation = QueryPreparation(
            self.query,
            extent=self.extent,
            area=self.area,
            overpass=self.server
        )
        raw_query = query_preparation.prepare_query()
        url = query_preparation.prepare_url()

        outputs = {
            self.OUTPUT_URL: url,
            self.OUTPUT_OQL_QUERY: raw_query,
        }
        return outputs
