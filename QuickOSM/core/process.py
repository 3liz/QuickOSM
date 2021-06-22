"""The full process of opening a query, an OSM file."""

import logging
import os
import time

from os.path import isfile, join
from typing import List, Union

from qgis.core import (
    Qgis,
    QgsCategorizedSymbolRenderer,
    QgsExpressionContextUtils,
    QgsProject,
    QgsRectangle,
    QgsRendererCategory,
    QgsSymbol,
    QgsVectorFileWriter,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QApplication, QDialog

from QuickOSM.core import actions
from QuickOSM.core.api.connexion_oapi import ConnexionOAPI
from QuickOSM.core.exceptions import FileOutPutException
from QuickOSM.core.parser.osm_parser import OsmParser
from QuickOSM.core.query_factory import QueryFactory
from QuickOSM.core.query_preparation import QueryPreparation
from QuickOSM.core.utilities.tools import get_setting
from QuickOSM.definitions.format import Format
from QuickOSM.definitions.osm import (
    LayerType,
    Osm_Layers,
    OsmType,
    QueryLanguage,
    QueryType,
)
from QuickOSM.definitions.overpass import OVERPASS_SERVERS
from QuickOSM.qgis_plugin_tools.tools.i18n import tr

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


LOGGER = logging.getLogger('QuickOSM')


def open_file(
        dialog: QDialog = None,
        osm_file: str = None,
        output_geom_types: list = Osm_Layers,
        white_list_column: dict = None,
        layer_name: str = "OsmFile",
        config_outputs: dict = None,
        output_dir: str = None,
        output_format: Format = None,
        final_query: str = None,
        prefix_file: str = None) -> int:
    """
    Open an osm file.

    Memory layer if no output directory is set, or Geojson in the output
    directory.

    :param final_query: The query where the file comes from. Might be empty if
    it's a local OSM file.
    :type final_query: basestring
    """
    outputs = {}
    if output_dir:
        for layer in ['points', 'lines', 'multilinestrings', 'multipolygons']:
            if not prefix_file:
                prefix_file = layer_name

            if output_format in [Format.GeoPackage, Format.Kml]:
                outputs[layer] = join(
                    output_dir, prefix_file + "." + output_format.value.extension)
            elif output_format in [Format.GeoJSON, Format.Shapefile]:
                outputs[layer] = join(
                    output_dir, prefix_file + "_" + layer + "." + output_format.value.extension)
            else:
                raise NotImplementedError

            if isfile(outputs[layer]):
                raise FileOutPutException(suffix='(' + outputs[layer] + ')')

    # Legacy, waiting to remove the OsmParser for QGIS >= 3.6
    # Change in osm_file_dialog.py L131 too
    output_geom_legacy = [geom.value.lower() for geom in output_geom_types]
    if not white_list_column:
        white_list_column = {}
    white_list_legacy = (
        {cols.value.lower(): csv for cols, csv in white_list_column.items()}
    )

    LOGGER.info('The OSM file is: {}'.format(osm_file))

    # Parsing the file
    osm_parser = OsmParser(
        osm_file=osm_file,
        layers=output_geom_legacy,
        white_list_column=white_list_legacy)

    if dialog:
        osm_parser.signalText.connect(dialog.set_progress_text)
        osm_parser.signalPercentage.connect(dialog.set_progress_percentage)

    start_time = time.time()
    layers = osm_parser.parse()
    elapsed_time = time.time() - start_time
    parser_time = time.strftime("%Hh %Mm %Ss", time.gmtime(elapsed_time))
    LOGGER.info('The OSM parser took: {}'.format(parser_time))

    # Finishing the process with an output format or memory layer
    num_layers = 0

    for i, (layer, item) in enumerate(layers.items()):
        if dialog:
            dialog.set_progress_percentage(i / len(layers) * 100)
        QApplication.processEvents()
        if item['featureCount'] and (
                LayerType(layer.capitalize()) in output_geom_types):

            final_layer_name = layer_name
            # If configOutputs is not None (from My Queries)
            if config_outputs:
                if config_outputs[layer]['namelayer']:
                    final_layer_name = config_outputs[layer]['namelayer']

            if output_dir:
                dialog.set_progress_text(
                    tr('From memory layer to file: ' + layer))
                # Transforming the vector file
                memory_layer = item['vector_layer']

                options = QgsVectorFileWriter.SaveVectorOptions()
                if output_format in [Format.GeoPackage, Format.Kml]:
                    final_layer_name += '_' + layer
                options.layerName = final_layer_name
                options.driverName = output_format.value.driver_name
                if os.path.exists(outputs[layer]):
                    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
                else:
                    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
                if Qgis.QGIS_VERSION_INT >= 32000:
                    context = QgsProject.instance().transformContext()
                    QgsVectorFileWriter.writeAsVectorFormatV3(
                        memory_layer, outputs[layer], context, options)
                elif Qgis.QGIS_VERSION_INT >= 31003:
                    context = QgsProject.instance().transformContext()
                    QgsVectorFileWriter.writeAsVectorFormatV2(
                        memory_layer, outputs[layer], context, options)
                else:
                    QgsVectorFileWriter.writeAsVectorFormat(
                        memory_layer, outputs[layer], options)

                # Loading the final vector file
                if output_format in [Format.GeoPackage, Format.Kml]:
                    outputs[layer] += '|layername=' + final_layer_name
                new_layer = QgsVectorLayer(
                    outputs[layer], final_layer_name, "ogr")
            else:
                new_layer = item['vector_layer']
                new_layer.setName(final_layer_name)

            # Try to set styling if defined
            if config_outputs and config_outputs[layer]['style']:
                new_layer.loadNamedStyle(config_outputs[layer]['style'])
            else:
                if "colour" in item['tags']:
                    index = item['tags'].index('colour')
                    colors = new_layer.uniqueValues(index)
                    categories = []
                    for value in colors:
                        if layer in ['lines', 'multilinestrings']:
                            symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.LineGeometry)
                        elif layer == "points":
                            symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PointGeometry)
                        elif layer == "multipolygons":
                            symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.MultiPolygon)
                        symbol.setColor(QColor(value))
                        category = QgsRendererCategory(value, symbol, value)
                        categories.append(category)

                    renderer = QgsCategorizedSymbolRenderer("colour", categories)
                    new_layer.setRenderer(renderer)

            # Add action about OpenStreetMap
            actions.add_actions(new_layer, item['tags'])

            QgsProject.instance().addMapLayer(new_layer)

            if final_query:
                QgsExpressionContextUtils.setLayerVariable(
                    new_layer, 'quickosm_query', final_query)
                actions.add_relaunch_action(new_layer, final_layer_name)
                if dialog:
                    dialog.iface.addCustomActionForLayer(dialog.reload_action, new_layer)

            num_layers += 1

    return num_layers


def reload_query(
        query: str,
        layer_name: str = 'Reloaded_query',
        dialog: QDialog = None,
        new_file: bool = True):
    """ Reload a query with only the query """
    # Getting the default overpass api and running the query
    server = get_setting('defaultOAPI', OVERPASS_SERVERS[0]) + 'interpreter'

    query = QueryPreparation(query, overpass=server)
    final_query = query.prepare_query()
    url = query.prepare_url()
    connexion_overpass_api = ConnexionOAPI(url)
    LOGGER.debug('Encoded URL: {}'.format(url))
    osm_file = connexion_overpass_api.run()

    if new_file:
        layer_name += "_reloaded"
        return open_file(
            dialog=dialog,
            osm_file=osm_file,
            layer_name=layer_name,
            final_query=final_query,)


def process_query(
        dialog: QDialog = None,
        query: str = None,
        area: Union[str, List[str]] = None,
        bbox: QgsRectangle = None,
        output_dir: str = None,
        output_format: Format = None,
        prefix_file: str = None,
        output_geometry_types: list = None,
        layer_name: str = "OsmQuery",
        white_list_values: dict = None,
        config_outputs: dict = None) -> int:
    """execute a query and send the result file to open_file."""

    # Prepare outputs
    dialog.set_progress_text(tr('Prepare outputs'))

    # Getting the default overpass api and running the query
    server = get_setting('defaultOAPI', OVERPASS_SERVERS[0]) + 'interpreter'
    dialog.set_progress_text(
        tr('Downloading data from Overpass {server_name}'.format(
            server_name=server)))
    # Replace Nominatim or BBOX
    query = QueryPreparation(query, bbox, area, server)
    QApplication.processEvents()
    final_query = query.prepare_query()
    url = query.prepare_url()
    connexion_overpass_api = ConnexionOAPI(url)
    LOGGER.debug('Encoded URL: {}'.format(url))
    osm_file = connexion_overpass_api.run()

    return open_file(
        dialog=dialog,
        osm_file=osm_file,
        output_geom_types=output_geometry_types,
        white_list_column=white_list_values,
        layer_name=layer_name,
        output_dir=output_dir,
        output_format=output_format,
        prefix_file=prefix_file,
        final_query=final_query,
        config_outputs=config_outputs)


def process_quick_query(
        dialog: QDialog = None,
        query_type: QueryType = None,
        key: str = None,
        value: str = None,
        bbox: QgsRectangle = None,
        area: str = None,
        distance: int = None,
        osm_objects: List[OsmType] = None,
        timeout: int = 25,
        output_directory: str = None,
        output_format: Format = None,
        prefix_file: str = None,
        output_geometry_types: list = None) -> int:
    """
    Generate a query and send it to process_query.
    """
    # Building the query
    query_factory = QueryFactory(
        query_type=query_type,
        key=key,
        value=value,
        area=area,
        around_distance=distance,
        osm_objects=osm_objects,
        timeout=timeout
    )
    query = query_factory.make(QueryLanguage.OQL)
    LOGGER.info(query_factory.friendly_message())

    # Generate layer name as following (if defined)
    if not key:
        key = tr('allKeys')
    distance_string = None
    if distance:
        distance_string = '{}'.format(distance)
    expected_name = [key, value, area, distance_string]
    layer_name = '_'.join([f for f in expected_name if f])
    LOGGER.info('Query: {}'.format(layer_name))

    # Call process_query with the new query
    return process_query(
        dialog=dialog,
        query=query,
        area=area,
        bbox=bbox,
        output_dir=output_directory,
        output_format=output_format,
        prefix_file=prefix_file,
        output_geometry_types=output_geometry_types,
        layer_name=layer_name)
