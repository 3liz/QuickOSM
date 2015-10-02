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

from os.path import split
from sys import exc_info

from PyQt4.QtGui import QWidget, QFileDialog, QApplication, QDesktopServices
from PyQt4.QtCore import QUrl
from qgis.utils import iface
from qgis.gui import QgsMessageBar
from qgis.core import \
    QgsGeometry, QgsCoordinateTransform, QgsCoordinateReferenceSystem

from QuickOSM.core.utilities.utilities_qgis import display_message_bar
from QuickOSM.core.utilities.tools import tr
from QuickOSM.core.exceptions import NoLayerException


class QuickOSMWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

    def fill_layer_combobox(self):
        """
        Fill the combobox with layers which are in the legend
        """
        layers = iface.legendInterface().layers()
        self.comboBox_extentLayer.clear()
        for layer in layers:
            self.comboBox_extentLayer.addItem(layer.name(), layer.id())

        if self.comboBox_extentLayer.count() < 1:
            self.radioButton_extentLayer.setCheckable(False)
            self.radioButton_extentMapCanvas.setChecked(True)
        else:
            self.radioButton_extentLayer.setCheckable(True)

    def disable_prefix_file(self):
        """
        If the directory is empty, we disable the file prefix
        """
        if self.lineEdit_browseDir.text():
            self.lineEdit_filePrefix.setDisabled(False)
        else:
            self.lineEdit_filePrefix.setText("")
            self.lineEdit_filePrefix.setDisabled(True)

    def set_output_directory_path(self):
        """
        Fill the output directory path
        """
        # noinspection PyTypeChecker
        output_file = QFileDialog.getExistingDirectory(
            None, caption=tr("QuickOSM", 'Select directory'))
        self.lineEdit_browseDir.setText(output_file)
        self.disable_prefix_file()

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
            index = self.comboBox_extentLayer.currentIndex()
            layer_id = self.comboBox_extentLayer.itemData(index)
            layers = iface.legendInterface().layers()
            for layer in layers:
                if layer.id() == layer_id:
                    geom_extent = layer.extent()
                    source_crs = layer.crs()
                    break
            else:
                # the layer could be deleted before
                layer_name = self.comboBox_extentLayer.itemText(index)
                raise NoLayerException(suffix=layer_name)

        geom_extent = QgsGeometry.fromRect(geom_extent)
        epsg_4326 = QgsCoordinateReferenceSystem('EPSG:4326')
        crs_transform = QgsCoordinateTransform(source_crs, epsg_4326)
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
        print(exc_type, f_name, exc_tb.tb_lineno)
        _, _, tb = exc_info()
        import traceback
        traceback.print_tb(tb)
        print e
        display_message_bar(
            tr('QuickOSM', 'Error in the python console, please report it'),
            level=QgsMessageBar.CRITICAL,
            duration=5)

    @staticmethod
    def open_map_features():
        """
        Open MapFeatures
        """
        desktop_service = QDesktopServices()
        desktop_service.openUrl(
            QUrl("http://wiki.openstreetmap.org/wiki/Mapfeatures"))
