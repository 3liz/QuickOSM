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
import inspect
import io
import logging
import traceback


from json import load
from os.path import isfile, isdir, split
from sys import exc_info


from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QDialog, QDialogButtonBox, QCompleter, QApplication, QPushButton)
from qgis.PyQt.QtGui import QPixmap, QIcon
from qgis._gui import QgsFileWidget
from qgis.core import (
    Qgis,
    QgsGeometry,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
)
from qgis.utils import iface

from QuickOSM.definitions.gui import Panels
from QuickOSM.definitions.osm import OsmType, LayerType
from QuickOSM.definitions.overpass import OVERPASS_SERVERS
from QuickOSM.core.exceptions import (
    QuickOsmException,
    OutPutGeomTypesException,
    DirectoryOutPutException,
    OsmObjectsException)
from QuickOSM.core.process import process_quick_query
from QuickOSM.core.utilities.tools import (
    get_setting,
    set_setting,
    resources_path,
    tr,
    nominatim_file,
    custom_config_file,
)
from QuickOSM.core.utilities.utilities_qgis import (
    open_map_features, open_log_panel)
from QuickOSM.ui.tools import query_type_updated

FORM_CLASS, _ = uic.loadUiType(resources_path('ui', 'main_window.ui'))
LOGGER = logging.getLogger('QuickOSM')


class MainDialog(QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)

        # Table mapping
        self.panels = {
            'run_quick_query': Panels.QuickQuery,
        }
        self.places_edits = {
            Panels.QuickQuery: self.line_place_qq,
        }
        self.query_type_buttons = {
            Panels.QuickQuery: self.combo_query_type_qq,
        }
        self.layers_buttons = {
            Panels.QuickQuery: self.combo_extent_layer_qq,
        }
        self.run_buttons = {
            Panels.QuickQuery: self.button_run_query_qq,
        }
        self.output_buttons = {
            Panels.QuickQuery: [
                self.checkbox_points_qq,
                self.checkbox_lines_qq,
                self.checkbox_multilinestrings_qq,
                self.checkbox_multipolygons_qq
            ]
        }
        self.output_directories = {
            Panels.QuickQuery: self.output_directory_qq,
        }
        self.advanced_panels = {
            Panels.QuickQuery: self.advanced_qq,
        }

        self.default_server = None
        self.last_places = []

        # Quick query
        self.osm_keys = None

        self.set_ui_menu()
        self.set_ui_configuration_panel()
        self.set_ui_quick_query_panel()

    def _set_custom_ui(self, panel):
        """Function to set custom UI for some panels.

        :param panel: Name of the panel.
        :type panel: Panels
        """
        self.output_directories[panel].lineEdit().setPlaceholderText(
            tr('Save to temporary file'))
        self.output_directories[panel].setStorageMode(
            QgsFileWidget.GetDirectory)
        self.output_directories[panel].setDialogTitle(tr('Select a directory'))

        # def disable_prefix_file():
        #     # TODO
        #     def disable_prefix_file(directory, file_prefix):
        #         """If the directory is empty, we disable the file prefix."""
        #         if directory.filePath():
        #             file_prefix.setDisabled(False)
        #         else:
        #             file_prefix.setText('')
        #             file_prefix.setDisabled(True)
        #
        # self.output_directories[panel].fileChanged.connect(
        #    disable_prefix_file)

        if panel in self.advanced_panels.keys():
            self.advanced_panels[panel].setSaveCollapsedState(False)
            self.advanced_panels[panel].setCollapsed(True)

    def set_ui_menu(self):
        """Set UI related to window and menus."""
        item = self.menu_widget.item(0)
        item.setIcon(QIcon(resources_path('icons', 'quick.png')))
        item = self.menu_widget.item(1)
        item.setIcon(QIcon(resources_path('icons', 'edit.png')))
        item = self.menu_widget.item(2)
        item.setIcon(QIcon(resources_path('icons', 'open.png')))
        item = self.menu_widget.item(3)
        item.setIcon(QIcon(resources_path('icons', 'general.svg')))
        item = self.menu_widget.item(4)
        item.setIcon(QIcon(resources_path('icons', 'info.png')))
        self.label_gnu.setPixmap(QPixmap(resources_path('icons', 'gnu.png')))

        # Set minimum width for the menu
        self.menu_widget.setMinimumWidth(
            self.menu_widget.sizeHintForColumn(0) + 10)

        self.progress_text.setText('')

        self.menu_widget.currentRowChanged['int'].connect(
            self.stacked_panels_widget.setCurrentIndex)

    def gather_values(self):
        """Called by QuickQuery, Query and Open widgets.

        :return: A dictionary with all values inside.
        :rtype: dict
        """
        caller = self.panels[inspect.stack()[1][3]]
        properties = {}

        if caller == Panels.QuickQuery:

            osm_objects = []
            if self.checkbox_node.isChecked():
                osm_objects.append(OsmType.Node)
            if self.checkbox_way.isChecked():
                osm_objects.append(OsmType.Way)
            if self.checkbox_relation.isChecked():
                osm_objects.append(OsmType.Relation)
            properties['osm_objects'] = osm_objects

            if not properties['osm_objects']:
                raise OsmObjectsException

            properties['key'] = self.combo_key.currentText()
            properties['value'] = self.combo_value.currentText()
            properties['timeout'] = self.spin_timeout.value()
            properties['distance'] = self.spin_place_qq.value()

        place = self.nominatim_value(caller)
        if place == '':
            place = None
        properties['place'] = place

        if caller in [Panels.QuickQuery, Panels.Query]:
            properties['query_type'] = (
                self.query_type_buttons[caller].currentData())
            properties['is_around'] = properties['query_type'] == 'around'

            if not properties['place']:
                if properties['query_type'] == 'canvas':
                    geom_extent = iface.mapCanvas().extent()
                    source_crs = (
                        iface.mapCanvas().mapSettings().destinationCrs())
                elif properties['query_type'] == 'layer':
                    # Else if a layer is checked
                    layer = self.layers_buttons[caller].currentLayer()
                    geom_extent = layer.extent()
                    source_crs = layer.crs()

                geom_extent = QgsGeometry.fromRect(geom_extent)
                epsg_4326 = QgsCoordinateReferenceSystem('EPSG:4326')
                crs_transform = QgsCoordinateTransform(
                    source_crs, epsg_4326, QgsProject.instance())
                geom_extent.transform(crs_transform)
                properties['bbox'] = geom_extent.boundingBox()
            else:
                properties['bbox'] = None

        properties['outputs'] = []
        if self.output_buttons[caller][0].isChecked():
            # noinspection PyTypeChecker
            properties['outputs'].append(LayerType.Points)
        if self.output_buttons[caller][1].isChecked():
            # noinspection PyTypeChecker
            properties['outputs'].append(LayerType.Lines)
        if self.output_buttons[caller][2].isChecked():
            # noinspection PyTypeChecker
            properties['outputs'].append(LayerType.Multilinestrings)
        if self.output_buttons[caller][3].isChecked():
            # noinspection PyTypeChecker
            properties['outputs'].append(LayerType.Multipolygons)

        if not properties['outputs']:
            raise OutPutGeomTypesException

        properties['output_directory'] = self.output_directory_qq.filePath()
        properties['prefix_file'] = self.line_file_prefix_qq.text()

        if properties['output_directory'] and not (
                isdir(properties['output_directory'])):
            raise DirectoryOutPutException

        LOGGER.debug(properties)

        return properties

    def display_geo_algorithm_exception(self, exception):
        """Display QuickOSM exceptions."""
        self.set_progress_text('')
        LOGGER.debug(exception.msg)
        self.display_message_bar(
            exception.msg, level=exception.level, duration=exception.duration)

    def display_exception(self, exception):
        """Display others exceptions."""
        exc_type, _, exc_tb = exc_info()
        f_name = split(exc_tb.tb_frame.f_code.co_filename)[1]
        _, _, tb = exc_info()
        traceback.print_tb(tb)
        LOGGER.critical(
            tr('A critical error occurred, this is the traceback:'))
        LOGGER.critical(exc_type)
        LOGGER.critical(f_name)
        LOGGER.critical(exception)
        LOGGER.critical('\n'.join(traceback.format_tb(tb)))

        self.display_message_bar(
            tr('Error in the logs, QuickOSM panel, please report it to '
               'GitHub'),
            level=Qgis.Critical,
            open_logs=True,
            duration=10)

    def display_message_bar(
            self,
            title,
            message=None,
            level=Qgis.Info,
            duration=5,
            open_logs=False):
        """Display a message.

        :param title: Title of the message.
        :type title: basestring

        :param message: The message.
        :type message: basestring

        :param level: A QGIS error level.

        :param duration: Duration in second.
        :type duration: int

        :param open_logs: If we need to add a button for the log panel.
        :type open_logs: bool
        """
        widget = self.message_bar.createMessage(title, message)

        if open_logs:
            button = QPushButton(widget)
            button.setText(tr('Report it!'))
            button.pressed.connect(
                lambda: open_log_panel())
            widget.layout().addWidget(button)

        self.message_bar.pushWidget(widget, level, duration)

    def end_query(self, num_layers):
        if num_layers:
            self.set_progress_text(tr('Successful query'))
            self.display_message_bar(
                tr('Successful query'), level=Qgis.Success, duration=5)
        else:
            self.set_progress_text(tr('No result'))
            self.display_message_bar(
                tr('Successful query, but no result.'),
                level=Qgis.Warning, duration=7)

    def reset_form(self):
        LOGGER.info(tr('Dialog has been reset'))
        # TODO need to add other dialog
        self.combo_key.setCurrentIndex(0)
        self.combo_value.setCurrentIndex(0)
        self.line_place_qq.setText('')
        self.spin_place_qq.setValue(1000)
        self.checkbox_points_qq.setChecked(True)
        self.checkbox_lines_qq.setChecked(True)
        self.checkbox_multilinestrings_qq.setChecked(True)
        self.checkbox_multipolygons_qq.setChecked(True)
        self.checkbox_node.setChecked(True)
        self.checkbox_way.setChecked(True)
        self.checkbox_relation.setChecked(True)
        self.spin_timeout.setValue(25)
        self.output_directory_qq.lineEdit().setText('')
        self.line_file_prefix_qq.setText('')

    def _start_process(self):
        """Make some stuff before launching the process."""
        caller = self.panels[inspect.stack()[1][3]]
        QApplication.setOverrideCursor(Qt.WaitCursor)

        if caller == Panels.QuickQuery:
            self.button_show_query.setDisabled(True)

        self.run_buttons[caller].setDisabled(True)
        self.run_buttons[caller].initial_text = self.run_buttons[caller].text()
        self.run_buttons[caller].setText(tr('Running query…'))
        self.output_directories[caller].setDisabled(True)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setValue(0)
        self.progress_text.setText('')
        QApplication.processEvents()

    def _end_process(self):
        """Make some stuff after the process."""
        caller = self.panels[inspect.stack()[1][3]]
        QApplication.restoreOverrideCursor()

        if caller == Panels.QuickQuery:
            self.button_show_query.setDisabled(False)

        self.output_directories[caller].setDisabled(True)
        self.run_buttons[caller].setDisabled(False)
        self.run_buttons[caller].setText(self.run_buttons[caller].initial_text)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(100)
        QApplication.processEvents()

    def init_nominatim_autofill(self):
        """Open the nominatim file and start setting up the auto-completion."""
        # Useful to avoid duplicate if we add a new completer.
        for line_edit in self.places_edits.values():
            line_edit.setCompleter(None)

        user_file = nominatim_file()

        if isfile(user_file):
            with io.open(user_file, 'r', encoding='utf8') as f:
                for line in f:
                    self.last_places.append(line.rstrip('\n'))

                nominatim_completer = QCompleter(self.last_places)
                for line_edit in self.places_edits.values():
                    line_edit.setCompleter(nominatim_completer)
                    line_edit.completer().setCompletionMode(
                        QCompleter.PopupCompletion)
        else:
            io.open(user_file, 'a').close()

    @staticmethod
    def sort_nominatim_places(existing_places, place):
        if place in existing_places:
            existing_places.pop(existing_places.index(place))
        existing_places.insert(0, place)
        return existing_places[:10]

    def nominatim_value(self, panel):
        """Edit the new nominatim file from a given panel.

        :param panel: Name of the panel.
        :type panel: Panels
        """
        value = self.places_edits[panel].text()
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
        return value

    def set_progress_percentage(self, percent):
        """Slot to update percentage during process."""
        self.progress_bar.setValue(percent)
        QApplication.processEvents()

    def set_progress_text(self, text):
        """Slot to update text during process."""
        self.progress_text.setText(text)
        QApplication.processEvents()

    # ###
    # configuration panel
    # ###

    def set_ui_configuration_panel(self):
        """Set UI related the configuration panel."""

        self._set_custom_ui(Panels.QuickQuery)

        # noinspection PyUnresolvedReferences
        self.combo_default_overpass.currentIndexChanged.connect(
            self.set_server_overpass_api)

        # Set settings about the overpass API
        self.default_server = get_setting('defaultOAPI')
        if self.default_server:
            index = self.combo_default_overpass.findText(self.default_server)
            self.combo_default_overpass.setCurrentIndex(index)
        else:
            self.default_server = self.combo_default_overpass.currentText()
            set_setting('defaultOAPI', self.default_server)

        for server in OVERPASS_SERVERS:
            self.combo_default_overpass.addItem(server)

        # Read the config file
        custom_config = custom_config_file()
        if custom_config:
            with open(custom_config) as f:
                config_json = load(f)
                for server in config_json.get('overpass_servers'):
                    if server not in OVERPASS_SERVERS:
                        LOGGER.info(
                            'Custom overpass server list added: {}'.format(
                                server))
                        self.combo_default_overpass.addItem(server)

    def set_server_overpass_api(self):
        """
        Save the new OAPI server.
        """
        self.default_server = self.combo_default_overpass.currentText()
        set_setting('defaultOAPI', self.default_server)

    # ###
    # quick query panel
    # ###
    def set_ui_quick_query_panel(self):

        # Query type
        self.combo_query_type_qq.addItem(tr('In'), 'in')
        self.combo_query_type_qq.addItem(tr('Around'), 'around')
        self.combo_query_type_qq.addItem(tr('Canvas Extent'), 'canvas')
        self.combo_query_type_qq.addItem(tr('Layer Extent'), 'layer')
        self.combo_query_type_qq.addItem(tr('Not Spatial'), 'attributes')

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

        self.combo_query_type_qq.currentIndexChanged.connect(
            self.query_type_updated_qq)

        self.line_file_prefix_qq.setDisabled(True)

        self.button_run_query_qq.clicked.connect(self.run_quick_query)
        # TODO self.button_show_query.clicked.connect(self.show_query)
        self.combo_key.editTextChanged.connect(self.key_edited)
        self.button_map_features.clicked.connect(open_map_features)
        self.button_box_qq.button(QDialogButtonBox.Reset).clicked.connect(
            self.reset_form)

        # Setup auto completion
        map_features_json_file = resources_path('json', 'map_features.json')
        if isfile(map_features_json_file):
            with open(map_features_json_file) as f:
                self.osm_keys = load(f)
                keys = list(self.osm_keys.keys())
                keys.append('')  # All keys request #118
                keys.sort()
                keys_completer = QCompleter(keys)
                self.combo_key.addItems(keys)
                self.combo_key.setCompleter(keys_completer)
                self.combo_key.completer().setCompletionMode(
                    QCompleter.PopupCompletion)
                self.combo_key.lineEdit().setPlaceholderText(
                    tr('Query on all keys'))

        self.combo_value.lineEdit().setPlaceholderText(
            tr('Query on all values'))
        self.key_edited()

        self.query_type_updated_qq()
        self.init_nominatim_autofill()

    def query_type_updated_qq(self):
        query_type_updated(
            self.combo_query_type_qq,
            self.stacked_query_type,
            self.spin_place_qq)

    def key_edited(self):
        """Add values to the combobox according to the key."""
        self.combo_value.clear()
        self.combo_value.setCompleter(None)

        try:
            current_values = self.osm_keys[self.combo_key.currentText()]
        except KeyError:
            return
        except AttributeError:
            return

        if len(current_values) == 0:
            current_values.insert(0, '')

        if len(current_values) > 1 and current_values[0] != '':
            current_values.insert(0, '')

        values_completer = QCompleter(current_values)
        self.combo_value.setCompleter(values_completer)
        self.combo_value.addItems(current_values)

    def run_quick_query(self):
        """Process for running the query."""
        try:
            self._start_process()
            p = self.gather_values()
            num_layers = process_quick_query(
                dialog=self,
                key=p['key'],
                value=p['value'],
                area=p['place'],
                is_around=p['is_around'],
                distance=p['distance'],
                bbox=p['bbox'],
                osm_objects=p['osm_objects'],
                timeout=p['timeout'],
                output_directory=p['output_directory'],
                prefix_file=p['prefix_file'],
                output_geometry_types=p['outputs'])
            self.end_query(num_layers)
        except QuickOsmException as e:
            self.display_geo_algorithm_exception(e)
        except Exception as e:
            self.display_exception(e)
        finally:
            self._end_process()

    # ###
    # query panel
    # ###

    # ###
    # osm file panel
    # ###
