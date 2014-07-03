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
#from QuickOSM.Controller.Process import ProcessQuickQuery


class QuickQueryWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setupUi(self)
        
        #Fill the combox
        osmObjects = {"all":"All","node":'Node','way':'Way','relation':'Relation'}
        for key, value in osmObjects.iteritems():
            self.comboBox_osmObjects.addItem(value, key)
        
        #connect
        self.buttonBox.rejected.connect(self.onReject)
        self.buttonBox.accepted.connect(self.onAccept)
        
    def onAccept(self):
        key = unicode(self.lineEdit_key.text())
        value = unicode(self.lineEdit_value.text())
        nominatim = unicode(self.lineEdit_nominatim.text())
        timeout = self.spinBox_timeout.value()
        
        #Checkbox ?
        osmObjects = self.comboBox_osmObjects.itemData(self.comboBox_osmObjects.currentIndex())
        if osmObjects == 'all':
            print "ok"
        
        print osmObjects
        
    def onReject(self):
        print "bye"

class QuickQueryDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.widget = QuickQueryWidget()
        self.setWidget(self.widget)
        self.setWindowTitle(QApplication.translate("Form", "Quick query"))