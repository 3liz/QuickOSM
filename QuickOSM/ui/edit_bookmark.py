"""Dialog that edit a bookmark"""
import logging

from qgis.core import QgsCoordinateReferenceSystem
from qgis.gui import QgsExtentWidget, QgsFileWidget
from qgis.PyQt.QtCore import QPoint, Qt
from qgis.PyQt.QtWidgets import QDialog, QInputDialog, QListWidgetItem, QMenu

from QuickOSM.core.utilities.query_saved import QueryManagement
from QuickOSM.definitions.format import Format
from QuickOSM.definitions.gui import Panels
from QuickOSM.definitions.osm import LayerType
from QuickOSM.qgis_plugin_tools.tools.i18n import tr
from QuickOSM.qgis_plugin_tools.tools.resources import load_ui

__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

from QuickOSM.ui.custom_table import TableKeyValue

FORM_CLASS = load_ui('edit_bookmark.ui')
LOGGER = logging.getLogger('QuickOSM')


class EditBookmark(QDialog, FORM_CLASS, TableKeyValue):
    """Dialog that edit a bookmark"""

    def __init__(self, parent=None, data_bookmark: dict = None):
        """Constructor."""
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.dialog = parent
        self.panel = Panels.MapPreset
        TableKeyValue.__init__(self, self.table_keys_values_eb, self.combo_preset_eb)
        self.setup_preset()
        self.setup_table()

        self.previous_name = data_bookmark['file_name']
        self.current_query = 0
        self.nb_queries = len(data_bookmark['query'])

        for k in range(self.nb_queries):
            self.list_queries.addItem(data_bookmark['query_name'][k])

        self.button_add.clicked.connect(self.add_query)
        self.list_queries.currentRowChanged.connect(self.change_query)
        self.list_queries.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_queries.customContextMenuRequested.connect(self.item_context)

        self.bbox = QgsExtentWidget()
        self.bbox.setMapCanvas(parent.iface.mapCanvas())
        self.bbox_layout.addWidget(self.bbox)
        self.crs = QgsCoordinateReferenceSystem('EPSG:4326')

        self.combo_output_format.addItem(
            Format.GeoPackage.value.label, Format.GeoPackage)
        self.combo_output_format.addItem(
            Format.GeoJSON.value.label, Format.GeoJSON)
        self.combo_output_format.addItem(
            Format.Shapefile.value.label, Format.Shapefile)
        self.combo_output_format.addItem(
            Format.Kml.value.label, Format.Kml)

        self.output_directory.lineEdit().setPlaceholderText(
            tr('Save to temporary file'))
        self.output_directory.setStorageMode(
            QgsFileWidget.GetDirectory)

        self.data = data_bookmark.copy()
        if self.data:
            self.bookmark_name.setText(self.data['file_name'])
            self.description.setPlainText('\\n'.join(self.data['description']))

            if self.data['advanced']:
                self.radio_advanced.setChecked(True)
                self.change_type_bookmark()
            self.data_filling_form()

        self.radio_advanced.toggled.connect(self.change_type_bookmark)
        self.button_validate.clicked.connect(self.validate)
        self.button_cancel.clicked.connect(self.close)

    def item_context(self, pos: QPoint):
        """Set context submenu to delete item in the list."""
        item = self.list_queries.mapToGlobal(pos)
        submenu = QMenu()
        delete_action = submenu.addAction(tr('Delete'))
        rename_action = submenu.addAction(tr('Rename'))
        right_click_item = submenu.exec_(item)
        if right_click_item and right_click_item == delete_action:
            index = self.list_queries.indexAt(pos).row()
            self.delete_query(index)
        if right_click_item and right_click_item == rename_action:
            query = self.list_queries.itemAt(pos)
            self.rename_query(query)

    def data_filling_form(self, num_query: int = 0):
        """Writing the form with data from bookmark"""

        self.layer_name.setText(self.data['query_layer_name'][num_query])
        self.query.setPlainText(self.data['query'][num_query])
        keys = self.data['keys'][num_query]
        values = self.data['values'][num_query]
        type_multi_request = self.data['type_multi_request'][num_query]
        self.fill_table(keys, values, type_multi_request)

        self.area.setText(self.data['area'][num_query])
        if self.data['bbox'][num_query]:
            self.bbox.setOutputExtentFromUser(self.data['bbox'][num_query], self.crs)
        else:
            self.bbox.clear()

        if LayerType.Points in self.data['output_geom_type'][num_query]:
            self.checkbox_points.setChecked(True)
        else:
            self.checkbox_points.setChecked(False)
        if LayerType.Lines in self.data['output_geom_type'][num_query]:
            self.checkbox_lines.setChecked(True)
        else:
            self.checkbox_lines.setChecked(False)
        if LayerType.Multilinestrings in self.data['output_geom_type'][num_query]:
            self.checkbox_multilinestrings.setChecked(True)
        else:
            self.checkbox_multilinestrings.setChecked(False)
        if LayerType.Multipolygons in self.data['output_geom_type'][num_query]:
            self.checkbox_multipolygons.setChecked(True)
        else:
            self.checkbox_multipolygons.setChecked(False)

        if self.data['white_list_column'][num_query]['points']:
            self.white_points.setText(self.data['white_list_column'][num_query]['points'])
        if self.data['white_list_column'][num_query]['lines']:
            self.white_lines.setText(self.data['white_list_column'][num_query]['lines'])
        if self.data['white_list_column'][num_query]['multilinestrings']:
            self.white_multilinestrings.setText(self.data['white_list_column'][num_query]['multilinestrings'])
        if self.data['white_list_column'][num_query]['multipolygons']:
            self.white_multipolygons.setText(self.data['white_list_column'][num_query]['multipolygons'])

        index = self.combo_output_format.findData(self.data['output_format'][num_query])
        self.combo_output_format.setCurrentIndex(index)

        self.output_directory.setFilePath(self.data['output_directory'][num_query])

    def change_type_bookmark(self):
        """Update the form according the bookmark type."""
        if self.radio_advanced.isChecked():
            self.stacked_parameters_bookmark.setCurrentWidget(self.advanced_parameters)
        else:
            self.stacked_parameters_bookmark.setCurrentWidget(self.basic_parameters)

    def change_query(self):
        """Display the selected query in the view."""
        self.gather_parameters(self.current_query)
        self.current_query = self.list_queries.currentRow()
        self.data_filling_form(self.current_query)

    def add_query(self):
        """Add a query in the bookmark"""
        q_manage = QueryManagement()
        self.data = q_manage.add_empty_query_in_bookmark(self.data)

        new_query = QListWidgetItem(tr('Query ') + str(self.nb_queries + 1))
        self.list_queries.addItem(new_query)
        self.nb_queries += 1

        self.list_queries.setCurrentItem(new_query)

    def delete_query(self, row: int):
        """Delete a query in the bookmark"""
        self.nb_queries -= 1

        self.list_queries.takeItem(row)

        q_manage = QueryManagement()
        self.data = q_manage.remove_query_in_bookmark(self.data, row)

        for k in range(row, self.nb_queries):
            self.list_queries.item(k).setText(tr('Query ') + str(k + 1))

        self.current_query = self.list_queries.currentRow()

    def rename_query(self, query: QListWidgetItem):
        """Rename a query in the bookmark"""
        input_dialog = QInputDialog(self)
        new_name = input_dialog.getText(
            self, tr("Rename the query"),
            tr("New name:"))
        if new_name[1] and new_name[0]:
            query.setText(new_name[0])

    def show_extent_canvas(self):
        """Show the extent in the canvas"""
        if self.data['bbox'][self.current_query]:
            self.canvas.setMapTool(self.show_extent_tool)
            self.show_extent_tool.show_extent(self.data['bbox'][self.current_query])

            self.setVisible(False)
            self.dialog.setVisible(False)

    def end_show_extent(self):
        """End the show of the extent."""
        self.canvas.unsetMapTool(self.show_extent_tool)

        self.setVisible(True)
        self.dialog.setVisible(True)

    def gather_general_parameters(self):
        """Save the general parameters."""
        self.data['file_name'] = self.bookmark_name.text()
        description = self.description.toPlainText().split('\\n')
        self.data['description'] = description
        self.data['advanced'] = self.radio_advanced.isChecked()
        list_name_queries = [self.list_queries.item(k).text() for k in range(self.list_queries.count())]
        self.data['query_name'] = list_name_queries

    def gather_parameters(self, num_query: int = 0):
        """Save the parameters."""
        self.data['query_layer_name'][num_query] = self.layer_name.text()
        self.data['query'][num_query] = self.query.toPlainText()
        properties = self.gather_couple({})
        self.data['keys'][num_query] = properties['key']
        self.data['values'][num_query] = properties['value']
        self.data['type_multi_request'][num_query] = properties['type_multi_request']
        self.data['area'][num_query] = self.area.text()
        if self.bbox.outputExtent():
            self.bbox.setOutputCrs(self.crs)
            self.data['bbox'][num_query] = self.bbox.outputExtent()
        else:
            self.data['bbox'][num_query] = ''

        output_geom = []
        if self.checkbox_points.isChecked():
            output_geom.append(LayerType.Points)
        if self.checkbox_lines.isChecked():
            output_geom.append(LayerType.Lines)
        if self.checkbox_multilinestrings.isChecked():
            output_geom.append(LayerType.Multilinestrings)
        if self.checkbox_multipolygons.isChecked():
            output_geom.append(LayerType.Multipolygons)
        self.data['output_geom_type'][num_query] = output_geom

        if self.white_points.text():
            white_list = {'points': self.white_points.text()}
        else:
            white_list = {'points': None}
        if self.white_lines.text():
            white_list['lines'] = self.white_lines.text()
        else:
            white_list['lines'] = None
        if self.white_multilinestrings.text():
            white_list['multilinestrings'] = self.white_multilinestrings.text()
        else:
            white_list['multilinestrings'] = None
        if self.white_multipolygons.text():
            white_list['multipolygons'] = self.white_multipolygons.text()
        else:
            white_list['multipolygons'] = None
        self.data['white_list_column'][num_query] = white_list

        self.data['output_format'][num_query] = self.combo_output_format.currentData()
        self.data['output_directory'][num_query] = self.output_directory.filePath()

    def validate(self):
        """Update the bookmark"""
        self.gather_parameters(self.current_query)
        self.gather_general_parameters()

        q_manage = QueryManagement()
        if self.previous_name != self.data['file_name']:
            q_manage.rename_bookmark(self.previous_name, self.data['file_name'], self.data)
        else:
            q_manage.update_bookmark(self.data)

        self.dialog.external_panels[Panels.MapPreset].update_bookmark_view()
        self.close()
