'''
Created on 11 juin 2014

@author: etienne
'''

from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException

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
        params = { 'q': query }
        params['polygon_geojson'] = 0
        url = self.__url + "&" +  urllib.urlencode(params)
        data = urllib2.urlopen(url)
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
        raise GeoAlgorithmExecutionException, "No nominatim area"