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
import re
import traceback


from json import load
from os.path import isfile, isdir, split
from sys import exc_info

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QCompleter,
    QApplication,
    QPushButton,
    QMenu,
    QAction,
)
from qgis.PyQt.QtGui import QPixmap, QIcon
from qgis.gui import QgsFileWidget
from qgis.core import (
    Qgis,
    QgsGeometry,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
)
from qgis.utils import iface

from QuickOSM.definitions.gui import Panels
from QuickOSM.definitions.osm import OsmType, LayerType, QueryType
from QuickOSM.definitions.overpass import OVERPASS_SERVERS
from QuickOSM.core.exceptions import (
    QuickOsmException,
    OutPutGeomTypesException,
    DirectoryOutPutException,
    OsmObjectsException, FileDoesntExistException, MissingParameterException)
from QuickOSM.core.query_factory import QueryFactory
from QuickOSM.core.process import process_quick_query, open_file, process_query
from QuickOSM.core.query_preparation import QueryPreparation
from QuickOSM.core.utilities.tools import (
    get_setting,
    set_setting,
    resources_path,
    tr,
    nominatim_file,
    custom_config_file,
)
from QuickOSM.core.utilities.utilities_qgis import (
    open_map_features, open_log_panel, open_doc_overpass, open_overpass_turbo)
from QuickOSM.core.parser.osm_parser import OsmParser
from QuickOSM.ui.xml_highlighter import XMLHighlighter


FORM_CLASS, _ = uic.loadUiType(resources_path('ui', 'main_window.ui'))
LOGGER = logging.getLogger('QuickOSM')


class MainDialog(QDialog, FORM_CLASS):

    """Main class about the dialog."""

    def __init__(self, parent=None):
        """Constructor."""
        QDialog.__init__(self, parent)
        self.setupUi(self)

        # Table mapping
        self.panels = {
            'run_quick_query': Panels.QuickQuery,
            'run_query': Panels.Query,
            'open_file': Panels.File,
        }
        self.places_edits = {
            Panels.QuickQuery: self.line_place_qq,
            Panels.Query: self.line_place_q,
        }
        self.query_type_buttons = {
            Panels.QuickQuery: self.combo_query_type_qq,
            Panels.Query: self.combo_query_type_q,
        }
        self.layers_buttons = {
            Panels.QuickQuery: self.combo_extent_layer_qq,
            Panels.Query: self.combo_extent_layer_q,
        }
        self.run_buttons = {
            Panels.QuickQuery: self.button_run_query_qq,
            Panels.Query: self.button_run_query_q,
            Panels.File: self.button_run_file,
        }
        self.output_buttons = {
            Panels.QuickQuery: [
                self.checkbox_points_qq,
                self.checkbox_lines_qq,
                self.checkbox_multilinestrings_qq,
                self.checkbox_multipolygons_qq
            ],
            Panels.Query: [
                self.checkbox_points_q,
                self.checkbox_lines_q,
                self.checkbox_multilinestrings_q,
                self.checkbox_multipolygons_q,
            ],
            Panels.File: [
                self.checkbox_points_f,
                self.checkbox_lines_f,
                self.checkbox_multilinestrings_f,
                self.checkbox_multipolygons_f,
            ]
        }
        self.output_directories = {
            Panels.QuickQuery: self.output_directory_qq,
            Panels.Query: self.output_directory_q,
            Panels.File: self.output_directory_f
        }
        self.prefix_edits = {
            Panels.QuickQuery: self.line_file_prefix_qq,
            Panels.Query: self.line_file_prefix_q,
            Panels.File: self.line_file_prefix_file,
        }
        self.advanced_panels = {
            Panels.QuickQuery: self.advanced_qq,
            Panels.Query: self.advanced_q,
        }

        self.default_server = None
        self.last_places = []

        # Quick query
        self.osm_keys = None

        self.set_ui_menu()
        self.set_ui_configuration_panel()
        self.set_ui_quick_query_panel()
        self.set_ui_query_panel()
        self.set_ui_file_panel()

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
        properties = dict()

        # For all queries
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

        properties['output_directory'] = (
            self.output_directories[caller].filePath())
        properties['prefix_file'] = self.prefix_edits[caller].text()

        if properties['output_directory'] and not (
                isdir(properties['output_directory'])):
            raise DirectoryOutPutException

        # Specific to files
        if caller == Panels.File:
            properties['osm_file'] = self.osm_file.filePath()
            conf = self.osm_conf.filePath()
            if conf:
                properties['osm_conf'] = conf
            else:
                properties['osm_conf'] = (
                    self.osm_conf.lineEdit().placeholderText())

            properties['load_only'] = self.radio_osm_conf.isChecked()

            if not isfile(properties['osm_file']):
                raise FileDoesntExistException(suffix="*.osm or *.pbf")

            if properties['load_only']:
                if not isfile(properties['osm_conf']):
                    raise FileDoesntExistException(suffix="*.ini")

            # End for OSM file
            return properties

        # Speficif for quick query
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

        # For quick query and query
        place = self.nominatim_value(caller)
        if place == '':
            place = None
        properties['place'] = place

        # Speficic for query
        if caller == Panels.Query:
            properties['query'] = self.text_query.toPlainText()

            properties['expected_csv'] = dict()
            if self.checkbox_points_q.isChecked():
                properties['expected_csv'][LayerType.Points] = (
                    self.edit_csv_points.text())
            if self.checkbox_lines_q.isChecked():
                properties['expected_csv'][LayerType.Lines] = (
                    self.edit_csv_lines.text())
            if self.checkbox_multilinestrings_q.isChecked():
                properties['expected_csv'][LayerType.Multilinestrings] = (
                    self.edit_csv_multilinestrings.text())
            if self.checkbox_multipolygons_q.isChecked():
                properties['expected_csv'][LayerType.Multipolygons] = (
                    self.edit_csv_multipolygons.text())

            if not place and \
                    re.search(r'\{\{nominatim\}\}', properties['query']) or \
                    re.search(r'\{\{nominatimArea:\}\}', properties['query']) \
                    or \
                    re.search(r'\{\{geocodeArea:\}\}', properties['query']):

                raise MissingParameterException(suffix='nominatim field')

        # For quick query and query
        properties['query_type'] = (
            self.query_type_buttons[caller].currentData())
        properties['is_around'] = properties['query_type'] == 'around'

        if not properties['place']:
            if properties['query_type'] == 'canvas':
                geom_extent = iface.mapCanvas().extent()
                source_crs = iface.mapCanvas().mapSettings().destinationCrs()
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

        return properties

    def display_geo_algorithm_exception(self, exception):
        """Display QuickOSM exceptions.

        :param exception: The exception to display.
        :rtype exception: GeoAlgorithmException
        """
        self.set_progress_text('')
        LOGGER.debug(exception.msg)
        self.display_message_bar(
            exception.msg, level=exception.level, duration=exception.duration)

    def display_exception(self, exception):
        """Display others exceptions.

        :param exception: The exception to display.
        :rtype exception: BaseException
        """
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
            tr('Error in the logs, in the QuickOSM panel, copy/paste it and '
               'please report it to GitHub'),
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
            button.setText(tr('Report it'))
            button.pressed.connect(
                lambda: open_log_panel())
            widget.layout().addWidget(button)

        self.message_bar.pushWidget(widget, level, duration)

    @staticmethod
    def query_type_updated(combo_query_type, widget, spinbox=None):
        """Enable/disable the extent/layer widget."""
        current = combo_query_type.currentData()

        if combo_query_type.count() == 2:
            # Query tab, widget is the layer selector
            widget.setVisible(current == 'layer')
        else:
            # Quick query tab, widget is the stackedwidget
            if current in ['in', 'around']:
                widget.setCurrentIndex(0)
                spinbox.setVisible(current == 'around')
            elif current in ['layer']:
                widget.setCurrentIndex(1)
            elif current in ['canvas', 'attributes']:
                widget.setCurrentIndex(2)

    def end_query(self, num_layers):
        """Display the message at the end of the query.

        :param num_layers: Number of layers which have been loaded.
        :rtype num_layers: int
        """
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
        """Reset all the GUI to default state."""
        LOGGER.info('Dialog has been reset')

        # Quickquery
        self.combo_key.setCurrentIndex(0)
        self.combo_value.setCurrentIndex(0)
        self.checkbox_node.setChecked(True)
        self.checkbox_way.setChecked(True)
        self.checkbox_relation.setChecked(True)
        self.spin_place_qq.setValue(1000)
        self.spin_timeout.setValue(25)

        # Query
        self.text_query.setText('')
        self.edit_csv_points.setText('')
        self.edit_csv_lines.setText('')
        self.edit_csv_multilinestrings.setText('')
        self.edit_csv_multipolygons.setText('')

        # OSM File
        self.osm_file.lineEdit().setText('')
        self.osm_conf.lineEdit().setText('')

        # Place nominatim
        for edit in self.places_edits.values():
            edit.setText('')

        # Output layers
        for panel in self.output_buttons.values():
            for output in panel:
                output.setChecked(True)

        # Directories
        for edit in self.output_directories.values():
            edit.lineEdit().setText('')

        # Prefix
        for edit in self.prefix_edits.values():
            edit.setText('')

    def _start_process(self):
        """Make some stuff before launching the process."""
        caller = self.panels[inspect.stack()[1][3]]
        QApplication.setOverrideCursor(Qt.WaitCursor)

        if caller == Panels.QuickQuery:
            self.button_show_query.setDisabled(True)

        if caller == Panels.Query:
            self.button_generate_query.setDisabled(True)

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

        if caller == Panels.Query:
            self.button_generate_query.setDisabled(False)

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

        with io.open(user_file, 'r', encoding='utf8') as f:
            for line in f:
                self.last_places.append(line.rstrip('\n'))

            nominatim_completer = QCompleter(self.last_places)
            for line_edit in self.places_edits.values():
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
        """Save the new Overpass server."""
        self.default_server = self.combo_default_overpass.currentText()
        set_setting('defaultOAPI', self.default_server)

    # ###
    # quick query panel
    # ###

    def set_ui_quick_query_panel(self):
        """Setup the UI for the QuickQuery."""
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
        self.query_type_updated(
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

    def show_query(self):
        """Show the query in the main window."""
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

    # ###
    # query panel
    # ###

    def set_ui_query_panel(self):

        self.combo_query_type_q.addItem(tr('Canvas Extent'), 'canvas')
        self.combo_query_type_q.addItem(tr('Layer Extent'), 'layer')
        self.combo_query_type_q.currentIndexChanged.connect(
            self.query_type_updated_q)

        highlighter = XMLHighlighter(self.text_query.document())
        self.text_query.cursorPositionChanged.connect(
            highlighter.rehighlight)
        self.text_query.cursorPositionChanged.connect(
            self.allow_nominatim_or_extent)

        self.button_overpass_turbo.setIcon(
            QIcon(resources_path('icons', 'turbo.png')))
        self.button_overpass_turbo.clicked.connect(open_overpass_turbo)

        # Setup menu for documentation
        popup_menu = QMenu()
        map_features_action = QAction(
            'Map Features', self.button_documentation)
        map_features_action.triggered.connect(open_map_features)
        popup_menu.addAction(map_features_action)
        overpass_action = QAction('Overpass', self.button_documentation)
        overpass_action.triggered.connect(open_doc_overpass)
        popup_menu.addAction(overpass_action)
        self.button_documentation.setMenu(popup_menu)

        self.run_buttons[Panels.File].clicked.connect(self.run_query)
        self.button_generate_query.clicked.connect(self.generate_query)
        self.button_box_q.button(QDialogButtonBox.Reset).clicked.connect(
            self.reset_form)

        self.allow_nominatim_or_extent()
        self.query_type_updated_q()

    def query_type_updated_q(self):
        self.query_type_updated(
            self.combo_query_type_q, self.combo_extent_layer_q)

    def allow_nominatim_or_extent(self):
        """Disable or enable radio buttons if nominatim or extent.
        Disable buttons if the query is empty.
        """
        query = self.text_query.toPlainText()

        self.button_generate_query.setDisabled(query == '')
        self.button_run_query_q.setDisabled(query == '')

        if re.search(r'\{\{nominatim\}\}', query) or \
                re.search(r'\{\{nominatimArea:(.*)\}\}', query) or \
                re.search(r'\{\{geocodeArea:(.*)\}\}', query):
            self.line_place_q.setEnabled(True)
        else:
            self.line_place_q.setEnabled(False)
            self.line_place_q.setText('')

        if re.search(r'\{\{(bbox|center)\}\}', query):
            self.combo_query_type_q.setEnabled(True)
        else:
            self.combo_query_type_q.setEnabled(False)

    def run_query(self):
        try:
            self._start_process()
            p = self.gather_values()
            num_layers = process_query(
                dialog=self,
                query=p['query'],
                output_dir=p['output_directory'],
                prefix_file=p['prefix_file'],
                output_geometry_types=p['outputs'],
                white_list_values=p['expected_csv'],
                area=p['place'],
                bbox=p['bbox'])
            self.end_query(num_layers)
        except QuickOsmException as e:
            self.display_geo_algorithm_exception(e)
        except Exception as e:
            self.display_exception(e)
        finally:
            self._end_process()

    def generate_query(self):
        query = self.text_query.toPlainText()
        area = self.nominatim_value(Panels.Query).text()
        bbox = self.get_bounding_box()
        query = QueryPreparation(query, bbox, area)
        query_string = query.prepare_query()
        self.text_query.setPlainText(query_string)

    # ###
    # osm file panel
    # ###

    def set_ui_file_panel(self):
        self._set_custom_ui(Panels.File)
        self.radio_osm_conf.setChecked(False)
        self.osm_conf.setEnabled(False)
        # TODO self.edit_file_prefix_f.setDisabled(True)

        self.osm_file.setDialogTitle(tr('Select an OSM file'))
        self.osm_file.setFilter('OSM file (*.osm *.pbf)')

        default_osm_conf = resources_path('ogr', 'to_be_modified_osmconf.ini')
        if not isfile(default_osm_conf):
            default_osm_conf = ''
        self.osm_conf.setDialogTitle(tr('Select OSM conf file'))
        self.osm_conf.setFilter('OSM conf (*.ini)')
        self.osm_conf.lineEdit().setPlaceholderText(default_osm_conf)

        self.osm_conf.fileChanged.connect(self.disable_run_file_button)
        self.radio_osm_conf.toggled.connect(self.disable_run_file_button)
        # TODO
        #  self.output_directory.fileChanged.connect(self.disable_prefix_file)
        self.run_buttons[Panels.File].clicked.connect(self.open_file)

        self.disable_run_file_button()

    def disable_run_file_button(self):
        """If the two fields are empty or allTags."""
        if self.osm_file.filePath():
            self.run_buttons[Panels.File].setEnabled(False)

        # if self.radio_osm_conf.isChecked():
        #     if self.osm_conf.filePath():
        #         self.run_buttons[Panels.File].setEnabled(True)
        #     else:
        #         self.run_buttons[Panels.File].setEnabled(False)
        # else:
        self.run_buttons[Panels.File].setEnabled(True)

    def open_file(self):
        """Open the osm file with the osmconf."""
        try:
            self._start_process()
            p = self.gather_values()
            if p['load_only']:
                # Legacy, waiting to remove the OsmParser for QGIS >= 3.6
                # Change in osm_file_dialog.py L131 too
                output_geom_legacy = [l.value.lower() for l in p['outputs']]
                osm_parser = OsmParser(
                    p['osm_file'],
                    load_only=True,
                    osm_conf=p['osm_conf'],
                    layers=output_geom_legacy)
                layers = osm_parser.parse()
                for item in layers.values():
                    QgsProject.instance().addMapLayer(item)
            else:
                open_file(
                    dialog=self,
                    osm_file=p['osm_file'],
                    output_geom_types=p['outputs'],
                    output_dir=p['output_directory'],
                    prefix_file=p['prefix_file'])
                self.display_message_bar(
                    tr('Successful query'),
                    level=Qgis.Success,
                    duration=5)
        except QuickOsmException as e:
            self.display_geo_algorithm_exception(e)
        except Exception as e:
            self.display_exception(e)
        finally:
            self._end_process()
