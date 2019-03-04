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
from QuickOSM.core.utilities.tools import get_setting, set_setting, resources_path
from QuickOSM.ui.main_window import Ui_ui_main_window
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtGui import QPixmap, QIcon


class MainWindowDialog(QDialog, Ui_ui_main_window):

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

        # Set settings about the overpass API
        self.defaultServer = get_setting('defaultOAPI')
        if self.defaultServer:
            index = self.comboBox_default_OAPI.findText(self.defaultServer)
            self.comboBox_default_OAPI.setCurrentIndex(index)
        else:
            self.defaultServer = self.comboBox_default_OAPI.currentText()
            set_setting('defaultOAPI', self.defaultServer)

        # Set minimum width for the menu
        self.listWidget.setMinimumWidth(
            self.listWidget.sizeHintForColumn(0) + 10)

    def get_root_help(self):
        """
        home button set the default help page
        """
        self.webBrowser.load(QUrl(self.help_file))

    def set_server_overpass_api(self):
        """
        Save the new OAPI server
        """
        self.defaultServer = self.comboBox_default_OAPI.currentText()
        set_setting('defaultOAPI', self.defaultServer)
