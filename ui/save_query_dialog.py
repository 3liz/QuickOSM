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
from __future__ import absolute_import

from qgis.PyQt.QtWidgets import QDialog, QSizePolicy
from qgis.PyQt.QtCore import pyqtSignal
from qgis.gui import QgsMessageBar

from QuickOSM.core.file_query_writer import FileQueryWriter
from QuickOSM.core.utilities.tools import get_user_query_folder
from QuickOSM.core.exceptions import \
    QuickOsmException, MissingParameterException
from .save_query import Ui_ui_save_query


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
        self.message_bar = QgsMessageBar()
        self.message_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.message_bar)

        self.white_list_values = white_list_values
        self.output_geometry_types = output_geometry_types
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
            white_list_values=self.white_list_values,
            output_geometry_types=self.output_geometry_types)
        try:

            if not category:
                raise MissingParameterException(suffix='category')
            if not name:
                raise MissingParameterException(suffix='name')

            ini_file.save()
            self.signal_new_query_successful.emit()
            self.hide()
        except QuickOsmException as e:
            self.message_bar.pushMessage(
                e.msg, level=e.level, duration=e.duration)
        except Exception as e:  # pylint: disable=broad-except
            self.display_exception(e)
