"""OSM Parser file."""

from os.path import dirname, realpath, join, isfile, basename

from osgeo import gdal
from qgis.PyQt.QtCore import QObject, pyqtSignal, QVariant
from qgis.core import (
    QgsVectorLayer,
    QgsFields,
    QgsField,
    QgsFeature,
    QgsMemoryProviderUtils,
    QgsHstoreUtils,
)

from ..exceptions import QuickOsmException
from ...qgis_plugin_tools.tools.i18n import tr

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class OsmParser(QObject):

    """
    Parse an OSM file with OGR.
    """

    # Signal percentage
    signalPercentage = pyqtSignal(int, name='signalPercentage')
    # Signal text
    signalText = pyqtSignal(str, name='signalText')

    # Layers available in the OGR, other_relations is useless.
    OSM_LAYERS = ['points', 'lines', 'multilinestrings', 'multipolygons']

    # Dict to build the full ID of an object
    DIC_OSM_TYPE = {'node': 'n', 'way': 'w', 'relation': 'r'}

    # White list for the attribute table
    # if set to None all the keys will be keep
    WHITE_LIST = {
        'multilinestrings': None,
        'points': None,
        'lines': None,
        'multipolygons': None}

    def __init__(
            self,
            osm_file,
            layers=OSM_LAYERS,
            white_list_column=WHITE_LIST,
            delete_empty_layers=False,
            load_only=False,
            osm_conf=None):
        self.__osmFile = osm_file
        self.__layers = layers

        if not white_list_column:
            white_list_column = {
                'multilinestrings': None,
                'points': None,
                'lines': None,
                'multipolygons': None}

        self.__whiteListColumn = white_list_column
        self.__deleteEmptyLayers = delete_empty_layers
        self.__loadOnly = load_only

        # If an osm_conf is provided ?
        if not osm_conf:
            current_dir = dirname(realpath(__file__))
            self._osm_conf = join(current_dir, 'QuickOSMconf.ini')
        else:
            self._osm_conf = osm_conf

        QObject.__init__(self)

    def parse(self):
        """
        Start parsing the osm file.
        """

        # Configuration for OGR
        gdal.SetConfigOption('OSM_CONFIG_FILE', self._osm_conf)
        gdal.SetConfigOption('OSM_USE_CUSTOM_INDEXING', 'NO')

        if not isfile(self.__osmFile):
            raise QuickOsmException(tr('File does not exist'))

        uri = self.__osmFile + "|layername="
        layers = {}

        # If loadOnly, no parsing required:
        # It's used only when we ask to open an osm file
        if self.__loadOnly:
            file_name = basename(self.__osmFile)
            for layer in self.__layers:
                layers[layer] = QgsVectorLayer(
                    uri + layer, file_name + ' ' + layer, 'ogr')

                if not layers[layer].isValid():
                    message = tr('Error on the layer : {layer}').format(layer=layer)
                    raise QuickOsmException(message)

            return layers

        # Foreach layers
        for layer in self.__layers:
            self.signalText.emit(tr('Parsing layer : {layer}').format(layer=layer))
            layers[layer] = {}

            # Reading it with a QgsVectorLayer
            layers[layer]['vectorLayer'] = QgsVectorLayer(
                uri + layer, 'test_' + layer, 'ogr')

            if not layers[layer]['vectorLayer'].isValid():
                message = 'Error on the layer : {layer}'.format(layer=layer)
                raise QuickOsmException(message)

            layers[layer]['vectorLayer'].setProviderEncoding('UTF-8')

            # Set some default tags
            layers[layer]['tags'] = ['full_id', 'osm_id', 'osm_type']

            # Save the geometry type of the layer
            layers[layer]['geomType'] = layers[layer]['vectorLayer'].wkbType()

            # Set a featureCount
            layers[layer]['featureCount'] = 0

            # Get the other_tags
            fields = layers[layer]['vectorLayer'].fields()
            field_names = [field.name() for field in fields]
            other_tags_index = field_names.index('other_tags')

            features = layers[layer]['vectorLayer'].getFeatures()
            for i, feature in enumerate(features):
                layers[layer]['featureCount'] += 1

                # Improve the parsing if comma in whitelist,
                # we skip the parsing of tags, but featureCount is needed
                if self.__whiteListColumn[layer] == ',':
                    continue

                # Get the 'others_tags' field
                attributes = str(feature.attributes()[other_tags_index])

                if attributes:
                    h_store = QgsHstoreUtils.parse(attributes)
                    for key in h_store.keys():
                        if key not in layers[layer]['tags']:
                            # If the key in OSM is not already in the table
                            if self.__whiteListColumn[layer]:
                                if key in self.__whiteListColumn[layer]:
                                    layers[layer]['tags'].append(key)
                            else:
                                layers[layer]['tags'].append(key)

                percent = int(100 / len(self.__layers) * (i + 1))
                self.signalPercentage.emit(percent)

        # Delete empty layers if this option is set to True
        if self.__deleteEmptyLayers:
            delete_layers = []
            for keys, values in layers.items():
                if values['featureCount'] < 1:
                    delete_layers.append(keys)
            for layer in delete_layers:
                del layers[layer]

        # Creating GeoJSON files for each layers
        for layer in self.__layers:
            message = tr('Creating memory layer : {layer}').format(layer=layer)
            self.signalText.emit(message)
            self.signalPercentage.emit(0)

            # Adding the attribute table
            fields = QgsFields()
            for key in layers[layer]['tags']:
                fields.append(QgsField(key, QVariant.String))

            layers[layer]['vector_layer'] = (
                QgsMemoryProviderUtils.createMemoryLayer(
                    layer,
                    fields,
                    layers[layer]['geomType'],
                    layers[layer]['vectorLayer'].crs()))
            layers[layer]['vector_layer'].startEditing()

            # Foreach feature in the layer
            features = layers[layer]['vectorLayer'].getFeatures()
            for i, feature in enumerate(features):
                fet = QgsFeature()
                fet.setGeometry(feature.geometry())

                new_attributes = []
                attributes = feature.attributes()

                if layer in ['points', 'lines', 'multilinestrings']:
                    if layer == 'points':
                        osm_type = 'node'
                    elif layer == 'lines':
                        osm_type = 'way'
                    elif layer == 'multilinestrings':
                        osm_type = 'relation'

                    new_attributes.append(
                        self.DIC_OSM_TYPE[osm_type] + str(attributes[0]))
                    new_attributes.append(attributes[0])
                    new_attributes.append(osm_type)

                    if attributes[1]:
                        h_store = QgsHstoreUtils.parse(str(attributes[1]))
                        for tag in layers[layer]['tags'][3:]:
                            if str(tag) in h_store:
                                new_attributes.append(h_store[tag])
                            else:
                                new_attributes.append("")
                        fet.setAttributes(new_attributes)
                        layers[layer]['vector_layer'].addFeature(fet)

                elif layer == 'multipolygons':
                    if attributes[0]:
                        osm_type = 'relation'
                        new_attributes.append(
                            self.DIC_OSM_TYPE[osm_type] + str(attributes[0]))
                        new_attributes.append(str(attributes[0]))
                    else:
                        osm_type = 'way'
                        new_attributes.append(
                            self.DIC_OSM_TYPE[osm_type] + str(attributes[1]))
                        new_attributes.append(attributes[1])
                    new_attributes.append(osm_type)

                    h_store = QgsHstoreUtils.parse(str(attributes[2]))
                    for tag in layers[layer]['tags'][3:]:
                        if str(tag) in h_store:
                            new_attributes.append(h_store[tag])
                        else:
                            new_attributes.append("")
                    fet.setAttributes(new_attributes)
                    layers[layer]['vector_layer'].addFeature(fet)

                    percentage = int(
                        100 / layers[layer]['featureCount'] * (i + 1))
                    self.signalPercentage.emit(percentage)

            layers[layer]['vector_layer'].commitChanges()

        return layers
