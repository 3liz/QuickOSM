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
    OverpassBadRequestException,
    OverpassTimeoutException,
    NetWorkErrorException,
    OverpassRuntimeError,
    OverpassMemoryException,
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
        self.errors = []

    def error(self, messages):
        self.errors = messages

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

        for message in self.errors:
            self.is_query_timed_out(message)
            self.is_bad_request(message)
            LOGGER.error(message)

        if len(self.errors):
            raise NetWorkErrorException('Overpass API', ', '.join(self.errors))

        osm_file = QFileInfo(self.result_path)
        if not osm_file.exists() and not osm_file.isFile():
            # Do not raise a QuickOSM exception here
            # It must be a bug from QuickOSM
            raise FileNotFoundError

        self.check_file(self.result_path)

        # Everything went fine
        return self.result_path

    @staticmethod
    def check_file(path):
        # The download is done, checking for not complete OSM file.
        # Overpass might aborted the request with HTTP 200.
        file_obj = codecs.open(path, 'r', 'utf-8')
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

        memory = (
            '<remark> runtime error: Query ran out of memory in "query" at '
            'line [\d]+. It would need at least ([\d]+) (.*) of RAM to '
            'continue. </remark>')
        search = re.search(memory, ''.join(lines))
        if search:
            raise OverpassMemoryException(search.group(1), search.group(2))

        generic = (
            '<remark> runtime error: (.*)</remark>')
        search = re.search(generic, ''.join(lines))
        if search:
            raise OverpassRuntimeError(search.group(1))

    @staticmethod
    def is_query_timed_out(string):
        text = 'Network request (.*) timed out'
        search = re.search(text, string)
        if search:
            raise OverpassTimeoutException

    @staticmethod
    def is_bad_request(string):
        text = '(.*)server replied: Bad Request'
        search = re.search(text, string)
        if search:
            raise OverpassBadRequestException

        text = '(.*)server replied: Forbidden'
        search = re.search(text, string)
        if search:
            raise OverpassBadRequestException
