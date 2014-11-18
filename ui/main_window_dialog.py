# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
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

from QuickOSM import *
from main_window import Ui_ui_main_window
from QuickOSM.CoreQuickOSM.API.ConnexionOAPI import ConnexionOAPI
from QuickOSM.CoreQuickOSM.Tools import Tools
from os.path import dirname,abspath,join,isfile

class MainWindowDialog(QDialog, Ui_ui_main_window):
    
    #Signal new query
    signalNewQuerySuccessful = pyqtSignal(name='signalNewQuerySuccessful')
    signalDeleteQuerySuccessful = pyqtSignal(name='signalDeleteQuerySuccessful')
       
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self)
        self.setupUi(self)
        self.setHelpWebView()
        
        #Connect
        self.pushButton_homeHelp.clicked.connect(self.getRootHelp)
        self.pushButton_OAPI_timestamp.clicked.connect(self.getTimestampOAPI)
        self.comboBox_default_OAPI.currentIndexChanged[int].connect(self.setServerOAPI)
        self.query.signalNewQuerySuccessful.connect(self.signalNewQuerySuccessful.emit)
        self.my_queries.signalDeleteQuerySuccessful.connect(self.signalDeleteQuerySuccessful.emit)
        self.pushButton_restoreQueries.clicked.connect(self.restoreDefaultQueries)
        
        #Set settings about the OAPI
        self.defaultServer = Tools.getSetting('defaultOAPI')
        if self.defaultServer:
            index = self.comboBox_default_OAPI.findText(self.defaultServer)
            self.comboBox_default_OAPI.setCurrentIndex(index)
        else:
            self.defaultServer = self.comboBox_default_OAPI.currentText()
            Tools.setSetting('defaultOAPI', self.defaultServer)

    def setHelpWebView(self):
        '''
        Set the help
        '''
        locale = QSettings().value("locale/userLocale")[0:2]
        locale = "." + locale
        helpFileBase = "main"
        helps = [helpFileBase + locale +".html", helpFileBase + ".html"]
        
        docPath = join(dirname(dirname(abspath(__file__))),'doc')
        for helpFileName in helps:
            fileHelpPath = join(docPath,helpFileName)
            if isfile(fileHelpPath):
                self.helpFile = fileHelpPath
                self.webBrowser.load(QUrl(self.helpFile))
                break
        else:
            self.webBrowser.setHtml("<h3>Help not available</h3>")
    
    def getRootHelp(self):
        '''
        "home" button set the default help page
        '''
        self.webBrowser.load(QUrl(self.helpFile))

    def refreshMyQueriesTree(self):
        '''
        Slot which force the tree to refresh
        '''
        self.my_queries.fillTree(force=True)
            
    def setServerOAPI(self,index):
        '''
        Save the new OAPI server
        '''
        self.defaultServer = self.comboBox_default_OAPI.currentText()
        Tools.setSetting('defaultOAPI', self.defaultServer)
        
    def getTimestampOAPI(self):
        '''
        Get the timestamp of the current server
        '''
        text = self.pushButton_OAPI_timestamp.text()
        self.pushButton_OAPI_timestamp.setText(QApplication.translate("QuickOSM", 'Fetching the timestamp ...'))
        oapi = ConnexionOAPI(url=self.defaultServer)
        self.label_timestamp_oapi.setText(oapi.getTimestamp())
        self.pushButton_OAPI_timestamp.setText(text)
        
    def restoreDefaultQueries(self):
        '''
        Overwrite all queries
        '''
        text = self.pushButton_restoreQueries.text()
        self.pushButton_restoreQueries.setText(QApplication.translate("QuickOSM", 'Copy ...'))
        Tools.getUserQueryFolder(overWrite=True)
        self.signalNewQuerySuccessful.emit()
        self.my_queries.fillTree(force=True)
        self.pushButton_restoreQueries.setText(text)