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
import urllib.request
from json import load
from os.path import dirname, join, exists, isfile

from QuickOSM.definitions.overpass import OVERPASS_SERVERS
from QuickOSM.core.custom_logging import setup_logger
# from QuickOSM.quick_osm_processing.algorithm_provider import (
#     QuickOSMAlgorithmProvider)
from QuickOSM.core.utilities.tools import (
    get_current_version,
    get_setting,
    set_setting,
    new_queries_available,
    tr,
    quickosm_user_folder,
    get_user_query_folder
)
from QuickOSM.ui.main_window_dialog import MainWindowDialog
from qgis.PyQt.QtCore import QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QMenu, QAction, QPushButton
from qgis.core import Qgis, QgsCoordinateTransform, \
    QgsCoordinateReferenceSystem, QgsProject, QgsSettings

# from processing.core.Processing import Processing

LOGGER = logging.getLogger('QuickOSM')


class QuickOSMPlugin(object):

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        setup_logger('QuickOSM')

        # initialize plugin directory
        self.plugin_dir = dirname(__file__)
        # initialize locale
        # noinspection PyBroadException
        try:
            locale = QgsSettings().value('locale/userLocale', 'en')[0:2]
        except AttributeError:
            # Fallback to english #132
            LOGGER.warning('Fallback to English as default language for the plugin')
            locale = 'en'
        locale_path = join(
            self.plugin_dir,
            'i18n',
            'QuickOSM_{0}.qm'.format(locale))

        if exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Create the folder if it does not exist.
        get_user_query_folder(over_write=True)

        # Add to processing
        # self.provider = QuickOSMAlgorithmProvider()
        # Processing.addProvider(self.provider, True)

        # Add the toolbar
        self.toolbar = self.iface.addToolBar('QuickOSM')
        self.toolbar.setObjectName('QuickOSM')

        self.quickosm_menu = None
        self.vector_menu = None
        self.mainWindowAction = None
        self.osmFileAction = None
        self.osmFileDockWidget = None
        # self.myQueriesAction = None
        # self.myQueriesDockWidget = None
        self.queryAction = None
        self.queryDockWidget = None
        self.quickQueryAction = None
        self.quickQueryDockWidget = None
        self.josmAction = None

    def initGui(self):

        # Setup menu
        self.quickosm_menu = QMenu('QuickOSM')
        self.quickosm_menu.setIcon(
            QIcon(join(dirname(__file__), 'resources', 'QuickOSM.svg')))
        self.vector_menu = self.iface.vectorMenu()
        self.vector_menu.addMenu(self.quickosm_menu)

        # Main window
        self.mainWindowAction = QAction(
            QIcon(join(dirname(__file__), 'resources', 'QuickOSM.svg')),
            'QuickOSM',
            self.iface.mainWindow())
        # noinspection PyUnresolvedReferences
        self.mainWindowAction.triggered.connect(self.openMainWindow)
        self.toolbar.addAction(self.mainWindowAction)
        self.iface.QuickOSM_mainWindowDialog = MainWindowDialog()

        # Action JOSM
        self.josmAction = QAction(
            QIcon(join(dirname(__file__), 'resources', 'josm_icon.svg')),
            'JOSM Remote',
            self.iface.mainWindow())
        self.josmAction.triggered.connect(self.josm_remote)
        self.toolbar.addAction(self.josmAction)

        # Insert in the good order
        self.quickosm_menu.addAction(self.mainWindowAction)
        self.quickosm_menu.addAction(self.josmAction)

        for server in OVERPASS_SERVERS:
            self.iface.QuickOSM_mainWindowDialog.comboBox_default_OAPI. \
                addItem(server)

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
                        self.iface.QuickOSM_mainWindowDialog.\
                            comboBox_default_OAPI.addItem(server)

        # Check previous version and if new queries are available
        version = get_setting('version')
        current_version = get_current_version()
        if version != current_version:
            if new_queries_available():
                widget = self.iface.messageBar().createMessage(
                    'QuickOSM',
                    tr('New queries are available in the plugin. Would like '
                       'to install them ? This will overwrite the current '
                       'default queries.'))
                button_ok = QPushButton(widget)
                button_ok.setText(tr('Install'))
                button_ok.pressed.connect(self.restoreDefaultQueries)
                widget.layout().addWidget(button_ok)
                self.iface.messageBar().pushWidget(
                    widget, Qgis.Info, 0)

            set_setting('version', current_version)

    def restoreDefaultQueries(self):
        self.iface.QuickOSM_mainWindowDialog.restore_default_queries()
        self.iface.messageBar().popWidget()

    def unload(self):
        self.iface.removePluginVectorMenu('&QuickOSM', self.mainWindowAction)
        self.iface.removeToolBarIcon(self.mainWindowAction)
        # Processing.removeProvider(self.provider)

    def josm_remote(self):
        map_settings = self.iface.mapCanvas().mapSettings()
        extent = map_settings.extent()
        crs_map = map_settings.destinationCrs()
        if crs_map.authid() != 'EPSG:4326':
            crs_4326 = QgsCoordinateReferenceSystem(4326)
            transform = QgsCoordinateTransform(crs_map, crs_4326, QgsProject.instance())
            extent = transform.transform(extent)

        url = 'http://localhost:8111/load_and_zoom?'
        query_string = 'left=%f&right=%f&top=%f&bottom=%f' % (
            extent.xMinimum(), extent.xMaximum(), extent.yMaximum(),
            extent.yMinimum())
        url += query_string
        try:
            request = urllib.request.Request(url)
            result_request = urllib.request.urlopen(request)
            result = result_request.read()
            result = result.decode('utf8')
            if result.strip().upper() != 'OK':
                self.iface.messageBar().pushCritical(
                    'JOSM Remote', result)
            else:
                self.iface.messageBar().pushSuccess(
                    'JOSM Remote', 'Import done, check JOSM')
        except IOError:
            self.iface.messageBar().pushCritical(
                'JOSM Remote', 'Is the remote enabled?')

    def openMainWindow(self):
        self.iface.QuickOSM_mainWindowDialog.listWidget.setCurrentRow(0)
        self.iface.QuickOSM_mainWindowDialog.exec_()
