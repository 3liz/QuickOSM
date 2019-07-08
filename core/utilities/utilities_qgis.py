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

from qgis.utils import iface
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtGui import QDesktopServices


from QuickOSM.definitions.urls import (
    BUG_REPORT_URL, MAP_FEATURES_URL, DOC_OVERPASS_URL, OVERPASS_TURBO_URL)


def open_log_panel():
    """Open the log panel for bug reporting."""
    iface.openMessageLog()
    open_webpage(BUG_REPORT_URL)


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
