"""Processing QuickOSM provider."""

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from QuickOSM.qgis_plugin_tools.tools.resources import resources_path
from QuickOSM.quick_osm_processing.advanced.build_query import (
    BuildQueryAroundAreaAlgorithm,
    BuildQueryExtentAlgorithm,
    BuildQueryInAreaAlgorithm,
    BuildQueryNotSpatialAlgorithm,
)

# from .advanced.download_overpass import (
#   DownloadOverpassUrl)
from QuickOSM.quick_osm_processing.advanced.open_osm_file import OpenOsmFile
from QuickOSM.quick_osm_processing.advanced.raw_query import RawQueryAlgorithm

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class Provider(QgsProcessingProvider):

    def id(self, *args, **kwargs):  # NOQA
        return 'quickosm'

    def name(self, *args, **kwargs):
        return 'QuickOSM'

    def icon(self):
        return QIcon(resources_path('icons', 'QuickOSM.svg'))

    def svgIconPath(self):
        return resources_path('icons', 'QuickOSM.svg')

    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(BuildQueryInAreaAlgorithm())
        self.addAlgorithm(BuildQueryAroundAreaAlgorithm())
        self.addAlgorithm(BuildQueryExtentAlgorithm())
        self.addAlgorithm(BuildQueryNotSpatialAlgorithm())
        self.addAlgorithm(RawQueryAlgorithm())
        # self.addAlgorithm(DownloadOverpassUrl())
        self.addAlgorithm(OpenOsmFile())
