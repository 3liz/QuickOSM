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

#from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
import urllib2
import tempfile

class ConnexionXAPI:
    '''
    Manage connexion to the eXtend API (XAPI)
    '''

    def __init__(self,url="api.openstreetmap.fr/xapi?"):
        self.__url = url
        
    def query(self,req):
        '''
        Make a query to the xapi
        '''
        req = req.encode('utf8')
        urlQuery = self.__url + req
        
        print urlQuery
        try:
            data = urllib2.urlopen(url=urlQuery).read()
        except urllib2.HTTPError as e:
            if e.code == 400:
                raise Exception
                #raise GeoAlgorithmExecutionException, "Bad request XAPI"
        
        return data

            
    def getFileFromQuery(self,req):
        '''
        Make a query to the overpass and put the result in a temp file
        '''
        req = self.query(req)
        tf = tempfile.NamedTemporaryFile(delete=False,suffix=".osm")
        tf.write(req)
        namefile = tf.name
        tf.flush()
        tf.close()
        return namefile