"""Panel OSM base class."""

from json import load
from os.path import isfile

from qgis.PyQt.QtWidgets import QDialogButtonBox, QCompleter

from .base_overpass_panel import BaseOverpassPanel
from ..core.exceptions import OsmObjectsException, QuickOsmException
from ..core.process import process_quick_query
from ..core.query_factory import QueryFactory
from ..core.utilities.utilities_qgis import open_map_features
from ..definitions.gui import Panels
from ..definitions.osm import QueryType, OsmType
from ..qgis_plugin_tools.tools.i18n import tr
from ..qgis_plugin_tools.tools.resources import resources_path


__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class QuickQueryPanel(BaseOverpassPanel):

    """Final implementation for the panel."""

    def __init__(self, dialog):
        super().__init__(dialog)
        self.panel = Panels.QuickQuery
        self.osm_keys = None
        
    def setup_panel(self):
        super().setup_panel()
        """Setup the UI for the QuickQuery."""
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

        self.dialog.button_run_query_qq.clicked.connect(self.run)
        self.dialog.button_show_query.clicked.connect(self.show_query)
        self.dialog.combo_key.editTextChanged.connect(self.key_edited)
        self.dialog.button_map_features.clicked.connect(open_map_features)
        self.dialog.button_box_qq.button(QDialogButtonBox.Reset).clicked.connect(
            self.dialog.reset_form)

        # setup callbacks for friendly-label-update only
        self.dialog.combo_value.editTextChanged.connect(self.update_friendly)
        self.dialog.line_place_qq.textChanged.connect(self.update_friendly)
        self.dialog.spin_place_qq.valueChanged.connect(self.update_friendly)
        self.dialog.combo_extent_layer_qq.layerChanged.connect(self.update_friendly)
                
        # Setup auto completion
        map_features_json_file = resources_path('json', 'map_features.json')
        if isfile(map_features_json_file):
            with open(map_features_json_file) as f:
                self.osm_keys = load(f)
                keys = list(self.osm_keys.keys())
                keys.append('')  # All keys request #118
                keys.sort()
                keys_completer = QCompleter(keys)
                self.dialog.combo_key.addItems(keys)
                self.dialog.combo_key.setCompleter(keys_completer)
                self.dialog.combo_key.completer().setCompletionMode(
                    QCompleter.PopupCompletion)

        self.dialog.combo_key.lineEdit().setPlaceholderText(
            tr('Query on all keys'))
        self.dialog.combo_value.lineEdit().setPlaceholderText(
            tr('Query on all values'))
        self.key_edited()
        self.query_type_updated()
        self.init_nominatim_autofill()
        self.update_friendly()

    def query_type_updated(self):
        self._core_query_type_updated(
            self.dialog.combo_query_type_qq,
            self.dialog.stacked_query_type,
            self.dialog.spin_place_qq)
        self.update_friendly()

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

        values_completer = QCompleter(current_values)
        self.dialog.combo_value.setCompleter(values_completer)
        self.dialog.combo_value.addItems(current_values)
        self.update_friendly()

    def gather_values(self):
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
            prefix_file=properties['prefix_file'],
            output_geometry_types=properties['outputs'])
        self.end_query(num_layers)

    def show_query(self):
        """Show the query in the main window."""
        try:
            p = self.gather_values()
        except QuickOsmException as e:
            self.dialog.display_quickosm_exception(e)
            return
        except Exception as e:
            self.dialog.display_critical_exception(e)
            return

        # Transfer each output with zip
        check_boxes = zip(
            self.dialog.output_buttons[Panels.QuickQuery],
            self.dialog.output_buttons[Panels.Query])
        for couple in check_boxes:
            couple[1].setChecked(couple[0].isChecked())

        # Transfer the output
        self.dialog.output_directory_q.setFilePath(p['output_directory'])
        if p['prefix_file']:
            self.dialog.line_file_prefix_q.setText(p['prefix_file'])
            self.dialog.line_file_prefix_q.setEnabled(True)

        # Make the query
        query_factory = QueryFactory(
            query_type=p['query_type'],
            key=p['key'],
            value=p['value'],
            area=p['place'],
            around_distance=p['distance'],
            osm_objects=p['osm_objects'],
            timeout=p['timeout']
        )
        try:
            query = query_factory.make()
        except QuickOsmException as e:
            self.dialog.display_quickosm_exception(e)
        except Exception as e:
            self.dialog.display_critical_exception(e)
        else:
            self.dialog.text_query.setPlainText(query)
            item = self.dialog.menu_widget.item(self.dialog.query_menu_index)
            self.dialog.menu_widget.setCurrentItem(item)

    def update_friendly(self):
        """Updates the QuickQuery friendly label (label_qq_friendly)."""
        try:
            p = self.gather_values()
        except QuickOsmException as e:
            self.dialog.display_quickosm_exception(e)
            return
        except Exception as e:
            self.dialog.display_critical_exception(e)
            return

        # Make the query, in order to create the friendly message
        query_factory = QueryFactory(
            query_type=p['query_type'],
            key=p['key'],
            value=p['value'],
            area=p['place'],
            around_distance=p['distance'],
            osm_objects=p['osm_objects'],
            timeout=p['timeout']
        )
        try:
            msg = query_factory.friendly_message()
        except QuickOsmException as e:
            self.dialog.label_qq_friendly.setStyleSheet('QLabel { color : red; }')
            self.dialog.label_qq_friendly.setText(e.message)
        except Exception as e:
            self.dialog.display_critical_exception(e)
            self.dialog.label_qq_friendly.setText('')
        else:
            self.dialog.label_qq_friendly.setStyleSheet('')
            self.dialog.label_qq_friendly.setText(msg)
