"""Simple Processing algorithm to open a OSM file with sub layers."""

from os.path import exists

from osgeo import gdal
from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm
from qgis.core import (
    Qgis,
    QgsVectorLayer,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFile,
    QgsProcessingOutputVectorLayer,
)

from ...qgis_plugin_tools.tools.i18n import tr

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class OpenOsmFile(QgisAlgorithm):

    FILE = 'FILE'
    OSM_CONF = 'OSM_CONF'
    OUTPUT_POINTS = 'OUTPUT_POINTS'
    OUTPUT_LINES = 'OUTPUT_LINES'
    OUTPUT_MULTILINESTRINGS = 'OUTPUT_MULTILINESTRINGS'
    OUTPUT_MULTIPOLYGONS = 'OUTPUT_MULTIPOLYGONS'
    OUTPUT_OTHER_RELATIONS = 'OUTPUT_OTHER_RELATIONS'

    def __init__(self):
        super(OpenOsmFile, self).__init__()
        self.feedback = None

    @staticmethod
    def group():
        return tr('Advanced')

    @staticmethod
    def groupId():
        return 'advanced'

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagHideFromToolbox

    @staticmethod
    def name():
        return 'openosmfile'

    def displayName(self):
        return self.tr('Open sublayers from an OSM file')

    def shortHelpString(self):
        return self.tr('Open all sublayers from an OSM file. A custom OSM '
                       'configuration file can be specified following the OGR '
                       'documentation. This algorithm will not make a copy of '
                       'the input file, it will only open it using OGR and '
                       'custom INI file if provided.')

    def initAlgorithm(self, config=None):
        param = QgsProcessingParameterFile(self.FILE, self.tr('OSM file'))
        help_string = tr('The extension can be a OSM or PBF file.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        param = QgsProcessingParameterFile(self.OSM_CONF, self.tr('OSM configuration'), optional=True)
        help_string = tr(
            'The OGR OSM configuration file. This file is used to customize the import process about OSM tags. '
            'You should read the OGR documentation {url}').format(url='https://gdal.org/drivers/vector/osm.html')
        if Qgis.QGIS_VERSION_INT >= 31500:
            param.setHelp(help_string)
        else:
            param.tooltip_3liz = help_string
        self.addParameter(param)

        output = QgsProcessingOutputVectorLayer(
            self.OUTPUT_POINTS, self.tr('Output points'), QgsProcessing.TypeVectorPoint)
        help_string = tr('The point layer from the OGR OSM driver.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            output.setHelp(help_string)
        else:
            output.tooltip_3liz = help_string
        self.addOutput(output)

        output = QgsProcessingOutputVectorLayer(
            self.OUTPUT_LINES, self.tr('Output lines'), QgsProcessing.TypeVectorLine)
        help_string = tr('The line layer from the OGR OSM driver.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            output.setHelp(help_string)
        else:
            output.tooltip_3liz = help_string
        self.addOutput(output)

        output = QgsProcessingOutputVectorLayer(
            self.OUTPUT_MULTILINESTRINGS, self.tr('Output multilinestrings'), QgsProcessing.TypeVectorLine)
        help_string = tr('The multilinestrings layer from the OGR OSM driver.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            output.setHelp(help_string)
        else:
            output.tooltip_3liz = help_string
        self.addOutput(output)

        output = QgsProcessingOutputVectorLayer(
            self.OUTPUT_MULTIPOLYGONS, self.tr('Output multipolygons'), QgsProcessing.TypeVectorPolygon)
        help_string = tr('The multipolygon layer from the OGR OSM driver.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            output.setHelp(help_string)
        else:
            output.tooltip_3liz = help_string
        self.addOutput(output)

        output = QgsProcessingOutputVectorLayer(
            self.OUTPUT_OTHER_RELATIONS, self.tr('Output other relations'), QgsProcessing.TypeVector)
        help_string = tr('The relation layer from the OGR OSM driver.')
        if Qgis.QGIS_VERSION_INT >= 31500:
            output.setHelp(help_string)
        else:
            output.tooltip_3liz = help_string
        self.addOutput(output)

    def processAlgorithm(self, parameters, context, feedback):
        self.feedback = feedback
        file = self.parameterAsString(parameters, self.FILE, context)
        osm_configuration = self.parameterAsString(
            parameters, self.OSM_CONF, context)

        if osm_configuration:
            if not exists(osm_configuration):
                raise QgsProcessingException(
                    self.tr('OSM Configuration file not found'))

            gdal.SetConfigOption('OSM_CONFIG_FILE', osm_configuration)

        gdal.SetConfigOption('OSM_USE_CUSTOM_INDEXING', 'NO')

        points = QgsVectorLayer(
            '{}|layername=points'.format(file), 'points', 'ogr')
        context.temporaryLayerStore().addMapLayer(points)

        lines = QgsVectorLayer(
            '{}|layername=lines'.format(file), 'lines', 'ogr')
        context.temporaryLayerStore().addMapLayer(lines)

        multilinestrings = QgsVectorLayer(
            '{}|layername=multilinestrings'.format(
                file), 'multilinestrings', 'ogr')
        context.temporaryLayerStore().addMapLayer(multilinestrings)

        multipolygons = QgsVectorLayer(
            '{}|layername=multipolygons'.format(file), 'multipolygons', 'ogr')
        context.temporaryLayerStore().addMapLayer(multipolygons)

        other_relations = QgsVectorLayer(
            '{}|layername=other_relations'.format(
                file), 'other_relations', 'ogr')
        context.temporaryLayerStore().addMapLayer(other_relations)

        outputs = {
            self.OUTPUT_POINTS: points.id(),
            self.OUTPUT_LINES: lines.id(),
            self.OUTPUT_MULTILINESTRINGS: multilinestrings.id(),
            self.OUTPUT_MULTIPOLYGONS: multipolygons.id(),
            self.OUTPUT_OTHER_RELATIONS: other_relations.id()
        }

        gdal.SetConfigOption('OSM_CONFIG_FILE', None)
        gdal.SetConfigOption('OSM_USE_CUSTOM_INDEXING', None)

        return outputs
