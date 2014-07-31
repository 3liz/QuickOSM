# -*- coding: utf-8 -*-
"""
/***************************************************************************
QuickOSM
A QGIS plugin
OSM's Overpass API frontend
-------------------
begin : 2014-06-11
copyright : (C) 2014 by 3Liz
email : info@3liz.com
***************************************************************************/

/***************************************************************************
* *
* This program is free software; you can redistribute it and/or modify *
* it under the terms of the GNU General Public License as published by *
* the Free Software Foundation; either version 2 of the License, or *
* (at your option) any later version. *
* *
***************************************************************************/
This script initializes the plugin, making it known to QGIS.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import resources_rc
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from CoreQuickOSM.ExceptionQuickOSM import *


def classFactory(iface):
    from quick_osm import QuickOSM
    return QuickOSM(iface)