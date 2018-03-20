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
from __future__ import absolute_import

import re
from os.path import isdir

from QuickOSM.controller.process import process_query
from QuickOSM.core.exceptions import (
    QuickOsmException,
    OutPutGeomTypesException,
    DirectoryOutPutException,
    MissingParameterException)
from QuickOSM.core.file_query import FileQuery
from QuickOSM.core.utilities.tools import tr, get_user_query_folder
from QuickOSM.core.utilities.utilities_qgis import display_message_bar
from QuickOSM.ui.QuickOSMWidget import QuickOSMWidget
from QuickOSM.ui.my_queries import Ui_ui_my_queries
from qgis.PyQt.QtCore import pyqtSignal, QFile, Qt
from qgis.PyQt.QtWidgets import QTreeWidgetItem, QMenu, QAction, QMessageBox, \
    QApplication, QDockWidget
from qgis.core import Qgis
from qgis.utils import iface


class MyQueriesWidget(QuickOSMWidget, Ui_ui_my_queries):

    signal_delete_query_successful = pyqtSignal(
        name='signal_delete_query_successful')

    # noinspection PyUnresolvedReferences
    def __init__(self, parent=None):
        """
        MyQueriesWidget constructor
        """
        QuickOSMWidget.__init__(self, parent)
        self.setupUi(self)
        self.current_query = None
        self.config_layer = None

        # Setup UI
        self.label_progress.setText("")
        self.pushButton_runQuery.setDisabled(True)
        self.pushButton_showQuery.setDisabled(True)
        self.groupBox.setDisabled(True)
        self.lineEdit_nominatim.setEnabled(False)
        self.radioButton_extentLayer.setEnabled(False)
        self.radioButton_extentMapCanvas.setEnabled(False)

        self.activate_extent_layer()
        self.fill_tree()
        self.groupBox.setCollapsed(True)

        # Enable autofill on nominatim
        self.init_nominatim_autofill()

        # Connect
        self.pushButton_runQuery.clicked.connect(self.run_query)
        self.pushButton_showQuery.clicked.connect(self.show_query)
        self.pushButton_browse_output_file.clicked.connect(
            self.set_output_directory_path)
        self.lineEdit_browseDir.textEdited.connect(self.disable_prefix_file)
        self.treeQueries.doubleClicked.connect(self.open_and_run_query)
        self.treeQueries.customContextMenuRequested.connect(
            self.show_popup_menu)
        self.treeQueries.clicked.connect(self.open_query)
        self.lineEdit_search.textChanged.connect(self.text_changed)
        self.radioButton_extentLayer.toggled.connect(self.extent_radio)

    def fill_tree(self, force=False):
        """
        Fill the tree with queries

        @param force:To force the tree to refresh.
        @type force: bool
        """

        self.treeQueries.clear()

        # Get the folder and all file queries
        folder = get_user_query_folder()
        categories_files = FileQuery.get_ini_files_from_folder(
            folder, force=force)

        # Fill all categories
        for cat, files in categories_files.items():
            category_item = QTreeWidgetItem([cat], 0)
            self.treeQueries.addTopLevelItem(category_item)
            for one_file in files:
                query_item = TreeQueryItem(category_item, one_file)
                self.treeQueries.addTopLevelItem(query_item)

        self.treeQueries.resizeColumnToContents(0)

    def text_changed(self):
        """
        Update the tree according to the search box
        """
        text = self.lineEdit_search.text().strip(' ').lower()
        self._filter_item(self.treeQueries.invisibleRootItem(), text)
        if text:
            self.treeQueries.expandAll()
        else:
            self.treeQueries.collapseAll()

    def _filter_item(self, item, text):
        """
        search an item in the tree

        @param item: check if the item should be shown
        @type item: QTreeItem

        @param text: text to search
        @type text: str

        @return: show or hide the item
        @rtype: bool
        """
        if item.childCount() > 0:
            show = False
            for i in range(item.childCount()):
                child = item.child(i)
                show_child = self._filter_item(child, text)
                show = show_child or show
            item.setHidden(not show)
            return show
        elif isinstance(item, TreeQueryItem):
            hide = bool(text) and (text not in item.text(0).lower())
            item.setHidden(hide)
            return not hide
        else:
            item.setHidden(True)
            return False

    def show_popup_menu(self, point):
        """
        Right click in the tree

        @param point:Cursor's point
        @type point:QPoint
        """
        item = self.treeQueries.itemAt(point)
        if isinstance(item, TreeQueryItem):
            config = item.query.getContent()

            # We set the query
            self.current_query = config['metadata']['query']

            # We create the menu
            popup_menu = QMenu()
            execute_action = QAction(
                tr('QuickOSM', 'Execute'), self.treeQueries)
            # noinspection PyUnresolvedReferences
            execute_action.triggered.connect(self.open_and_run_query)
            popup_menu.addAction(execute_action)
            show_action = QAction(
                tr('QuickOSM', 'Show query'), self.treeQueries)
            # noinspection PyUnresolvedReferences
            show_action.triggered.connect(self.show_query)
            popup_menu.addAction(show_action)
            delete_action = QAction(
                tr('QuickOSM', 'Delete'), self.treeQueries)
            # noinspection PyUnresolvedReferences
            delete_action.triggered.connect(self.delete_query)
            popup_menu.addAction(delete_action)
            popup_menu.exec_(self.treeQueries.mapToGlobal(point))

    def open_and_run_query(self):
        """
        If we choose "execute" from the right-click menu
        """
        item = self.treeQueries.currentItem()
        if isinstance(item, TreeQueryItem):
            self.open_query()
            self.run_query()

    def open_query(self):
        """
        simple click on the tree
        open the query
        """
        item = self.treeQueries.currentItem()
        if isinstance(item, TreeQueryItem):
            template = item.query.isTemplate()
            if template['bbox']:
                self.radioButton_extentLayer.setEnabled(True)
                self.radioButton_extentMapCanvas.setEnabled(True)
                if self.radioButton_extentLayer.isChecked():
                    self.comboBox_extentLayer.setEnabled(True)
                else:
                    self.comboBox_extentLayer.setEnabled(False)
            else:
                self.radioButton_extentLayer.setEnabled(False)
                self.radioButton_extentMapCanvas.setEnabled(False)

            if template['nominatim']:
                self.lineEdit_nominatim.setEnabled(True)

                if template['nominatimDefaultValue']:
                    self.lineEdit_nominatim.setPlaceholderText(
                        template['nominatimDefaultValue'] + " " +
                        tr('QuickOSM', 'can be overridden'))
                else:
                    self.lineEdit_nominatim.setPlaceholderText(
                        tr("QuickOSM", "A village, a town, ..."))

            else:
                self.lineEdit_nominatim.setEnabled(False)
                self.lineEdit_nominatim.setText("")
                self.lineEdit_nominatim.setPlaceholderText("")

            config = item.query.getContent()
            self.config_layer = config['layers']

            # setup the UI with parameters
            self.checkBox_points.setChecked(
                self.config_layer['points']['load'])
            self.lineEdit_csv_points.setText(
                self.config_layer['points']['columns'])
            self.checkBox_lines.setChecked(
                self.config_layer['lines']['load'])
            self.lineEdit_csv_lines.setText(
                self.config_layer['lines']['columns'])
            self.checkBox_multilinestrings.setChecked(
                self.config_layer['multilinestrings']['load'])
            self.lineEdit_csv_multilinestrings.setText(
                self.config_layer['multilinestrings']['columns'])
            self.checkBox_multipolygons.setChecked(
                self.config_layer['multipolygons']['load'])
            self.lineEdit_csv_multipolygons.setText(
                self.config_layer['multipolygons']['columns'])
            self.current_query = config['metadata']['query']
            self.pushButton_runQuery.setDisabled(False)
            self.pushButton_showQuery.setDisabled(False)
            self.groupBox.setDisabled(False)
        else:
            self.groupBox.setDisabled(True)
            self.pushButton_runQuery.setDisabled(True)
            self.pushButton_showQuery.setDisabled(True)

    def delete_query(self):
        """
        If we want to delete the query from the right-click menu
        """
        item = self.treeQueries.currentItem()
        if isinstance(item, TreeQueryItem):
            # noinspection PyCallByClass,PyTypeChecker
            ret = QMessageBox.warning(
                self,
                "QuickOSM",
                tr("QuickOSM", "Are you sure you want to delete the query ?"),
                QMessageBox.Yes,
                QMessageBox.Cancel)

            if ret == QMessageBox.Yes:
                QFile.remove(item.query.getFilePath())
                QFile.remove(item.query.getQueryFile())
                contents = item.query.getContent()
                layers = contents['layers']
                for layer in layers:
                    if layers[layer]['style']:
                        QFile.remove(layers[layer]['style'])
                self.signal_delete_query_successful.emit()

    def run_query(self):
        """
        Process for running the query
        """
        # Block the button and save the initial text

        self.pushButton_browse_output_file.setDisabled(True)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.start_process()
        QApplication.processEvents()

        # Get all values
        query = self.current_query
        output_directory = self.lineEdit_browseDir.text()
        prefix_file = self.lineEdit_filePrefix.text()
        nominatim = self.nominatim_value()

        # Set the bbox
        bbox = None
        if self.radioButton_extentLayer.isChecked() or \
                self.radioButton_extentMapCanvas.isChecked():
            bbox = self.get_bounding_box()

        # Which geometry at the end ?
        output_geometry_types = self.get_output_geometry_types()
        white_list_values = self.get_white_list_values()

        try:
            # Test values
            if not output_geometry_types:
                raise OutPutGeomTypesException

            if output_directory and not isdir(output_directory):
                raise DirectoryOutPutException

            geocode_area = re.search(r'\{\{nominatim\}\}', query) or \
                re.search(r'\{\{nominatimArea:\}\}', query) or \
                re.search(r'\{\{geocodeArea:\}\}', query)

            if not nominatim and geocode_area:
                raise MissingParameterException(suffix="nominatim field")

            num_layers = process_query(
                dialog=self,
                query=query,
                output_dir=output_directory,
                prefix_file=prefix_file,
                output_geometry_types=output_geometry_types,
                white_list_values=white_list_values,
                nominatim=nominatim,
                bbox=bbox,
                config_outputs=self.config_layer)

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
        query = self.current_query
        output_directory = self.lineEdit_browseDir.text()
        prefix_file = self.lineEdit_filePrefix.text()
        nominatim = self.lineEdit_nominatim.text()

        # If bbox, we must set None to nominatim, we can't have both
        if self.radioButton_extentLayer.isChecked() or \
                self.radioButton_extentMapCanvas.isChecked():
            nominatim = None

        if nominatim == '':
            nominatim = None

        # Which geometry at the end ?
        query_widget.checkBox_points.setChecked(
            self.checkBox_points.isChecked())
        query_widget.lineEdit_csv_points.setText(
            self.lineEdit_csv_points.text())

        query_widget.checkBox_lines.setChecked(
            self.checkBox_lines.isChecked())
        query_widget.lineEdit_csv_lines.setText(
            self.lineEdit_csv_lines.text())

        query_widget.checkBox_multilinestrings.setChecked(
            self.checkBox_multilinestrings.isChecked())
        query_widget.lineEdit_csv_multilinestrings.setText(
            self.lineEdit_csv_multilinestrings.text())

        query_widget.checkBox_multipolygons.setChecked(
            self.checkBox_multipolygons.isChecked())
        query_widget.lineEdit_csv_multipolygons.setText(
            self.lineEdit_csv_multipolygons.text())

        query_widget.radioButton_extentLayer.setChecked(
            self.radioButton_extentLayer.isChecked())
        query_widget.radioButton_extentMapCanvas.setChecked(
            self.radioButton_extentMapCanvas.isChecked())

        # Transfer the combobox from my queries to query
        if self.comboBox_extentLayer.count():
            query_widget.radioButton_extentLayer.setCheckable(True)

        # Transfer parameters
        query_widget.lineEdit_nominatim.setText(nominatim)

        # Transfer the output
        query_widget.lineEdit_browseDir.setText(output_directory)
        if prefix_file:
            query_widget.lineEdit_filePrefix.setText(prefix_file)
            query_widget.lineEdit_filePrefix.setEnabled(True)

        # Transfer the query
        query_widget.textEdit_query.setPlainText(query)
        iface.QuickOSM_mainWindowDialog.listWidget.setCurrentRow(
            index_quick_query_widget)
        iface.QuickOSM_mainWindowDialog.exec_()


class TreeQueryItem(QTreeWidgetItem):
    """
    Class QTreeQueryItem which populate the tree
    """
    def __init__(self, parent, query):
        QTreeWidgetItem.__init__(self, parent)
        self.query = query
        icon = query.getIcon()
        name = query.getName()

        if icon:
            self.setIcon(0, icon)

        self.setToolTip(0, name)
        self.setText(0, name)


class MyQueriesDockWidget(QDockWidget):

    signal_delete_query_successful = pyqtSignal(
        name='signal_delete_query_successful')

    def __init__(self, parent=None):
        QDockWidget.__init__(self, parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(MyQueriesWidget())
        self.setWindowTitle(tr("ui_my_queries", "QuickOSM - My queries"))
        self.widget().signal_delete_query_successful.connect(
            self.signal_delete_query_successful.emit)

    def refresh_my_queries_tree(self):
        """
        Slots which refresh the tree
        """
        self.widget().fill_tree(force=True)
