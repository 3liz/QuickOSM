# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
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

from QuickOSM import *
from PyQt4.QtNetwork import QNetworkAccessManager,QNetworkRequest,QNetworkReply
import json

class Nominatim:
    '''
    Manage connexion to Nominatim
    '''
        
    def __init__(self, url = "http://nominatim.openstreetmap.org/search?format=json"):
        '''
        Constructor
        @param url:URL of Nominatim
        @type url:str
        '''

        self.__url = url
        self.network = QNetworkAccessManager()
        self.data = None
        
    def query(self, query):
        '''
        Perform a nominatim query
        @param req:Query to execute
        @type req:str
        @raise NetWorkErrorException
        @return: the result of the query
        @rtype: str
        '''
        
        urlQuery = QUrl(self.__url)
        
        query = QUrl.toPercentEncoding(query)
        urlQuery.addEncodedQueryItem('q',query)
        urlQuery.addQueryItem('info','QgisQuickOSMPlugin')
        urlQuery.setPort(80)
        
        from QuickOSM.CoreQuickOSM.Tools import *
        proxy = Tools.getProxy()
        if proxy:
            self.network.setProxy(proxy)

        request = QNetworkRequest(urlQuery)
        request.setRawHeader("User-Agent", "QuickOSM");
        self.networkReply = self.network.get(request)
        self.loop = QEventLoop();
        self.network.finished.connect(self.__endOfRequest)
        self.loop.exec_()
        
        if self.networkReply.error() == QNetworkReply.NoError:
            return json.loads(self.data)
        else:
            raise NetWorkErrorException(suffix="Nominatim API")

    def __endOfRequest(self,test):
        self.data = self.networkReply.readAll().data().decode('utf-8')
        self.loop.quit()
    
    def getFirstPolygonFromQuery(self,query):
        '''
        Get first OSM_ID of a Nominatim area
        @param query: Query to execute
        @type query: str
        @raise NominatimAreaException: 
        @return: First relation's osm_id
        @rtype: str
        '''
        data = self.query(query)
        for result in data:
            if result['osm_type'] == "relation":
                return result['osm_id']
        
        #If no result has been return
        raise NominatimAreaException
    
    def getFirstPointFromQuery(self,query):
        '''
        Get first longitude, latitude of a Nominatim point
        @param query: Query to execute
        @type query: str
        @raise NominatimAreaException: 
        @return: First relation's osm_id
        @rtype: str
        '''
        data = self.query(query)
        for result in data:
            if result['osm_type'] == "node":
                return result['lon'], result['lat']
        
        #If no result has been return
        raise NominatimAreaException