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
from save_query import Ui_ui_save_query
from os.path import dirname,abspath,isfile, join
from QuickOSM.CoreQuickOSM.FileQueryWriter import FileQueryWriter
from QuickOSM.CoreQuickOSM.Tools import Tools

class SaveQueryDialog(QDialog, Ui_ui_save_query):
    
    #Signal new query
    signalNewQuerySuccessful = pyqtSignal(name='signalNewQuerySuccessful')
    
    def __init__(self, parent=None, query=None,whiteListValues=None,outputGeomTypes=None):
        '''
        SaveQueryDialog constructor
        @param query:query to save
        @type query: str
        @param whiteListValues: doc of layers with columns
        @type whiteListValues: dic
        @param outputGeomTypes: list of layers
        @type outputGeomTypes: list
        '''
        super(SaveQueryDialog, self).__init__(parent)
        QDialog.__init__(self)
        self.setupUi(self)
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )
        self.layout().addWidget(self.bar)
        
        self.whiteListValues = whiteListValues
        self.outputGeomTypes = outputGeomTypes
        self.query = query
        
    def accept(self):
        '''
        On accept, we call the FileQueryWriter
        '''
        category = self.lineEdit_category.text()
        name = self.lineEdit_name.text()
        
        #Get folder .qgis2/QuickOSM/queries on linux for instance
        folder = Tools.getUserQueryFolder()
        
        iniFile = FileQueryWriter(path=folder,name=name,category=category,query=self.query,whiteListValues=self.whiteListValues,outputGeomTypes=self.outputGeomTypes)
        try:
            iniFile.save()
            self.signalNewQuerySuccessful.emit()
            self.hide()
        except GeoAlgorithmExecutionException,e:
            self.bar.pushMessage(e.msg, level=e.level , duration=e.duration)
        except Exception,e:
            import sys,os
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            ex_type, ex, tb = sys.exc_info()
            import traceback
            traceback.print_tb(tb)
            self.bar.pushMessage("Error in the python console, please report it", level=QgsMessageBar.CRITICAL , duration=5)