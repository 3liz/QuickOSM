"""Manage Overpass API connexion."""

import codecs
import logging
import os
import re

from qgis.PyQt.QtCore import (
    QUrl,
    QEventLoop,
    QTemporaryFile,
    QDir,
    QFileInfo,
)
from qgis.core import QgsFileDownloader

from ..exceptions import (
    OverpassTimeoutException,
    NetWorkErrorException,
)

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'

LOGGER = logging.getLogger('QuickOSM')


class ConnexionOAPI:

    """
    Manage connexion to the overpass API.
    """

    def __init__(self, url):
        """Constructor of query.

        :param url:Full URL of OverPass Query with the query encoded in it.
        :type url:str
        """
        self._url = QUrl(url)

        temporary = QTemporaryFile(
            os.path.join(QDir.tempPath(), 'request-XXXXXX.osm'))
        temporary.open()
        self.result_path = temporary.fileName()
        temporary.close()

    @staticmethod
    def error(messages):
        for msg in messages:
            LOGGER.error(msg)
        raise NetWorkErrorException(msg)

    @staticmethod
    def canceled():
        LOGGER.info('Request canceled')
        # TODO, need to handle this to stop the process.

    @staticmethod
    def completed():
        LOGGER.info('Request completed')

    def run(self):
        """Run the query.

        @raise OverpassBadRequestException,NetWorkErrorException,
        OverpassTimeoutException

        @return: The result of the query.
        @rtype: str
        """
        loop = QEventLoop()
        downloader = QgsFileDownloader(
            self._url, self.result_path, delayStart=True)
        downloader.downloadExited.connect(loop.quit)
        downloader.downloadError.connect(self.error)
        downloader.downloadCanceled.connect(self.canceled)
        downloader.downloadCompleted.connect(self.completed)
        downloader.startDownload()
        loop.exec_()

        osm_file = QFileInfo(self.result_path)
        if not osm_file.exists() and not osm_file.isFile():
            raise OverpassTimeoutException

        # The download is done, checking for not complete OSM file.
        # Overpass might aborted the request with HTTP 200.
        file_obj = codecs.open(self.result_path, 'r', 'utf-8')
        file_obj.seek(0, 2)
        fsize = file_obj.tell()
        file_obj.seek(max(fsize - 1024, 0), 0)
        lines = file_obj.readlines()
        file_obj.close()
        lines = lines[-10:]  # Get last 10 lines
        timeout = (
            '<remark> runtime error: Query timed out in "[a-z]+" at line '
            '[\d]+ after ([\d]+) seconds. </remark>')
        if re.search(timeout, ''.join(lines)):
            raise OverpassTimeoutException

        # Everything went fine
        return self.result_path
