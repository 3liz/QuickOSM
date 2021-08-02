"""Manage downloader."""

import logging

from qgis.core import QgsFileDownloader
from qgis.PyQt.QtCore import QEventLoop, QUrl

__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

LOGGER = logging.getLogger('QuickOSM')


class Downloader:
    """Manage downloader."""

    def __init__(self, url: str = None):
        """Constructor."""
        if url is None:
            url = 'https://nominatim.openstreetmap.org/search?'

        self._url = QUrl(url)
        self.result_path = None
        self.errors = []

    def error(self, messages: str):
        """Store the messages error"""
        self.errors = messages

    @staticmethod
    def canceled():
        """Display the status in logger"""
        LOGGER.info('Request canceled')
        # TODO, need to handle this to stop the process.

    @staticmethod
    def completed():
        """Display the status in logger"""
        LOGGER.info('Request completed')

    def download(self):
        """Download the data"""
        loop = QEventLoop()
        downloader = QgsFileDownloader(
            self._url, self.result_path, delayStart=True)
        downloader.downloadExited.connect(loop.quit)
        downloader.downloadError.connect(self.error)
        downloader.downloadCanceled.connect(self.canceled)
        downloader.downloadCompleted.connect(self.completed)
        downloader.startDownload()
        loop.exec_()
