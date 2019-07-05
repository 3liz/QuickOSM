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

import io
import logging
import traceback

from os.path import split, isfile
from sys import exc_info

from qgis.core import (
    Qgis,
    QgsGeometry,
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsCoordinateTransform,
)
from qgis.gui import QgsFileWidget
from qgis.PyQt.QtWidgets import QApplication, QCompleter

from QuickOSM.core.utilities.tools import tr
from QuickOSM.core.utilities.utilities_qgis import display_message_bar
from QuickOSM.definitions.osm import LayerType


LOGGER = logging.getLogger('QuickOSM')


def init_ui(output_directory, advanced_panel=None):
    """Init after the UI is loaded."""
    output_directory.lineEdit().setPlaceholderText(
        tr('Save to temporary file'))
    output_directory.setStorageMode(QgsFileWidget.GetDirectory)
    output_directory.setDialogTitle(tr('Select a directory'))
    output_directory.fileChanged.connect(disable_prefix_file)

    if advanced_panel:
        advanced_panel.setSaveCollapsedState(False)
        advanced_panel.setCollapsed(True)


def init_nominatim_autofill(self):
    """Open the nominatim file and start setting up the completion."""
    # Useful to avoid duplicate if we add a new completer.
    self.lineEdit_nominatim.setCompleter(None)
    self.last_places = []

    if isfile(self.last_nominatim_places_filepath):
        with io.open(
                self.last_nominatim_places_filepath,
                'r',
                encoding='utf8') as f:
            for line in f:
                self.last_places.append(line.rstrip('\n'))

            nominatim_completer = QCompleter(self.last_places)
            self.lineEdit_nominatim.setCompleter(nominatim_completer)
            self.lineEdit_nominatim.completer().setCompletionMode(
                QCompleter.PopupCompletion)
    else:
        io.open(self.last_nominatim_places_filepath, 'a').close()


# def sort_nominatim_places(existing_places, place):
#     if place in existing_places:
#         existing_places.pop(existing_places.index(place))
#     existing_places.insert(0, place)
#     return existing_places[:10]
#
#
# def nominatim_value(line_edit, completer, last_places):
#     """Edit the new nominatim file."""
#     value = line_edit.text()
#     new_list = sort_nominatim_places(last_places, value)
#
#     try:
#         with io.open(
#                 self.last_nominatim_places_filepath,
#                 'w',
#                 encoding='utf8') as f:
#             for item in new_list:
#                 f.write('{}\n'.format(item))
#     except UnicodeDecodeError:
#         # The file is corrupted ?
#         # Remove all old places
#         with io.open(
#                 self.last_nominatim_places_filepath,
#                 'w',
#                 encoding='utf8') as f:
#             f.write('\n')
#
#     self.init_nominatim_autofill()
#
#     return value


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


def get_output_geometry_types(points, lines, multilines, polygons):
    """Get all checkbox about outputs and return a list.

    :return: List of layers.
    :rtype: list
    """
    output_geom_types = []
    if points.isChecked():
        output_geom_types.append(LayerType.Points)
    if lines.isChecked():
        output_geom_types.append(LayerType.Lines)
    if multilines.isChecked():
        output_geom_types.append(LayerType.Multilinestrings)
    if polygons.isChecked():
        output_geom_types.append(LayerType.Multipolygons)

    return output_geom_types


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


def get_bounding_box(iface, query_type_combo, extent_layer_combo):
    """Get the geometry of the bbox in WGS84.

    :return: The extent of the query in WGS84.
    :rtype: QgsRectangle
    """
    query_type = query_type_combo.currentData()

    if query_type == 'canvas':
        geom_extent = iface.mapCanvas().extent()
        source_crs = iface.mapCanvas().mapSettings().destinationCrs()
    else:
        # Else if a layer is checked
        layer = extent_layer_combo.currentLayer()
        geom_extent = layer.extent()
        source_crs = layer.crs()

    geom_extent = QgsGeometry.fromRect(geom_extent)
    epsg_4326 = QgsCoordinateReferenceSystem('EPSG:4326')
    crs_transform = QgsCoordinateTransform(
        source_crs, epsg_4326, QgsProject.instance())
    geom_extent.transform(crs_transform)
    return geom_extent.boundingBox()


def start_process(run_button, progress_bar, label_progress):
    """Make some stuff before launching the process."""
    run_button.setDisabled(True)
    run_button.initialText = run_button.text()
    run_button.setText(tr('Running query…'))
    progress_bar.setMinimum(0)
    progress_bar.setMaximum(0)
    progress_bar.setValue(0)
    label_progress.setText('')


def end_process(run_button, progress_bar):
    """Make some stuff after the process."""
    run_button.setDisabled(False)
    run_button.setText(run_button.initialText)
    progress_bar.setMinimum(0)
    progress_bar.setMaximum(100)
    progress_bar.setValue(100)
    QApplication.processEvents()


def set_progress_percentage(label, percent):
    """Slot to update percentage during process."""
    label.setValue(percent)
    QApplication.processEvents()


def set_progress_text(label, text):
    """Slot to update text during process."""
    label.setText(text)
    QApplication.processEvents()


def display_geo_algorithm_exception(exception, label):
    """Display QuickOSM exceptions.

    The label will be set to empty string.
    """
    label.setText("")
    LOGGER.debug(exception.msg)
    display_message_bar(
        exception.msg, level=exception.level, duration=exception.duration)


def display_exception(exception):
    """Display others exceptions."""
    exc_type, _, exc_tb = exc_info()
    f_name = split(exc_tb.tb_frame.f_code.co_filename)[1]
    _, _, tb = exc_info()
    traceback.print_tb(tb)
    LOGGER.critical(
        tr('A critical error occurred, this is the traceback:'))
    LOGGER.critical(exc_type)
    LOGGER.critical(f_name)
    LOGGER.critical(exception)
    LOGGER.critical('\n'.join(traceback.format_tb(tb)))

    display_message_bar(
        tr('Error in the logs, QuickOSM panel, please report it to '
           'GitHub'),
        level=Qgis.Critical,
        open_logs=True,
        duration=10)
