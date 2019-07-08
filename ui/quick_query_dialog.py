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

from QuickOSM.core.query_factory import QueryFactory
from QuickOSM.definitions.osm import QueryType
from QuickOSM.ui.QuickOSMWidget import QuickOSMWidget
from QuickOSM.ui.quick_query import Ui_ui_quick_query
from qgis.utils import iface


class QuickQueryWidget(QuickOSMWidget, Ui_ui_quick_query):

    def show_query(self):
        """
        Show the query in the main window
        """

        # We have to find the widget in the stacked widget of the main window
        query_widget = None
        index_quick_query_widget = None
        for i in range(iface.QuickOSM_mainWindowDialog.stackedWidget.count()):
            widget = iface.QuickOSM_mainWindowDialog.stackedWidget.widget(i)
            if widget.__class__.__name__ == "QueryWidget":
                query_widget = iface.QuickOSM_mainWindowDialog.stackedWidget.\
                    widget(i)
                index_quick_query_widget = i
                break

        # Get all values
        key = self.comboBox_key.currentText()
        value = self.comboBox_value.currentText()
        nominatim = self.lineEdit_nominatim.text()
        timeout = self.spinBox_timeout.value()
        output_directory = self.output_directory.filePath()
        prefix_file = self.lineEdit_filePrefix.text()
        query_type = self.cb_query_type.currentData()
        is_around = query_type == 'around'
        distance = self.spinBox_distance_point.value()

        # If bbox, we must set None to nominatim, we can't have both
        bbox = None
        if query_type in ['layer', 'canvas']:
            nominatim = None
            bbox = True
        elif query_type in ['attributes']:
            nominatim = None

        if nominatim == '':
            nominatim = None

        # Which osm objects ?
        osm_objects = self._get_osm_objects()

        # Which geometry at the end ?
        query_widget.checkBox_points.setChecked(
            self.checkBox_points.isChecked())
        query_widget.checkBox_lines.setChecked(
            self.checkBox_lines.isChecked())
        query_widget.checkBox_multilinestrings.setChecked(
            self.checkBox_multilinestrings.isChecked())
        query_widget.checkBox_multipolygons.setChecked(
            self.checkBox_multipolygons.isChecked())

        # What kind of extent query
        # query_widget.radioButton_extentLayer.setChecked(
        #     self.radioButton_extentLayer.isChecked())
        # query_widget.radioButton_extentMapCanvas.setChecked(
        #     self.radioButton_extentMapCanvas.isChecked())

        # Transfer the combobox from QuickQuery to Query
        # if self.comboBox_extentLayer.count():
        #     query_widget.radioButton_extentLayer.setCheckable(True)

        # Transfer the output
        query_widget.output_directory.setFilePath(output_directory)
        if prefix_file:
            query_widget.lineEdit_filePrefix.setText(prefix_file)
            query_widget.lineEdit_filePrefix.setEnabled(True)

        # TODO
        # Move this logic UP
        # Copy/paste in quick_query_dialog.py
        if is_around and nominatim:
            query_type = QueryType.AroundArea
        elif not is_around and nominatim:
            query_type = QueryType.InArea
        elif bbox:
            query_type = QueryType.BBox
        else:
            query_type = QueryType.NotSpatial
        # End todo

        # Make the query
        query_factory = QueryFactory(
            query_type=query_type,
            key=key,
            value=value,
            area=nominatim,
            around_distance=distance,
            osm_objects=osm_objects,
            timeout=timeout
        )
        query = query_factory.make()
        query_widget.textEdit_query.setPlainText(query)
        iface.QuickOSM_mainWindowDialog.listWidget.setCurrentRow(
            index_quick_query_widget)
        iface.QuickOSM_mainWindowDialog.exec_()
