# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
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

from QuickOSM import *

from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException

"""
QApplication.translate doesn't work in contructor's parameters
"""

class QuickOsmException(GeoAlgorithmExecutionException):
    def __init__(self, msg=None):
        GeoAlgorithmExecutionException.__init__(self,msg)    
        self.level = QgsMessageBar.CRITICAL
        self.duration = 7

'''
Overpass or network
'''
class OverpassBadRequestException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = QApplication.translate("QuickOSM", u"Bad request OverpassAPI")
        QuickOsmException.__init__(self,msg)
        
class OverpassTimeoutException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = QApplication.translate("Exception", u"OverpassAPI timeout")
        QuickOsmException.__init__(self,msg)

class NetWorkErrorException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg = QApplication.translate("Exception", u"Network error")
        if suffix:
            msg = msg + " with " + suffix
        QuickOsmException.__init__(self,msg)

'''
Nominatim
'''
class NominatimAreaException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = QApplication.translate("Exception", u"No nominatim area")
        QuickOsmException.__init__(self,msg)

'''
Ogr2Ogr
'''
class Ogr2OgrException(QuickOsmException):
    def __init__(self,msg=None):
        if not msg:
            msg = QApplication.translate("Exception", u"Error with ogr2ogr")
        QuickOsmException.__init__(self,msg)

class NoPointsLayerException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg= QApplication.translate("Exception", u"The result doesn't contain any nodes. Only nodes have coordinates. You should modify the query.")
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self,msg)
        self.level = QgsMessageBar.WARNING
        
class NoLayerException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg= QApplication.translate("Exception", u"The layer is missing :")
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self,msg)

class WrongOrderOSMException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg= QApplication.translate("Exception", u"The order must be node-way-relation. Check the print statement.")
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self,msg)

'''
File and directory
'''     
class FileDoesntExistException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg= QApplication.translate("Exception", u"The file doesn't exist")
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self,msg)

class DirectoryOutPutException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = QApplication.translate("Exception", u"The output directory does not exist.")
        QuickOsmException.__init__(self,msg)
        
class FileOutPutException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg= QApplication.translate("Exception", u"The output file already exist, set a prefix")
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self,msg)
        
class OutPutFormatException(QuickOsmException):
    def __init__(self,msg=None):
        if not msg:
            msg = QApplication.translate("Exception", u"Output not available")
        QuickOsmException.__init__(self,msg)
        
class QueryAlreadyExistsException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg= QApplication.translate("Exception", u"This query already exists")
        QuickOsmException.__init__(self,msg)
        
'''
Forms
'''
class MissingParameterException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg= QApplication.translate("Exception", u"A parameter is missing :")
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self,msg)
        
class OsmObjectsException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg= QApplication.translate("Exception", u"No osm objects selected")
        QuickOsmException.__init__(self,msg)
        
class OutPutGeomTypesException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg= QApplication.translate("Exception", u"No outputs selected")
        QuickOsmException.__init__(self,msg)