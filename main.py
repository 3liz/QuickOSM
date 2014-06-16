# -*- coding: utf-8 -*-

'''
Created on 10 juin 2014

@author: etienne
'''
from qgis.core import QgsApplication
from QueryOverpass.connexion_OAPI import ConnexionOAPI
from QueryOverpass.osm_parser import OsmParser
from QueryOverpass.Nominatim import Nominatim

if __name__ == '__main__':
    
    QgsApplication.setPrefixPath('/usr', True)  
    QgsApplication.initQgis()
    
    layers = ['points','lines','multilinestrings','multipolygons','other_relations']
    
    #nominatim = Nominatim()
    #print nominatim.getFirstPolygonFromQuery("Baume les dames")
    
    
    #oapi = ConnexionOAPI(url="http://overpass-api.de/api/interpreter",output="xml")
    #req = '[out:json];area(3600028722)->.area;(node["amenity"="school"](area.area);way["amenity"="school"](area.area);relation["amenity"="school"](area.area););out body;>;out skel qt;'
    
    #osmFile = oapi.getFileFromQuery(req)
    #print req
    osmFile = "/home/etienne/.qgis2/python/plugins/QuickOSM/data_test/limite_baume_josm.osm"
    print osmFile
    
    whiteList = {}
    whiteList['points'] = None
    whiteList['lines'] = None
    whiteList['multilinestrings'] = None
    whiteList['multipolygons'] = ('wikipedia')
    whiteList['other_relations'] = None
    
    parser = OsmParser(osmFile)
    layers = parser.parse()
    
    for key, values in layers.iteritems() :
        print key
        for value in values.iteritems():
            print "    " + str(value)
            
    
    QgsApplication.exitQgis()