# -*- coding: utf-8 -*-
"""
/***************************************************************************
QuickOSM
A QGIS plugin
OSM Overpass API frontend
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
from __future__ import absolute_import


# noinspection PyDocstring,PyPep8Naming
def classFactory(iface):
    from .quick_osm import QuickOSM
    return QuickOSM(iface)


# noinspection PyDocstring,PyPep8Naming
def serverClassFactory(serverIface):
    # from .quick_osm_processing.algorithm_provider import (
    #     QuickOSMAlgorithmProvider)
    pass
