'''
Created on 16 juin 2014

@author: etienne
'''
import unittest
from qgis.core import QgsApplication
from QueryOverpass.connexion_OAPI import ConnexionOAPI
from QueryOverpass.osm_parser import OsmParser


class initConnexionTest(unittest.TestCase):
    def setUp(self):
        QgsApplication.setPrefixPath('/usr', True)  
        QgsApplication.initQgis()
        self.connexion = ConnexionOAPI(url="http://overpass-api.de/api/interpreter",output="xml")
        self.req = '[out:json];area(3600028722)->.area;(node["amenity"="school"](area.area);way["amenity"="school"](area.area);relation["amenity"="school"](area.area););out body;>;out skel qt;'


class TestQueryConnexion(initConnexionTest):

    def testConnexionOAPI(self):
        data = self.connexion.query(self.req)
        assert len(data) > 100000,'not enough data in overpass query'
        
    def testParserPoints(self):

        parseur = OsmParser("data_test/limite_baume_josm.osm")
        result = parseur.parse()
        assert result['multipolygons']['featureCount'] == 1
        


if __name__ == "__main__":
    
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()
    #QgsApplication.exitQgis()