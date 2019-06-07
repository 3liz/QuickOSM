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

from qgis.core import Qgis
from qgis.utils import iface
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtGui import QDesktopServices
from qgis.PyQt.QtWidgets import QPushButton


from QuickOSM.definitions.urls import (
    BUG_REPORT_URL, MAP_FEATURES_URL, DOC_OVERPASS_URL, OVERPASS_TURBO_URL)
from QuickOSM.core.utilities.tools import tr


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


def display_message_bar(
        title, message=None, level=Qgis.Info, duration=5, open_logs=False):
    """Display the message at the good place.

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
    if iface.QuickOSM_mainWindowDialog.isVisible():
        message_bar = iface.QuickOSM_mainWindowDialog.messageBar
    else:
        message_bar = iface.QuickOSM_mainWindowDialog.messageBar()

    widget = message_bar.createMessage(title, message)

    if open_logs:
        button = QPushButton(widget)
        button.setText(tr('Report it!'))
        button.pressed.connect(
            lambda: open_log_panel())
        widget.layout().addWidget(button)

    message_bar.pushWidget(widget, level, duration)
