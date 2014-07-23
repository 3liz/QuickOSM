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
from save_query import Ui_ui_save_query
from qgis.gui import QgsMessageBar
from os.path import dirname,abspath,isfile, join
from QuickOSM.CoreQuickOSM.FileQueryWriter import FileQueryWriter
from QuickOSM.CoreQuickOSM.Tools import Tools

class SaveQueryDialog(QDialog, Ui_ui_save_query):
    
    #Signal new query
    signalNewQuerySuccessful = pyqtSignal(name='signalNewQuerySuccessful')
    
    def __init__(self, parent=None, query=None,whiteListValues=None,outputGeomTypes=None):
        super(SaveQueryDialog, self).__init__(parent)
        QDialog.__init__(self)
        self.setupUi(self)
        self.whiteListValues = whiteListValues
        self.outputGeomTypes = outputGeomTypes
        self.query = query
        self.setWindowTitle(QApplication.translate("QuickOSM", "QuickOSM - Save query"))
        
    def accept(self):
        category = self.lineEdit_category.text()
        name = self.lineEdit_name.text()
        
        folder = Tools.userFolder()
        
        iniFile = FileQueryWriter(path=folder,name=name,category=category,query=self.query,whiteListValues=self.whiteListValues,outputGeomTypes=self.outputGeomTypes)
        result = iniFile.save()
        if result:
            self.signalNewQuerySuccessful.emit()
            self.hide()