"""Exceptions definitions."""

from QuickOSM.core.utilities.tools import tr
# from processing.core.GeoAlgorithmExecutionException import \
#     GeoAlgorithmExecutionException
from qgis.core import Qgis

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class QuickOsmException(BaseException):
    def __init__(self, msg=None):
        if not msg:
            msg = 'QuickOSM'
        self.msg = msg
        BaseException.__init__(self, msg)
        self.level = Qgis.Critical
        self.duration = 7


class GeoAlgorithmException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr('GeoAlgorithm exception')
        QuickOsmException.__init__(self, msg)


"""
Overpass or network
"""


# TODO, not used, but need to be fixed
class OverpassBadRequestException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr('Bad request OverpassAPI')
        QuickOsmException.__init__(self, msg)


class OverpassTimeoutException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr('OverpassAPI timeout, try again later or a smaller query')
        QuickOsmException.__init__(self, msg)


class NetWorkErrorException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg = tr('Network error')
        if suffix:
            msg = msg + ' with ' + suffix
        QuickOsmException.__init__(self, msg)


"""
QueryFactory
"""


class QueryFactoryException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg = tr('Error while building the query')
        if suffix:
            msg = msg + " : " + suffix
        QuickOsmException.__init__(self, msg)


class QueryNotSupported(QuickOsmException):
    def __init__(self, key):
        msg = tr('The query is not supported by the plugin because of '
                 ': {}'.format(key))
        QuickOsmException.__init__(self, msg)


"""
Nominatim
"""


class NominatimAreaException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr('No nominatim area')
        QuickOsmException.__init__(self, msg)


"""
File and directory
"""


class FileDoesntExistException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg = tr('The file does not exist')
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self, msg)


class DirectoryOutPutException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr('The output directory does not exist.')
        QuickOsmException.__init__(self, msg)


class FileOutPutException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg = tr('The output file already exist, set a prefix')
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self, msg)


"""
Forms
"""


class MissingParameterException(QuickOsmException):
    def __init__(self, msg=None, suffix=None):
        if not msg:
            msg = tr('A parameter is missing :')
        if suffix:
            msg = msg + " " + suffix
        QuickOsmException.__init__(self, msg)


class OsmObjectsException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr('No osm objects selected')
        QuickOsmException.__init__(self, msg)


class OutPutGeomTypesException(QuickOsmException):
    def __init__(self, msg=None):
        if not msg:
            msg = tr('No outputs selected')
        QuickOsmException.__init__(self, msg)
