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

import urllib.request
from json import load
from os.path import dirname, join, exists, abspath, isfile

from QuickOSM.core.custom_logging import setup_logger
# from QuickOSM.ui.my_queries_dialog import MyQueriesDockWidget
# from QuickOSM.ui.query_dialog import QueryDockWidget
# from QuickOSM.ui.osm_file_dialog import OsmFileDockWidget
# from QuickOSM.ui.quick_query_dialog import QuickQueryDockWidget
# from QuickOSM.quick_osm_processing.algorithm_provider import (
#     QuickOSMAlgorithmProvider)
from QuickOSM.core.utilities.tools import (
    get_current_version,
    get_setting,
    set_setting,
    new_queries_available,
    tr,
    get_user_query_folder
)
from QuickOSM.ui.main_window_dialog import MainWindowDialog
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QMenu, QAction, QPushButton
from qgis.core import Qgis, QgsCoordinateTransform, \
    QgsCoordinateReferenceSystem, QgsProject


# from processing.core.Processing import Processing


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
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = join(
            self.plugin_dir,
            'i18n',
            'QuickOSM_{0}.qm'.format(locale))

        if exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                # noinspection PyTypeChecker
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
        self.dock_menu = None
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
        self.quickosm_menu = QMenu('Quick OSM')
        self.quickosm_menu.setIcon(
            QIcon(join(dirname(__file__), 'resources', 'QuickOSM.svg')))
        self.dock_menu = QMenu(tr('QuickOSM', u'Dock'))
        self.vector_menu = self.iface.vectorMenu()
        self.vector_menu.addMenu(self.quickosm_menu)

        # Main window
        self.mainWindowAction = QAction(
            QIcon(join(dirname(__file__), 'resources', 'QuickOSM.svg')),
            u'QuickOSM',
            self.iface.mainWindow())
        # noinspection PyUnresolvedReferences
        self.mainWindowAction.triggered.connect(self.openMainWindow)
        self.toolbar.addAction(self.mainWindowAction)
        self.iface.QuickOSM_mainWindowDialog = MainWindowDialog()

        self.josmAction = QAction(
            QIcon(join(dirname(__file__), 'resources', 'josm_icon.svg')),
            'JOSM Remote',
            self.iface.mainWindow())
        self.josmAction.triggered.connect(self.josm_remote)
        self.toolbar.addAction(self.josmAction)

        # OSM File
        # self.osmFileAction = QAction(
        #     QIcon(':/plugins/QuickOSM/resources/open.png'),
        #     tr('ui_osm_file', 'OSM File'),
        #     self.iface.mainWindow())
        # # noinspection PyUnresolvedReferences
        # self.osmFileAction.triggered.connect(self.openOsmFileDockWidget)
        # self.osmFileDockWidget = OsmFileDockWidget()
        # self.iface.addDockWidget(
        #     Qt.RightDockWidgetArea, self.osmFileDockWidget)
        # self.osmFileDockWidget.hide()
        # self.osmFileDockWidget.setObjectName('osmFileWidget')

        # My queries
        # self.myQueriesAction = QAction(
        #     QIcon(':/plugins/QuickOSM/resources/favorites.png'),
        #     tr('ui_my_queries', 'My queries'),
        #     self.iface.mainWindow())
        # # noinspection PyUnresolvedReferences
        # self.myQueriesAction.triggered.connect(self.openMyQueriesDockWidget)
        # self.myQueriesDockWidget = MyQueriesDockWidget()
        # self.iface.addDockWidget(
        #     Qt.RightDockWidgetArea, self.myQueriesDockWidget)
        # self.myQueriesDockWidget.hide()
        # self.myQueriesDockWidget.setObjectName('myQueriesWidget')

        # Query
        # self.queryAction = QAction(
        #     QIcon(':/plugins/QuickOSM/resources/edit.png'),
        #     tr('ui_query', 'Query'),
        #     self.iface.mainWindow())
        # # noinspection PyUnresolvedReferences
        # self.queryAction.triggered.connect(self.openQueryDockWidget)
        # self.queryDockWidget = QueryDockWidget()
        # self.iface.addDockWidget(Qt.RightDockWidgetArea, self.queryDockWidget)
        # self.queryDockWidget.hide()
        # self.queryDockWidget.setObjectName('queryWidget')

        # Quick query
        # self.quickQueryAction = QAction(
        #     QIcon(':/plugins/QuickOSM/resources/quick.png'),
        #     tr('ui_quick_query', 'Quick query'),
        #     self.iface.mainWindow())
        # # noinspection PyUnresolvedReferences
        # self.quickQueryAction.triggered.connect(self.openQuickQueryDockWidget)
        # self.quickQueryDockWidget = QuickQueryDockWidget()
        # self.iface.addDockWidget(
        #     Qt.RightDockWidgetArea, self.quickQueryDockWidget)
        # self.quickQueryDockWidget.hide()
        # self.quickQueryDockWidget.setObjectName('quickQueryWidget')

        # Insert in the good order
        self.quickosm_menu.addAction(self.mainWindowAction)
        # self.quickosm_menu.addMenu(self.dock_menu)
        # self.dock_menu.addAction(self.quickQueryAction)
        # self.dock_menu.addAction(self.queryAction)
        # self.dock_menu.addAction(self.myQueriesAction)
        # self.dock_menu.addAction(self.osmFileAction)

        # Connect signals and slots from dock
        # self.queryDockWidget.signal_new_query_successful.connect(
        #     self.iface.QuickOSM_mainWindowDialog.refresh_my_queries_tree)
        # self.queryDockWidget.signal_new_query_successful.connect(
        #     self.myQueriesDockWidget.refresh_my_queries_tree)
        # self.myQueriesDockWidget.signal_delete_query_successful.connect(
        #     self.myQueriesDockWidget.refresh_my_queries_tree)
        # self.myQueriesDockWidget.signal_delete_query_successful.connect(
        #     self.iface.QuickOSM_mainWindowDialog.refresh_my_queries_tree)

        # Connect signals and slots from mainWindow
        # self.iface.QuickOSM_mainWindowDialog.signal_new_query_successful.\
        #     connect(self.myQueriesDockWidget.refresh_my_queries_tree)
        # self.iface.QuickOSM_mainWindowDialog.signal_new_query_successful.\
        #     connect(
        #         self.iface.QuickOSM_mainWindowDialog.refresh_my_queries_tree)
        # self.iface.QuickOSM_mainWindowDialog.signal_delete_query_successful.\
        #     connect(self.myQueriesDockWidget.refresh_my_queries_tree)
        # self.iface.QuickOSM_mainWindowDialog.signal_delete_query_successful.\
        #     connect(
        #         self.iface.QuickOSM_mainWindowDialog.refresh_my_queries_tree)

        # Read the config file
        json_file_config = join(dirname(abspath(__file__)), 'config.json')
        if isfile(json_file_config):
            with open(json_file_config) as f:
                config_json = load(f)
                for server in config_json['overpass_servers']:
                    self.iface.QuickOSM_mainWindowDialog.comboBox_default_OAPI.\
                        addItem(server)

        # Check previous version and if new queries are available
        version = get_setting('version')
        current_version = get_current_version()
        if version != current_version:
            if new_queries_available():
                message = 'New queries are available in the plugin. Would ' \
                          'like to install them ? This will overwrite the ' \
                          'current default queries.'
                title = 'QuickOSM'
                message = tr('QuickOSM', message)
                widget = self.iface.messageBar().createMessage(title, message)
                button_ok = QPushButton(widget)
                button_ok.setText(
                    tr('QuickOSM', 'Install'))
                button_ok.pressed.connect(self.restoreDefaultQueries)
                widget.layout().addWidget(button_ok)
                self.iface.messageBar().pushWidget(
                    widget, Qgis.Info, 0)

            set_setting('version', current_version)

    def restoreDefaultQueries(self):
        self.iface.QuickOSM_mainWindowDialog.restore_default_queries()
        self.iface.messageBar().popWidget()

    def unload(self):
        self.iface.removePluginVectorMenu(u'&QuickOSM', self.mainWindowAction)
        # self.iface.removePluginVectorMenu(u'&QuickOSM', self.myQueriesAction)
        # self.iface.removePluginVectorMenu(u'&QuickOSM', self.queryAction)
        # self.iface.removePluginVectorMenu(u'&QuickOSM', self.quickQueryAction)
        # self.iface.removePluginVectorMenu(u'&QuickOSM', self.osmFileAction)
        self.iface.removeToolBarIcon(self.mainWindowAction)
        # Processing.removeProvider(self.provider)

    def josm_remote(self):
        map_settings = self.iface.mapCanvas().mapSettings()
        extent = map_settings.extent()
        crs_map = map_settings.destinationCrs()
        if crs_map.authid() != u'EPSG:4326':
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

    # def openMyQueriesDockWidget(self):
    #     if self.myQueriesDockWidget.isVisible():
    #         self.myQueriesDockWidget.hide()
    #     else:
    #         self.myQueriesDockWidget.show()
    #
    # def openQueryDockWidget(self):
    #     if self.queryDockWidget.isVisible():
    #         self.queryDockWidget.hide()
    #     else:
    #         self.queryDockWidget.show()
    #
    # def openOsmFileDockWidget(self):
    #     if self.osmFileDockWidget.isVisible():
    #         self.osmFileDockWidget.hide()
    #     else:
    #         self.osmFileDockWidget.show()
    #
    # def openQuickQueryDockWidget(self):
    #     if self.quickQueryDockWidget.isVisible():
    #         self.quickQueryDockWidget.hide()
    #     else:
    #         self.quickQueryDockWidget.show()
