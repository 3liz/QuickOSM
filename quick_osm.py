# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
                              -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info@3liz.com
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from processing.core.Processing import Processing
# Initialize Qt resources from file resources.py
#import resources_rc
# Import the code for the dialog
from ui.main_window_dialog import MainWindowDialog
from ui.my_queries_dialog import MyQueriesDockWidget
from ui.query_dialog import QueryDockWidget
from ui.quick_query_dialog import QuickQueryDockWidget
from ProcessingQuickOSM.QuickOSMAlgorithmProvider import QuickOSMAlgorithmProvider
import os.path


class QuickOSM:

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'QuickOSM_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        #Add to processing
        self.provider = QuickOSMAlgorithmProvider()
        Processing.addProvider(self.provider, True)

    def initGui(self):
        
        self.mainWindowAction = QAction(
            QIcon(os.path.dirname(__file__) +"/icon.png"),
            u"Quick OSM",
            self.iface.mainWindow())
        
        self.mainWindowAction.triggered.connect(self.openMainWindow)
        self.iface.addToolBarIcon(self.mainWindowAction)
        self.iface.addPluginToWebMenu(u"&Quick OSM",self.mainWindowAction)
        self.iface.mainWindowDialog = MainWindowDialog()
        
        
        self.myQueriesAction = QAction(
            QIcon(os.path.dirname(__file__) +"/icon.png"),
            QApplication.translate("ui_my_queries", "My queries"),
            self.iface.mainWindow())
        self.myQueriesAction.triggered.connect(self.openMyQueriesDockWidget)
        self.iface.addPluginToWebMenu(u"&Quick OSM",self.myQueriesAction)
        self.myQueriesDockWidget = MyQueriesDockWidget()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.myQueriesDockWidget)
        self.myQueriesDockWidget.hide()
        self.myQueriesDockWidget.setObjectName("myQueriesWidget");
        
        
        self.queryAction = QAction(
            QIcon(os.path.dirname(__file__) +"/icon.png"),
            QApplication.translate("ui_query", "Query"),
            self.iface.mainWindow())
        self.queryAction.triggered.connect(self.openQueryDockWidget)
        self.iface.addPluginToWebMenu(u"&Quick OSM",self.queryAction)
        self.queryDockWidget = QueryDockWidget()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.queryDockWidget)
        self.queryDockWidget.hide()
        self.queryDockWidget.setObjectName("queryWidget");
        
        
        self.quickQueryAction = QAction(
            QIcon(os.path.dirname(__file__) +"/icon.png"),
            QApplication.translate("ui_quick_query", "Quick query"),
            self.iface.mainWindow())
        self.quickQueryAction.triggered.connect(self.openQuickQueryDockWidget)
        self.iface.addPluginToWebMenu(u"&Quick OSM",self.quickQueryAction)
        self.quickQueryDockWidget = QuickQueryDockWidget()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.quickQueryDockWidget)
        #self.quickQueryDockWidget.hide()
        self.quickQueryDockWidget.setObjectName("quickQueryWidget");
        
        
    def unload(self):
        self.iface.removePluginWebMenu(u"&Quick OSM",self.mainWindowAction)
        self.iface.removePluginWebMenu(u"&Quick OSM",self.myQueriesAction)
        self.iface.removePluginWebMenu(u"&Quick OSM",self.queryAction)
        self.iface.removePluginWebMenu(u"&Quick OSM",self.quickQueryAction)
        self.iface.removeToolBarIcon(self.mainWindowAction)
        Processing.removeProvider(self.provider)
    
    def openMainWindow(self):
        self.provider = QuickOSMAlgorithmProvider()
        Processing.addProvider(self.provider, True)
        self.iface.mainWindowDialog.exec_()     
    
    def openMyQueriesDockWidget(self):
        if self.myQueriesDockWidget.isVisible():
            self.myQueriesDockWidget.hide()
        else:
            self.myQueriesDockWidget.show()
            
    def openQueryDockWidget(self):
        if self.queryDockWidget.isVisible():
            self.queryDockWidget.hide()
        else:
            self.queryDockWidget.show()
            
    def openQuickQueryDockWidget(self):
        if self.quickQueryDockWidget.isVisible():
            self.quickQueryDockWidget.hide()
        else:
            self.quickQueryDockWidget.show()