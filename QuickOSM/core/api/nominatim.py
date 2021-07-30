"""Manage nominatim connexion."""

import json
import logging
import os

from qgis.core import QgsFileDownloader
from qgis.PyQt.QtCore import QDir, QEventLoop, QTemporaryFile, QUrl, QUrlQuery

from QuickOSM.core.exceptions import (
    NetWorkErrorException,
    NominatimAreaException,
    NominatimBadRequest,
)
from QuickOSM.definitions.osm import OsmType

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

LOGGER = logging.getLogger('QuickOSM')


class Nominatim:

    """Manage connexion to Nominatim."""

    def __init__(self, url: str = None):
        """Constructor.

        :param url: URL of Nominatim server.
        :type url: basestring
        """
        if url is None:
            url = 'https://nominatim.openstreetmap.org/search?'

        self.__url = url
        temporary = QTemporaryFile(
            os.path.join(QDir.tempPath(), 'request-XXXXXX.json'))
        temporary.open()
        self.result_path = temporary.fileName()
        temporary.close()

    @staticmethod
    def error(messages: str):
        """Display the status in logger"""
        for message in messages:
            LOGGER.error(message)
        raise NetWorkErrorException('Nominatim API', ', '.join(messages))

    @staticmethod
    def canceled():
        """Display the status in logger"""
        LOGGER.info('Request canceled')
        # TODO, need to handle this to stop the process.

    @staticmethod
    def completed():
        """Display the status in logger"""
        LOGGER.info('Request completed')

    def query(self, query: str) -> dict:
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

        with open(self.result_path, encoding='utf8') as json_file:
            data = json.load(json_file)
            if not data:
                raise NominatimBadRequest(query)
            return data

    def get_first_polygon_from_query(self, query: str) -> str:
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
        raise NominatimAreaException(query)

    def get_first_point_from_query(self, query: str) -> (str, str):
        """Get first longitude, latitude of a Nominatim point.

        :param query: Query to execute.
        :type query: basestring

        :return: First node with its longitude and latitude.
        :rtype: tuple(float, float)

        :raise NominatimAreaException:
        """
        data = self.query(query)
        for result in data:
            lon = result.get('lon')
            lat = result.get('lat')
            if lon and lat:
                return lon, lat
