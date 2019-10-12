"""Manage nominatim connexion."""

import json

from qgis.PyQt.QtCore import QUrl, QUrlQuery, QEventLoop
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply
from qgis.core import QgsNetworkAccessManager

from ..exceptions import (
    NetWorkErrorException,
    NominatimAreaException
)
from ...definitions.osm import OsmType

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class Nominatim:

    """Manage connexion to Nominatim."""

    def __init__(self, url=None):
        """Constructor.

        :param url: URL of Nominatim server.
        :type url: basestring
        """
        if url is None:
            url = 'https://nominatim.openstreetmap.org/search?format=json'

        self.__url = url
        # noinspection PyArgumentList
        self.network = QgsNetworkAccessManager.instance()
        self.data = None
        self.network_reply = None
        self.loop = None

    def query(self, query):
        """Perform a nominatim query.

        :param query: Query to execute on the nominatim server.
        :type query: basestring

        :return: The result of the query as a dictionary.
        :rtype: dict

        :raise NetWorkErrorException
        """
        url_query = QUrl(self.__url)

        query_string = QUrlQuery()
        query_string.addQueryItem('q', query)
        query_string.addQueryItem('format', 'json')
        query_string.addQueryItem('info', 'QgisQuickOSMPlugin')
        url_query.setQuery(query_string)

        request = QNetworkRequest(url_query)
        self.network_reply = self.network.get(request)
        self.loop = QEventLoop()
        self.network.finished.connect(self._end_of_request)
        self.loop.exec_()

        if self.network_reply.error() == QNetworkReply.NoError:
            return json.loads(self.data)
        else:
            raise NetWorkErrorException('Nominatim API')

    def _end_of_request(self):
        """Internal function to read the content."""
        self.data = self.network_reply.readAll().data().decode('utf-8')
        self.loop.quit()

    def get_first_polygon_from_query(self, query):
        """Get first OSM_ID of a Nominatim area.

        :param query: Query to execute.
        :type query: basestring

        :return: First relation's with an "osm_id".
        :rtype: int

        :raise NominatimAreaException:
        """
        data = self.query(query)
        for result in data:
            if result.get('osm_type') == OsmType.Relation.name.lower():
                osm_id = result.get('osm_id')
                if osm_id:
                    return osm_id

        # If no result has been return
        raise NominatimAreaException(OsmType.Relation, query)

    def get_first_point_from_query(self, query):
        """Get first longitude, latitude of a Nominatim point.

        :param query: Query to execute.
        :type query: basestring

        :return: First node with its longitude and latitude.
        :rtype: tuple(float, float)

        :raise NominatimAreaException:
        """
        data = self.query(query)
        for result in data:
            if result.get('osm_type') == OsmType.Node.name.lower():
                lon = result.get('lon')
                lat = result.get('lat')
                if lon and lat:
                    return lon, lat

        # If no result has been return
        raise NominatimAreaException(OsmType.Node, query)
