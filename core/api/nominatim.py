"""Manage nominatim connexion."""

import json

from qgis.PyQt.QtCore import QUrl, QUrlQuery, QEventLoop
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply
from qgis.core import QgsNetworkAccessManager

from ..exceptions import (
    NetWorkErrorException,
    NominatimAreaException
)

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class Nominatim:
    """Manage connexion to Nominatim."""

    def __init__(self,
                 url="https://nominatim.openstreetmap.org/search?format=json"):
        """
        Constructor
        @param url:URL of Nominatim
        @type url:str
        """

        self.__url = url
        self.network = QgsNetworkAccessManager.instance()
        self.data = None
        self.network_reply = None
        self.loop = None

    def query(self, query):
        """
        Perform a nominatim query

        @param query: Query to execute
        @type query: str

        @raise NetWorkErrorException

        @return: the result of the query
        @rtype: str
        """

        url_query = QUrl(self.__url)

        # query = QUrl.toPercentEncoding(query)
        query_string = QUrlQuery()
        query_string.addQueryItem('q', query)
        query_string.addQueryItem('format', 'json')
        query_string.addQueryItem('info', 'QgisQuickOSMPlugin')
        url_query.setQuery(query_string)

        request = QNetworkRequest(url_query)
        # request.setRawHeader("User-Agent", "QuickOSM")
        self.network_reply = self.network.get(request)
        self.loop = QEventLoop()
        self.network.finished.connect(self._end_of_request)
        self.loop.exec_()

        if self.network_reply.error() == QNetworkReply.NoError:
            return json.loads(self.data)
        else:
            raise NetWorkErrorException(suffix="Nominatim API")

    def _end_of_request(self):
        self.data = self.network_reply.readAll().data().decode('utf-8')
        self.loop.quit()

    def get_first_polygon_from_query(self, query):
        """
        Get first OSM_ID of a Nominatim area

        @param query: Query to execute
        @type query: str

        @raise NominatimAreaException:

        @return: First relation's osm_id
        @rtype: str
        """
        data = self.query(query)
        for result in data:
            if result['osm_type'] == "relation":
                return result['osm_id']

        # If no result has been return
        raise NominatimAreaException

    def get_first_point_from_query(self, query):
        """
        Get first longitude, latitude of a Nominatim point

        @param query: Query to execute
        @type query: str

        @raise NominatimAreaException:

        @return: First relation's osm_id
        @rtype: str
        """
        data = self.query(query)
        for result in data:
            if result['osm_type'] == "node":
                return result['lon'], result['lat']

        # If no result has been return
        raise NominatimAreaException
