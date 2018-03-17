# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
 A QGIS plugin
 OSM Overpass API frontend
                             -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info at 3liz dot com
        contributor          : Etienne Trimaille
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import tempfile
from os.path import dirname, abspath, join, isfile
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import \
    QGis, QgsVectorLayer, QgsVectorFileWriter, QgsAction, QgsMapLayerRegistry

from QuickOSM.core.query_factory import QueryFactory
from QuickOSM.core.utilities.tools import tr
from QuickOSM.core.exceptions import \
    FileOutPutException, OsmDriverNotFound, GDALVersion
from QuickOSM.core.api.connexion_oapi import ConnexionOAPI
from QuickOSM.core.parser.osm_parser import OsmParser
from QuickOSM.core.utilities.operating_system import get_default_encoding
from QuickOSM.core.utilities.utilities_qgis import \
    is_osm_driver_enabled, is_ogr_version_ok
from QuickOSM.core.utilities.tools import get_setting
from QuickOSM.core.query_parser import prepare_query


def get_outputs(output_dir, output_format, prefix_file, layer_name):
    outputs = {}
    for layer in ['points', 'lines', 'multilinestrings', 'multipolygons']:
        if not output_dir:
            # if no directory, get a temporary file

            if output_format == "shape":
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False, suffix="_" + layer + "_quickosm.shp")
            else:
                # We should avoid this copy of geojson in the temp folder
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False, suffix="_" + layer + "_quickosm.geojson")

            outputs[layer] = temp_file.name
            temp_file.flush()
            temp_file.close()

        else:
            if not prefix_file:
                prefix_file = layer_name

            if output_format == "shape":
                outputs[layer] = join(
                    output_dir, prefix_file + "_" + layer + ".shp")
            else:
                outputs[layer] = join(
                    output_dir, prefix_file + "_" + layer + ".geojson")

            if isfile(outputs[layer]):
                raise FileOutPutException(suffix='(' + outputs[layer] + ')')

    return outputs


def open_file(
        dialog=None,
        osm_file=None,
        output_geom_types=None,
        white_list_column=None,
        output_format=None,
        layer_name="OsmFile",
        config_outputs=None,
        output_dir=None,
        prefix_file=None):
    """
    open an osm file
    """
    outputs = get_outputs(output_dir, output_format, prefix_file, layer_name)

    # Parsing the file
    osm_parser = OsmParser(
        osm_file=osm_file,
        layers=output_geom_types,
        white_list_column=white_list_column)

    osm_parser.signalText.connect(dialog.set_progress_text)
    osm_parser.signalPercentage.connect(dialog.set_progress_percentage)
    layers = osm_parser.parse()

    # Finishing the process with geojson or shapefile
    num_layers = 0
    if output_format == "shape":
        dialog.set_progress_text(tr("QuickOSM", u"From GeoJSON to Shapefile"))

    for i, (layer, item) in enumerate(layers.items()):
        dialog.set_progress_percentage(i / len(layers) * 100)
        QApplication.processEvents()
        if item['featureCount'] and layer in output_geom_types:

            final_layer_name = layer_name
            # If configOutputs is not None (from My Queries)
            if config_outputs:
                if config_outputs[layer]['namelayer']:
                    final_layer_name = config_outputs[layer]['namelayer']

            # Transforming the vector file
            osm_geometries = {
                'points': QGis.WKBPoint,
                'lines': QGis.WKBLineString,
                'multilinestrings': QGis.WKBMultiLineString,
                'multipolygons': QGis.WKBMultiPolygon}
            geojson_layer = QgsVectorLayer(item['geojsonFile'], "temp", "ogr")

            encoding = get_default_encoding()
            if output_format == "shape":
                writer = QgsVectorFileWriter(
                    outputs[layer],
                    encoding,
                    geojson_layer.pendingFields(),
                    osm_geometries[layer],
                    geojson_layer.crs(),
                    "ESRI Shapefile")
            else:
                writer = QgsVectorFileWriter(
                    outputs[layer],
                    encoding,
                    geojson_layer.pendingFields(),
                    osm_geometries[layer],
                    geojson_layer.crs(),
                    "GeoJSON")

            for f in geojson_layer.getFeatures():
                writer.addFeature(f)

            del writer

            # Loading the final vector file
            new_layer = QgsVectorLayer(outputs[layer], final_layer_name, "ogr")

            # Try to set styling if defined
            if config_outputs and config_outputs[layer]['style']:
                new_layer.loadNamedStyle(config_outputs[layer]['style'])
            else:
                # Loading default styles
                if layer == "multilinestrings" or layer == "lines":
                    if "colour" in item['tags']:
                        new_layer.loadNamedStyle(
                            join(dirname(dirname(abspath(__file__))),
                                 "styles",
                                 layer + "_colour.qml"))

            # Add action about OpenStreetMap
            actions = new_layer.actions()
            actions.addAction(
                QgsAction.OpenUrl,
                "OpenStreetMap Browser",
                'http://www.openstreetmap.org/browse/'
                '[% "osm_type" %]/[% "osm_id" %]',
                False)
            actions.addAction(
                QgsAction.GenericPython,
                'JOSM',
                'from QuickOSM.CoreQuickOSM.Actions import Actions;'
                'Actions.run("josm","[% "full_id" %]")',
                False)
            actions.addAction(
                QgsAction.OpenUrl,
                "User default editor",
                'http://www.openstreetmap.org/edit?'
                '[% "osm_type" %]=[% "osm_id" %]',
                False)

            for link in ['url', 'website', 'wikipedia', 'ref:UAI']:
                if link in item['tags']:
                    link = link.replace(":", "_")
                    actions.addAction(
                        QgsAction.GenericPython,
                        link,
                        'from QuickOSM.core.actions import Actions;'
                        'Actions.run("' + link + '","[% "' + link + '" %]")',
                        False)

            if 'network' in item['tags'] and 'ref' in item['tags']:
                actions.addAction(
                    QgsAction.GenericPython,
                    "Sketchline",
                    'from QuickOSM.core.actions import Actions;'
                    'Actions.run_sketch_line("[% "network" %]","[% "ref" %]")',
                    False)

            # Add index if possible
            if output_format == "shape":
                new_layer.dataProvider().createSpatialIndex()

            QgsMapLayerRegistry.instance().addMapLayer(new_layer)
            num_layers += 1

    return num_layers


def process_query(
        dialog=None,
        query=None,
        nominatim=None,
        bbox=None,
        output_dir=None,
        prefix_file=None,
        output_geometry_types=None,
        layer_name="OsmQuery",
        white_list_values=None,
        config_outputs=None):
    """execute a query and send the result file to open_file."""

    # Check OGR
    if not is_ogr_version_ok():
        raise GDALVersion

    if not is_osm_driver_enabled():
        raise OsmDriverNotFound

    # Get output's format
    output_format = get_setting('outputFormat')

    # Prepare outputs
    dialog.set_progress_text(tr("QuickOSM", u"Prepare outputs"))

    # Replace Nominatim or BBOX
    query = prepare_query(query=query, nominatim_name=nominatim, extent=bbox)

    # Getting the default overpass api and running the query
    server = get_setting('defaultOAPI')
    dialog.set_progress_text(tr("QuickOSM", u"Downloading data from Overpass"))
    QApplication.processEvents()
    connexion_overpass_api = ConnexionOAPI(url=server, output="xml")
    osm_file = connexion_overpass_api.get_file_from_query(query)

    return open_file(
        dialog=dialog,
        osm_file=osm_file,
        output_geom_types=output_geometry_types,
        white_list_column=white_list_values,
        layer_name=layer_name,
        output_format=output_format,
        output_dir=output_dir,
        prefix_file=prefix_file,
        config_outputs=config_outputs)


def process_quick_query(
        dialog=None,
        key=None,
        value=None,
        bbox=None,
        nominatim=None,
        is_around=None,
        distance=None,
        osm_objects=None,
        timeout=25,
        output_directory=None,
        prefix_file=None,
        output_geometry_types=None):
    """
    generate a query and send it to process_query
    """
    # Set the layer name
    layer_name = u''
    for i in [key, value, nominatim]:
        if i:
            layer_name += i + u'_'

    if is_around:
        layer_name += '%s_' % distance

    # Delete last "_"
    layer_name = layer_name[:-1]

    # Building the query
    query_factory = QueryFactory(
        timeout=timeout,
        key=key,
        value=value,
        bbox=bbox,
        is_around=is_around,
        distance=distance,
        nominatim=nominatim,
        osm_objects=osm_objects)
    query = query_factory.make()

    # Call process_query with the new query
    return process_query(
        dialog=dialog,
        query=query,
        nominatim=nominatim,
        bbox=bbox,
        output_dir=output_directory,
        prefix_file=prefix_file,
        output_geometry_types=output_geometry_types,
        layer_name=layer_name)
