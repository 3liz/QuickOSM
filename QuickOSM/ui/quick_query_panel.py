"""Panel OSM base class."""

from functools import partial

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QCompleter, QDialog, QDialogButtonBox, QMenu

from QuickOSM.core.exceptions import OsmObjectsException, QuickOsmException
from QuickOSM.core.parser.preset_parser import PresetsParser
from QuickOSM.core.process import process_quick_query
from QuickOSM.core.query_factory import QueryFactory
from QuickOSM.core.utilities.utilities_qgis import open_plugin_documentation
from QuickOSM.definitions.gui import Panels
from QuickOSM.definitions.osm import OsmType, QueryLanguage, QueryType
from QuickOSM.qgis_plugin_tools.tools.i18n import tr
from QuickOSM.ui.base_overpass_panel import BaseOverpassPanel

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class QuickQueryPanel(BaseOverpassPanel):

    """Final implementation for the panel."""

    def __init__(self, dialog: QDialog):
        super().__init__(dialog)
        self.panel = Panels.QuickQuery
        self.osm_keys = None
        self.preset_data = None

    def setup_panel(self):
        """Setup the UI for the QuickQuery."""
        super().setup_panel()
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
        self.dialog.combo_key.editTextChanged.connect(self.key_edited)
        self.dialog.button_map_features.clicked.connect(open_plugin_documentation)
        self.dialog.button_box_qq.button(QDialogButtonBox.Reset).clicked.connect(
            self.dialog.reset_form)

        # setup callbacks for friendly-label-update only
        self.dialog.combo_value.editTextChanged.connect(self.update_friendly)
        self.dialog.line_place_qq.textChanged.connect(self.update_friendly)
        self.dialog.spin_place_qq.valueChanged.connect(self.update_friendly)
        self.dialog.combo_extent_layer_qq.layerChanged.connect(self.query_type_updated)

        # Setup presets auto completion
        parser = PresetsParser()
        self.preset_data = parser.parser()
        keys_preset = list(self.preset_data.elements.keys())
        keys_preset.append('')
        keys_preset.sort()
        keys_preset_completer = QCompleter(keys_preset)
        self.dialog.combo_preset.addItems(keys_preset)
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
        keys = list(self.osm_keys.keys())
        keys.append('')
        keys.sort()
        while keys[1] == '':
            keys.pop(1)
        keys_completer = QCompleter(keys)
        self.dialog.combo_key.addItems(keys)
        self.dialog.combo_key.setCompleter(keys_completer)
        self.dialog.combo_key.completer().setCompletionMode(
            QCompleter.PopupCompletion)

        self.dialog.combo_preset.lineEdit().setPlaceholderText(
            tr('Write the preset you want'))
        self.dialog.combo_key.lineEdit().setPlaceholderText(
            tr('Query on all keys'))
        self.dialog.combo_value.lineEdit().setPlaceholderText(
            tr('Query on all values'))
        self.key_edited()
        self.query_type_updated()
        self.init_nominatim_autofill()
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

    def choice_preset(self):
        """Fill the table with the keys/values from the preset."""
        choice = self.dialog.combo_preset.currentText()
        element_chosen = self.preset_data.elements[choice]

        keys, values = [], []
        for item in element_chosen.heirs:
            item_chosen = self.preset_data.items[item]
            item_keys = list(item_chosen.keys())
            for key in item_keys:
                keys.append(key)
                value = item_chosen[key]
                if isinstance(value, list):
                    for val in value:
                        values.append(val)
                elif isinstance(value, str):
                    values.append(value)

        self.dialog.combo_key.setCurrentText(str(keys))
        self.dialog.combo_value.setCurrentText(str(values))

    def key_edited(self):
        """Add values to the combobox according to the key."""
        self.dialog.combo_value.clear()
        self.dialog.combo_value.setCompleter(None)

        try:
            current_values = self.osm_keys[self.dialog.combo_key.currentText()]
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
        self.dialog.combo_value.setCompleter(values_completer)
        self.dialog.combo_value.addItems(current_values)
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

        properties['key'] = self.dialog.combo_key.currentText()
        properties['value'] = self.dialog.combo_value.currentText()
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
