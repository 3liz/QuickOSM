# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
 A QGIS plugin
 OSM Overpass API frontend
                             -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info at 3liz dot com
        contributor          : Etienne Trimaille
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import logging
import codecs
import os
import re

from QuickOSM.core.exceptions import (
    OverpassTimeoutException,
)
from qgis.PyQt.QtCore import (
    QUrl, QEventLoop, QTemporaryFile, QDir)
from qgis.core import QgsFileDownloader

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

    @staticmethod
    def canceled():
        LOGGER.info('Request canceled')

    @staticmethod
    def completed():
        pass

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

        file_obj = codecs.open(self.result_path, 'r', 'utf-8')
        file_obj.seek(0, 2)
        fsize = file_obj.tell()
        file_obj.seek(max(fsize - 1024, 0), 0)
        lines = file_obj.readlines()
        file_obj.close()

        lines = lines[-10:]  # Get last 10 lines
        timeout = '<remark> runtime error: Query timed out in "[a-z]+" ' \
                  'at line [\d]+ after ([\d]+) seconds. </remark>'
        if re.search(timeout, ''.join(lines)):
            raise OverpassTimeoutException
        else:
            return self.result_path
