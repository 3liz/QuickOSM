"""Manage nominatim connexion."""

import json
import logging
import os

from qgis.PyQt.QtCore import (
    QUrl,
    QUrlQuery,
    QEventLoop,
    QTemporaryFile,
    QDir,
)
from qgis.core import QgsFileDownloader

from ..exceptions import (
    NetWorkErrorException,
    NominatimAreaException
)
from ...definitions.osm import OsmType

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'

LOGGER = logging.getLogger('QuickOSM')


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
        temporary = QTemporaryFile(
            os.path.join(QDir.tempPath(), 'request-XXXXXX.json'))
        temporary.open()
        self.result_path = temporary.fileName()
        temporary.close()

    @staticmethod
    def error(messages):
        for message in messages:
            LOGGER.error(message)
        raise NetWorkErrorException('Nominatim API', ', '.join(messages))

    @staticmethod
    def canceled():
        LOGGER.info('Request canceled')
        # TODO, need to handle this to stop the process.

    @staticmethod
    def completed():
        LOGGER.info('Request completed')

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

        loop = QEventLoop()
        downloader = QgsFileDownloader(
            url_query, self.result_path, delayStart=True)
        downloader.downloadExited.connect(loop.quit)
        downloader.downloadError.connect(self.error)
        downloader.downloadCanceled.connect(self.canceled)
        downloader.downloadCompleted.connect(self.completed)
        downloader.startDownload()
        loop.exec_()

        with open(self.result_path) as json_file:
            data = json.load(json_file)
            return data

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
