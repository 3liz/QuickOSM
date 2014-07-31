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
import urllib2
import tempfile

class ConnexionXAPI:
    '''
    Manage connexion to the eXtend API (XAPI)
    '''

    def __init__(self,url="api.openstreetmap.fr/xapi?"):
        '''
        Constructor
        @param url:URL of OverPass
        @type url:str
        '''

        self.__url = url
        
    def query(self,req):
        '''
        Make a query to the xapi
        @param req:Query to execute
        @type req:str
        @raise Exception : Bad, should be a ExceptionQuickOSM
        @return: the result of the query
        @rtype: str
        '''
        req = req.encode('utf8')
        urlQuery = self.__url + req
        
        try:
            data = urllib2.urlopen(url=urlQuery).read()
        except urllib2.HTTPError as e:
            raise NetWorkErrorException(suffix="XAPI")   
        except urllib2.URLError as e:
            raise NetWorkErrorException(suffix="XAPI")
        
        return data

            
    def getFileFromQuery(self,req):
        '''
        Make a query to the xapi and put the result in a temp file
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