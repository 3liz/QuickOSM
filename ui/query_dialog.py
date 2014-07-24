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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from QuickOSMWidget import *
from qgis.gui import QgsMessageBar
from qgis.core import *
from QuickOSM.Controller.Process import Process
from QuickOSM.CoreQuickOSM.ExceptionQuickOSM import *
from save_query_dialog import SaveQueryDialog
from QuickOSM.CoreQuickOSM.Tools import Tools
from XMLHighlighter import XMLHighlighter
import os
import re
from qgis.utils import iface
from query import Ui_ui_query

class QueryWidget(QuickOSMWidget, Ui_ui_query):
    
    #Signal new query
    signalNewQuerySuccessful = pyqtSignal(name='signalNewQuerySuccessful')
    
    def __init__(self, parent=None):
        QuickOSMWidget.__init__(self)
        self.setupUi(self)
        
        #Highlight XML
        self.highlighter = XMLHighlighter(self.textEdit_query.document())
               
        #Setup UI
        self.lineEdit_filePrefix.setDisabled(True)
        self.groupBox.setCollapsed(True)
        self.bbox = None
        self.fillLayerCombobox()
        
        #Setup menu for saving
        popupmenu = QMenu()
        saveFinalQueryAction = QAction(QApplication.translate("QuickOSM", 'Save as final query'),self.pushButton_saveQuery)
        saveFinalQueryAction.triggered.connect(self.saveFinalQuery)
        popupmenu.addAction(saveFinalQueryAction)
        saveTemplateQueryAction = QAction(QApplication.translate("QuickOSM", 'Save as template'),self.pushButton_saveQuery)
        saveTemplateQueryAction.triggered.connect(self.saveTemplateQuery)
        popupmenu.addAction(saveTemplateQueryAction)
        self.pushButton_saveQuery.setMenu(popupmenu)
        
        #connect
        self.pushButton_runQuery.clicked.connect(self.runQuery)
        self.pushButton_generateQuery.clicked.connect(self.generateQuery)
        self.pushButton_browse_output_file.clicked.connect(self.setOutDirPath)
        self.lineEdit_browseDir.textEdited.connect(self.disablePrefixFile)
        self.textEdit_query.cursorPositionChanged.connect(self.highlighter.rehighlight)
        self.textEdit_query.cursorPositionChanged.connect(self.allowNominatimOrExtent)
        self.radioButton_extentLayer.toggled.connect(self.extentRadio)
        self.pushButton_refreshLayers.clicked.connect(self.fillLayerCombobox)

    def allowNominatimOrExtent(self):
        '''
        Disable or enable radiobuttons if nominatim or extent
        '''
        query = unicode(self.textEdit_query.toPlainText())

        if re.search('{{nominatim}}', query) or re.search('{{nominatimArea:(.*)}}', query):
            self.lineEdit_nominatim.setEnabled(True)
        else:
            self.lineEdit_nominatim.setEnabled(False)
            self.lineEdit_nominatim.setText("")
            
        if re.search('{{bbox}}', query):
            self.radioButton_extentLayer.setEnabled(True)
            self.radioButton_extentMapCanvas.setEnabled(True)
            if self.radioButton_extentLayer.isChecked():
                self.comboBox_extentLayer.setEnabled(True)
            else:
                self.comboBox_extentLayer.setEnabled(False)
        else:
            self.radioButton_extentLayer.setEnabled(False)
            self.radioButton_extentMapCanvas.setEnabled(False)
            self.comboBox_extentLayer.setEnabled(False)

    def runQuery(self):
        '''
        Process for running the query
        '''
        #Block the button and save the initial text
        self.pushButton_browse_output_file.setDisabled(True)
        self.pushButton_generateQuery.setDisabled(True)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.startProcess()
        QApplication.processEvents()
        
        #Get all values
        query = unicode(self.textEdit_query.toPlainText())
        outputDir = self.lineEdit_browseDir.text()
        prefixFile = self.lineEdit_filePrefix.text()
        nominatim = self.lineEdit_nominatim.text()
        
        bbox = None
        if self.radioButton_extentLayer.isChecked() or self.radioButton_extentMapCanvas.isChecked():
            bbox = self.getBBox()
        
        #Which geometry at the end ?
        outputGeomTypes = self.getOutputGeomTypes()
        whiteListValues = self.getWhiteListValues()
        
        try:
            #Test values
            if not outputGeomTypes:
                raise OutPutGeomTypesException
            
            if outputDir and not os.path.isdir(outputDir):
                raise DirectoryOutPutException

            if not nominatim and (re.search('{{nominatim}}', query) or re.search('{{nominatimArea:}}', query)):
                raise MissingParameterException(suffix="nominatim field")

            numLayers = Process.ProcessQuery(dialog = self, query=query, outputDir=outputDir, prefixFile=prefixFile,outputGeomTypes=outputGeomTypes, whiteListValues=whiteListValues, nominatim=nominatim, bbox=bbox)
            if numLayers:
                iface.messageBar().pushMessage(QApplication.translate("QuickOSM",u"Successful query !"), level=QgsMessageBar.INFO , duration=5)
                self.label_progress.setText(QApplication.translate("QuickOSM",u"Successful query !"))
            else:
                iface.messageBar().pushMessage(QApplication.translate("QuickOSM", u"Successful query, but no result."), level=QgsMessageBar.WARNING , duration=7)
        
        except GeoAlgorithmExecutionException,e:
            self.displayGeoAlgorithmException(e)
        except Exception,e:
            self.displayException(e)
        
        finally:
            #Resetting the button
            self.pushButton_browse_output_file.setDisabled(False)
            self.pushButton_generateQuery.setDisabled(False)
            QApplication.restoreOverrideCursor()
            self.endProcess()
            QApplication.processEvents()
            
    def generateQuery(self):
        '''
        Transform the template to query "out of the box"
        '''
        query = unicode(self.textEdit_query.toPlainText())
        nominatim = unicode(self.lineEdit_nominatim.text())
        bbox = self.getBBox()
        query = Tools.PrepareQueryOqlXml(query=query, extent=bbox, nominatimName=nominatim)
        self.textEdit_query.setPlainText(query)  

    def saveFinalQuery(self):
        
        #Which geometry at the end ?
        outputGeomTypes = self.getOutputGeomTypes()
        whiteListValues = self.getWhiteListValues()
        
        query = unicode(self.textEdit_query.toPlainText())
        nominatim = unicode(self.lineEdit_nominatim.text())
        bbox = self.getBBox()
        query = Tools.PrepareQueryOqlXml(query=query, extent=bbox, nominatimName=nominatim)
        
        saveQueryDialog = SaveQueryDialog(query=query,outputGeomTypes=outputGeomTypes,whiteListValues=whiteListValues)
        saveQueryDialog.signalNewQuerySuccessful.connect(self.signalNewQuerySuccessful.emit)
        saveQueryDialog.exec_()
        
    def saveTemplateQuery(self):
        #Which geometry at the end ?
        outputGeomTypes = self.getOutputGeomTypes()
        whiteListValues = self.getWhiteListValues()
        
        query = unicode(self.textEdit_query.toPlainText())
        
        saveQueryDialog = SaveQueryDialog(query=query,outputGeomTypes=outputGeomTypes,whiteListValues=whiteListValues)
        saveQueryDialog.signalNewQuerySuccessful.connect(self.signalNewQuerySuccessful.emit)
        saveQueryDialog.exec_()

class QueryDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(QueryWidget())
        self.setWindowTitle(QApplication.translate("ui_query", "QuickOSM - Query"))