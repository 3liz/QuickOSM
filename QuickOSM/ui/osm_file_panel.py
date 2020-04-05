"""Configuration panel."""

import logging

from os.path import isfile

from qgis.core import QgsProject, Qgis

from .base_processing_panel import BaseProcessingPanel
from ..core.exceptions import FileDoesntExistException
from ..core.parser.osm_parser import OsmParser
from ..core.process import open_file
from ..definitions.gui import Panels
from ..qgis_plugin_tools.tools.i18n import tr
from ..qgis_plugin_tools.tools.resources import resources_path


__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'

LOGGER = logging.getLogger('QuickOSM')


class OsmFilePanel(BaseProcessingPanel):

    """Final implementation for the panel."""

    def __init__(self, dialog):
        super().__init__(dialog)
        self.panel = Panels.File

    def setup_panel(self):
        self.dialog.radio_osm_conf.setChecked(False)
        self.dialog.osm_conf.setEnabled(False)
        # TODO self.edit_file_prefix_f.setDisabled(True)

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
            if self.dialog.osm_conf.filePath() or self.dialog.osm_conf.lineEdit().placeholderText():
                self.dialog.run_buttons[Panels.File].setEnabled(True)
            else:
                self.dialog.run_buttons[Panels.File].setEnabled(False)
        else:
            self.dialog.osm_conf.setEnabled(False)
            self.dialog.run_buttons[self.panel].setEnabled(True)

    def gather_values(self):
        properties = super().gather_values()

        properties['osm_file'] = self.dialog.osm_file.filePath()
        conf = self.dialog.osm_conf.filePath()
        if conf:
            properties['osm_conf'] = conf
        else:
            properties['osm_conf'] = (
                self.dialog.osm_conf.lineEdit().placeholderText())

        properties['load_only'] = self.dialog.radio_osm_conf.isChecked()

        if not isfile(properties['osm_file']):
            raise FileDoesntExistException(suffix="*.osm or *.pbf")

        if properties['load_only']:
            if not isfile(properties['osm_conf']):
                raise FileDoesntExistException(suffix="*.ini")

        return properties

    def _run(self):
        properties = self.gather_values()
        if properties['load_only']:
            # Legacy, waiting to remove the OsmParser for QGIS >= 3.6
            # Change in osm_file_dialog.py L131 too
            output_geom_legacy = [l.value.lower() for l in properties['outputs']]
            osm_parser = OsmParser(
                properties['osm_file'],
                load_only=True,
                osm_conf=properties['osm_conf'],
                layers=output_geom_legacy)
            layers = osm_parser.parse()
            for item in layers.values():
                # noinspection PyArgumentList
                QgsProject.instance().addMapLayer(item)
        else:
            open_file(
                dialog=self.dialog,
                osm_file=properties['osm_file'],
                output_geom_types=properties['outputs'],
                output_dir=properties['output_directory'],
                prefix_file=properties['prefix_file'])
            self.dialog.display_message_bar(
                tr('Successful query'),
                level=Qgis.Success,
                duration=5)
