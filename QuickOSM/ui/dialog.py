"""Main dialog of QuickOSM."""

import logging
import traceback
from os.path import split
from sys import exc_info

from qgis.PyQt.QtGui import QPixmap, QIcon
from qgis.PyQt.QtWidgets import (
    QDialog,
    QApplication,
    QPushButton,
    QMessageBox,
)
from qgis.core import Qgis

from .configuration_panel import ConfigurationPanel
from .osm_file_panel import OsmFilePanel
from .query_panel import QueryPanel
from .quick_query_panel import QuickQueryPanel
from ..core.exceptions import QuickOsmException
from ..core.utilities.utilities_qgis import open_log_panel
from ..definitions.gui import Panels
from ..qgis_plugin_tools.tools.i18n import tr
from ..qgis_plugin_tools.tools.resources import load_ui, resources_path

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'

FORM_CLASS = load_ui('main_window.ui')
LOGGER = logging.getLogger('QuickOSM')


class Dialog(QDialog, FORM_CLASS):

    """Main class about the dialog of the plugin"""

    def __init__(self, iface, parent=None):
        """Constructor."""
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface

        self.query_menu_index = 1

        # Table mapping

        # Explaining quickly, these letters are referring to the panel
        # in the UI:
        # qq : Quick Query
        # q : Query
        # f : file
        self.external_panels = {
            Panels.QuickQuery: QuickQueryPanel(self),
            Panels.Query: QueryPanel(self),
            Panels.File: OsmFilePanel(self),
            Panels.Configuration: ConfigurationPanel(self),
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

        for panel in self.external_panels.values():
            panel.setup_panel()
        self.menu_widget.setCurrentRow(0)

    def display_quickosm_exception(self, exception):
        """Display QuickOSM exceptions.

        These exceptions are been raised by QuickOSM itself.
        It should be an error from the user.

        :param exception: The exception to display.
        :rtype exception: QuickOsmException
        """
        self.set_progress_text('')
        if isinstance(exception, QuickOsmException):
            self.display_message_bar(
                exception.message,
                level=exception.level,
                duration=exception.duration,
                more_details=exception.more_details,
            )
        else:
            # Should not happen, just in case
            self.display_critical_exception(exception)

    def display_critical_exception(self, exception):
        """Display others exceptions, these are criticals.

        They are not managed by QuickOSM so it's a bug from the plugin.

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
            more_details=None,
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

        :param more_details: The message to display in the "More button".
        :type more_details: basestring
        """
        widget = self.message_bar.createMessage(title, message)

        if more_details or open_logs:
            # Adding the button
            button = QPushButton(widget)
            widget.layout().addWidget(button)

            if open_logs:
                button.setText(tr('Report it'))
                # noinspection PyUnresolvedReferences
                button.pressed.connect(
                    lambda: open_log_panel())
            else:
                button.setText(tr('More details'))
                # noinspection PyUnresolvedReferences
                button.pressed.connect(
                    lambda: QMessageBox.information(None, title, more_details))

        self.message_bar.pushWidget(widget, level, duration)

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

    def set_progress_percentage(self, percent):
        """Slot to update percentage during process."""
        self.progress_bar.setValue(percent)
        QApplication.processEvents()

    def set_progress_text(self, text):
        """Slot to update text during process."""
        self.progress_text.setText(text)
        QApplication.processEvents()
