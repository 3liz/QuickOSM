"""Configuration panel."""

import logging

from os.path import isfile

from qgis.core import Qgis, QgsProject
from qgis.PyQt.QtWidgets import QDialog

from QuickOSM.core.exceptions import FileDoesntExistException
from QuickOSM.core.parser.osm_parser import OsmParser
from QuickOSM.core.process import open_file
from QuickOSM.definitions.gui import Panels
from QuickOSM.definitions.osm import MultiType
from QuickOSM.qgis_plugin_tools.tools.i18n import tr
from QuickOSM.qgis_plugin_tools.tools.resources import resources_path
from QuickOSM.ui.base_processing_panel import BaseProcessingPanel
from QuickOSM.ui.custom_table import TableKeyValue

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

LOGGER = logging.getLogger('QuickOSM')


class OsmFilePanel(BaseProcessingPanel, TableKeyValue):

    """Final implementation for the panel."""

    def __init__(self, dialog: QDialog):
        """Constructor"""
        BaseProcessingPanel.__init__(self, dialog)
        TableKeyValue.__init__(self, dialog.table_keys_values_f, self.dialog.combo_preset_f)
        super().__init__(dialog)
        self.panel = Panels.File

    def setup_panel(self):
        """Setup the panel"""
        super().setup_panel()
        self.dialog.radio_osm_conf.setChecked(False)
        self.dialog.osm_conf.setEnabled(False)
        # TODO self.edit_file_prefix_f.setDisabled(True)

        self.dialog.radio_selection_keys.setChecked(False)

        # Setup key auto completion
        self.setup_preset()

        # Table Keys/Values
        self.setup_table()

        self.dialog.osm_file.setDialogTitle(tr('Select an OSM/PBF file'))
        self.dialog.osm_file.setFilter('OSM file (*.osm *.pbf)')

        default_osm_conf = resources_path('ogr', 'to_be_modified_osmconf.ini')
        if not isfile(default_osm_conf):
            default_osm_conf = ''
        self.dialog.osm_conf.setDialogTitle(tr('Select OSM conf file'))
        self.dialog.osm_conf.setFilter('OSM conf (*.ini)')
        self.dialog.osm_conf.lineEdit().setPlaceholderText(default_osm_conf)

        self.dialog.osm_conf.fileChanged.connect(self.disable_run_file_button)
        self.dialog.radio_osm_conf.toggled.connect(self.disable_run_file_button)
        self.dialog.radio_selection_keys.toggled.connect(self.disable_run_file_button)
        # TODO
        #  self.output_directory.fileChanged.connect(self.disable_prefix_file)
        self.dialog.run_buttons[self.panel].clicked.connect(self.run)

        self.disable_run_file_button()

    def disable_run_file_button(self):
        """If the two fields are empty or allTags."""
        if not self.dialog.osm_file.filePath():
            self.dialog.run_buttons[self.panel].setEnabled(False)

        if self.dialog.radio_osm_conf.isChecked():
            self.dialog.osm_conf.setEnabled(True)
            self.dialog.table_keys_values_f.setEnabled(False)
            self.dialog.combo_preset_f.setEnabled(False)
            self.dialog.output_directory_f.setEnabled(False)
            self.dialog.combo_format_f.setEnabled(False)
            self.dialog.line_file_prefix_file.setEnabled(False)
            if self.dialog.osm_conf.filePath() or self.dialog.osm_conf.lineEdit().placeholderText():
                self.dialog.run_buttons[Panels.File].setEnabled(True)
            else:
                self.dialog.run_buttons[Panels.File].setEnabled(False)
        elif self.dialog.radio_selection_keys.isChecked():
            self.dialog.table_keys_values_f.setEnabled(True)
            self.dialog.combo_preset_f.setEnabled(True)
            self.dialog.output_directory_f.setEnabled(True)
            self.dialog.combo_format_f.setEnabled(True)
            self.dialog.line_file_prefix_file.setEnabled(True)
            self.dialog.osm_conf.setEnabled(False)
            self.dialog.run_buttons[self.panel].setEnabled(True)
        else:
            self.dialog.table_keys_values_f.setEnabled(False)
            self.dialog.combo_preset_f.setEnabled(False)
            self.dialog.output_directory_f.setEnabled(True)
            self.dialog.combo_format_f.setEnabled(True)
            self.dialog.line_file_prefix_file.setEnabled(True)
            self.dialog.osm_conf.setEnabled(False)
            self.dialog.run_buttons[self.panel].setEnabled(True)

    def gather_values(self) -> dict:
        """Retrieval of the values set by the user."""
        properties = super().gather_values()

        properties['osm_file'] = self.dialog.osm_file.filePath()
        conf = self.dialog.osm_conf.filePath()
        if conf:
            properties['osm_conf'] = conf
        else:
            properties['osm_conf'] = (
                self.dialog.osm_conf.lineEdit().placeholderText())

        properties['subset'] = self.dialog.radio_selection_keys.isChecked()
        if properties['subset']:
            properties = self.gather_couple(properties)
        properties['load_only'] = self.dialog.radio_osm_conf.isChecked()

        if not isfile(properties['osm_file']):
            raise FileDoesntExistException(suffix="*.osm or *.pbf")

        if properties['load_only']:
            if not isfile(properties['osm_conf']):
                raise FileDoesntExistException(suffix="*.ini")

        return properties

    @staticmethod
    def generate_sql(properties: dict) -> str:
        """Generate the subset query."""
        key = properties['key']
        val = properties['value']
        if len(val) == 0:
            val = ['']

        multi_keys = len(key) > 1

        if key:

            keys = []
            for k, v in zip(key, val):
                if v:
                    keys.append('\"{k}\"=\'{v}\''.format(k=k, v=v))
                else:
                    keys.append('\"{k}\"'.format(k=k))

            if multi_keys:
                type_multi = properties['type_multi_request']
                key_lbl = ''
                index = 0
                for k, type_multi_k in enumerate(type_multi):
                    if index == k:
                        if type_multi_k == MultiType.AND:
                            i = 1
                            key_and = keys[k] + ' AND ' + keys[k + i]

                            while (k + i) < len(type_multi) and type_multi[k + i] == MultiType.AND:
                                i += 1
                                key_and += ' AND ' + keys[k + i]

                            key_lbl += '({})'.format(key_and)
                            index = k + i
                        elif type_multi_k == MultiType.OR:
                            if k == 0:
                                key_lbl += keys[k]
                            key_lbl += ' OR '
                            i = 1
                            while (k + i) < len(type_multi) and type_multi[k + i] == MultiType.OR:
                                key_lbl += keys[k + i] + ' or '
                                i += 1
                            index = k + i
                            if k + i == len(type_multi):
                                key_lbl += keys[k + i]
            else:
                key_lbl = keys[0]

            return key_lbl

    def _run(self):
        """Run the process"""
        properties = self.gather_values()
        if properties['load_only']:
            # Legacy, waiting to remove the OsmParser for QGIS >= 3.6
            # Change in osm_file_dialog.py L131 too
            output_geom_legacy = [layer.value.lower() for layer in properties['outputs']]
            osm_parser = OsmParser(
                properties['osm_file'],
                load_only=True,
                osm_conf=properties['osm_conf'],
                layers=output_geom_legacy)
            layers = osm_parser.parse()
            for item in layers.values():
                # noinspection PyArgumentList
                QgsProject.instance().addMapLayer(item)
        elif properties['subset']:
            sql_query = self.generate_sql(properties)
            open_file(
                dialog=self.dialog,
                osm_file=properties['osm_file'],
                key=properties['key'],
                output_geom_types=properties['outputs'],
                output_dir=properties['output_directory'],
                output_format=properties['output_format'],
                prefix_file=properties['prefix_file'],
                subset=True,
                subset_query=sql_query
            )
            self.dialog.display_message_bar(
                tr('Successful query'),
                level=Qgis.Success,
                duration=5)
        else:
            open_file(
                dialog=self.dialog,
                osm_file=properties['osm_file'],
                output_geom_types=properties['outputs'],
                output_dir=properties['output_directory'],
                output_format=properties['output_format'],
                prefix_file=properties['prefix_file'])
            self.dialog.display_message_bar(
                tr('Successful query'),
                level=Qgis.Success,
                duration=5)
