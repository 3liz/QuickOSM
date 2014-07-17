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
from osm_file import Ui_ui_osm_file
from os.path import dirname,abspath,join,isfile
from QuickOSM.CoreQuickOSM.ExceptionQuickOSM import *
from QuickOSM.CoreQuickOSM.Parser.OsmParser import *
from qgis.core import QgsMapLayerRegistry
from qgis.gui import QgsMessageBar
from qgis.utils import iface

class OsmFileWidget(QWidget, Ui_ui_osm_file):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setupUi(self)
        
        defaultOsmConf = join(dirname(dirname(abspath(__file__))),"CoreQuickOSM","Parser","osmconf.ini")
        self.lineEdit_osmConf.setText(defaultOsmConf)
        self.pushButton_openOsmFile.setEnabled(False)
        
        #Connect
        self.pushButton_browseOsmFile.clicked.connect(self.setOsmFilePath)
        self.pushButton_browseOsmConf.clicked.connect(self.setOsmConfPath)
        self.lineEdit_osmConf.textEdited.connect(self.disableRunButton)
        self.lineEdit_osmFile.textEdited.connect(self.disableRunButton)
        self.pushButton_openOsmFile.clicked.connect(self.openFile)
        
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
        self.lineEdit_osmConf.setText(osmConf)
        self.disableRunButton()
            
    def disableRunButton(self):
        if self.lineEdit_osmConf.text() and self.lineEdit_osmFile.text():
            self.pushButton_openOsmFile.setEnabled(True)
        else:
            self.pushButton_openOsmFile.setEnabled(False)
        
    def openFile(self):
        #Get fields
        osmFile = self.lineEdit_osmFile.text()
        osmConf = self.lineEdit_osmConf.text()
        
        #Which geometry at the end ?
        outputGeomTypes = []
        if self.checkBox_points.isChecked():
            outputGeomTypes.append('points')
        if self.checkBox_lines.isChecked():
            outputGeomTypes.append('lines')
        if self.checkBox_multilinestrings.isChecked():
            outputGeomTypes.append('multilinestrings')
        if self.checkBox_multipolygons.isChecked():
            outputGeomTypes.append('multipolygons')
        
        try:
            if not isfile(osmFile):
                raise FileDoesntExistException(suffix="*.osm or *.pbf")
            
            if not isfile(osmConf):
                raise FileDoesntExistException(suffix="*.ini")
            
            osmParser = OsmParser(osmFile, loadOnly=True, osmConf=osmConf, layers = outputGeomTypes)
            layers = osmParser.parse()
            for layer,item in layers.iteritems():
                QgsMapLayerRegistry.instance().addMapLayer(item)
            
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

class OsmFileDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(OsmFileWidget())
        self.setWindowTitle(QApplication.translate("ui_osm_file", "OSM File"))