'''
Created on 11 juin 2014

@author: etienne
'''

import urllib
import urllib2
import json

class Nominatim:
    
    def __init__(self, url = "http://nominatim.openstreetmap.org/search?format=json"):
        self.__url = url
        
        
    def query(self, query):

        params = { 'q': query }
        params['polygon_geojson'] = 0
        url = self.__url + "&" +  urllib.urlencode(params)
        data = urllib2.urlopen(url)
        response = data.read()
        return json.loads(response)
    
    def getFirstPolygonFromQuery(self,query):
        data = self.query(query)
        for result in data:
            if result['osm_type'] == "relation":
                return result['osm_id']