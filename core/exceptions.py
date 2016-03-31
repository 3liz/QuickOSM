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

from processing.core.GeoAlgorithmExecutionException import \
    GeoAlgorithmExecutionException
from qgis.gui import QgsMessageBar

from QuickOSM.core.utilities.tools import tr


class QuickOsmException(GeoAlgorithmExecutionException):
    def __init__(self, msg=None):
        GeoAlgorithmExecutionException.__init__(self, msg)
        self.level = QgsMessageBar.CRITICAL
        self.duration = 7

'''
Overpass or network
'''


class OverpassBadRequestException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr('Exception', u'Bad request OverpassAPI')
        QuickOsmException.__init__(self, msg)


class OverpassTimeoutException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr('Exception', u'OverpassAPI timeout')
        QuickOsmException.__init__(self, msg)


class NetWorkErrorException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg = tr("Exception", u"Network error")
        if suffix:
            msg = msg + " with " + suffix
        QuickOsmException.__init__(self, msg)

'''
QueryFactory
'''


class QueryFactoryException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg = tr("Exception", u"Error while building the query")
        if suffix:
            msg = msg + " : " + suffix
        QuickOsmException.__init__(self, msg)


class QueryNotSupported(QuickOsmException):
    def __init__(self, key):
        msg = tr("Exception",
                 u"The query is not supported by the plugin because of"
                 u" : %s" % key)
        QuickOsmException.__init__(self, msg)

'''
Nominatim
'''


class NominatimAreaException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr("Exception", u"No nominatim area")
        QuickOsmException.__init__(self, msg)

'''
Ogr2Ogr
'''


class OsmDriverNotFound(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr(
                'Exception', u"The OSM's driver is not installed. "
                             u"Please install the OSM driver for GDAL "
                             u": http://www.gdal.org/drv_osm.html")
        QuickOsmException.__init__(self, msg)


class GDALVersion(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr(
                'Exception', u"You must upgrade GDAL/OGR >= 1.10.0.")
        QuickOsmException.__init__(self, msg)


class Ogr2OgrException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr("Exception", u"Error with ogr2ogr")
        QuickOsmException.__init__(self, msg)


class NoLayerException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg = tr("Exception", u"The layer is missing :")
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self, msg)


class WrongOrderOSMException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg = tr(
                'Exception',
                u'The order must be node-way-relation. '
                u'Check the print statement.')
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self, msg)

'''
File and directory
'''


class FileDoesntExistException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg = tr("Exception", u"The file doesn't exist")
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self, msg)


class DirectoryOutPutException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr('Exception', u'The output directory does not exist.')
        QuickOsmException.__init__(self, msg)


class FileOutPutException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg = tr(
                'Exception', u'The output file already exist, set a prefix')
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self, msg)


class OutPutFormatException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr("Exception", u"Output not available")
        QuickOsmException.__init__(self, msg)


class QueryAlreadyExistsException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr("Exception", u"This query already exists")
        QuickOsmException.__init__(self, msg)

'''
Forms
'''


class MissingParameterException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg = tr("Exception", u"A parameter is missing :")
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self, msg)


class OsmObjectsException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr("Exception", u"No osm objects selected")
        QuickOsmException.__init__(self, msg)


class OutPutGeomTypesException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr('Exception', u'No outputs selected')
        QuickOsmException.__init__(self, msg)
