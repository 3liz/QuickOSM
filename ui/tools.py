"""
/***************************************************************************
 QuickOSM
 A QGIS plugin
 OSM Overpass API frontend
                             -------------------
        begin                : 2019-07-05
        copyright            : (C) 2019 by 3Liz
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

import logging

from QuickOSM.definitions.osm import LayerType


LOGGER = logging.getLogger('QuickOSM')


def disable_prefix_file(directory, file_prefix):
    """If the directory is empty, we disable the file prefix."""
    if directory.filePath():
        file_prefix.setDisabled(False)
    else:
        file_prefix.setText('')
        file_prefix.setDisabled(True)


def query_type_updated(combo_query_type, stacked_widget, spinbox):
    """Enable/disable the extent widget."""
    current = combo_query_type.currentData()

    if combo_query_type.count() == 2:
        # Query tab
        combo_query_type.setVisible(current == 'layer')
    else:
        # Quick query tab
        if current in ['in', 'around']:
            stacked_widget.setCurrentIndex(0)
            spinbox.setVisible(current == 'around')
        elif current in ['layer']:
            stacked_widget.setCurrentIndex(1)
        elif current in ['canvas', 'attributes']:
            stacked_widget.setCurrentIndex(2)


def get_white_list_values(
        points, points_csv,
        lines, lines_csv,
        multilines, multilines_csv,
        polygons, polygons_csv):
    """Get all line edits about columns for each layers and return a dic

    :return: Definition of layers with columns.
    :rtype: dict
    """
    white_list_values = {}
    if points.isChecked():
        white_list_values[LayerType.Points] = points_csv.text()
    if lines.isChecked():
        white_list_values[LayerType.Lines] = lines_csv.text()
    if multilines.isChecked():
        white_list_values[LayerType.Multilinestrings] = multilines_csv.text()
    if polygons.isChecked():
        white_list_values[LayerType.Multipolygons] = polygons_csv.text()

    return white_list_values
