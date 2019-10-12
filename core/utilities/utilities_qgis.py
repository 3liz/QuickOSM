"""Utilities when using QGIS."""

from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtGui import QDesktopServices
from qgis.utils import iface

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


from ...definitions.urls import (
    MAP_FEATURES_URL, DOC_OVERPASS_URL, OVERPASS_TURBO_URL)


def open_log_panel():
    """Open the log panel for bug reporting."""
    iface.openMessageLog()
    # Disabled because too much tickets without useful info.
    # open_webpage(BUG_REPORT_URL)


def open_overpass_turbo():
    """Open Overpass Turbo."""
    open_webpage(OVERPASS_TURBO_URL)


def open_doc_overpass():
    """Open Overpass's documentation."""
    open_webpage(DOC_OVERPASS_URL)


def open_map_features():
    """Open the map features webpage."""
    open_webpage(MAP_FEATURES_URL)


def open_webpage(url):
    """Open a specific webpage."""
    desktop_service = QDesktopServices()
    if isinstance(url, str):
        desktop_service.openUrl(QUrl(url))
    else:
        desktop_service.openUrl(url)
