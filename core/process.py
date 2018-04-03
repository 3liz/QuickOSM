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
from os.path import dirname, abspath, join, isfile

from QuickOSM.core.api.connexion_oapi import ConnexionOAPI
from QuickOSM.core.exceptions import FileOutPutException
from QuickOSM.core.parser.osm_parser import OsmParser
from QuickOSM.core.query_factory import QueryFactory
from QuickOSM.core.query_parser import prepare_query
from QuickOSM.core.utilities.operating_system import get_default_encoding
from QuickOSM.core.utilities.tools import get_setting
from QuickOSM.core.utilities.tools import tr
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import (
    QgsVectorLayer, QgsVectorFileWriter, QgsAction, QgsProject, QgsWkbTypes)


def open_file(
        dialog=None,
        osm_file=None,
        output_geom_types=None,
        white_list_column=None,
        layer_name="OsmFile",
        config_outputs=None,
        output_dir=None,
        prefix_file=None):
    """
    Open an osm file.

    Memory layer if no output directory is set, or Geojson in the output directory.
    """
    outputs = {}
    if output_dir:
        for layer in ['points', 'lines', 'multilinestrings', 'multipolygons']:
            if not prefix_file:
                prefix_file = layer_name

            outputs[layer] = join(
                output_dir, prefix_file + "_" + layer + ".geojson")

            if isfile(outputs[layer]):
                raise FileOutPutException(suffix='(' + outputs[layer] + ')')

    # Parsing the file
    osm_parser = OsmParser(
        osm_file=osm_file,
        layers=output_geom_types,
        white_list_column=white_list_column)

    osm_parser.signalText.connect(dialog.set_progress_text)
    osm_parser.signalPercentage.connect(dialog.set_progress_percentage)
    layers = osm_parser.parse()

    # Finishing the process with geojson or memory layer
    num_layers = 0

    for i, (layer, item) in enumerate(layers.items()):
        dialog.set_progress_percentage(i / len(layers) * 100)
        QApplication.processEvents()
        if item['featureCount'] and layer in output_geom_types:

            final_layer_name = layer_name
            # If configOutputs is not None (from My Queries)
            if config_outputs:
                if config_outputs[layer]['namelayer']:
                    final_layer_name = config_outputs[layer]['namelayer']

            if output_dir:
                dialog.set_progress_text(tr("QuickOSM", u"From memory to GeoJSON: " + layer))
                # Transforming the vector file
                osm_geometries = {
                    'points': QgsWkbTypes.Point,
                    'lines': QgsWkbTypes.LineString,
                    'multilinestrings': QgsWkbTypes.MultiLineString,
                    'multipolygons': QgsWkbTypes.MultiPolygon}
                memory_layer = item['vector_layer']

                encoding = get_default_encoding()
                writer = QgsVectorFileWriter(
                    outputs[layer],
                    encoding,
                    memory_layer.fields(),
                    osm_geometries[layer],
                    memory_layer.crs(),
                    "GeoJSON")

                for f in memory_layer.getFeatures():
                    writer.addFeature(f)

                del writer

                # Loading the final vector file
                new_layer = QgsVectorLayer(outputs[layer], final_layer_name, "ogr")
            else:
                new_layer = item['vector_layer']
                new_layer.setName(final_layer_name)

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

            QgsProject.instance().addMapLayer(new_layer)
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

    # Prepare outputs
    dialog.set_progress_text(tr("QuickOSM", u"Prepare outputs"))

    # Replace Nominatim or BBOX
    query = prepare_query(query=query, nominatim_name=nominatim, extent=bbox)

    # Getting the default overpass api and running the query
    server = get_setting('defaultOAPI')
    dialog.set_progress_text(tr("QuickOSM", u"Downloading data from Overpass"))
    QApplication.processEvents()
    connexion_overpass_api = ConnexionOAPI(url=server, output="xml")
    osm_file = connexion_overpass_api.query(query)

    return open_file(
        dialog=dialog,
        osm_file=osm_file,
        output_geom_types=output_geometry_types,
        white_list_column=white_list_values,
        layer_name=layer_name,
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
