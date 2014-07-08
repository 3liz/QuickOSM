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
from QuickOSM.CoreQuickOSM.ExceptionQuickOSM import *
import os
from qgis.utils import iface


class QuickQueryWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        '''
        QuickQueryWidget constructor
        '''
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
        '''
        If the directory is empty, we disable the file prefix
        '''
        if self.lineEdit_browseDir.text():
            self.lineEdit_filePrefix.setDisabled(False)
        else:
            self.lineEdit_filePrefix.setText("")
            self.lineEdit_filePrefix.setDisabled(True)
        
    def setOutDirPath(self):
        '''
        Fill the output directory path
        '''
        outputFile = QFileDialog.getExistingDirectory(None, caption=QApplication.translate("QuickOSM", 'Select directory'))
        self.lineEdit_browseDir.setText(outputFile)
        self.disablePrefixFile()
        
    def runQuery(self):
        '''
        Process for running the query
        '''
        #Block the button and save the initial text
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.pushButton_runQuery.setDisabled(True)
        self.pushButton_runQuery.initialText = self.pushButton_runQuery.text()
        self.pushButton_runQuery.setText(QApplication.translate("QuickOSM","Running query ..."))
        self.progressBar_execution.setMinimum(0)
        self.progressBar_execution.setMaximum(0)
        self.progressBar_execution.setValue(0)
        self.label_progress.setText("")
        QApplication.processEvents()
        
        #Get all values
        key = unicode(self.lineEdit_key.text())
        value = unicode(self.lineEdit_value.text())
        nominatim = unicode(self.lineEdit_nominatim.text())
        timeout = self.spinBox_timeout.value()
        outputDir = self.lineEdit_browseDir.text()
        prefixFile = self.lineEdit_filePrefix.text()
        
        osmObjects = []
        if self.checkBox_node.isChecked():
            osmObjects.append('node')
        if self.checkBox_way.isChecked():
            osmObjects.append('way')
        if self.checkBox_relation.isChecked():
            osmObjects.append('relation')
        
        try:
            #Test values
            if outputDir and not os.path.isdir(outputDir):
                raise DirectoryOutPutException

            #miss bbox
            Process.ProcessQuickQuery(dialog = self, key=key, value=value, nominatim=nominatim, osmObjects=osmObjects, timeout=timeout, outputDir=outputDir, prefixFile=prefixFile)
            msg = u"Successful query !"
            iface.messageBar().pushMessage(msg, level=QgsMessageBar.INFO , duration=5)
        
        except GeoAlgorithmExecutionException,e:
            iface.messageBar().pushMessage(e.msg, level=QgsMessageBar.CRITICAL , duration=7)
        except Exception,e:
            import sys
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            ex_type, ex, tb = sys.exc_info()
            import traceback
            traceback.print_tb(tb)
            iface.messageBar().pushMessage("Erreur dans la console python", level=QgsMessageBar.CRITICAL , duration=5)
        
        finally:
            #Resetting the button
            self.pushButton_runQuery.setDisabled(False)
            self.pushButton_runQuery.setText(self.pushButton_runQuery.initialText)
            self.progressBar_execution.setMinimum(0)
            self.progressBar_execution.setMaximum(100)
            self.progressBar_execution.setValue(100)
            self.label_progress.setText("Successful query !")
            QApplication.restoreOverrideCursor()
            QApplication.processEvents()
        
    def showQuery(self):
        msg = u"Sorry man, not implemented yet ! ;-)"
        iface.messageBar().pushMessage(msg, level=QgsMessageBar.CRITICAL , duration=5)
        
    def setProgressPercentage(self,percent):
        self.progressBar_execution.setValue(percent)
        QApplication.processEvents()
        
    def setProgressText(self,text):
        self.label_progress.setText(text)
        QApplication.processEvents()

class QuickQueryDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.widget = QuickQueryWidget()
        self.setWidget(self.widget)
        self.setWindowTitle(QApplication.translate("Form", "Quick query"))