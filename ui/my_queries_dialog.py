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
from QuickOSMWidget import *
from my_queries import Ui_ui_my_queries
from QuickOSM.Controller.Process import Process
from os.path import dirname,abspath,isfile, join
from QuickOSM.CoreQuickOSM.FileQuery import FileQuery
from QuickOSM.CoreQuickOSM.Tools import *
from qgis.utils import iface
import os
import re

class MyQueriesWidget(QuickOSMWidget, Ui_ui_my_queries):
    
    signalDeleteQuerySuccessful = pyqtSignal(name='signalDeleteQuerySuccessful')
    
    def __init__(self, parent=None):
        '''
        MyQueriesWidget constructor
        '''
        QuickOSMWidget.__init__(self)
        self.setupUi(self)
        
        #Setup UI
        self.label_progress.setText("")
        self.pushButton_runQuery.setDisabled(True)
        self.pushButton_showQuery.setDisabled(True)
        self.groupBox.setDisabled(True)
        self.lineEdit_nominatim.setEnabled(False)
        self.radioButton_extentLayer.setEnabled(False)
        self.radioButton_extentMapCanvas.setEnabled(False)
        
        self.fillLayerCombobox()
        self.fillTree()
        self.groupBox.setCollapsed(True)
        
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
        @param force:To force the tree to refresh. Force=False with class's var in FileQuery to avoir to parse twice each query
        @type force: bool
        '''
        
        self.treeQueries.clear()
        
        #Get the folder and all filequeries
        folder = Tools.getUserQueryFolder()
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
        @param item: check if the item should be shown
        @type item: QTreeItem
        @param text: text to search
        @type text: str
        @return: show or hide the item
        @rtype: bool 
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
        @param point:Cursor's point
        @type point:QPoint
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
                
                if template['nominatimDefaultValue']:
                    self.lineEdit_nominatim.setPlaceholderText(template['nominatimDefaultValue'] + " " + QApplication.translate("QuickOSM","can be overridden"))
                else:
                    self.lineEdit_nominatim.setPlaceholderText(QApplication.translate("QuickOSM","A village, a town, ..."))
                
            else:
                self.lineEdit_nominatim.setEnabled(False)
                self.lineEdit_nominatim.setText("")
                self.lineEdit_nominatim.setPlaceholderText("")
                
            config = item.query.getContent()
            self.configLayer = config['layers']
            #setup the UI with parameters
            self.checkBox_points.setChecked(self.configLayer['points']['load'])
            self.lineEdit_csv_points.setText(self.configLayer['points']['columns'])
            self.checkBox_lines.setChecked(self.configLayer['lines']['load'])
            self.lineEdit_csv_lines.setText(self.configLayer['lines']['columns'])
            self.checkBox_multilinestrings.setChecked(self.configLayer['multilinestrings']['load'])
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
                self.signalDeleteQuerySuccessful.emit()
        
    def runQuery(self):
        '''
        Process for running the query
        '''
        #Block the button and save the initial text

        self.pushButton_browse_output_file.setDisabled(True)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.startProcess()
        QApplication.processEvents()
        
        #Get all values
        query = self.currentQuery
        outputDir = self.lineEdit_browseDir.text()
        prefixFile = self.lineEdit_filePrefix.text()
        nominatim = self.lineEdit_nominatim.text()
        
        #Set the bbox
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

            numLayers = Process.ProcessQuery(dialog = self, query=query, outputDir=outputDir, prefixFile=prefixFile,outputGeomTypes=outputGeomTypes, whiteListValues=whiteListValues, nominatim=nominatim, bbox=bbox, configOutputs=self.configLayer)
            if numLayers:
                Tools.displayMessageBar(QApplication.translate("QuickOSM",u"Successful query !"), level=QgsMessageBar.INFO , duration=5)
                self.label_progress.setText(QApplication.translate("QuickOSM",u"Successful query !"))
            else:
                Tools.displayMessageBar(QApplication.translate("QuickOSM", u"Successful query, but no result."), level=QgsMessageBar.WARNING , duration=7)
        
        except GeoAlgorithmExecutionException,e:
            self.displayGeoAlgorithmException(e)
        except Exception,e:
            self.displayException(e)
                    
        finally:
            #Resetting the button
            self.pushButton_browse_output_file.setDisabled(False)
            QApplication.restoreOverrideCursor()
            self.endProcess()
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
        
        queryWidget.checkBox_multilinestrings.setChecked(self.checkBox_multilinestrings.isChecked())
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
    
    signalDeleteQuerySuccessful = pyqtSignal(name='signalDeleteQuerySuccessful')
    
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(MyQueriesWidget())
        self.setWindowTitle(QApplication.translate("ui_my_queries", "QuickOSM - My queries"))
        
        self.widget().signalDeleteQuerySuccessful.connect(self.signalDeleteQuerySuccessful.emit)
        
    def refreshMyQueriesTree(self):
        '''
        Slots which refresh the tree
        '''
        self.widget().fillTree(force=True)