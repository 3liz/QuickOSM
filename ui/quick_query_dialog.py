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
from quick_query import Ui_Form      
from QuickOSM.Controller.Process import Process


class QuickQueryWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setupUi(self)
                
        #connect
        self.buttonBox.rejected.connect(self.onReject)
        self.buttonBox.accepted.connect(self.onAccept)
        self.pushButton_browse_output_file.clicked.connect(self.setOutFilePath)
        
    def setOutFilePath(self):
        outputFile = QFileDialog.getSaveFileName(None, QApplication.translate("QuickOSM", 'Select file'),'output',"Shapefiles (*.shp)")
        self.lineEdit_browseFile.setText(outputFile)
        
    def onAccept(self):
        key = unicode(self.lineEdit_key.text())
        value = unicode(self.lineEdit_value.text())
        nominatim = unicode(self.lineEdit_nominatim.text())
        timeout = self.spinBox_timeout.value()
        output = self.lineEdit_browseFile.text()
        
        osmObjects = []
        if self.checkBox_node.isChecked():
            osmObjects.append('node')
        if self.checkBox_way.isChecked():
            osmObjects.append('way')
        if self.checkBox_relation.isChecked():
            osmObjects.append('relation')

        #miss bbox
        quickQuery = Process.ProcessQuickQuery(key=key, value=value, nominatim=nominatim, osmObjects=osmObjects, timeout=timeout, output=output)
        print quickQuery
        
    def onReject(self):
        print "bye"

class QuickQueryDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.widget = QuickQueryWidget()
        self.setWidget(self.widget)
        self.setWindowTitle(QApplication.translate("Form", "Quick query"))