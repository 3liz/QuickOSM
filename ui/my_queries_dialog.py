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
from qgis.core import *
from my_queries import Ui_ui_my_queries
from QuickOSM.Controller.Process import Process
from qgis.gui import QgsMessageBar
from os.path import dirname,abspath,isfile, join
from QuickOSM.CoreQuickOSM.FileQuery import FileQuery
from QuickOSM.CoreQuickOSM.ExceptionQuickOSM import *
from QuickOSM.CoreQuickOSM.Tools import *
from qgis.utils import iface
import os
import re

class MyQueriesWidget(QWidget, Ui_ui_my_queries):
    def __init__(self, parent=None):
        '''
        MyQueriesWidget constructor
        '''
        QWidget.__init__(self)
        self.setupUi(self)
        
        #Setup UI
        self.pushButton_runQuery.setDisabled(True)
        self.pushButton_showQuery.setDisabled(True)
        self.groupBox.setDisabled(True)
        self.fillLayerCombobox()
        self.fillTree()
        
        #Connect
        self.pushButton_runQuery.clicked.connect(self.runQuery)
        self.pushButton_showQuery.clicked.connect(self.showQuery)
        self.pushButton_browse_output_file.clicked.connect(self.setOutDirPath)
        self.lineEdit_browseDir.textEdited.connect(self.disablePrefixFile)
        self.treeQueries.doubleClicked.connect(self.openAndRunQuery)
        self.treeQueries.customContextMenuRequested.connect(self.showPopupMenu)
        self.treeQueries.clicked.connect(self.openQuery)
        self.lineEdit_search.textChanged.connect(self.textChanged)
        self.radioButton_extentLayer.toggled.connect(self.extentRadio)
        self.pushButton_refreshLayers.clicked.connect(self.fillLayerCombobox)

    def fillTree(self, force=False):
        '''
        Fill the tree with queries
        '''
        
        self.treeQueries.clear()
        
        #Get the folder and all filequeries
        folder = Tools.userFolder()
        catfiles = FileQuery.getIniFilesFromFolder(folder,force=force)
        
        #Fill all categories
        for cat,files in catfiles.iteritems():
            catItem = QTreeWidgetItem([cat],0)
            self.treeQueries.addTopLevelItem(catItem)
            for file in files:
                queryItem = TreeQueryItem(catItem,file)
                self.treeQueries.addTopLevelItem(queryItem)
            
        self.treeQueries.resizeColumnToContents(0)
        
    def textChanged(self):
        '''
        Update the tree according to the search box
        '''
        text = self.lineEdit_search.text().strip(' ').lower()
        self.__filterItem(self.treeQueries.invisibleRootItem(), text)
        if text:
            self.treeQueries.expandAll()
        else:
            self.treeQueries.collapseAll()

    def __filterItem(self, item, text):
        '''
        search an item in the tree
        '''
        if (item.childCount() > 0):
            show = False
            for i in xrange(item.childCount()):
                child = item.child(i)
                showChild = self.__filterItem(child, text)
                show = showChild or show
            item.setHidden(not show)
            return show
        elif isinstance(item, (TreeQueryItem)):
            hide = bool(text) and (text not in item.text(0).lower())
            item.setHidden(hide)
            return not hide
        else:
            item.setHidden(True)
            return False

    def showPopupMenu(self, point):
        '''
        Right click in the tree
        '''
        item = self.treeQueries.itemAt(point)
        if isinstance(item, TreeQueryItem):
            config = item.query.getContent()
            
            #We set the query
            self.currentQuery = config['metadata']['query']
            
            #We create the menu
            popupmenu = QMenu()
            executeAction = QAction(QApplication.translate("QuickOSM", 'Execute'), self.treeQueries)
            executeAction.triggered.connect(self.openAndRunQuery)
            popupmenu.addAction(executeAction)
            showAction = QAction(QApplication.translate("QuickOSM", 'Show query'), self.treeQueries)
            showAction.triggered.connect(self.showQuery)
            popupmenu.addAction(showAction)
            deleteAction = QAction(QApplication.translate("QuickOSM", 'Delete'), self.treeQueries)
            deleteAction.triggered.connect(self.deleteQuery)
            popupmenu.addAction(deleteAction)
            popupmenu.exec_(self.treeQueries.mapToGlobal(point))

    def openAndRunQuery(self):
        '''
        If we choose "execute" from the right-click menu
        '''
        item = self.treeQueries.currentItem()
        if isinstance(item, TreeQueryItem):
            self.openQuery()
            self.runQuery()
    
    def openQuery(self):
        '''
        simple click on the tree
        open the query
        '''
        item = self.treeQueries.currentItem()
        if isinstance(item, TreeQueryItem):
            template = item.query.isTemplate()
            if template['bbox']:
                self.radioButton_extentLayer.setEnabled(True)
                self.radioButton_extentMapCanvas.setEnabled(True)
                if self.radioButton_extentLayer.isChecked():
                    self.comboBox_extentLayer.setEnabled(True)
                else:
                    self.comboBox_extentLayer.setEnabled(False)
            else:
                self.radioButton_extentLayer.setEnabled(False)
                self.radioButton_extentMapCanvas.setEnabled(False)
        
            if template['nominatim']:
                self.lineEdit_nominatim.setEnabled(True)
            else:
                self.lineEdit_nominatim.setEnabled(False)
                self.lineEdit_nominatim.setText("")
                
            config = item.query.getContent()
            self.configLayer = config['layers']
            self.checkBox_points.setChecked(self.configLayer['points']['load'])
            self.lineEdit_csv_points.setText(self.configLayer['points']['columns'])
            self.checkBox_lines.setChecked(self.configLayer['lines']['load'])
            self.lineEdit_csv_lines.setText(self.configLayer['lines']['columns'])
            self.checkBox_linestrings.setChecked(self.configLayer['multilinestrings']['load'])
            self.lineEdit_csv_multilinestrings.setText(self.configLayer['multilinestrings']['columns'])
            self.checkBox_multipolygons.setChecked(self.configLayer['multipolygons']['load'])
            self.lineEdit_csv_multipolygons.setText(self.configLayer['multipolygons']['columns'])
            self.currentQuery = config['metadata']['query']
            self.pushButton_runQuery.setDisabled(False)
            self.pushButton_showQuery.setDisabled(False)
            self.groupBox.setDisabled(False)
        else:
            self.groupBox.setDisabled(True)
            self.pushButton_runQuery.setDisabled(True)
            self.pushButton_showQuery.setDisabled(True)

    def deleteQuery(self):
        '''
        If we want to delete the query from the right-click menu
        '''
        item = self.treeQueries.currentItem()
        if isinstance(item, TreeQueryItem):
            ret = QMessageBox.warning(self, "QuickOSM",QApplication.translate("QuickOSM","Are you sure you want to delete the query ?"),QMessageBox.Yes,QMessageBox.Cancel)
            if (ret == QMessageBox.Yes):
                QFile.remove(item.query.getFilePath())
                QFile.remove(item.query.getQueryFile())
                contents = item.query.getContent()
                layers = contents['layers']
                for layer in layers:
                    if layers[layer]['style']:
                        QFile.remove(layers[layer]['style'])
                self.fillTree(force=True)

    def extentRadio(self):
        '''
        Disable or enable the comboxbox
        '''
        if self.radioButton_extentLayer.isChecked():
            self.comboBox_extentLayer.setDisabled(False)
        else:
            self.comboBox_extentLayer.setDisabled(True)
            
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
        
    def runQuery(self):
        '''
        Process for running the query
        '''
        #Block the button and save the initial text
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.pushButton_browse_output_file.setDisabled(True)
        self.pushButton_runQuery.setDisabled(True)
        self.pushButton_runQuery.initialText = self.pushButton_runQuery.text()
        self.pushButton_runQuery.setText(QApplication.translate("QuickOSM","Running query ..."))
        self.progressBar_execution.setMinimum(0)
        self.progressBar_execution.setMaximum(0)
        self.progressBar_execution.setValue(0)
        self.label_progress.setText("")
        QApplication.processEvents()
        
        #Get all values
        query = self.currentQuery
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
            if not outputGeomTypes:
                raise OutPutGeomTypesException
            
            if outputDir and not os.path.isdir(outputDir):
                raise DirectoryOutPutException

            if not nominatim and (re.search('{{nominatim}}', query) or re.search('{{nominatimArea:}}', query)):
                raise MissingParameterException(suffix="nominatim field")

            numLayers = Process.ProcessQuery(dialog = self, query=query, outputDir=outputDir, prefixFile=prefixFile,outputGeomTypes=outputGeomTypes, whiteListValues=whiteListValues, nominatim=nominatim, bbox=bbox, configOutputs=self.configLayer)
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
            #self.pushButton_generateQuery.setDisabled(False)
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
        for i in xrange(iface.QuickOSM_mainWindowDialog.stackedWidget.count()):
            if iface.QuickOSM_mainWindowDialog.stackedWidget.widget(i).__class__.__name__ == "QueryWidget":
                queryWidget = iface.QuickOSM_mainWindowDialog.stackedWidget.widget(i)
                indexQuickQueryWidget = i
                break
        
        #Get all values
        query = self.currentQuery
        outputDir = self.lineEdit_browseDir.text()
        prefixFile = self.lineEdit_filePrefix.text()
        nominatim = self.lineEdit_nominatim.text()
        
        #If bbox, we must set None to nominatim, we can't have both
        bbox = None
        if self.radioButton_extentLayer.isChecked() or self.radioButton_extentMapCanvas.isChecked():
            nominatim = None
            bbox = True
        
        if nominatim == '':
            nominatim = None
            
        #Which geometry at the end ?
        queryWidget.checkBox_points.setChecked(self.checkBox_points.isChecked())
        queryWidget.lineEdit_csv_points.setText(self.lineEdit_csv_points.text())
        
        queryWidget.checkBox_lines.setChecked(self.checkBox_lines.isChecked())
        queryWidget.lineEdit_csv_lines.setText(self.lineEdit_csv_lines.text())
        
        queryWidget.checkBox_linestrings.setChecked(self.checkBox_linestrings.isChecked())
        queryWidget.lineEdit_csv_multilinestrings.setText(self.lineEdit_csv_multilinestrings.text())
        
        queryWidget.checkBox_multipolygons.setChecked(self.checkBox_multipolygons.isChecked())
        queryWidget.lineEdit_csv_multipolygons.setText(self.lineEdit_csv_multipolygons.text())
        
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

        #Transfert the query
        queryWidget.textEdit_query.setPlainText(query)
        iface.QuickOSM_mainWindowDialog.listWidget.setCurrentRow(indexQuickQueryWidget)
        iface.QuickOSM_mainWindowDialog.exec_()

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
            
class TreeQueryItem(QTreeWidgetItem):
    '''
    Class QTreeQueryItem which populate the tree
    '''
    def __init__(self, parent, query):
        QTreeWidgetItem.__init__(self,parent)
        self.query = query
        icon = query.getIcon()
        name = query.getName()
        if icon:
            self.setIcon(0, icon)
        self.setToolTip(0, name)
        self.setText(0, name)

class MyQueriesDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(MyQueriesWidget())
        self.setWindowTitle(QApplication.translate("ui_my_queries", "QuickOSM - My queries"))
        
    def onNewQuerySuccessful(self):
        '''
        Slots which refresh the tree
        '''
        self.widget().fillTree(force=True)