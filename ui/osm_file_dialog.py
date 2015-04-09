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
from QuickOSM.Controller.Process import Process
from osm_file import Ui_ui_osm_file
from os.path import dirname,abspath,join,isfile
from QuickOSM.CoreQuickOSM.Parser.OsmParser import *
from qgis.utils import iface

class OsmFileWidget(QuickOSMWidget, Ui_ui_osm_file):
    def __init__(self, parent=None):
        '''
        OsmFileWidget constructor
        '''
        QuickOSMWidget.__init__(self)
        self.setupUi(self)
        
        #Set UI
        self.radioButton_osmConf.setChecked(False)
        self.label_progress.setText("")
        self.lineEdit_filePrefix.setDisabled(True)
        
        #Set default osmconf
        self.defaultOsmConf = join(dirname(dirname(abspath(__file__))),"osmconf.ini")
        if not isfile(self.defaultOsmConf):
            self.defaultOsmConf = ''
        self.lineEdit_osmConf.setText(self.defaultOsmConf)
        self.pushButton_runQuery.setEnabled(False)
        
        #Connect
        self.pushButton_browseOsmFile.clicked.connect(self.setOsmFilePath)
        self.pushButton_browseOsmConf.clicked.connect(self.setOsmConfPath)
        self.lineEdit_osmConf.textEdited.connect(self.disableRunButton)
        self.lineEdit_osmFile.textEdited.connect(self.disableRunButton)
        self.radioButton_osmConf.toggled.connect(self.disableRunButton)
        self.pushButton_runQuery.clicked.connect(self.openFile)
        self.pushButton_resetIni.clicked.connect(self.resetIni)
        self.lineEdit_browseDir.textEdited.connect(self.disablePrefixFile)
        
    def setOsmFilePath(self):
        '''
        Fill the osm file
        '''
        osmFile = QFileDialog.getOpenFileName(parent=None, caption=QApplication.translate("QuickOSM", 'Select *.osm or *.pbf'),filter="OSM file (*.osm *.pbf)")
        self.lineEdit_osmFile.setText(osmFile)
        self.disableRunButton()
            
    def setOsmConfPath(self):
        '''
        Fill the osmConf file
        '''
        osmConf = QFileDialog.getOpenFileName(parent=None, caption=QApplication.translate("QuickOSM", 'Select osm conf'), filter="OsmConf file (*.ini)")
        if osmConf:
            self.lineEdit_osmConf.setText(osmConf)
        self.disableRunButton()
        
    def resetIni(self):
        '''
        Reset the default osmConf file
        '''
        self.lineEdit_osmConf.setText(self.defaultOsmConf)
            
    def disableRunButton(self):
        '''
        If the two fields are empty or allTags
        '''
        if self.lineEdit_osmFile.text():
            self.pushButton_runQuery.setEnabled(False)
        
        if self.radioButton_osmConf.isChecked():
            if self.lineEdit_osmConf.text():
                self.pushButton_runQuery.setEnabled(True)
            else:
                self.pushButton_runQuery.setEnabled(False)
        else:
            self.pushButton_runQuery.setEnabled(True)
        
    def openFile(self):
        '''
        Open the osm file with the osmconf
        '''
        
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.startProcess()
        QApplication.processEvents()
        
        #Get fields
        osmFile = self.lineEdit_osmFile.text()
        osmConf = self.lineEdit_osmConf.text()
        outputDir = self.lineEdit_browseDir.text()
        prefixFile = self.lineEdit_filePrefix.text()
        loadOnly = self.radioButton_osmConf.isChecked()
        
        #Which geometry at the end ?
        outputGeomTypes = self.getOutputGeomTypes()
        
        try:
            if not outputGeomTypes:
                raise OutPutGeomTypesException
            
            if not isfile(osmFile):
                raise FileDoesntExistException(suffix="*.osm or *.pbf")
            
            if loadOnly:
                if not isfile(osmConf):
                    raise FileDoesntExistException(suffix="*.ini")
            
            if outputDir and not os.path.isdir(outputDir):
                raise DirectoryOutPutException
            
            #Check OGR
            if not Tools.osmDriverIsEnabled():
                raise OsmDriver
        
            if loadOnly:
                osmParser = OsmParser(osmFile, loadOnly=True, osmConf=osmConf, layers=outputGeomTypes)
                layers = osmParser.parse()
                for layer,item in layers.iteritems():
                    QgsMapLayerRegistry.instance().addMapLayer(item)
            else:
                Process.openFile(dialog=self,osmFile=osmFile, outputGeomTypes = outputGeomTypes, outputDir=outputDir, prefixFile=prefixFile)
            
        except GeoAlgorithmExecutionException,e:
            self.displayGeoAlgorithmException(e)
        except Exception,e:
            self.displayException(e)
        finally:
            QApplication.restoreOverrideCursor()
            self.endProcess()
            QApplication.processEvents()

class OsmFileDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(OsmFileWidget())