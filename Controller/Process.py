'''
Created on 17 juin 2014

@author: etienne
'''

from QuickOSM.CoreQuickOSM.QueryFactory import QueryFactory
from QuickOSM.CoreQuickOSM.API.ConnexionOAPI import ConnexionOAPI

class Process:

    '''
    @staticmethod
    def execute(query,\
                url = "http://overpass-api.de/api/",\
                layers = ['points','lines','multilinestrings','multipolygons','other_relations'],\
                whiteList = None):
        
        query = PrepareQueryOqlXml(query)
        oapi = ConnexionOAPI()
        osmFile = oapi.getFileFromQuery(query)
        parser = OsmParser(osmFile)
        layers = parser.parse()
        
        return layers
    '''
    
    @staticmethod
    def ProcessQuickQuery(self,key = None,value = None,bbox = None,nominatim = None,osmObjects = None, timeout=25):
        queryFactory = QueryFactory(key=key,value=value,bbox=bbox,nominatim=nominatim,osmObjects=osmObjects)
        query = queryFactory.make()
        
        connexionOAPI = ConnexionOAPI(output = "xml")
        
        osmFile = connexionOAPI.getFileFromQuery(query)
        
        print osmFile