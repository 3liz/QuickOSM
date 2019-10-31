"""Panel OSM base class."""

import re

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QDialogButtonBox,
    QMenu,
    QAction,
)

from .base_overpass_panel import BaseOverpassPanel
from .xml_highlighter import XMLHighlighter
from ..core.exceptions import MissingParameterException
from ..core.process import process_query
from ..core.query_preparation import QueryPreparation
from ..core.utilities.utilities_qgis import (
    open_map_features, open_doc_overpass, open_overpass_turbo)
from ..definitions.gui import Panels
from ..definitions.osm import LayerType
from ..qgis_plugin_tools.tools.i18n import tr
from ..qgis_plugin_tools.tools.resources import resources_path

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class QueryPanel(BaseOverpassPanel):

    """Final implementation for the panel."""

    def __init__(self, dialog):
        super().__init__(dialog)
        self.panel = Panels.Query

        # Fix #203, the XML Highlighter must be a member of the class
        self.highlighter = None

    def setup_panel(self):
        super().setup_panel()
        self.dialog.combo_query_type_q.addItem(tr('Canvas Extent'), 'canvas')
        self.dialog.combo_query_type_q.addItem(tr('Layer Extent'), 'layer')
        self.dialog.combo_query_type_q.currentIndexChanged.connect(
            self.query_type_updated)

        self.highlighter = XMLHighlighter(self.dialog.text_query.document())
        self.dialog.text_query.cursorPositionChanged.connect(
            self.highlighter.rehighlight)
        self.dialog.text_query.cursorPositionChanged.connect(
            self.allow_nominatim_or_extent)

        self.dialog.button_overpass_turbo.setIcon(
            QIcon(resources_path('icons', 'turbo.png')))
        self.dialog.button_overpass_turbo.clicked.connect(open_overpass_turbo)

        # Setup menu for documentation
        popup_menu = QMenu()
        map_features_action = QAction(
            'Map Features', self.dialog.button_documentation)
        # noinspection PyUnresolvedReferences
        map_features_action.triggered.connect(open_map_features)
        popup_menu.addAction(map_features_action)
        overpass_action = QAction('Overpass', self.dialog.button_documentation)
        # noinspection PyUnresolvedReferences
        overpass_action.triggered.connect(open_doc_overpass)
        popup_menu.addAction(overpass_action)
        self.dialog.button_documentation.setMenu(popup_menu)

        self.dialog.run_buttons[self.panel].clicked.connect(self.run)
        self.dialog.button_generate_query.clicked.connect(self.generate_query)
        self.dialog.button_box_q.button(QDialogButtonBox.Reset).clicked.connect(
            self.dialog.reset_form)

        self.allow_nominatim_or_extent()
        self.query_type_updated()

    def gather_values(self):
        properties = super().gather_values()

        properties['query'] = self.dialog.text_query.toPlainText()

        properties['expected_csv'] = dict()
        if self.dialog.checkbox_points_q.isChecked():
            properties['expected_csv'][LayerType.Points] = (
                self.dialog.edit_csv_points.text())
        if self.dialog.checkbox_lines_q.isChecked():
            properties['expected_csv'][LayerType.Lines] = (
                self.dialog.edit_csv_lines.text())
        if self.dialog.checkbox_multilinestrings_q.isChecked():
            properties['expected_csv'][LayerType.Multilinestrings] = (
                self.dialog.edit_csv_multilinestrings.text())
        if self.dialog.checkbox_multipolygons_q.isChecked():
            properties['expected_csv'][LayerType.Multipolygons] = (
                self.dialog.edit_csv_multipolygons.text())

        # TODO check this regex
        # noinspection RegExpRedundantEscape
        if not properties['place'] and \
                re.search(r'\{\{nominatim\}\}', properties['query']) or \
                re.search(r'\{\{nominatimArea:\}\}', properties['query']) \
                or \
                re.search(r'\{\{geocodeArea:\}\}', properties['query']):
            raise MissingParameterException(suffix='nominatim field')

        return properties

    def _run(self):
        self.write_nominatim_file(self.panel)
        properties = self.gather_values()
        num_layers = process_query(
            dialog=self.dialog,
            query=properties['query'],
            output_dir=properties['output_directory'],
            prefix_file=properties['prefix_file'],
            output_geometry_types=properties['outputs'],
            white_list_values=properties['expected_csv'],
            area=properties['place'],
            bbox=properties['bbox'])
        self.end_query(num_layers)

    def generate_query(self):
        query = self.dialog.text_query.toPlainText()
        area = self.dialog.places_edits[Panels.Query].text()
        self.write_nominatim_file(Panels.Query)
        bbox = self.dialog.get_bounding_box()
        query = QueryPreparation(query, bbox, area)
        query_string = query.prepare_query()
        self.dialog.text_query.setPlainText(query_string)

    def allow_nominatim_or_extent(self):
        """Disable or enable radio buttons if nominatim or extent.

        Disable buttons if the query is empty.
        """
        query = self.dialog.text_query.toPlainText()

        self.dialog.button_generate_query.setDisabled(query == '')
        self.dialog.button_run_query_q.setDisabled(query == '')

        # TODO check this regexp
        # noinspection RegExpRedundantEscape
        if re.search(r'\{\{nominatim\}\}', query) or \
                re.search(r'\{\{nominatimArea:(.*)\}\}', query) or \
                re.search(r'\{\{geocodeArea:(.*)\}\}', query):
            self.dialog.line_place_q.setEnabled(True)
        else:
            self.dialog.line_place_q.setEnabled(False)
            self.dialog.line_place_q.setText('')

        # TODO check this regexp
        # noinspection RegExpRedundantEscape
        if re.search(r'\{\{(bbox|center)\}\}', query):
            self.dialog.combo_query_type_q.setEnabled(True)
        else:
            self.dialog.combo_query_type_q.setEnabled(False)

    def query_type_updated(self):
        self._core_query_type_updated(
            self.dialog.combo_query_type_q,
            self.dialog.combo_extent_layer_q)
