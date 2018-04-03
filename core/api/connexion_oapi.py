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

import codecs
import os
import re
import urllib.error
import urllib.parse
import urllib.request

from QuickOSM.core.exceptions import (
    OutPutFormatException,
    OverpassTimeoutException,
    OverpassBadRequestException,
    NetWorkErrorException
)
from qgis.PyQt.QtCore import (
    QUrl, QUrlQuery, QEventLoop, QTemporaryFile, QDir, QIODevice)
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply
from qgis.core import QgsNetworkAccessManager


class ConnexionOAPI(object):
    """
    Manage connexion to the overpass API
    """

    def __init__(self, url="http://overpass-api.de/api/", output=None):
        """
        Constructor

        @param url:URL of OverPass
        @type url:str

        @param output:Output desired (XML or JSON)
        @type output:str
        """

        if not url:
            url = "http://overpass-api.de/api/"

        self.__url = url
        self.result_path = None

        if output not in (None, "json", "xml"):
            raise OutPutFormatException

        self.__output = output
        self.network = QgsNetworkAccessManager.instance()
        self.network_reply = None
        self.loop = None

    def query(self, query):
        """
        Make a query to the overpass

        @param query:Query to execute
        @type query:str

        @raise OverpassBadRequestException,NetWorkErrorException,
        OverpassTimeoutException

        @return: the result of the query
        @rtype: str
        """

        url_query = QUrl(self.__url + 'interpreter')

        # The output format can be forced (JSON or XML)
        if self.__output:
            query = re.sub(
                r'output="[a-z]*"', 'output="' + self.__output + '"', query)
            query = re.sub(
                r'\[out:[a-z]*', '[out:' + self.__output, query)

        # noinspection PyCallByClass
        # encoded_query = QUrl.toPercentEncoding(query)
        query_string = QUrlQuery()
        query_string.addQueryItem('data', query)
        query_string.addQueryItem('info', 'QgisQuickOSMPlugin')
        url_query.setQuery(query_string)

        request = QNetworkRequest(url_query)
        # request.setRawHeader("User-Agent", "QuickOSM")
        self.network_reply = self.network.get(request)
        self.loop = QEventLoop()
        self.network.finished.connect(self._end_of_request)
        self.loop.exec_()

        if self.network_reply.error() == QNetworkReply.NoError:
            file_obj = codecs.open(self.result_path, 'r', 'utf-8')
            file_obj.seek(0, 2)
            fsize = file_obj.tell()
            file_obj.seek(max(fsize - 1024, 0), 0)
            lines = file_obj.readlines()

            lines = lines[-10:]  # Get last 10 lines
            timeout = '<remark> runtime error: Query timed out in "[a-z]+" ' \
                      'at line [\d]+ after ([\d]+) seconds. </remark>'
            if re.search(timeout, ''.join(lines)):
                raise OverpassTimeoutException
            else:
                return self.result_path

        elif self.network_reply.error() == QNetworkReply.UnknownContentError:
            raise OverpassBadRequestException
        else:
            raise NetWorkErrorException(suffix="Overpass OSM API")

    def _end_of_request(self):
        tf = QTemporaryFile(
            os.path.join(QDir.tempPath(), 'request-XXXXXX.osm'))
        tf.setAutoRemove(False)
        tf.open(QIODevice.WriteOnly | QIODevice.Text)
        tf.write(self.network_reply.readAll().simplified())
        tf.close()
        self.result_path = tf.fileName()
        self.loop.quit()
