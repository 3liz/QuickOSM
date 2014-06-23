'''
Created on 20 juin 2014

@author: etienne
'''

from CoreQuickOSM.ConnexionXAPI import ConnexionXAPI
from CoreQuickOSM.FirstRelationIdParser import FirstRelationIdParser

if __name__ == '__main__':
    connexion = ConnexionXAPI("http://www.overpass-api.de/api/xapi?")
    req = "relation[ref:INSEE=25047]"
    osmFile = connexion.getFileFromQuery(req)
    print osmFile
    
    parser = FirstRelationIdParser(osmFile)
    print parser.parse()