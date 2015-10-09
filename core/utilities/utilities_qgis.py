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
from qgis.gui import QgsMessageBar
from qgis.utils import iface


def display_message_bar(
        title=None, msg=None, level=QgsMessageBar.INFO, duration=5):
    """
    Display the message at the good place
    """
    if iface.QuickOSM_mainWindowDialog.isVisible():
        iface.QuickOSM_mainWindowDialog.messageBar.pushMessage(
            title, msg, level, duration)
    else:
        iface.messageBar().pushMessage(title, msg, level, duration)


def get_ogr_version():
    return int(gdal.VersionInfo('VERSION_NUM'))


def is_osm_driver_enabled():
    if get_ogr_version < 1100000:
        return False

    if not ogr.GetDriverByName('OSM'):
        return False

    return True
