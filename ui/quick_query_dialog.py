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
from quick_query import Ui_ui_quick_query      
from QuickOSM.Controller.Process import Process
from QuickOSM.CoreQuickOSM.ExceptionQuickOSM import *
#from QuickOSM.ui.main_window_dialog import MainWindowDialog

#shoud not be here, use controller
from QuickOSM.CoreQuickOSM.QueryFactory import QueryFactory

import os
from qgis.utils import iface


class QuickQueryWidget(QWidget, Ui_ui_quick_query):
    def __init__(self, parent=None):
        '''
        QuickQueryWidget constructor
        '''
        QWidget.__init__(self)
        self.setupUi(self)
        
        #Default query
        self.lineEdit_key.setText("route")
        self.lineEdit_value.setText("bus")
        self.lineEdit_nominatim.setText("grenoble")
        self.checkBox_points.setChecked(False)
        self.checkBox_lines.setChecked(False)
        self.checkBox_linestrings.setChecked(True)
        self.checkBox_multipolygons.setChecked(False)
        
        #Setup UI
        self.lineEdit_filePrefix.setDisabled(True)
        self.groupBox.setCollapsed(True)
        self.fillLayerCombobox()
               
        #connect
        self.pushButton_runQuery.clicked.connect(self.runQuery)
        self.pushButton_showQuery.clicked.connect(self.showQuery)
        self.pushButton_browse_output_file.clicked.connect(self.setOutDirPath)
        self.lineEdit_browseDir.textEdited.connect(self.disablePrefixFile)
        self.radioButton_extentLayer.toggled.connect(self.allowNominatimOrExtent)
        self.radioButton_extentMapCanvas.toggled.connect(self.allowNominatimOrExtent)
        self.radioButton_place.toggled.connect(self.allowNominatimOrExtent)
        self.buttonBox_layers.button(QDialogButtonBox.Reset).clicked.connect(self.fillLayerCombobox)
 
    def allowNominatimOrExtent(self):
        '''
        Disable or enable radiobuttons if nominatim or extent
        '''
        if self.radioButton_extentMapCanvas.isChecked() or self.radioButton_extentLayer.isChecked():
            self.lineEdit_nominatim.setDisabled(True)
        else:
            self.lineEdit_nominatim.setDisabled(False)
        
        if self.radioButton_extentLayer.isChecked():
            self.comboBox_extentLayer.setDisabled(False)
            #self.buttonBox_layers.setDisabled(False)
        else:
            self.comboBox_extentLayer.setDisabled(True)
            self.buttonBox_layers.setDisabled(True)


    def fillLayerCombobox(self):
        '''
        Fill the combobox with layers which are in the legend
        '''
        layers = iface.legendInterface().layers()
        self.comboBox_extentLayer.clear()
        for layer in layers:
            self.comboBox_extentLayer.addItem(layer.name(),layer.id())
            
        if self.comboBox_extentLayer.count() < 1:
            self.radioButton_extentLayer.setCheckable(False)
        else:
            self.radioButton_extentLayer.setCheckable(True)

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
        self.pushButton_browse_output_file.setDisabled(True)
        self.pushButton_showQuery.setDisabled(True)
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
        
        #Which geometry at the end ?
        outputGeomTypes = []
        if self.checkBox_points.isChecked():
            outputGeomTypes.append('points')
        if self.checkBox_lines.isChecked():
            outputGeomTypes.append('lines')
        if self.checkBox_linestrings.isChecked():
            outputGeomTypes.append('multilinestrings')
        if self.checkBox_multipolygons.isChecked():
            outputGeomTypes.append('multipolygons')
        
        #Which osm's objects ?
        osmObjects = []
        if self.checkBox_node.isChecked():
            osmObjects.append('node')
        if self.checkBox_way.isChecked():
            osmObjects.append('way')
        if self.checkBox_relation.isChecked():
            osmObjects.append('relation')
        
        try:
            #Test values
            if not osmObjects:
                raise OsmObjectsException
            
            if not outputGeomTypes:
                raise OutPutGeomTypesException
            
            #If bbox, we must set None to nominatim, we can't have both
            bbox = None
            if self.radioButton_extentLayer.isChecked() or self.radioButton_extentMapCanvas.isChecked():
                nominatim = None
                bbox = self.__getBBox()
            
            if nominatim == '':
                nominatim = None
            
            if outputDir and not os.path.isdir(outputDir):
                raise DirectoryOutPutException

            numLayers = Process.ProcessQuickQuery(dialog = self, key=key, value=value, nominatim=nominatim, bbox=bbox, osmObjects=osmObjects, timeout=timeout, outputDir=outputDir, prefixFile=prefixFile,outputGeomTypes=outputGeomTypes)
            if numLayers:
                self.label_progress.setText(QApplication.translate("QuickOSM",u"Successful query !"))
                iface.messageBar().pushMessage(QApplication.translate("QuickOSM",u"Successful query !"), level=QgsMessageBar.INFO , duration=5)
            else:
                self.label_progress.setText(QApplication.translate("QuickOSM",u"No result"))
                iface.messageBar().pushMessage(QApplication.translate("QuickOSM", u"Successful query, but no result."), level=QgsMessageBar.WARNING , duration=7)
        
        except GeoAlgorithmExecutionException,e:
            self.label_progress.setText("")
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
            self.pushButton_showQuery.setDisabled(False)
            self.pushButton_runQuery.setDisabled(False)
            self.pushButton_runQuery.setText(self.pushButton_runQuery.initialText)
            self.progressBar_execution.setMinimum(0)
            self.progressBar_execution.setMaximum(100)
            self.progressBar_execution.setValue(100)
            QApplication.restoreOverrideCursor()
            QApplication.processEvents()
        
    def showQuery(self):
        '''
        Show the query in the main window
        '''
        #We have to find the widget in the stackedwidget of the main window
        queryWidget = None
        indexQuickQueryWidget = None
        for i in xrange(iface.mainWindowDialog.stackedWidget.count()):
            if iface.mainWindowDialog.stackedWidget.widget(i).__class__.__name__ == "QueryWidget":
                queryWidget = iface.mainWindowDialog.stackedWidget.widget(i)
                indexQuickQueryWidget = i
                break
        
        #Get all values
        key = unicode(self.lineEdit_key.text())
        value = unicode(self.lineEdit_value.text())
        nominatim = unicode(self.lineEdit_nominatim.text())
        timeout = self.spinBox_timeout.value()
        outputDir = self.lineEdit_browseDir.text()
        prefixFile = self.lineEdit_filePrefix.text()
        
        #If bbox, we must set None to nominatim, we can't have both
        bbox = None
        if self.radioButton_extentLayer.isChecked() or self.radioButton_extentMapCanvas.isChecked():
            nominatim = None
            bbox = True
        
        if nominatim == '':
            nominatim = None
        
        #Which osm's objects ?
        osmObjects = []
        if self.checkBox_node.isChecked():
            osmObjects.append('node')
        if self.checkBox_way.isChecked():
            osmObjects.append('way')
        if self.checkBox_relation.isChecked():
            osmObjects.append('relation')
            
        #Which geometry at the end ?
        queryWidget.checkBox_points.setChecked(self.checkBox_points.isChecked())
        queryWidget.checkBox_lines.setChecked(self.checkBox_lines.isChecked())
        queryWidget.checkBox_linestrings.setChecked(self.checkBox_linestrings.isChecked())
        queryWidget.checkBox_multipolygons.setChecked(self.checkBox_multipolygons.isChecked())
        
        queryWidget.radioButton_extentLayer.setChecked(self.radioButton_extentLayer.isChecked())
        queryWidget.radioButton_extentMapCanvas.setChecked(self.radioButton_extentMapCanvas.isChecked())
        
        #Transfer the combobox from QuickQuery to Query
        if self.comboBox_extentLayer.count():
            queryWidget.radioButton_extentLayer.setCheckable(True)
        queryWidget.comboBox_extentLayer.setModel(self.comboBox_extentLayer.model())
        
        #Transfer the output
        queryWidget.lineEdit_browseDir.setText(outputDir)
        if prefixFile:
            queryWidget.lineEdit_filePrefix.setText(prefixFile)
            queryWidget.lineEdit_filePrefix.setEnabled(True)

        #Make the query
        queryFactory = QueryFactory(timeout=timeout,key=key,value=value,bbox=bbox,nominatim=nominatim,osmObjects=osmObjects)
        query = queryFactory.make()
        queryWidget.textEdit_query.setPlainText(query)
        iface.mainWindowDialog.listWidget.setCurrentRow(indexQuickQueryWidget)
        iface.mainWindowDialog.exec_()

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

class QuickQueryDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.widget = QuickQueryWidget()
        self.setWidget(self.widget)
        self.setWindowTitle(QApplication.translate("ui_quick_query", "Quick query"))