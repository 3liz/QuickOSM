'''
Created on 17 juin 2014

@author: etienne
'''


from CoreQuickOSM.Parser.OsmParser import OsmParser
from CoreQuickOSM.API.ConnexionOAPI import ConnexionOAPI
from CoreQuickOSM.Tools import PrepareQueryOqlXml

def execute(query,\
            url = "http://overpass-api.de/api/",\
            layers = ['points','lines','multilinestrings','multipolygons','other_relations'],\
            whiteList = None):
    '''
    Process which takes all the GUI's options and execute the process
    '''
    
    query = PrepareQueryOqlXml(query)
    oapi = ConnexionOAPI()
    osmFile = oapi.getFileFromQuery(query)
    parser = OsmParser(osmFile)
    layers = parser.parse()
    
    return layers