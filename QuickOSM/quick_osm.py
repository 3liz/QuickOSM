"""QuickOSM main entry point for setting up the UI, Processing."""

import logging
import urllib.request

from qgis.core import (
    Qgis,
    QgsApplication,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
)
from qgis.PyQt.QtCore import QCoreApplication, QTranslator, QUrl
from qgis.PyQt.QtGui import QDesktopServices, QIcon
from qgis.PyQt.QtWidgets import (
    QAction,
    QDialog,
    QMenu,
    QMessageBox,
    QPushButton,
)

from QuickOSM.core.utilities.tools import get_setting, set_setting
from QuickOSM.core.utilities.utilities_qgis import open_webpage
from QuickOSM.definitions.urls import DOC_PLUGIN_URL
from QuickOSM.qgis_plugin_tools.tools.custom_logging import setup_logger
from QuickOSM.qgis_plugin_tools.tools.i18n import setup_translation, tr
from QuickOSM.qgis_plugin_tools.tools.resources import (
    plugin_name,
    plugin_path,
    resources_path,
)
from QuickOSM.quick_osm_processing.provider import Provider

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

LOGGER = logging.getLogger(plugin_name())


class QuickOSMPlugin:
    """Plugin QuickOSM."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        setup_logger(plugin_name())

        locale, file_path = setup_translation(
            folder=plugin_path("i18n"), file_pattern="quickosm_{}.qm")
        if file_path:
            # LOGGER.info('Translation to {}'.format(file_path))
            self.translator = QTranslator()
            self.translator.load(file_path)
            QCoreApplication.installTranslator(self.translator)
        else:
            # LOGGER.info('Translation not found: {}'.format(locale))
            pass

        self.provider = None

        self.toolbar = None
        self.help_action = None
        self.quickosm_menu = None
        self.vector_menu = None
        self.main_window_action = None
        self.josm_action = None

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = Provider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        """Init the user interface."""
        self.initProcessing()

        icon = QIcon(resources_path('icons', 'QuickOSM.svg'))

        if Qgis.QGIS_VERSION_INT >= 31000:
            self.help_action = QAction(icon, 'QuickOSM', self.iface.mainWindow())
            self.iface.pluginHelpMenu().addAction(self.help_action)
            self.help_action.triggered.connect(self.show_help)

        # Add the toolbar
        self.toolbar = self.iface.addToolBar('QuickOSM')
        self.toolbar.setObjectName('QuickOSM')

        # Setup menu
        self.quickosm_menu = QMenu('QuickOSM')
        self.quickosm_menu.setIcon(icon)
        self.vector_menu = self.iface.vectorMenu()
        self.vector_menu.addMenu(self.quickosm_menu)

        # Main window
        self.main_window_action = QAction(icon, 'QuickOSM…', self.iface.mainWindow())
        # noinspection PyUnresolvedReferences
        self.main_window_action.triggered.connect(self.open_dialog)
        self.toolbar.addAction(self.main_window_action)

        # Action JOSM
        self.josm_action = QAction(
            QIcon(resources_path('icons', 'josm_icon.svg')),
            tr('JOSM Remote'),
            self.iface.mainWindow())
        self.josm_action.triggered.connect(self.josm_remote)
        self.toolbar.addAction(self.josm_action)

        # Insert in the good order
        self.quickosm_menu.addAction(self.main_window_action)
        self.quickosm_menu.addAction(self.josm_action)

    def unload(self):
        """Unload the user interface."""
        self.iface.removePluginVectorMenu('&QuickOSM', self.main_window_action)
        self.iface.removeToolBarIcon(self.main_window_action)
        QgsApplication.processingRegistry().removeProvider(self.provider)

        if Qgis.QGIS_VERSION_INT >= 31000 and self.help_action:
            self.iface.pluginHelpMenu().removeAction(self.help_action)
            del self.help_action

    @staticmethod
    def show_help():
        """Open the help web page"""
        QDesktopServices.openUrl(QUrl(DOC_PLUGIN_URL))

    def josm_remote(self):
        """Call the JOSM remote control using the current canvas extent."""
        map_settings = self.iface.mapCanvas().mapSettings()
        extent = map_settings.extent()
        crs_map = map_settings.destinationCrs()
        if crs_map.authid() != 'EPSG:4326':
            crs_4326 = QgsCoordinateReferenceSystem(4326)
            transform = QgsCoordinateTransform(
                crs_map, crs_4326, QgsProject.instance())
            extent = transform.transform(extent)

        url = 'http://localhost:8111/load_and_zoom?'
        query_string = 'left={}&right={}&top={}&bottom={}'.format(
            extent.xMinimum(), extent.xMaximum(), extent.yMaximum(),
            extent.yMinimum())
        url += query_string
        try:
            request = urllib.request.Request(url)
            result_request = urllib.request.urlopen(request)
            result = result_request.read()
            result = result.decode('utf8')
            if result.strip().upper() != 'OK':
                self.iface.messageBar().pushCritical(
                    tr('JOSM Remote'), result)
            else:
                self.iface.messageBar().pushSuccess(
                    tr('JOSM Remote'), tr('Import done, check JOSM.'))
        except IOError:
            self.iface.messageBar().pushCritical(
                tr('JOSM Remote'), tr('Is the remote enabled in the JOSM settings?'))

    def open_dialog(self):
        """Create and open the main dialog."""
        from QuickOSM.ui.dialog import Dialog
        dialog = Dialog()
        self.open_copyright_message(dialog)
        dialog.exec_()

    @staticmethod
    def open_copyright_message(dialog: QDialog):
        """Display a window to bring a reminder of the OSM copyrights."""

        def read_copyright():
            open_webpage('https://www.openstreetmap.org/copyright')
            set_setting("copyright_dialog", "OpenStreetMap")

        def know_copyright():
            set_setting("copyright_dialog", "OpenStreetMap")

        if not get_setting("copyright_dialog"):

            message = QMessageBox(dialog)
            text = tr(
                'OpenStreetMap® is open data, licensed under the'
                ' Open Data Commons Open Database License (ODbL) '
                'by the OpenStreetMap Foundation.'
            ) + '\n'
            text += tr(
                'The Foundation requires that you use the credit '
                '“© OpenStreetMap contributors” on any product using OSM data.'
            ) + '\n'
            text += tr(
                'You should read https://www.openstreetmap.org/copyright'
            )
            message.setText(text)
            message.setIcon(QMessageBox.Question)
            no_button = QPushButton(tr('I understand the copyrights, access to the plugin'), message)
            yes_button = QPushButton(tr('I want to read the copyrights'), message)
            message.addButton(no_button, QMessageBox.NoRole)
            message.addButton(yes_button, QMessageBox.YesRole)
            yes_button.clicked.connect(read_copyright)
            no_button.clicked.connect(know_copyright)
            message.exec()

    @staticmethod
    def run_tests():
        """Run the test inside QGIS."""
        try:
            from pathlib import Path

            from qgis_plugin_tools.infrastructure.test_runner import (
                test_package,
            )
            test_package('{}.__init__'.format(Path(__file__).parent.name))
        except (AttributeError, ModuleNotFoundError):
            message = 'Could not load tests. Are you using a production package?'
            print(message)
            LOGGER.debug(message)
