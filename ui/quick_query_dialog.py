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
from json import load
from os.path import dirname, abspath, join, isfile, isdir

from QuickOSM.core.process import process_quick_query
from QuickOSM.core.exceptions import (
    QuickOsmException,
    OutPutGeomTypesException,
    DirectoryOutPutException,
    OsmObjectsException)
from QuickOSM.core.query_factory import QueryFactory
from QuickOSM.core.utilities.tools import tr
from QuickOSM.core.utilities.utilities_qgis import display_message_bar
from QuickOSM.ui.QuickOSMWidget import QuickOSMWidget
from QuickOSM.ui.quick_query import Ui_ui_quick_query
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QDockWidget, QApplication, QCompleter, \
    QDialogButtonBox
from qgis.core import Qgis
from qgis.utils import iface


class QuickQueryWidget(QuickOSMWidget, Ui_ui_quick_query):
    # noinspection PyUnresolvedReferences
    def __init__(self, parent=None):
        """
        QuickQueryWidget constructor
        """
        QuickOSMWidget.__init__(self, parent)
        self.setupUi(self)
        self.init()

        # Setup UI
        self.label_progress.setText("")
        self.lineEdit_filePrefix.setDisabled(True)
        self.activate_extent_layer()
        self.comboBox_in_around.setDisabled(True)
        self.lineEdit_nominatim.setDisabled(True)
        self.radioButton_extentMapCanvas.setChecked(True)
        self.spinBox_distance_point.setDisabled(True)
        self.label_distance_point.setDisabled(True)

        # Setup in/around combobox
        self.comboBox_in_around.insertItem(0, tr('ui_quick_query', u'In'))
        self.comboBox_in_around.insertItem(1, tr('ui_quick_query', u'Around'))

        # connect
        self.pushButton_runQuery.clicked.connect(self.run_query)
        self.pushButton_showQuery.clicked.connect(self.show_query)
        self.comboBox_key.editTextChanged.connect(self.key_edited)
        self.radioButton_extentLayer.toggled.connect(
            self.allow_nominatim_or_extent)
        self.radioButton_extentMapCanvas.toggled.connect(
            self.allow_nominatim_or_extent)
        self.radioButton_place.toggled.connect(self.allow_nominatim_or_extent)
        self.pushButton_mapFeatures.clicked.connect(self.open_map_features)
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(
            self.reset_form)
        self.comboBox_in_around.currentIndexChanged.connect(self.in_or_around)

        # Setup auto completion
        map_features_json_file = join(
            dirname(dirname(abspath(__file__))), 'mapFeatures.json')

        if isfile(map_features_json_file):
            with open(map_features_json_file) as f:
                self.osmKeys = load(f)
                keys = list(self.osmKeys.keys())
                keys.sort()
                keys_completer = QCompleter(keys)
                self.comboBox_key.addItems(keys)
                self.comboBox_key.setCompleter(keys_completer)
                self.comboBox_key.completer().setCompletionMode(
                    QCompleter.PopupCompletion)
        self.key_edited()

        self.init_nominatim_autofill()

    def reset_form(self):
        self.comboBox_key.setCurrentIndex(0)
        self.lineEdit_nominatim.setText("")
        self.radioButton_place.setChecked(True)
        self.spinBox_distance_point.setValue(1000)
        self.comboBox_in_around.setCurrentIndex(0)
        self.checkBox_points.setChecked(True)
        self.checkBox_lines.setChecked(True)
        self.checkBox_multilinestrings.setChecked(True)
        self.checkBox_multipolygons.setChecked(True)
        self.checkBox_node.setChecked(True)
        self.checkBox_way.setChecked(True)
        self.checkBox_relation.setChecked(True)
        self.spinBox_timeout.setValue(25)
        self.lineEdit_browseDir.setText("")
        self.lineEdit_filePrefix.setText("")

    def key_edited(self):
        """
        Disable show and run buttons if the key is empty
        and add values to the combobox
        """
        if self.comboBox_key.currentText():
            self.pushButton_runQuery.setDisabled(False)
            self.pushButton_showQuery.setDisabled(False)
        else:
            self.pushButton_runQuery.setDisabled(True)
            self.pushButton_showQuery.setDisabled(True)

        self.comboBox_value.clear()
        self.comboBox_value.setCompleter(None)

        try:
            current_values = self.osmKeys[
                str(self.comboBox_key.currentText())]
        except KeyError:
            return
        except AttributeError:
            return

        if current_values[0] != "":
            current_values.insert(0, "")

        values_completer = QCompleter(current_values)
        self.comboBox_value.setCompleter(values_completer)
        self.comboBox_value.addItems(current_values)

    def allow_nominatim_or_extent(self):
        """
        Disable or enable radiobuttons if nominatim or extent
        """

        if self.radioButton_extentMapCanvas.isChecked() or \
                self.radioButton_extentLayer.isChecked():
            self.lineEdit_nominatim.setDisabled(True)
            self.spinBox_distance_point.setDisabled(True)
            self.label_distance_point.setDisabled(True)
            self.comboBox_in_around.setDisabled(True)
        else:
            self.lineEdit_nominatim.setDisabled(False)
            self.comboBox_in_around.setDisabled(False)
            self.in_or_around()

        if self.radioButton_extentLayer.isChecked():
            self.comboBox_extentLayer.setDisabled(False)
        else:
            self.comboBox_extentLayer.setDisabled(True)

    def in_or_around(self):
        """
        Disable the spinbox distance if 'in' or 'around'
        """

        index = self.comboBox_in_around.currentIndex()

        if index == 1:
            self.spinBox_distance_point.setEnabled(True)
            self.label_distance_point.setEnabled(True)
        else:
            self.spinBox_distance_point.setEnabled(False)
            self.label_distance_point.setEnabled(False)

    def _get_osm_objects(self):
        """
        Get a list of osm objects from checkbox

        @return: list of osm objects to query on
        @rtype: list
        """
        osm_objects = []
        if self.checkBox_node.isChecked():
            osm_objects.append('node')
        if self.checkBox_way.isChecked():
            osm_objects.append('way')
        if self.checkBox_relation.isChecked():
            osm_objects.append('relation')
        return osm_objects

    def run_query(self):
        """
        Process for running the query
        """

        # Block the button and save the initial text
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.output_directory.setDisabled(True)
        self.pushButton_showQuery.setDisabled(True)
        self.start_process()
        QApplication.processEvents()

        # Get all values
        key = str(self.comboBox_key.currentText())
        value = str(self.comboBox_value.currentText())
        nominatim = self.nominatim_value()
        timeout = self.spinBox_timeout.value()
        output_directory = self.output_directory.filePath()
        prefix_file = self.lineEdit_filePrefix.text()
        if self.comboBox_in_around.currentIndex() == 1:
            is_around = True
        else:
            is_around = False
        distance = self.spinBox_distance_point.value()

        # Which geometry at the end ?
        output_geometry_types = self.get_output_geometry_types()

        # Which osm objects ?
        osm_objects = self._get_osm_objects()

        try:
            # Test values
            if not osm_objects:
                raise OsmObjectsException

            if not output_geometry_types:
                raise OutPutGeomTypesException

            # If bbox, we must set None to nominatim, we can't have both
            bbox = None
            if self.radioButton_extentLayer.isChecked() or \
                    self.radioButton_extentMapCanvas.isChecked():
                nominatim = None
                bbox = self.get_bounding_box()

            if nominatim == '':
                nominatim = None

            if output_directory and not isdir(output_directory):
                raise DirectoryOutPutException

            num_layers = process_quick_query(
                dialog=self,
                key=key,
                value=value,
                nominatim=nominatim,
                is_around=is_around,
                distance=distance,
                bbox=bbox,
                osm_objects=osm_objects,
                timeout=timeout,
                output_directory=output_directory,
                prefix_file=prefix_file,
                output_geometry_types=output_geometry_types)

            # We can test numLayers to see if there are some results
            if num_layers:
                self.label_progress.setText(
                    tr('QuickOSM', u'Successful query !'))

                display_message_bar(
                    tr('QuickOSM', u'Successful query !'),
                    level=Qgis.Success,
                    duration=5)
            else:
                self.label_progress.setText(tr("QuickOSM", u'No result'))

                display_message_bar(
                    tr('QuickOSM', u'Successful query, but no result.'),
                    level=Qgis.Warning,
                    duration=7)

        except QuickOsmException as e:
            self.display_geo_algorithm_exception(e)
        except Exception as e:  # pylint: disable=broad-except
            self.display_exception(e)

        finally:
            # Resetting the button
            self.output_directory.setDisabled(False)
            self.pushButton_showQuery.setDisabled(False)
            QApplication.restoreOverrideCursor()
            self.end_process()
            QApplication.processEvents()

    def show_query(self):
        """
        Show the query in the main window
        """

        # We have to find the widget in the stacked widget of the main window
        query_widget = None
        index_quick_query_widget = None
        for i in range(iface.QuickOSM_mainWindowDialog.stackedWidget.count()):
            widget = iface.QuickOSM_mainWindowDialog.stackedWidget.widget(i)
            if widget.__class__.__name__ == "QueryWidget":
                query_widget = iface.QuickOSM_mainWindowDialog.stackedWidget.\
                    widget(i)
                index_quick_query_widget = i
                break

        # Get all values
        key = str(self.comboBox_key.currentText())
        value = str(self.comboBox_value.currentText())
        nominatim = str(self.lineEdit_nominatim.text())
        timeout = self.spinBox_timeout.value()
        output_directory = self.output_directory.filePath()
        prefix_file = self.lineEdit_filePrefix.text()
        if self.comboBox_in_around.currentIndex() == 1:
            is_around = True
        else:
            is_around = False
        distance = self.spinBox_distance_point.value()

        # If bbox, we must set None to nominatim, we can't have both
        bbox = None
        if self.radioButton_extentLayer.isChecked() or \
                self.radioButton_extentMapCanvas.isChecked():
            nominatim = None
            bbox = True

        if nominatim == '':
            nominatim = None

        # Which osm objects ?
        osm_objects = self._get_osm_objects()

        # Which geometry at the end ?
        query_widget.checkBox_points.setChecked(
            self.checkBox_points.isChecked())
        query_widget.checkBox_lines.setChecked(
            self.checkBox_lines.isChecked())
        query_widget.checkBox_multilinestrings.setChecked(
            self.checkBox_multilinestrings.isChecked())
        query_widget.checkBox_multipolygons.setChecked(
            self.checkBox_multipolygons.isChecked())

        query_widget.radioButton_extentLayer.setChecked(
            self.radioButton_extentLayer.isChecked())
        query_widget.radioButton_extentMapCanvas.setChecked(
            self.radioButton_extentMapCanvas.isChecked())

        # Transfer the combobox from QuickQuery to Query
        if self.comboBox_extentLayer.count():
            query_widget.radioButton_extentLayer.setCheckable(True)

        # Transfer the output
        query_widget.output_directory.setFilePath(output_directory)
        if prefix_file:
            query_widget.lineEdit_filePrefix.setText(prefix_file)
            query_widget.lineEdit_filePrefix.setEnabled(True)

        # Make the query
        query_factory = QueryFactory(
            timeout=timeout,
            key=key,
            value=value,
            bbox=bbox,
            nominatim=nominatim,
            is_around=is_around,
            distance=distance,
            osm_objects=osm_objects)
        query = query_factory.make()
        query_widget.textEdit_query.setPlainText(query)
        iface.QuickOSM_mainWindowDialog.listWidget.setCurrentRow(
            index_quick_query_widget)
        iface.QuickOSM_mainWindowDialog.exec_()


class QuickQueryDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self, parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.widget = QuickQueryWidget()
        self.setWidget(self.widget)
        self.setWindowTitle(tr("ui_quick_query", "QuickOSM - Quick query"))
