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

from QuickOSM.CoreQuickOSM.ExceptionQuickOSM import NominatimAreaException,NetWorkErrorException

import urllib
import urllib2
import json

class Nominatim:
    
    def __init__(self, url = "http://nominatim.openstreetmap.org/search?format=json"):
        self.__url = url
        
    def query(self, query):
        '''
        Perform a nominatim query
        '''
        query = query.encode('utf8')
        params = { 'q': query }
        params['polygon_geojson'] = 0
        url = self.__url + "&" +  urllib.urlencode(params)
        try:
            data = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            raise NetWorkErrorException(suffix="Nominatim API")    
        response = data.read()
        return json.loads(response)
    
    def getFirstPolygonFromQuery(self,query):
        '''
        Get first OSM_ID of a Nominatim area
        '''
        data = self.query(query)
        for result in data:
            if result['osm_type'] == "relation":
                return result['osm_id']
        
        #If no result has been return
        raise NominatimAreaException