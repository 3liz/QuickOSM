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

from QuickOSM.core.process import process_query
from QuickOSM.core.exceptions import (
    QuickOsmException,
    DirectoryOutPutException,
    OutPutGeomTypesException,
    MissingParameterException)
from QuickOSM.core.query_preparation import QueryPreparation
from QuickOSM.core.utilities.tools import tr, resources_path
from QuickOSM.core.utilities.utilities_qgis import (
    display_message_bar,
    open_map_features,
    open_overpass_turbo,
    open_doc_overpass,
)
from QuickOSM.ui.QuickOSMWidget import QuickOSMWidget
from QuickOSM.ui.XMLHighlighter import XMLHighlighter
from QuickOSM.ui.query import Ui_ui_query
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QMenu, QAction, QApplication, \
    QDialogButtonBox
from qgis.core import Qgis


class QueryWidget(QuickOSMWidget, Ui_ui_query):

    # noinspection PyUnresolvedReferences
    def __init__(self, parent=None):
        """
        QueryWidget constructor
        """
        QuickOSMWidget.__init__(self, parent)
        self.setupUi(self)
        self.init()

        # Highlight XML
        self.highlighter = XMLHighlighter(self.textEdit_query.document())

        # QGIS 3
        self.pushButton_saveQuery.setVisible(False)

        # Setup UI
        self.cb_query_type.addItem(tr('Canvas Extent'), 'canvas')
        self.cb_query_type.addItem(tr('Layer Extent'), 'layer')
        self.cb_query_type.currentIndexChanged.connect(self.query_type_updated)

        self.label_progress.setText("")
        self.lineEdit_filePrefix.setDisabled(True)
        self.bbox = None
        # self.activate_extent_layer()
        self.pushButton_overpassTurbo.setIcon(
            QIcon(resources_path('icons', 'turbo.png')))
        # Disable buttons
        self.pushButton_generateQuery.setDisabled(True)
        self.pushButton_saveQuery.setDisabled(True)
        self.pushButton_runQuery.setDisabled(True)

        # Setup menu for saving
        popup_menu = QMenu()
        save_final_query_action = QAction(
            tr('Save as final query'), self.pushButton_saveQuery)
        # save_final_query_action.triggered.connect(self.save_final_query)
        popup_menu.addAction(save_final_query_action)
        save_template_query_action = QAction(
            tr('Save as template'), self.pushButton_saveQuery)
        # save_template_query_action.triggered.connect(self.save_template_query)
        popup_menu.addAction(save_template_query_action)
        self.pushButton_saveQuery.setMenu(popup_menu)

        # Setup menu for documentation
        popup_menu = QMenu()
        map_features_action = QAction(
            'Map Features', self.pushButton_documentation)
        map_features_action.triggered.connect(open_map_features)
        popup_menu.addAction(map_features_action)
        overpass_action = QAction('Overpass', self.pushButton_documentation)
        overpass_action.triggered.connect(open_doc_overpass)
        popup_menu.addAction(overpass_action)
        self.pushButton_documentation.setMenu(popup_menu)

        # Enable autofill on nominatim
        self.init_nominatim_autofill()

        # connect
        self.pushButton_runQuery.clicked.connect(self.run_query)
        self.pushButton_generateQuery.clicked.connect(self.generate_query)
        self.textEdit_query.cursorPositionChanged.connect(
            self.highlighter.rehighlight)
        self.textEdit_query.cursorPositionChanged.connect(
            self.allow_nominatim_or_extent)
        self.pushButton_overpassTurbo.clicked.connect(open_overpass_turbo)
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(
            self.reset_form)

        self.query_type_updated()

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

        query = self.textEdit_query.toPlainText()

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
            self.cb_query_type.setEnabled(True)
        else:
            self.cb_query_type.setEnabled(False)

    def run_query(self):
        """
        Process for running the query
        """

        # Block the button and save the initial text
        self.output_directory.setDisabled(True)
        self.pushButton_generateQuery.setDisabled(True)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.start_process()
        QApplication.processEvents()

        # Get all values
        query = self.textEdit_query.toPlainText()
        output_directory = self.output_directory.filePath()
        prefix_file = self.lineEdit_filePrefix.text()
        nominatim = self.nominatim_value()

        # Set bbox
        bbox = None
        if self.cb_query_type.isEnabled():
            query_type = self.cb_query_type.currentData()
            if query_type in ['layer', 'canvas']:
                nominatim = None
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
                area=nominatim,
                bbox=bbox)

            if num_layers:
                display_message_bar(
                    tr('Successful query'),
                    level=Qgis.Success,
                    duration=5)
                self.label_progress.setText(
                    tr('Successful query'))
            else:
                display_message_bar(
                    tr('Successful query, but no result.'),
                    level=Qgis.Warning,
                    duration=7)

        except QuickOsmException as e:
            self.display_geo_algorithm_exception(e)
            pass
        except Exception as e:  # pylint: disable=broad-except
            self.display_exception(e)
            pass

        finally:
            # Resetting the button
            self.output_directory.setDisabled(False)
            self.pushButton_generateQuery.setDisabled(False)
            QApplication.restoreOverrideCursor()
            self.end_process()
            QApplication.processEvents()

    def generate_query(self):
        """
        Transform the template to query "out of the box"
        """

        query = self.textEdit_query.toPlainText()
        nominatim = self.lineEdit_nominatim.text()
        bbox = self.get_bounding_box()
        query = QueryPreparation(query, bbox, nominatim)
        query_string = query.prepare_query()
        self.textEdit_query.setPlainText(query_string)
