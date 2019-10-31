"""Processing QuickOSM provider."""

from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProcessingProvider

from .advanced.build_query import (
    BuildQueryInAreaAlgorithm,
    BuildQueryAroundAreaAlgorithm,
    BuildQueryExtentAlgorithm,
    BuildQueryNotSpatialAlgorithm,
)
# from .advanced.download_overpass import (
#   DownloadOverpassUrl)
from .advanced.open_osm_file import OpenOsmFile
from .advanced.raw_query import RawQueryAlgorithm
from ..qgis_plugin_tools.tools.resources import resources_path

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class Provider(QgsProcessingProvider):

    def id(self, *args, **kwargs):
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
