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
from qgis.core import *
from QuickOSM.Controller.Process import Process
from QuickOSM.CoreQuickOSM.ExceptionQuickOSM import *
from QuickOSM.CoreQuickOSM.Tools import Tools
from XMLHighlighter import XMLHighlighter
import os
import re
from qgis.utils import iface
from query import Ui_ui_query

class QueryWidget(QWidget, Ui_ui_query):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setupUi(self)
        
        #Highlight XML
        self.highlighter = XMLHighlighter(self.textEdit_query.document())
        
        #Default query
        self.textEdit_query.setPlainText('\
<osm-script output="json" timeout="25">\n \
    <id-query into="area" ref="3600028722" type="area"/>\n \
    <union>\n \
        <query type="node">\n \
            <has-kv k="amenity" v="school"/>\n \
            <area-query from="area"/>\n \
        </query>\n \
        <query type="way">\n \
            <has-kv k="amenity" v="school"/>\n \
            <area-query from="area"/>\n \
        </query>\n \
        <query type="relation">\n \
            <has-kv k="amenity" v="school"/>\n \
            <area-query from="area"/>\n \
        </query>\n \
    </union>\n \
    <print mode="body"/>\n \
    <recurse type="down"/>\n \
    <print mode="skeleton" order="quadtile"/>\n \
</osm-script>')

        self.checkBox_points.setChecked(True)
        self.checkBox_lines.setChecked(False)
        self.checkBox_linestrings.setChecked(False)
        self.checkBox_multipolygons.setChecked(True)
        
        #Setup UI
        self.lineEdit_filePrefix.setDisabled(True)
        self.groupBox.setCollapsed(True)
        self.bbox = None
        self.fillLayerCombobox()
          
        #connect
        self.pushButton_runQuery.clicked.connect(self.runQuery)
        self.pushButton_generateQuery.clicked.connect(self.generateQuery)
        self.pushButton_browse_output_file.clicked.connect(self.setOutDirPath)
        self.lineEdit_browseDir.textEdited.connect(self.disablePrefixFile)
        self.textEdit_query.cursorPositionChanged.connect(self.highlighter.rehighlight)
        self.textEdit_query.cursorPositionChanged.connect(self.allowNominatimOrExtent)
        self.radioButton_extentLayer.toggled.connect(self.extentRadio)

        #Add or remove layers
        qgsMapLayerRegistry = QgsMapLayerRegistry.instance()
        qgsMapLayerRegistry.layerRemoved.connect(self.fillLayerCombobox)
        qgsMapLayerRegistry.layerWasAdded.connect(self.fillLayerCombobox)

    def fillLayerCombobox(self):
        '''
        Fill the combobox with layers which are in the legend
        '''
        layers = iface.legendInterface().layers()
        self.comboBox_extentLayer.clear()
        for layer in layers:
            self.comboBox_extentLayer.addItem(layer.name(),layer)
            
        if self.comboBox_extentLayer.count() < 1:
            self.radioButton_extentLayer.setCheckable(False)
            self.radioButton_extentMapCanvas.setChecked(True)

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

    def extentRadio(self):
        '''
        Disable or enable the comboxbox
        '''
        if self.radioButton_extentLayer.isChecked():
            self.comboBox_extentLayer.setDisabled(False)
        else:
            self.comboBox_extentLayer.setDisabled(True)

    def runQuery(self):
        '''
        Process for running the query
        '''
        #Block the button and save the initial text
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.pushButton_browse_output_file.setDisabled(True)
        self.pushButton_generateQuery.setDisabled(True)
        self.pushButton_runQuery.setDisabled(True)
        self.pushButton_runQuery.initialText = self.pushButton_runQuery.text()
        self.pushButton_runQuery.setText(QApplication.translate("QuickOSM","Running query ..."))
        self.progressBar_execution.setMinimum(0)
        self.progressBar_execution.setMaximum(0)
        self.progressBar_execution.setValue(0)
        self.label_progress.setText("")
        QApplication.processEvents()
        
        #Get all values
        query = unicode(self.textEdit_query.toPlainText())
        outputDir = self.lineEdit_browseDir.text()
        prefixFile = self.lineEdit_filePrefix.text()
        nominatim = self.lineEdit_nominatim.text()
        
        bbox = None
        if self.radioButton_extentLayer.isChecked() or self.radioButton_extentMapCanvas.isChecked():
            bbox = self.__getBBox()
        
        #Which geometry at the end ?
        outputGeomTypes = []
        whiteListValues = {}
        if self.checkBox_points.isChecked():
            outputGeomTypes.append('points')
            whiteListValues['points'] = self.lineEdit_csv_points.text()
        if self.checkBox_lines.isChecked():
            outputGeomTypes.append('lines')
            whiteListValues['lines'] = self.lineEdit_csv_lines.text()
        if self.checkBox_linestrings.isChecked():
            outputGeomTypes.append('multilinestrings')
            whiteListValues['multilinestrings'] = self.lineEdit_csv_multilinestrings.text()
        if self.checkBox_multipolygons.isChecked():
            outputGeomTypes.append('multipolygons')
            whiteListValues['multipolygons'] = self.lineEdit_csv_multipolygons.text()
        
        try:
            #Test values
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
            iface.messageBar().pushMessage(e.msg, level=QgsMessageBar.CRITICAL , duration=7)
        except Exception,e:
            import sys
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            ex_type, ex, tb = sys.exc_info()
            import traceback
            traceback.print_tb(tb)
            iface.messageBar().pushMessage("Error in the python console, please report it", level=QgsMessageBar.CRITICAL , duration=5)
        
        finally:
            #Resetting the button
            self.pushButton_browse_output_file.setDisabled(False)
            self.pushButton_generateQuery.setDisabled(False)
            self.pushButton_runQuery.setDisabled(False)
            self.pushButton_runQuery.setText(self.pushButton_runQuery.initialText)
            self.progressBar_execution.setMinimum(0)
            self.progressBar_execution.setMaximum(100)
            self.progressBar_execution.setValue(100)
            
            QApplication.restoreOverrideCursor()
            QApplication.processEvents()
            
    def generateQuery(self):
        '''
        Transform the template to query "out of the box"
        '''
        query = unicode(self.textEdit_query.toPlainText())
        bbox = self.__getBBox()
        query = Tools.PrepareQueryOqlXml(query=query, extent=bbox)
        self.textEdit_query.setPlainText(query)
        
    def __getBBox(self):
        '''
        Get the geometry of the bbox in WGS84
        '''
        geomExtent = None
        sourceCrs = None
        
        #If mapCanvas is checked
        if self.radioButton_extentMapCanvas.isChecked():
            geomExtent = iface.mapCanvas().extent()
            sourceCrs = iface.mapCanvas().mapRenderer().destinationCrs()
        else:
            #Else if a layer is checked
            index = self.comboBox_extentLayer.currentIndex()
            layerID = self.comboBox_extentLayer.itemData(index)
            layerName = self.comboBox_extentLayer.itemText(index)
            layers = iface.legendInterface().layers()
            for layer in layers:
                if layer.id() == layerID:
                    geomExtent = layer.extent()
                    sourceCrs = layer.crs()
                    break
            else:
                #the layer could be deleted before
                raise NoLayerException(suffix=layerName)
        
        geomExtent = QgsGeometry.fromRect(geomExtent)
        crsTransform = QgsCoordinateTransform(sourceCrs, QgsCoordinateReferenceSystem("EPSG:4326"))
        geomExtent.transform(crsTransform)
        return geomExtent.boundingBox()   
            

    def setProgressPercentage(self,percent):
        '''
        Slot to update percentage during process
        '''
        self.progressBar_execution.setValue(percent)
        QApplication.processEvents()
        
    def setProgressText(self,text):
        '''
        Slot to update text during process
        '''
        self.label_progress.setText(text)
        QApplication.processEvents()

class QueryDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(QueryWidget())
        self.setWindowTitle(QApplication.translate("ui_query", "Query"))