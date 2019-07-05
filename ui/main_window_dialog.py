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
from json import load
from os.path import join, isfile
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox, QCompleter
from qgis.PyQt.QtGui import QPixmap, QIcon
from QuickOSM.definitions.overpass import OVERPASS_SERVERS
from QuickOSM.core.utilities.tools import (
    get_setting, set_setting, resources_path, quickosm_user_folder, tr
)

FORM_CLASS, _ = uic.loadUiType(resources_path('ui', 'main_window.ui'))
LOGGER = logging.getLogger('QuickOSM')


class MainDialog(QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)

        # self variable
        self.defaultServer = None
        self.last_places = []
        self.last_nominatim_places_filepath = join(
            quickosm_user_folder(), 'nominatim.txt')

        self.set_ui_menu()
        self.set_ui_configuration_panel()

    def set_ui_menu(self):
        """Set UI related to window and menus."""
        item = self.listWidget.item(0)
        item.setIcon(QIcon(resources_path('icons', 'quick.png')))
        item = self.listWidget.item(1)
        item.setIcon(QIcon(resources_path('icons', 'edit.png')))
        item = self.listWidget.item(2)
        item.setIcon(QIcon(resources_path('icons', 'open.png')))
        item = self.listWidget.item(3)
        item.setIcon(QIcon(resources_path('icons', 'general.svg')))
        item = self.listWidget.item(4)
        item.setIcon(QIcon(resources_path('icons', 'info.png')))
        self.label_gnu.setPixmap(QPixmap(resources_path('icons', 'gnu.png')))

        # Set minimum width for the menu
        self.listWidget.setMinimumWidth(
            self.listWidget.sizeHintForColumn(0) + 10)

    # ###
    # configuration panel
    # ###

    def set_ui_configuration_panel(self):
        """Set UI related the configuration panel."""
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

        for server in OVERPASS_SERVERS:
            self.comboBox_default_OAPI.addItem(server)

        # Read the config file
        custom_config = join(quickosm_user_folder(), 'custom_config.json')
        if isfile(custom_config):
            with open(custom_config) as f:
                config_json = load(f)
                for server in config_json.get('overpass_servers'):
                    if server not in OVERPASS_SERVERS:
                        LOGGER.info(
                            'Custom overpass server list added: {}'.format(
                                server))
                        self.comboBox_default_OAPI.addItem(server)

    def set_server_overpass_api(self):
        """
        Save the new OAPI server
        """
        self.defaultServer = self.comboBox_default_OAPI.currentText()
        set_setting('defaultOAPI', self.defaultServer)

    # ###
    # quick query panel
    # ###
    def set_ui_quick_query_panel(self):
        # Query type
        self.cb_query_type.addItem(tr('In'), 'in')
        self.cb_query_type.addItem(tr('Around'), 'around')
        self.cb_query_type.addItem(tr('Canvas Extent'), 'canvas')
        self.cb_query_type.addItem(tr('Layer Extent'), 'layer')
        self.cb_query_type.addItem(tr('Not Spatial'), 'attributes')

        # self.cb_query_type.setItemIcon(
        #   0, QIcon(resources_path('in.svg')))
        # self.cb_query_type.setItemIcon(
        #   1, QIcon(resources_path('around.svg')))
        # self.cb_query_type.setItemIcon(
        #   2, QIcon(resources_path('map_canvas.svg')))
        # self.cb_query_type.setItemIcon(
        #   3, QIcon(resources_path('extent.svg')))
        # self.cb_query_type.setItemIcon(
        #   4, QIcon(resources_path('mIconTableLayer.svg')))

        self.cb_query_type.currentIndexChanged.connect(self.query_type_updated)

        self.label_progress.setText("")
        self.lineEdit_filePrefix.setDisabled(True)
        # self.activate_extent_layer()

        # connect
        self.pushButton_runQuery.clicked.connect(self.run_query)
        self.pushButton_showQuery.clicked.connect(self.show_query)
        self.comboBox_key.editTextChanged.connect(self.key_edited)
        self.pushButton_mapFeatures.clicked.connect(self.open_map_features)
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(
            self.reset_form)

        # Setup auto completion
        map_features_json_file = resources_path('json', 'map_features.json')

        if isfile(map_features_json_file):
            with open(map_features_json_file) as f:
                self.osmKeys = load(f)
                keys = list(self.osmKeys.keys())
                keys.append('')  # All keys request #118
                keys.sort()
                keys_completer = QCompleter(keys)
                self.comboBox_key.addItems(keys)
                self.comboBox_key.setCompleter(keys_completer)
                self.comboBox_key.completer().setCompletionMode(
                    QCompleter.PopupCompletion)
                self.comboBox_key.lineEdit().setPlaceholderText(
                    tr('Query on all keys'))

        self.comboBox_value.lineEdit().setPlaceholderText(
            tr('Query on all values'))
        self.key_edited()

        self.query_type_updated()
        self.init_nominatim_autofill()

    # ###
    # query panel
    # ###

    # ###
    # osm file panel
    # ###
