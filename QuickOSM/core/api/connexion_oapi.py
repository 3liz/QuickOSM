"""Manage Overpass API connexion."""

import logging
import os
import re

from typing import List

from qgis.core import QgsFileDownloader
from qgis.PyQt.QtCore import QDir, QEventLoop, QFileInfo, QTemporaryFile, QUrl

from QuickOSM.core.exceptions import (
    NetWorkErrorException,
    OverpassBadRequestException,
    OverpassManyRequestException,
    OverpassMemoryException,
    OverpassRuntimeError,
    OverpassTimeoutException,
)

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

LOGGER = logging.getLogger('QuickOSM')


class ConnexionOAPI:

    """
    Manage connexion to the overpass API.
    """

    def __init__(self, url: str):
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
            self.too_many_request(message)
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
    def check_file(path: str):
        # The download is done, checking for not complete OSM file.
        # Overpass might aborted the request with HTTP 200.
        LOGGER.info('Checking OSM file content {}'.format(path))

        def last_lines(file_path: str, line_count: int) -> List[str]:
            bufsize = 8192
            fsize = os.stat(file_path).st_size
            iteration = 0
            with open(file_path, encoding='utf8') as f:
                if bufsize > fsize:
                    bufsize = fsize - 1
                    data = []
                    while True:
                        iteration += 1
                        seek_size = fsize - bufsize * iteration
                        if seek_size < 0:
                            seek_size = 0
                        f.seek(seek_size)
                        data.extend(f.readlines())
                        if len(data) >= line_count or f.tell() == 0:
                            line_content = data[-line_count:]
                            return line_content
                else:
                    return list(f.readlines())

        lines = last_lines(path, 10)

        # Check if we can use the static method below
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
    def is_query_timed_out(string: str):
        text = 'Network request (.*) timed out'
        search = re.search(text, string)
        if search:
            raise OverpassTimeoutException

    @staticmethod
    def too_many_request(string: str):
        text = '(.*)server replied: Too Many Requests'
        search = re.search(text, string)
        if search:
            raise OverpassManyRequestException

    @staticmethod
    def is_bad_request(string: str):
        text = '(.*)server replied: Bad Request'
        search = re.search(text, string)
        if search:
            raise OverpassBadRequestException

        text = '(.*)server replied: Forbidden'
        search = re.search(text, string)
        if search:
            raise OverpassBadRequestException
