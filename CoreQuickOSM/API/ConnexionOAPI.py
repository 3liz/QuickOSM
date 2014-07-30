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

import urllib2
import urllib
import re
import tempfile

class ConnexionOAPI:
    '''
    Manage connexion to the overpass API
    '''

    def __init__(self,url="http://overpass-api.de/api/", output = None):
        '''
        Constructor
        @param url:URL of OverPass
        @type url:str
        @param output:Output desired (XML or JSON)
        @type output:str
        '''
        
        if not url:
            url="http://overpass-api.de/api/"
            
        self.__url = url

        if output not in (None, "json","xml"):
            raise OutPutFormatException
        self.__output = output
        
    def query(self,req):
        '''
        Make a query to the overpass
        @param req:Query to execute
        @type req:str
        @raise OverpassBadRequestException,NetWorkErrorException,OverpassTimeoutException
        @return: the result of the query
        @rtype: str
        '''
        req = req.encode('utf8')
        urlQuery = self.__url + 'interpreter'
        
        #The output format can be forced (JSON or XML)
        if self.__output:
            req = re.sub(r'output="[a-z]*"','output="'+self.__output+'"', req)
            req = re.sub(r'\[out:[a-z]*','[out:'+self.__output, req)
        
        queryString = urllib.urlencode({'data':req})
        
        try:
            data = urllib2.urlopen(url=urlQuery, data=queryString).read()
        except urllib2.HTTPError as e:
            if e.code == 400:
                raise OverpassBadRequestException
            else:
                raise NetWorkErrorException(suffix="Overpass API")
        except urllib2.URLError as e:
            raise NetWorkErrorException(suffix="Overpass API")

        result = re.search('<remark> runtime error: Query timed out in "[a-z]+" at line [\d]+ after ([\d]+) seconds. </remark>', data)
        if result:
            result = result.groups()
            raise OverpassTimeoutException
            
        return data
            
    def getFileFromQuery(self,req):
        '''
        Make a query to the overpass and put the result in a temp file
        @param req:Query to execute
        @type req:str
        @return: temporary filepath
        @rtype: str
        '''
        req = self.query(req)
        tf = tempfile.NamedTemporaryFile(delete=False,suffix=".osm")
        tf.write(req)
        namefile = tf.name
        tf.flush()
        tf.close()
        return namefile
    
    def getTimestamp(self):
        '''
        Get the timestamp of the OSM data on the server
        @return: Timestamp
        @rtype: str
        '''
        urlQuery = self.__url + 'timestamp'
        try:
            return urllib2.urlopen(url=urlQuery).read()
        except urllib2.HTTPError as e:
            if e.code == 400:
                raise OverpassBadRequestException
            
    def isValid(self):
        '''
        Try if the url is valid, NOT TESTED YET
        '''
        urlQuery = self.__url + 'interpreter'
        try:
            urllib2.urlopen(url=urlQuery)
            return True
        except urllib2.HTTPError:
            return False