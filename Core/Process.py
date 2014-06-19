'''
Created on 17 juin 2014

@author: etienne
'''


from Core.OsmParser import OsmParser
from Core.ConnexionOAPI import ConnexionOAPI
from Core.PrepareQuery import PrepareQuery

def execute(query,\
            url = "http://overpass-api.de/api/",\
            layers = ['points','lines','multilinestrings','multipolygons','other_relations'],\
            whiteList = None):
    '''
    Process which takes all the GUI's options and execute the process
    '''
    
    query = PrepareQuery(query)
    oapi = ConnexionOAPI()
    osmFile = oapi.getFileFromQuery(query)
    parser = OsmParser(osmFile)
    layers = parser.parse()
    
    return layers