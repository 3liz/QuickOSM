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
import re
from os.path import isdir

from QuickOSM.controller.process import process_query
from QuickOSM.core.exceptions import (
    QuickOsmException,
    DirectoryOutPutException,
    OutPutGeomTypesException,
    MissingParameterException)
from QuickOSM.core.query_parser import prepare_query
from QuickOSM.core.utilities.tools import tr, resources_path
from QuickOSM.core.utilities.utilities_qgis import display_message_bar
from QuickOSM.ui.QuickOSMWidget import QuickOSMWidget
from QuickOSM.ui.XMLHighlighter import XMLHighlighter
from QuickOSM.ui.query import Ui_ui_query
from QuickOSM.ui.save_query_dialog import SaveQueryDialog
from qgis.PyQt.QtCore import pyqtSignal, Qt, QUrl
from qgis.PyQt.QtGui import QDesktopServices, QIcon
from qgis.PyQt.QtWidgets import QDockWidget, QMenu, QAction, QApplication, \
    QDialogButtonBox
from qgis.core import Qgis


class QueryWidget(QuickOSMWidget, Ui_ui_query):
    # Signal new query
    signal_new_query_successful = pyqtSignal(
        name='signal_new_query_successful')

    # noinspection PyUnresolvedReferences
    def __init__(self, parent=None):
        """
        QueryWidget constructor
        """
        QuickOSMWidget.__init__(self, parent)
        self.setupUi(self)

        # Highlight XML
        self.highlighter = XMLHighlighter(self.textEdit_query.document())

        # QGIS 3
        self.pushButton_saveQuery.setVisible(False)

        # Setup UI
        self.label_progress.setText("")
        self.lineEdit_filePrefix.setDisabled(True)
        self.groupBox.setCollapsed(True)
        self.bbox = None
        self.activate_extent_layer()
        self.groupBox.setCollapsed(True)
        self.pushButton_overpassTurbo.setIcon(QIcon(resources_path('turbo.png')))
        # Disable buttons
        self.pushButton_generateQuery.setDisabled(True)
        self.pushButton_saveQuery.setDisabled(True)
        self.pushButton_runQuery.setDisabled(True)

        # Setup menu for saving
        popup_menu = QMenu()
        save_final_query_action = QAction(
            tr('QuickOSM', 'Save as final query'), self.pushButton_saveQuery)
        save_final_query_action.triggered.connect(self.save_final_query)
        popup_menu.addAction(save_final_query_action)
        save_template_query_action = QAction(
            tr('QuickOSM', 'Save as template'), self.pushButton_saveQuery)
        save_template_query_action.triggered.connect(self.save_template_query)
        popup_menu.addAction(save_template_query_action)
        self.pushButton_saveQuery.setMenu(popup_menu)

        # Setup menu for documentation
        popup_menu = QMenu()
        map_features_action = QAction(
            'Map Features', self.pushButton_documentation)
        map_features_action.triggered.connect(self.open_map_features)
        popup_menu.addAction(map_features_action)
        overpass_action = QAction('Overpass', self.pushButton_documentation)
        overpass_action.triggered.connect(self.open_doc_overpass)
        popup_menu.addAction(overpass_action)
        self.pushButton_documentation.setMenu(popup_menu)

        # Enable autofill on nominatim
        self.init_nominatim_autofill()

        # connect
        self.pushButton_runQuery.clicked.connect(self.run_query)
        self.pushButton_generateQuery.clicked.connect(self.generate_query)
        self.pushButton_browse_output_file.clicked.connect(
            self.set_output_directory_path)
        self.lineEdit_browseDir.textEdited.connect(self.disable_prefix_file)
        self.textEdit_query.cursorPositionChanged.connect(
            self.highlighter.rehighlight)
        self.textEdit_query.cursorPositionChanged.connect(
            self.allow_nominatim_or_extent)
        self.radioButton_extentLayer.toggled.connect(self.extent_radio)
        self.pushButton_overpassTurbo.clicked.connect(self.open_overpass_turbo)
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(
            self.reset_form)

    def reset_form(self):
        self.textEdit_query.setText("")
        self.lineEdit_nominatim.setText("")
        self.checkBox_points.setChecked(True)
        self.checkBox_lines.setChecked(True)
        self.checkBox_multilinestrings.setChecked(True)
        self.checkBox_multipolygons.setChecked(True)
        self.lineEdit_csv_points.setText("")
        self.lineEdit_csv_lines.setText("")
        self.lineEdit_csv_multilinestrings.setText("")
        self.lineEdit_csv_multipolygons.setText("")
        self.lineEdit_browseDir.setText("")
        self.lineEdit_filePrefix.setText("")

    def allow_nominatim_or_extent(self):
        """
        Disable or enable radio buttons if nominatim or extent
        Disable buttons if the query is empty
        """

        query = str(self.textEdit_query.toPlainText())

        if not query:
            self.pushButton_generateQuery.setDisabled(True)
            self.pushButton_saveQuery.setDisabled(True)
            self.pushButton_runQuery.setDisabled(True)
        else:
            self.pushButton_generateQuery.setDisabled(False)
            self.pushButton_saveQuery.setDisabled(False)
            self.pushButton_runQuery.setDisabled(False)

        if re.search(r'\{\{nominatim\}\}', query) or \
                re.search(r'\{\{nominatimArea:(.*)\}\}', query) or \
                re.search(r'\{\{geocodeArea:(.*)\}\}', query):
            self.lineEdit_nominatim.setEnabled(True)
        else:
            self.lineEdit_nominatim.setEnabled(False)
            self.lineEdit_nominatim.setText("")

        if re.search(r'\{\{(bbox|center)\}\}', query):
            self.radioButton_extentLayer.setEnabled(True)
            self.radioButton_extentMapCanvas.setEnabled(True)
            if self.radioButton_extentLayer.isChecked():
                self.comboBox_extentLayer.setEnabled(True)
            else:
                self.comboBox_extentLayer.setEnabled(False)
        else:
            self.radioButton_extentLayer.setEnabled(False)
            self.radioButton_extentMapCanvas.setEnabled(False)
            self.comboBox_extentLayer.setEnabled(False)

    def run_query(self):
        """
        Process for running the query
        """

        # Block the button and save the initial text
        self.pushButton_browse_output_file.setDisabled(True)
        self.pushButton_generateQuery.setDisabled(True)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.start_process()
        QApplication.processEvents()

        # Get all values
        query = str(self.textEdit_query.toPlainText())
        output_directory = self.lineEdit_browseDir.text()
        prefix_file = self.lineEdit_filePrefix.text()
        nominatim = self.nominatim_value()

        # Set bbox
        bbox = None
        if self.radioButton_extentLayer.isChecked() or \
                self.radioButton_extentMapCanvas.isChecked():
            bbox = self.get_bounding_box()

        # Check nominatim
        if nominatim == '':
            nominatim = None

        # Which geometry at the end ?
        output_geometry_types = self.get_output_geometry_types()
        white_list_values = self.get_white_list_values()

        try:
            # Test values
            if not output_geometry_types:
                raise OutPutGeomTypesException

            if output_directory and not isdir(output_directory):
                raise DirectoryOutPutException

            if not nominatim and \
                    re.search(r'\{\{nominatim\}\}', query) or \
                    re.search(r'\{\{nominatimArea:\}\}', query) or \
                    re.search(r'\{\{geocodeArea:\}\}', query):

                raise MissingParameterException(suffix="nominatim field")

            num_layers = process_query(
                dialog=self,
                query=query,
                output_dir=output_directory,
                prefix_file=prefix_file,
                output_geometry_types=output_geometry_types,
                white_list_values=white_list_values,
                nominatim=nominatim,
                bbox=bbox)

            if num_layers:
                display_message_bar(
                    tr('QuickOSM', u'Successful query !'),
                    level=Qgis.Info,
                    duration=5)
                self.label_progress.setText(
                    tr('QuickOSM', u'Successful query !'))
            else:
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
            self.pushButton_browse_output_file.setDisabled(False)
            self.pushButton_generateQuery.setDisabled(False)
            QApplication.restoreOverrideCursor()
            self.end_process()
            QApplication.processEvents()

    def generate_query(self):
        """
        Transform the template to query "out of the box"
        """

        query = str(self.textEdit_query.toPlainText())
        nominatim = str(self.lineEdit_nominatim.text())
        bbox = self.get_bounding_box()
        query = prepare_query(
            query=query, extent=bbox, nominatim_name=nominatim)
        self.textEdit_query.setPlainText(query)

    def save_final_query(self):
        """
        Save the query without any templates, usefull for bbox
        """

        # Which geometry at the end ?
        output_geometry_types = self.get_output_geometry_types()
        white_list_values = self.get_white_list_values()

        query = str(self.textEdit_query.toPlainText())
        nominatim = str(self.lineEdit_nominatim.text())
        bbox = self.get_bounding_box()

        # Delete any templates
        query = prepare_query(
            query=query, extent=bbox, nominatim_name=nominatim)

        # Save the query
        save_query_dialog = SaveQueryDialog(
            query=query,
            output_geometry_types=output_geometry_types,
            white_list_values=white_list_values)
        save_query_dialog.signal_new_query_successful.connect(
            self.signal_new_query_successful.emit)
        save_query_dialog.exec_()

    def save_template_query(self):
        """
        Save the query with templates if some are presents
        """

        # Which geometry at the end ?
        output_geometry_types = self.get_output_geometry_types()
        white_list_values = self.get_white_list_values()

        query = str(self.textEdit_query.toPlainText())

        # save the query
        save_query_dialog = SaveQueryDialog(
            query=query,
            output_geometry_types=output_geometry_types,
            white_list_values=white_list_values)
        save_query_dialog.signal_new_query_successful.connect(
            self.signal_new_query_successful.emit)
        save_query_dialog.exec_()

    @staticmethod
    def open_overpass_turbo():
        """
        Open Overpass Turbo
        """
        desktop_service = QDesktopServices()
        desktop_service.openUrl(QUrl("http://overpass-turbo.eu/"))

    @staticmethod
    def open_doc_overpass():
        """
        Open Overpass's documentation
        """
        url = "http://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide"
        desktop_service = QDesktopServices()
        desktop_service.openUrl(QUrl(url))


class QueryDockWidget(QDockWidget):
    signal_new_query_successful = pyqtSignal(
        name='signal_new_query_successful')

    def __init__(self, parent=None):
        QDockWidget.__init__(self, parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(QueryWidget())
        self.setWindowTitle(tr("ui_query", "QuickOSM - Query"))
        self.widget().signal_new_query_successful.connect(
            self.signal_new_query_successful.emit)
