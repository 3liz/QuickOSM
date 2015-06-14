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

from PyQt4.QtGui import QDockWidget, QApplication, QCompleter, QDialogButtonBox
from PyQt4.QtCore import Qt
from qgis.gui import QgsMessageBar

from QuickOSM.core.exceptions import (
    QuickOsmException,
    OutPutGeomTypesException,
    DirectoryOutPutException,
    OsmObjectsException)
from QuickOSM.core.utilities.utilities_qgis import display_message_bar
from QuickOSM.core.utilities.tools import tr
from QuickOSM.core.query_factory import QueryFactory
from QuickOSM.controller.process import process_quick_query
from QuickOSMWidget import QuickOSMWidget
from quick_query import Ui_ui_quick_query


from qgis.utils import iface


class QuickQueryWidget(QuickOSMWidget, Ui_ui_quick_query):
    # noinspection PyUnresolvedReferences
    def __init__(self, parent=None):
        """
        QuickQueryWidget constructor
        """
        QuickOSMWidget.__init__(self, parent)
        self.setupUi(self)
        
        # Setup UI
        self.label_progress.setText("")
        self.lineEdit_filePrefix.setDisabled(True)
        self.groupBox.setCollapsed(True)
        self.fill_layer_combobox()
        self.groupBox.setCollapsed(True)
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
        self.pushButton_browse_output_file.clicked.connect(
            self.set_output_directory_path)
        self.comboBox_key.editTextChanged.connect(self.key_edited)
        self.lineEdit_browseDir.textEdited.connect(self.disable_prefix_file)
        self.radioButton_extentLayer.toggled.connect(
            self.allow_nominatim_or_extent)
        self.radioButton_extentMapCanvas.toggled.connect(
            self.allow_nominatim_or_extent)
        self.radioButton_place.toggled.connect(self.allow_nominatim_or_extent)
        self.pushButton_refreshLayers.clicked.connect(self.fill_layer_combobox)
        self.pushButton_mapFeatures.clicked.connect(self.open_map_features)
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(
            self.reset_form)
        self.comboBox_in_around.currentIndexChanged.connect(self.in_or_around)
        
        # Setup auto completion
        map_features_json_file = join(
            dirname(dirname(abspath(__file__))), 'mapFeatures.json')

        if isfile(map_features_json_file):
            self.osmKeys = load(open(map_features_json_file))
            keys = self.osmKeys.keys()
            keys.sort()
            keys_completer = QCompleter(keys)
            self.comboBox_key.addItems(keys)
            self.comboBox_key.setCompleter(keys_completer)
            self.comboBox_key.completer().setCompletionMode(
                QCompleter.PopupCompletion)
        self.key_edited()

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
                unicode(self.comboBox_key.currentText())]
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
        self.pushButton_browse_output_file.setDisabled(True)
        self.pushButton_showQuery.setDisabled(True)
        self.start_process()
        QApplication.processEvents()
        
        # Get all values
        key = unicode(self.comboBox_key.currentText())
        value = unicode(self.comboBox_value.currentText())
        nominatim = unicode(self.lineEdit_nominatim.text())
        timeout = self.spinBox_timeout.value()
        output_directory = self.lineEdit_browseDir.text()
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
                isAround=is_around,
                distance=distance,
                bbox=bbox,
                osmObjects=osm_objects,
                timeout=timeout,
                outputDir=output_directory,
                prefixFile=prefix_file,
                outputGeomTypes=output_geometry_types)

            # We can test numLayers to see if there are some results
            if num_layers:
                self.label_progress.setText(
                    tr('QuickOSM', u'Successful query !'))

                display_message_bar(
                    tr('QuickOSM', u'Successful query !'),
                    level=QgsMessageBar.INFO,
                    duration=5)
            else:
                self.label_progress.setText(tr("QuickOSM", u'No result'))

                display_message_bar(
                    tr('QuickOSM', u'Successful query, but no result.'),
                    level=QgsMessageBar.WARNING,
                    duration=7)
        
        except QuickOsmException, e:
            self.display_geo_algorithm_exception(e)
        except Exception, e:
            self.display_exception(e)
        
        finally:
            # Resetting the button
            self.pushButton_browse_output_file.setDisabled(False)
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
        for i in xrange(iface.QuickOSM_mainWindowDialog.stackedWidget.count()):
            widget = iface.QuickOSM_mainWindowDialog.stackedWidget.widget(i)
            if widget.__class__.__name__ == "QueryWidget":
                query_widget = iface.QuickOSM_mainWindowDialog.stackedWidget.\
                    widget(i)
                index_quick_query_widget = i
                break
        
        # Get all values
        key = unicode(self.comboBox_key.currentText())
        value = unicode(self.comboBox_value.currentText())
        nominatim = unicode(self.lineEdit_nominatim.text())
        timeout = self.spinBox_timeout.value()
        output_directory = self.lineEdit_browseDir.text()
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
        query_widget.comboBox_extentLayer.setModel(
            self.comboBox_extentLayer.model())
        
        # Transfer the output
        query_widget.lineEdit_browseDir.setText(output_directory)
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
            isAround=is_around,
            distance=distance,
            osmObjects=osm_objects)
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