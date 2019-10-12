"""Exceptions definitions."""

from qgis.core import Qgis

from ..definitions.osm import OsmType
from ..qgis_plugin_tools.i18n import tr

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class QuickOsmException(Exception):

    """These exceptions are created by QuickOSM during a process."""

    def __init__(self, message=None, more_details=None):
        """Constructor.

        :param message: The base message to display in the message bar.
        :type message: basestring

        :param more_details: More information to be displayed in the "More info" button.
        :type more_details: basestring
        """
        if not message:
            message = 'QuickOSM'

        self.message = message
        self.more_details = more_details
        self.level = Qgis.Critical
        self.duration = 7
        super(Exception, self).__init__(message, more_details)


"""
Overpass or network
"""


# TODO, not used, but need to be fixed
class OverpassBadRequestException(QuickOsmException):
    def __init__(self, message=None):
        if not message:
            message = tr('Bad request OverpassAPI')
        super().__init__(message)


class OverpassTimeoutException(QuickOsmException):
    def __init__(self, message=None):
        if not message:
            message = tr('OverpassAPI timeout, try again later or a smaller query')
        super().__init__(message)


class NetWorkErrorException(QuickOsmException):
    def __init__(self, message=None, suffix=None):
        if not message:
            message = tr('Network error')
        if suffix:
            message = message + ' with ' + suffix
        super().__init__(message)


"""
QueryFactory
"""


class QueryFactoryException(QuickOsmException):
    def __init__(self, message=None, suffix=None):
        if not message:
            message = tr('Error while building the query')
        if suffix:
            message = message + " : " + suffix
        super().__init__(message)


class QueryNotSupported(QuickOsmException):
    def __init__(self, key):
        message = tr(
            'The query is not supported by the plugin because of : {}'.format(key))
        super().__init__(message)


"""
Nominatim
"""


class NominatimAreaException(QuickOsmException):

    """Raised when no Nominatim area has been found."""

    def __init__(self, osm_type, query):
        """Raised when no Nominatim area has been found.

        :param osm_type: Name of the OSM type object we were looking for.
        :type osm_type: OsmType

        :param query: Name of the place.
        :type query: basestring
        """
        message = tr(
            'No nominatim area found for OSM {osm_type} named {place_name}".')
        message = message.format(osm_type=osm_type.name.lower(), place_name=query)

        more_details = None
        if osm_type == OsmType.Relation:
            # No polygon has been found, we propose the "around" query.
            more_details = tr(
                'No OSM polygon (relation) has been found, you should try the '
                '"Around" query which will search for a point (node).')
        super().__init__(message, more_details)


"""
File and directory
"""


class FileDoesntExistException(QuickOsmException):
    def __init__(self, message=None, suffix=None):
        if not message:
            message = tr('The file does not exist')
        if suffix:
            message = message + " " + suffix
        super().__init__(message)


class DirectoryOutPutException(QuickOsmException):
    def __init__(self, message=None):
        if not message:
            message = tr('The output directory does not exist.')
        super().__init__(message)


class FileOutPutException(QuickOsmException):
    def __init__(self, message=None, suffix=None):
        if not message:
            message = tr('The output file already exist, set a prefix')
        if suffix:
            message = message + " " + suffix
        super().__init__(message)


"""
Forms
"""


class MissingParameterException(QuickOsmException):
    def __init__(self, message=None, suffix=None):
        if not message:
            message = tr('A parameter is missing :')
        if suffix:
            message = message + " " + suffix
        super().__init__(message)


class OsmObjectsException(QuickOsmException):
    def __init__(self, message=None):
        if not message:
            message = tr('No osm objects selected')
        super().__init__(message)


class OutPutGeomTypesException(QuickOsmException):
    def __init__(self, message=None):
        if not message:
            message = tr('No outputs selected')
        super().__init__(message)
