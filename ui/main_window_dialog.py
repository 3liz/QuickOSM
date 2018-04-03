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
from QuickOSM.core.utilities.tools import get_setting, set_setting, tr, get_user_query_folder, resources_path
from QuickOSM.ui.main_window import Ui_ui_main_window
from qgis.PyQt.QtCore import pyqtSignal, QUrl
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtGui import QPixmap, QIcon


class MainWindowDialog(QDialog, Ui_ui_main_window):

    # Signal new query
    signal_new_query_successful = pyqtSignal(
        name='signal_new_query_successful')
    signal_delete_query_successful = pyqtSignal(
        name='signal_delete_query_successful')

    def __init__(self, parent=None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)

        # Set icons
        item = self.listWidget.item(0)
        item.setIcon(QIcon(resources_path('quick.png')))
        item = self.listWidget.item(1)
        item.setIcon(QIcon(resources_path('edit.png')))
        item = self.listWidget.item(2)
        item.setIcon(QIcon(resources_path('open.png')))
        item = self.listWidget.item(3)
        item.setIcon(QIcon(resources_path('general.svg')))
        item = self.listWidget.item(4)
        item.setIcon(QIcon(resources_path('info.png')))
        self.label_gnu.setPixmap(QPixmap(resources_path('gnu.png')))

        # Disabled in QGIS3
        # self.set_help_web_view()
        self.restore_queries_group.setVisible(False)
        self.timestamp_group.setVisible(False)

        self.help_file = None

        # Connect
        # noinspection PyUnresolvedReferences
        # self.pushButton_homeHelp.clicked.connect(self.get_root_help) QGIS 3
        # noinspection PyUnresolvedReferences
        # self.pushButton_OAPI_timestamp.clicked.connect(
        #     self.get_timestamp_overpass_api)
        # noinspection PyUnresolvedReferences
        self.comboBox_default_OAPI.currentIndexChanged[int].connect(
            self.set_server_overpass_api)
        self.query.signal_new_query_successful.connect(
            self.signal_new_query_successful.emit)
        # self.my_queries.signal_delete_query_successful.connect(
        #     self.signal_delete_query_successful.emit)
        # noinspection PyUnresolvedReferences
        self.pushButton_restoreQueries.clicked.connect(
            self.restore_default_queries)
        # noinspection PyUnresolvedReferences
        self.radioButton_outputJson.toggled.connect(self.set_output_format)

        # Set settings about the overpass API
        self.defaultServer = get_setting('defaultOAPI')
        if self.defaultServer:
            index = self.comboBox_default_OAPI.findText(self.defaultServer)
            self.comboBox_default_OAPI.setCurrentIndex(index)
        else:
            self.defaultServer = self.comboBox_default_OAPI.currentText()
            set_setting('defaultOAPI', self.defaultServer)

        # Set settings about the output
        self.outputFormat = get_setting('outputFormat')
        if self.outputFormat == "geojson":
            self.radioButton_outputJson.setChecked(True)
        elif self.outputFormat == "shape":
            self.radioButton_outputShape.setChecked(True)
        else:
            set_setting('outputFormat', 'shape')
            self.radioButton_outputShape.setChecked(True)

        # Set minimum width for the menu
        self.listWidget.setMinimumWidth(
            self.listWidget.sizeHintForColumn(0) + 10)

    # def set_help_web_view(self):
    #     """
    #     Set the help
    #     """
    #     locale = QSettings().value("locale/userLocale")[0:2]
    #     locale += "."
    #     help_file_base = "main"
    #     helps = [help_file_base + locale + ".html", help_file_base + ".html"]
    #
    #     doc_path = join(dirname(dirname(abspath(__file__))), 'doc')
    #     for helpFileName in helps:
    #         file_help_path = join(doc_path, helpFileName)
    #         if isfile(file_help_path):
    #             self.help_file = file_help_path
    #             self.webBrowser.load(QUrl(self.help_file))
    #             break
    #     else:
    #         self.webBrowser.setHtml("<h3>Help not available</h3>")

    def get_root_help(self):
        """
        home button set the default help page
        """
        self.webBrowser.load(QUrl(self.help_file))

    # def refresh_my_queries_tree(self):
    #     """
    #     Slot which force the tree to refresh
    #     """
    #     self.my_queries.fill_tree(force=True)

    def set_server_overpass_api(self):
        """
        Save the new OAPI server
        """
        self.defaultServer = self.comboBox_default_OAPI.currentText()
        set_setting('defaultOAPI', self.defaultServer)

    def set_output_format(self):
        """
        Save the new output format
        """
        if self.radioButton_outputJson.isChecked():
            set_setting('outputFormat', 'geojson')
        else:
            set_setting('outputFormat', 'shape')

    def restore_default_queries(self):
        """
        Overwrite all queries
        """
        text = self.pushButton_restoreQueries.text()
        self.pushButton_restoreQueries.setText(tr('QuickOSM', 'Copy ...'))
        get_user_query_folder(over_write=True)
        self.signal_new_query_successful.emit()
        # self.my_queries.fill_tree(force=True)
        self.pushButton_restoreQueries.setText(text)
