"""Panel OSM base class."""

import logging

from functools import partial

from qgis.core import QgsApplication
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QCompleter,
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QListWidgetItem,
    QMenu,
    QPushButton,
)

from QuickOSM.core.exceptions import OsmObjectsException, QuickOsmException
from QuickOSM.core.parser.preset_parser import PresetsParser
from QuickOSM.core.process import process_quick_query
from QuickOSM.core.query_factory import QueryFactory
from QuickOSM.core.utilities.utilities_qgis import open_plugin_documentation
from QuickOSM.definitions.gui import Panels
from QuickOSM.definitions.osm import OsmType, QueryLanguage, QueryType
from QuickOSM.qgis_plugin_tools.tools.i18n import tr
from QuickOSM.qgis_plugin_tools.tools.resources import resources_path
from QuickOSM.ui.base_overpass_panel import BaseOverpassPanel
from QuickOSM.ui.wizard import Wizard

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

LOGGER = logging.getLogger('QuickOSM')


class QuickQueryPanel(BaseOverpassPanel):

    """Final implementation for the panel."""

    def __init__(self, dialog: QDialog):
        super().__init__(dialog)
        self.panel = Panels.QuickQuery
        self.osm_keys = None
        self.keys = None
        self.all_keys_placeholder = tr('Query on all keys')
        self.all_values_placeholder = tr('Query on all values')
        self.preset_data = None
        self.preset_items = []
        self.wizard = None

    def setup_panel(self):
        super().setup_panel()
        """Setup the UI for the QuickQuery."""

        # Setup presets auto completion
        parser = PresetsParser()
        self.preset_data = parser.parser()
        keys_preset = list(self.preset_data.elements.keys())
        keys_preset.append('')
        keys_preset.sort()
        keys_preset_completer = QCompleter(keys_preset)
        self.dialog.combo_preset.addItem(keys_preset.pop(0))
        for key in keys_preset:
            icon_path = self.preset_data.elements[key].icon
            icon_path = resources_path('icons', icon_path)
            icon = QIcon(icon_path)
            self.preset_items.append(QListWidgetItem(icon, key))
            self.dialog.combo_preset.addItem(icon, key)
        self.dialog.combo_preset.setCompleter(keys_preset_completer)
        self.dialog.combo_preset.completer().setCompletionMode(
            QCompleter.PopupCompletion)
        self.dialog.combo_preset.completer().setFilterMode(
            Qt.MatchContains
        )
        self.dialog.combo_preset.completer().setCaseSensitivity(
            Qt.CaseInsensitive
        )

        # Setup key auto completion
        self.osm_keys = parser.osm_keys_values()
        self.keys = list(self.osm_keys.keys())
        self.keys.append('')
        self.keys.sort()
        while self.keys[1] == '':
            self.keys.pop(1)

        # Table Keys/Values
        header = self.dialog.table_keys_values.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setMinimumSectionSize(50)

        add_row, remove_row, preset = self.prepare_button()

        self.dialog.table_keys_values.setCellWidget(0, 3, preset)
        self.dialog.table_keys_values.setCellWidget(0, 4, add_row)
        self.dialog.table_keys_values.setCellWidget(0, 5, remove_row)

        key_field = self.prepare_key_field()
        value_field = self.prepare_value_field()

        self.dialog.table_keys_values.setCellWidget(0, 1, key_field)
        self.dialog.table_keys_values.setCellWidget(0, 2, value_field)

        # Query type
        self.dialog.combo_query_type_qq.addItem(tr('In'), 'in')
        self.dialog.combo_query_type_qq.addItem(tr('Around'), 'around')
        self.dialog.combo_query_type_qq.addItem(tr('Canvas Extent'), 'canvas')
        self.dialog.combo_query_type_qq.addItem(tr('Layer Extent'), 'layer')
        self.dialog.combo_query_type_qq.addItem(tr('Not Spatial'), 'attributes')

        # self.cb_query_type_qq.setItemIcon(
        #   0, QIcon(resources_path('in.svg')))
        # self.cb_query_type_qq.setItemIcon(
        #   1, QIcon(resources_path('around.svg')))
        # self.cb_query_type_qq.setItemIcon(
        #   2, QIcon(resources_path('map_canvas.svg')))
        # self.cb_query_type_qq.setItemIcon(
        #   3, QIcon(resources_path('extent.svg')))
        # self.cb_query_type_qq.setItemIcon(
        #   4, QIcon(resources_path('mIconTableLayer.svg')))

        self.dialog.combo_query_type_qq.currentIndexChanged.connect(
            self.query_type_updated)

        self.dialog.line_file_prefix_qq.setDisabled(True)

        self.dialog.button_show_query.setMenu(QMenu())

        self.dialog.action_oql_qq.triggered.connect(self.query_language_oql)
        self.dialog.action_xml_qq.triggered.connect(self.query_language_xml)
        self.dialog.button_show_query.menu().addAction(self.dialog.action_oql_qq)
        self.dialog.button_show_query.menu().addAction(self.dialog.action_xml_qq)

        query_oql = partial(self.show_query, QueryLanguage.OQL)
        self.dialog.button_show_query.clicked.connect(query_oql)

        self.dialog.button_run_query_qq.clicked.connect(self.run)
        self.dialog.combo_preset.activated.connect(self.choice_preset)
        self.dialog.button_map_features.clicked.connect(open_plugin_documentation)
        self.dialog.button_box_qq.button(QDialogButtonBox.Reset).clicked.connect(
            self.dialog.reset_form)

        # setup callbacks for friendly-label-update only
        self.dialog.line_place_qq.textChanged.connect(self.update_friendly)
        self.dialog.spin_place_qq.valueChanged.connect(self.update_friendly)
        self.dialog.combo_extent_layer_qq.layerChanged.connect(self.query_type_updated)

        self.dialog.combo_preset.lineEdit().setPlaceholderText(
            tr('Write the preset you want'))
        self.query_type_updated()
        self.init_nominatim_autofill()
        self.update_friendly()

    def prepare_button(self) -> (QPushButton, QPushButton, QPushButton):
        add_row = QPushButton()
        add_row.setIcon(QIcon(QgsApplication.iconPath('symbologyAdd.svg')))
        add_row.setText('')
        remove_row = QPushButton()
        remove_row.setIcon(QIcon(QgsApplication.iconPath('symbologyRemove.svg')))
        remove_row.setText('')
        preset = QPushButton()
        preset.setText(tr('Wizard'))

        add_row.clicked.connect(self.add_row_to_table)
        remove_row.clicked.connect(self.remove_selection)
        preset.clicked.connect(self.select_preset)

        return add_row, remove_row, preset

    def prepare_type_multi_request(self) -> QComboBox:
        type_operation = QComboBox()
        type_operation.setToolTip(
            tr('Set the type of multi-request. '
                '"And" verify both conditions. "Or" verify either of the conditions.'))
        type_operation.addItem(tr('And'), 'and')
        type_operation.addItem(tr('Or'), 'or')

        type_operation.currentIndexChanged.connect(self.update_friendly)

        return type_operation

    def prepare_key_field(self) -> QComboBox:
        key_field = QComboBox()
        key_field.setEditable(True)
        key_field.setToolTip(tr('An OSM key to fetch. If empty, all keys will be fetched.'))

        keys_completer = QCompleter(self.keys)
        key_field.addItems(self.keys)
        key_field.setCompleter(keys_completer)
        key_field.completer().setCompletionMode(
            QCompleter.PopupCompletion)

        key_field.lineEdit().setPlaceholderText(
            self.all_keys_placeholder)

        row = partial(self.key_edited, None)
        key_field.editTextChanged.connect(row)

        return key_field

    def prepare_value_field(self) -> QComboBox:
        value_field = QComboBox()
        value_field.setEditable(True)
        value_field.setToolTip(tr('An OSM value to fetch. If empty, all values will be fetched.'))

        value_field.lineEdit().setPlaceholderText(
            self.all_values_placeholder)

        value_field.editTextChanged.connect(self.update_friendly)

        return value_field

    def add_row_to_table(self, row: int = None):
        # noinspection PyCallingNonCallable
        table = self.dialog.table_keys_values
        nb_row = table.rowCount()
        table.setRowCount(nb_row + 1)

        if not row:
            selection = table.selectedIndexes()
            if selection:
                row = selection[0].row()
            else:
                row = 0
        index_value = table.cellWidget(row, 2).currentIndex()

        type_operation = self.prepare_type_multi_request()

        self.dialog.table_keys_values.setCellWidget(nb_row, 0, type_operation)

        key_field = self.prepare_key_field()
        value_field = self.prepare_value_field()

        table.setCellWidget(nb_row, 1, key_field)
        table.setCellWidget(nb_row, 2, value_field)

        add_row, remove_row, preset = self.prepare_button()

        table.setCellWidget(nb_row, 3, preset)
        table.setCellWidget(nb_row, 4, add_row)
        table.setCellWidget(nb_row, 5, remove_row)

        if nb_row - 1 != row:
            for line in range(1, nb_row - row):
                key = table.cellWidget(nb_row - line, 1).currentText()
                value = table.cellWidget(nb_row - line, 2).currentText()

                index = table.cellWidget(nb_row - line + 1, 1).findText(key)
                table.cellWidget(nb_row - line + 1, 1).setCurrentIndex(index)
                self.key_edited(int(nb_row - line + 1))
                index = table.cellWidget(nb_row - line + 1, 2).findText(value)
                table.cellWidget(nb_row - line + 1, 2).setCurrentIndex(index)

                and_or = table.cellWidget(nb_row - line, 0).currentIndex()
                table.cellWidget(nb_row - line + 1, 0).setCurrentIndex(and_or)

                table.cellWidget(nb_row - line, 0).setCurrentIndex(0)
                table.cellWidget(nb_row - line, 1).setCurrentIndex(0)
                self.key_edited(int(nb_row - line))

            table.cellWidget(row, 2).setCurrentIndex(index_value)

        self.update_friendly()

    def remove_selection(self):
        """Remove the selected row from the table."""
        selection = self.dialog.table_keys_values.selectedIndexes()
        if len(selection) <= 0:
            return

        row = selection[0].row()
        if self.dialog.table_keys_values.rowCount() > 1:
            if row == 0:
                self.dialog.table_keys_values.setCellWidget(1, 0, None)
            self.dialog.table_keys_values.clearSelection()
            self.dialog.table_keys_values.removeRow(row)
            self.update_friendly()

    def query_type_updated(self):
        """Update the ui when the query type is modified."""
        self._core_query_type_updated(
            self.dialog.combo_query_type_qq,
            self.dialog.stacked_query_type,
            self.dialog.spin_place_qq,
            self.dialog.checkbox_selection_qq)
        self.update_friendly()

    def query_language_oql(self):
        """Update the wanted language."""
        super().query_language_oql()
        query_oql = partial(self.show_query, QueryLanguage.OQL)
        self.dialog.button_show_query.clicked.connect(query_oql)

    def query_language_xml(self):
        """Update the wanted language."""
        super().query_language_xml()
        query_xml = partial(self.show_query, QueryLanguage.XML)
        self.dialog.button_show_query.clicked.connect(query_xml)

    def select_preset(self):
        if self.wizard:
            self.wizard.activateWindow()
        else:
            self.wizard = Wizard(self.dialog)
            self.wizard.show()

    def choice_preset(self, choice: str = None):
        """Fill the table with the keys/values from the preset."""
        if not isinstance(choice, str):
            choice = self.dialog.combo_preset.currentText()
        element_chosen = self.preset_data.elements[choice]

        keys, values = [], []
        for item in element_chosen.heirs:
            item_chosen = self.preset_data.items[item]
            item_keys = list(item_chosen.keys())
            for key in item_keys:
                value = item_chosen[key]
                if isinstance(value, list):
                    for val in value:
                        keys.append(key)
                        values.append(val)
                elif isinstance(value, str):
                    keys.append(key)
                    values.append(value)

        table = self.dialog.table_keys_values
        selection = table.selectedIndexes()
        if selection:
            row = selection[0].row()
        else:
            row = 0
        for num in range(len(keys) - 1):
            if table.cellWidget(row + num, 0):
                table.cellWidget(row + num, 0).setCurrentIndex(1)
            index = table.cellWidget(row + num, 1).findText(keys[num])
            table.cellWidget(row + num, 1).setCurrentIndex(index)
            self.key_edited(row + num)
            index = table.cellWidget(row + num, 2).findText(values[num])
            table.cellWidget(row + num, 2).setCurrentIndex(index)
            self.add_row_to_table(row + num)
        num = len(keys) - 1
        if table.cellWidget(row + num, 0) and num != 0:
            table.cellWidget(row + num, 0).setCurrentIndex(1)
        index = table.cellWidget(row + num, 1).findText(keys[-1])
        table.cellWidget(row + num, 1).setCurrentIndex(index)
        self.key_edited(row + num)
        index = table.cellWidget(row + num, 2).findText(values[-1])
        table.cellWidget(row + num, 2).setCurrentIndex(index)

        index = table.cellWidget(row, 2).findText(values[0])
        table.cellWidget(row, 2).setCurrentIndex(index)

    def key_edited(self, row: int = None):
        """Add values to the combobox according to the key."""
        if row is None:
            selection = self.dialog.table_keys_values.selectedIndexes()
            if selection:
                row = selection[0].row()
            else:
                row = 0
        key_field = self.dialog.table_keys_values.cellWidget(row, 1)
        value_field = self.dialog.table_keys_values.cellWidget(row, 2)

        value_field.clear()
        value_field.setCompleter(None)

        try:
            current_values = self.osm_keys[key_field.currentText()]
        except KeyError:
            self.update_friendly()
            return
        except AttributeError:
            self.update_friendly()
            return

        if len(current_values) == 0:
            current_values.insert(0, '')

        if len(current_values) > 1 and current_values[0] != '':
            current_values.insert(0, '')
            current_values.sort()

        values_completer = QCompleter(current_values)
        value_field.setCompleter(values_completer)
        value_field.addItems(current_values)
        self.update_friendly()

    def gather_values(self) -> dict:
        """Retrieval of the values set by the user."""
        properties = super().gather_values()
        osm_objects = []
        if self.dialog.checkbox_node.isChecked():
            osm_objects.append(OsmType.Node)
        if self.dialog.checkbox_way.isChecked():
            osm_objects.append(OsmType.Way)
        if self.dialog.checkbox_relation.isChecked():
            osm_objects.append(OsmType.Relation)
        properties['osm_objects'] = osm_objects

        if not properties['osm_objects']:
            raise OsmObjectsException

        rows = self.dialog.table_keys_values.rowCount()
        key_added = False
        properties['key'] = []
        properties['value'] = []
        properties['type_multi_request'] = []
        for row in range(rows):
            keys = self.dialog.table_keys_values.cellWidget(row, 1)
            if keys:
                values = self.dialog.table_keys_values.cellWidget(row, 2)
                type_request = self.dialog.table_keys_values.cellWidget(row, 0)
                properties['key'].append(keys.currentText())
                properties['value'].append(values.currentText())
                if type_request:
                    properties['type_multi_request'].append(type_request.currentData())
                key_added = True
        if not key_added:
            properties['key'] = None
            properties['value'] = None
            properties['type_multi_request'] = None

        properties['timeout'] = self.dialog.spin_timeout.value()

        properties['distance'] = self.dialog.spin_place_qq.value()
        if properties['query_type'] != QueryType.AroundArea:
            properties['distance'] = None
        return properties

    def _run(self):
        """Process for running the query."""
        self.write_nominatim_file(self.panel)
        properties = self.gather_values()
        num_layers = process_quick_query(
            dialog=self.dialog,
            type_multi_request=properties['type_multi_request'],
            query_type=properties['query_type'],
            key=properties['key'],
            value=properties['value'],
            area=properties['place'],
            distance=properties['distance'],
            bbox=properties['bbox'],
            osm_objects=properties['osm_objects'],
            timeout=properties['timeout'],
            output_directory=properties['output_directory'],
            output_format=properties['output_format'],
            prefix_file=properties['prefix_file'],
            output_geometry_types=properties['outputs'])
        self.end_query(num_layers)

    def show_query(self, output: QueryLanguage):
        """Show the query in the main window."""
        self.write_nominatim_file(self.panel)
        try:
            properties = self.gather_values()
        except QuickOsmException as error:
            self.dialog.display_quickosm_exception(error)
            return
        except Exception as error:
            self.dialog.display_critical_exception(error)
            return

        # Transfer each output with zip
        check_boxes = zip(
            self.dialog.output_buttons[Panels.QuickQuery],
            self.dialog.output_buttons[Panels.Query])
        for couple in check_boxes:
            couple[1].setChecked(couple[0].isChecked())

        # Transfer the language of the query
        self.query_language_updated()

        # Transfer the output
        self.dialog.output_directory_q.setFilePath(properties['output_directory'])
        index_format = self.dialog.combo_format_q.findData(properties['output_format'])
        self.dialog.combo_format_q.setCurrentIndex(index_format)
        if properties['prefix_file']:
            self.dialog.line_file_prefix_q.setText(properties['prefix_file'])
            self.dialog.line_file_prefix_q.setEnabled(True)

        # Make the query
        query_factory = QueryFactory(
            type_multi_request=properties['type_multi_request'],
            query_type=properties['query_type'],
            key=properties['key'],
            value=properties['value'],
            area=properties['place'],
            around_distance=properties['distance'],
            osm_objects=properties['osm_objects'],
            timeout=properties['timeout']
        )
        try:
            query = query_factory.make(output)
        except QuickOsmException as error:
            self.dialog.display_quickosm_exception(error)
        except Exception as error:
            self.dialog.display_critical_exception(error)
        else:
            self.dialog.text_query.setPlainText(query)
            item = self.dialog.menu_widget.item(self.dialog.query_menu_index)
            self.dialog.menu_widget.setCurrentItem(item)

    def update_friendly(self):
        """Updates the QuickQuery friendly label (label_qq_friendly)."""
        try:
            properties = self.gather_values()
        except QuickOsmException as error:
            self.dialog.display_quickosm_exception(error)
            return
        except Exception as error:
            self.dialog.display_critical_exception(error)
            return

        # Make the query, in order to create the friendly message
        query_factory = QueryFactory(
            type_multi_request=properties['type_multi_request'],
            query_type=properties['query_type'],
            key=properties['key'],
            value=properties['value'],
            area=properties['place'],
            around_distance=properties['distance'],
            osm_objects=properties['osm_objects'],
            timeout=properties['timeout']
        )
        try:
            msg = query_factory.friendly_message()
        except QuickOsmException as error:
            self.dialog.label_qq_friendly.setStyleSheet('QLabel { color : red; }')
            self.dialog.label_qq_friendly.setText(str(error))
        except Exception as error:
            self.dialog.display_critical_exception(error)
            self.dialog.label_qq_friendly.setText('')
        else:
            self.dialog.label_qq_friendly.setStyleSheet('')
            self.dialog.label_qq_friendly.setText(msg)
