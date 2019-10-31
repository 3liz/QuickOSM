"""Panel OSM Queries based on Overpass base class."""

import io

from qgis.core import (
    Qgis,
    QgsGeometry,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
)
from qgis.PyQt.QtWidgets import QCompleter

from .base_processing_panel import BaseProcessingPanel
from ..core.exceptions import MissingLayerUI
from ..core.utilities.tools import nominatim_file
from ..definitions.gui import Panels
from ..definitions.osm import QueryType
from ..qgis_plugin_tools.tools.i18n import tr


__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class BaseOverpassPanel(BaseProcessingPanel):

    """Panel OSM Processing base class.

    This panels will have an run button.

    This is a kind of virtual class.
    """

    def __init__(self, dialog):
        super().__init__(dialog)
        self.last_places = []

    def setup_panel(self):
        """Function to set custom UI for some panels."""
        super().setup_panel()
        self.dialog.advanced_panels[self.panel].setSaveCollapsedState(False)
        self.dialog.advanced_panels[self.panel].setCollapsed(True)

    def init_nominatim_autofill(self):
        """Open the nominatim file and start setting up the auto-completion."""
        # Useful to avoid duplicate if we add a new completer.
        for line_edit in self.dialog.places_edits.values():
            line_edit.setCompleter(None)

        user_file = nominatim_file()

        with io.open(user_file, 'r', encoding='utf8') as f:
            for line in f:
                self.last_places.append(line.rstrip('\n'))

            nominatim_completer = QCompleter(self.last_places)
            for line_edit in self.dialog.places_edits.values():
                line_edit.setCompleter(nominatim_completer)
                line_edit.completer().setCompletionMode(
                    QCompleter.PopupCompletion)

    @staticmethod
    def sort_nominatim_places(existing_places, place):
        """Helper to sort and limit results of saved nominatim places."""
        if place in existing_places:
            existing_places.pop(existing_places.index(place))
        existing_places.insert(0, place)
        return existing_places[:10]

    def write_nominatim_file(self, panel):
        """Write new nominatim value in the file.

        :param panel: The panel to use so as to fetch the nominatim value.
        :type panel: Panels
        """
        value = self.dialog.places_edits[panel].text()
        new_list = self.sort_nominatim_places(self.last_places, value)

        user_file = nominatim_file()

        try:
            with io.open(user_file, 'w', encoding='utf8') as f:
                for item in new_list:
                    if item:
                        f.write('{}\n'.format(item))
        except UnicodeDecodeError:
            # The file is corrupted ?
            # Remove all old places
            with io.open(user_file, 'w', encoding='utf8') as f:
                f.write('\n')

        self.init_nominatim_autofill()

    @staticmethod
    def _core_query_type_updated(combo_query_type, widget, spinbox=None):
        """Enable/disable the extent/layer widget."""
        current = combo_query_type.currentData()

        if combo_query_type.count() == 2:
            # Query tab, widget is the layer selector
            widget.setVisible(current == 'layer')
        else:
            # Quick query tab, widget is the stacked widget
            if current in ['in', 'around']:
                widget.setCurrentIndex(0)
                spinbox.setVisible(current == 'around')
            elif current in ['layer']:
                widget.setCurrentIndex(1)
            elif current in ['canvas', 'attributes']:
                widget.setCurrentIndex(2)

    # TODO remove
    def _start_process(self):
        """Make some stuff before launching the process."""
        self.dialog.button_show_query.setDisabled(True)
        self.dialog.button_generate_query.setDisabled(True)
        super()._start_process()

    # TODO remove
    def _end_process(self):
        """Make some stuff after the process."""
        self.dialog.button_show_query.setDisabled(False)
        self.dialog.button_generate_query.setDisabled(False)
        super()._end_process()

    def end_query(self, num_layers):
        """Display the message at the end of the query.

        :param num_layers: Number of layers which have been loaded.
        :rtype num_layers: int
        """
        if num_layers:
            text = tr(
                'Successful query, {} layer(s) has been loaded.').format(
                num_layers)
            self.dialog.set_progress_text(text)
            self.dialog.display_message_bar(text, level=Qgis.Success, duration=5)
        else:
            self.dialog.set_progress_text(tr('No result'))
            self.dialog.display_message_bar(
                tr('Successful query, but no result.'),
                level=Qgis.Warning, duration=7)

    def gather_values(self):
        properties = super().gather_values()

        place = self.dialog.places_edits[self.panel].text()
        if place == '':
            place = None
        properties['place'] = place

        query_type = self.dialog.query_type_buttons[self.panel].currentData()

        if not properties['place']:
            if query_type in ['canvas', 'layer']:
                if query_type == 'canvas':
                    geom_extent = self.dialog.iface.mapCanvas().extent()
                    source_crs = self.dialog.iface.mapCanvas().mapSettings().destinationCrs()
                elif query_type == 'layer':
                    # Else if a layer is checked
                    layer = self.dialog.layers_buttons[self.panel].currentLayer()
                    if not layer:
                        raise MissingLayerUI
                    geom_extent = layer.extent()
                    source_crs = layer.crs()
                else:
                    raise NotImplemented

                # noinspection PyArgumentList
                geom_extent = QgsGeometry.fromRect(geom_extent)
                epsg_4326 = QgsCoordinateReferenceSystem('EPSG:4326')
                # noinspection PyArgumentList
                crs_transform = QgsCoordinateTransform(
                    source_crs, epsg_4326, QgsProject.instance())
                geom_extent.transform(crs_transform)
                properties['bbox'] = geom_extent.boundingBox()
            else:
                properties['bbox'] = None
        else:
            properties['bbox'] = None

        if query_type == 'in':
            properties['query_type'] = QueryType.InArea
        elif query_type == 'around':
            properties['query_type'] = QueryType.AroundArea
        elif query_type == 'canvas':
            properties['query_type'] = QueryType.BBox
        elif query_type == 'layer':
            properties['query_type'] = QueryType.BBox
        elif query_type == 'attributes':
            properties['query_type'] = QueryType.NotSpatial
        else:
            raise NotImplemented

        return properties
