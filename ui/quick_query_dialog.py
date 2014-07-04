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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import QgsMessageBar
from quick_query import Ui_Form      
from QuickOSM.Controller.Process import Process
import os
from qgis.utils import iface


class QuickQueryWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setupUi(self)
        
        #Setup UI
        self.lineEdit_filePrefix.setDisabled(True)
               
        #connect
        self.pushButton_runQuery.clicked.connect(self.runQuery)
        self.pushButton_showQuery.clicked.connect(self.showQuery)
        self.pushButton_browse_output_file.clicked.connect(self.setOutDirPath)
        self.lineEdit_browseDir.textEdited.connect(self.disablePrefixFile)

    def disablePrefixFile(self):
        if self.lineEdit_browseDir.text():
            self.lineEdit_filePrefix.setDisabled(False)
        else:
            self.lineEdit_filePrefix.setText("")
            self.lineEdit_filePrefix.setDisabled(True)
        
    def setOutDirPath(self):
        outputFile = QFileDialog.getExistingDirectory(None, caption=QApplication.translate("QuickOSM", 'Select directory'))
        self.lineEdit_browseDir.setText(outputFile)
        
    def runQuery(self):
        #Block the button
        self.pushButton_runQuery.setDisabled(True)
        self.pushButton_runQuery.initialText = self.pushButton_runQuery.text()
        self.pushButton_runQuery.setText("Running query ...")
        
        #Get all values
        key = unicode(self.lineEdit_key.text())
        value = unicode(self.lineEdit_value.text())
        nominatim = unicode(self.lineEdit_nominatim.text())
        timeout = self.spinBox_timeout.value()
        outputDir = self.lineEdit_browseDir.text()
        prefixFile = self.lineEdit_filePrefix.text()
        
        #Test values
        if outputDir and os.path.isdir(outputDir):
            msg = u"The output directory does not exist."
            iface.messageBar().pushMessage(msg, level=QgsMessageBar.CRITICAL , duration=5)
        else:
            osmObjects = []
            if self.checkBox_node.isChecked():
                osmObjects.append('node')
            if self.checkBox_way.isChecked():
                osmObjects.append('way')
            if self.checkBox_relation.isChecked():
                osmObjects.append('relation')
    
            #miss bbox
            if not Process.ProcessQuickQuery(key=key, value=value, nominatim=nominatim, osmObjects=osmObjects, timeout=timeout, outputDir=outputDir, prefixFile=prefixFile):
                msg = u"Error"
                iface.messageBar().pushMessage(msg, level=QgsMessageBar.CRITICAL , duration=5)

        #Resetting the button
        msg = u"Successful query !"
        iface.messageBar().pushMessage(msg, level=QgsMessageBar.INFO , duration=5)
        
        self.pushButton_runQuery.setDisabled(False)
        self.pushButton_runQuery.setText(self.pushButton_runQuery.initialText)
        
    def showQuery(self):
        msg = u"Sorry man, not implemented yet ! ;-)"
        iface.messageBar().pushMessage(msg, level=QgsMessageBar.CRITICAL , duration=5)


class QuickQueryDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.widget = QuickQueryWidget()
        self.setWidget(self.widget)
        self.setWindowTitle(QApplication.translate("Form", "Quick query"))