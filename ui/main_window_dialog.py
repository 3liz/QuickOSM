# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSMDialog
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

from PyQt4 import QtCore,QtGui
from main_window import Ui_ui_main_window
from QuickOSM.CoreQuickOSM.API.ConnexionOAPI import ConnexionOAPI
from QuickOSM.CoreQuickOSM.Tools import Tools

class MainWindowDialog(QtGui.QDialog, Ui_ui_main_window):
    
    #Signal new query
    signalNewQuerySuccessful = QtCore.pyqtSignal(name='signalNewQuerySuccessful')
    
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        #Connect
        self.pushButton_OAPI_timestamp.clicked.connect(self.getTimestampOAPI)
        self.comboBox_default_OAPI.currentIndexChanged[int].connect(self.setServerOAPI)
        self.query.signalNewQuerySuccessful.connect(self.onNewQuerySuccessful)
        self.query.signalNewQuerySuccessful.connect(self.signalNewQuerySuccessful.emit)
        
        #Set settings about the OAPI
        self.defaultServer = Tools.getSetting('defaultOAPI')
        if self.defaultServer:
            index = self.comboBox_default_OAPI.findText(self.defaultServer)
            self.comboBox_default_OAPI.setCurrentIndex(index)
        else:
            self.defaultServer = self.comboBox_default_OAPI.currentText()
            Tools.setSetting('defaultOAPI', self.defaultServer)

    def onNewQuerySuccessful(self):
        self.my_queries.fillTree(force=True)
            
    def setServerOAPI(self,index):
        self.defaultServer = self.comboBox_default_OAPI.currentText()
        Tools.setSetting('defaultOAPI', self.defaultServer)
        self.getTimestampOAPI()
        
    def getTimestampOAPI(self):
        oapi = ConnexionOAPI(url=self.defaultServer)
        self.label_timestamp_oapi.setText(oapi.getTimestamp())