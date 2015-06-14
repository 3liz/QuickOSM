# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
 A QGIS plugin
 OSM Overpass API frontend
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

from PyQt4.QtGui import QDialog, QSizePolicy
from PyQt4.QtCore import pyqtSignal
from qgis.gui import QgsMessageBar

from QuickOSM.core.file_query_writer import FileQueryWriter
from QuickOSM.core.utilities.tools import get_user_query_folder
from QuickOSM.core.exceptions import QuickOsmException
from save_query import Ui_ui_save_query


class SaveQueryDialog(QDialog, Ui_ui_save_query):
    
    # Signal new query
    signal_new_query_successful = pyqtSignal(
        name='signal_new_query_successful')
    
    def __init__(
            self,
            parent=None,
            query=None,
            white_list_values=None,
            output_geometry_types=None):
        """
        SaveQueryDialog constructor

        @param query:query to save
        @type query: str

        @param white_list_values: doc of layers with columns
        @type white_list_values: dic

        @param output_geometry_types: list of layers
        @type output_geometry_types: list
        """
        super(SaveQueryDialog, self).__init__(parent)
        QDialog.__init__(self)
        self.setupUi(self)
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar)
        
        self.whiteListValues = white_list_values
        self.outputGeomTypes = output_geometry_types
        self.query = query
        
    def accept(self):
        """
        On accept, we call the FileQueryWriter
        """
        category = self.lineEdit_category.text()
        name = self.lineEdit_name.text()
        
        # Get folder .qgis2/QuickOSM/queries on linux for instance
        folder = get_user_query_folder()
        
        ini_file = FileQueryWriter(
            path=folder,
            name=name,
            category=category,
            query=self.query,
            whiteListValues=self.whiteListValues,
            outputGeomTypes=self.outputGeomTypes)
        try:
            ini_file.save()
            self.signal_new_query_successful.emit()
            self.hide()
        except QuickOsmException, e:
            self.bar.pushMessage(e.msg, level=e.level, duration=e.duration)
        except Exception, e:
            self.display_exception(e)