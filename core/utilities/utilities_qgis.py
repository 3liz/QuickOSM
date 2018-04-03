# -*- coding: utf-8 -*-
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

from osgeo import gdal, ogr
from qgis.core import Qgis
from qgis.utils import iface


def display_message_bar(
        title=None, msg=None, level=Qgis.Info, duration=5):
    """
    Display the message at the good place
    """
    if iface.QuickOSM_mainWindowDialog.isVisible():
        iface.QuickOSM_mainWindowDialog.messageBar.pushMessage(
            title, msg, level, duration)
    else:
        iface.messageBar().pushMessage(title, msg, level, duration)
