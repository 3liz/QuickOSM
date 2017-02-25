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

import urllib2
import re
import tempfile
from PyQt4.QtNetwork import QNetworkRequest, QNetworkReply
from PyQt4.QtCore import QUrl, QEventLoop
from qgis.core import QgsNetworkAccessManager

from QuickOSM.core.exceptions import (
    OutPutFormatException,
    OverpassTimeoutException,
    OverpassBadRequestException,
    NetWorkErrorException
)


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
        self.data = None

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
        encoded_query = QUrl.toPercentEncoding(query)
        url_query.addEncodedQueryItem('data', encoded_query)
        url_query.addQueryItem('info', 'QgisQuickOSMPlugin')
        url_query.setPort(80)

        request = QNetworkRequest(url_query)
        request.setRawHeader("User-Agent", "QuickOSM")
        self.network_reply = self.network.get(request)
        self.loop = QEventLoop()
        self.network.finished.connect(self._end_of_request)
        self.loop.exec_()

        if self.network_reply.error() == QNetworkReply.NoError:
            timeout = '<remark> runtime error: Query timed out in "[a-z]+" ' \
                      'at line [\d]+ after ([\d]+) seconds. </remark>'
            if re.search(timeout, self.data):
                raise OverpassTimeoutException
            else:
                return self.data

        elif self.network_reply.error() == QNetworkReply.UnknownContentError:
            raise OverpassBadRequestException
        else:
            raise NetWorkErrorException(suffix="Overpass API")

    def _end_of_request(self):
        self.data = self.network_reply.readAll()
        self.loop.quit()

    def get_file_from_query(self, query):
        """
        Make a query to the overpass and put the result in a temp file

        @param query:Query to execute
        @type query:str

        @return: temporary file path
        @rtype: str
        """
        query = self.query(query)
        tf = tempfile.NamedTemporaryFile(delete=False, suffix=".osm")
        tf.write(query)
        name_file = tf.name
        tf.flush()
        tf.close()
        return name_file

    def get_timestamp(self):
        """
        Get the timestamp of the OSM data on the server

        @return: Timestamp
        @rtype: str
        """
        url_query = self.__url + 'timestamp'
        try:
            return urllib2.urlopen(url=url_query).read()
        except urllib2.HTTPError as e:
            if e.code == 400:
                raise OverpassBadRequestException

    def is_valid(self):
        """
        Try if the url is valid, NOT TESTED YET
        """
        url_query = self.__url + 'interpreter'
        try:
            urllib2.urlopen(url=url_query)
            return True
        except urllib2.HTTPError:
            return False
