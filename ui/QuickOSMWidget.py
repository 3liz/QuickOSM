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
import logging
from os.path import split, join, isfile
from sys import exc_info

from QuickOSM.core.utilities.tools import tr, quickosm_user_folder
from QuickOSM.core.utilities.utilities_qgis import display_message_bar
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtGui import QDesktopServices
from qgis.PyQt.QtWidgets import QWidget, QFileDialog, QApplication, QCompleter
from qgis.core import (
    QgsGeometry,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem,
    QgsProject,
    Qgis,
)
from qgis.gui import QgsFileWidget
from qgis.utils import iface

LOGGER = logging.getLogger('QuickOSM')


class QuickOSMWidget(QWidget):
    def __init__(self, parent=None):
        self.last_places = []
        self.last_nominatim_places_filepath = join(
            quickosm_user_folder(),
            'nominatim.txt')
        QWidget.__init__(self, parent)

        project = QgsProject.instance()
        project.layersAdded.connect(self.activate_extent_layer)
        project.layersRemoved.connect(self.activate_extent_layer)

    def init(self):
        """Init after the UI is loaded."""
        self.output_directory.lineEdit().setPlaceholderText(tr('QuickOSM', 'Save to temporary file'))
        self.output_directory.setStorageMode(QgsFileWidget.GetDirectory)
        self.output_directory.setDialogTitle(tr('QuickOSM', 'Select a directory'))
        self.output_directory.fileChanged.connect(self.disable_prefix_file)

        try:
            self.advanced.setSaveCollapsedState(False)
            self.advanced.setCollapsed(True)
        except AttributeError:
            # OSM File widget does not have this QgsGroupBox
            pass

    def init_nominatim_autofill(self):

        # Usefull to avoid duplicate if we add a new completer.
        self.lineEdit_nominatim.setCompleter(None)
        self.last_places = []

        if isfile(self.last_nominatim_places_filepath):
            last = open(self.last_nominatim_places_filepath, 'r')
            for line in last:
                self.last_places.append(line.rstrip('\n'))

            nominatim_completer = QCompleter(self.last_places)
            self.lineEdit_nominatim.setCompleter(nominatim_completer)
            self.lineEdit_nominatim.completer().setCompletionMode(
                QCompleter.PopupCompletion)
            last.close()
        else:
            open(self.last_nominatim_places_filepath, 'a').close()

    @staticmethod
    def sort_nominatim_places(existing_places, place):
        if place in existing_places:
            existing_places.pop(existing_places.index(place))
        existing_places.insert(0, place)
        return existing_places[:10]

    def nominatim_value(self):
        value = str(self.lineEdit_nominatim.text())
        new_list = self.sort_nominatim_places(self.last_places, value)

        f = open(self.last_nominatim_places_filepath, 'w')
        for item in new_list:
            f.write('%s\n' % item)
        f.close()

        self.init_nominatim_autofill()

        return value

    def activate_extent_layer(self):
        """Activate or deactivate the radio button about the extent layer."""
        try:
            if self.comboBox_extentLayer.count() < 1:
                self.radioButton_extentLayer.setCheckable(False)
                self.radioButton_extentMapCanvas.setChecked(True)
            else:
                self.radioButton_extentLayer.setCheckable(True)
        except AttributeError:
            pass

    def disable_prefix_file(self):
        """
        If the directory is empty, we disable the file prefix
        """
        if self.output_directory.filePath():
            self.lineEdit_filePrefix.setDisabled(False)
        else:
            self.lineEdit_filePrefix.setText("")
            self.lineEdit_filePrefix.setDisabled(True)

    def extent_radio(self):
        """
        Disable or enable the combox box
        """
        if self.radioButton_extentLayer.isChecked():
            self.comboBox_extentLayer.setDisabled(False)
        else:
            self.comboBox_extentLayer.setDisabled(True)

    def get_output_geometry_types(self):
        """
        Get all checkbox about outputs and return a list

        @rtype: list
        @return: list of layers
        """
        output_geom_types = []
        if self.checkBox_points.isChecked():
            output_geom_types.append('points')
        if self.checkBox_lines.isChecked():
            output_geom_types.append('lines')
        if self.checkBox_multilinestrings.isChecked():
            output_geom_types.append('multilinestrings')
        if self.checkBox_multipolygons.isChecked():
            output_geom_types.append('multipolygons')
        return output_geom_types

    def get_white_list_values(self):
        """
        Get all line edits about columns for each layers and return a dic

        @rtype: dic
        @return: doc of layers with columns
        """
        white_list_values = {}
        if self.checkBox_points.isChecked():
            white_list_values['points'] = self.lineEdit_csv_points.text()
        if self.checkBox_lines.isChecked():
            white_list_values['lines'] = self.lineEdit_csv_lines.text()
        if self.checkBox_multilinestrings.isChecked():
            white_list_values['multilinestrings'] = \
                self.lineEdit_csv_multilinestrings.text()
        if self.checkBox_multipolygons.isChecked():
            white_list_values['multipolygons'] = \
                self.lineEdit_csv_multipolygons.text()
        return white_list_values

    def get_bounding_box(self):
        """
        Get the geometry of the bbox in WGS84

        @rtype: QGsRectangle in WGS84
        @return: the extent of the map canvas
        """

        # If mapCanvas is checked
        if self.radioButton_extentMapCanvas.isChecked():
            geom_extent = iface.mapCanvas().extent()
            if hasattr(iface.mapCanvas(), "mapSettings"):
                source_crs = iface.mapCanvas().mapSettings().destinationCrs()
            else:
                source_crs = iface.mapCanvas().mapRenderer().destinationCrs()
        else:
            # Else if a layer is checked
            layer = self.comboBox_extentLayer.currentLayer()
            geom_extent = layer.extent()
            source_crs = layer.crs()

        geom_extent = QgsGeometry.fromRect(geom_extent)
        epsg_4326 = QgsCoordinateReferenceSystem('EPSG:4326')
        crs_transform = QgsCoordinateTransform(
            source_crs, epsg_4326, QgsProject.instance())
        geom_extent.transform(crs_transform)
        return geom_extent.boundingBox()

    def start_process(self):
        """
        Make some stuff before launching the process
        """
        self.pushButton_runQuery.setDisabled(True)
        self.pushButton_runQuery.initialText = self.pushButton_runQuery.text()
        self.pushButton_runQuery.setText(tr('QuickOSM', 'Running query ...'))
        self.progressBar_execution.setMinimum(0)
        self.progressBar_execution.setMaximum(0)
        self.progressBar_execution.setValue(0)
        self.label_progress.setText('')

    def end_process(self):
        """
        Make some stuff after the process
        """
        self.pushButton_runQuery.setDisabled(False)
        self.pushButton_runQuery.setText(self.pushButton_runQuery.initialText)
        self.progressBar_execution.setMinimum(0)
        self.progressBar_execution.setMaximum(100)
        self.progressBar_execution.setValue(100)
        QApplication.processEvents()

    def set_progress_percentage(self, percent):
        """
        Slot to update percentage during process
        """
        self.progressBar_execution.setValue(percent)
        QApplication.processEvents()

    def set_progress_text(self, text):
        """
        Slot to update text during process
        """
        self.label_progress.setText(text)
        QApplication.processEvents()

    def display_geo_algorithm_exception(self, e):
        """
        Display quickosm exceptions
        """
        self.label_progress.setText("")
        display_message_bar(e.msg, level=e.level, duration=e.duration)

    @staticmethod
    def display_exception(e):
        """
        Display others exceptions
        """
        exc_type, _, exc_tb = exc_info()
        f_name = split(exc_tb.tb_frame.f_code.co_filename)[1]
        _, _, tb = exc_info()
        import traceback
        traceback.print_tb(tb)
        LOGGER.critical(exc_type)
        LOGGER.critical(f_name)
        LOGGER.critical(str(e))
        LOGGER.critical(traceback.format_tb(tb))

        display_message_bar(
            tr('QuickOSM',
               'Error in the QGIS Logs, QuickOSM panel, please report it to '
               '<a href="https://github.com/3liz/QuickOSM/issues/new?'
               'template=1_BUG_REPORT.md">GitHub</a>'),
            level=Qgis.Critical,
            duration=10)

    @staticmethod
    def open_map_features():
        """
        Open MapFeatures
        """
        desktop_service = QDesktopServices()
        desktop_service.openUrl(
            QUrl("http://wiki.openstreetmap.org/wiki/Mapfeatures"))
