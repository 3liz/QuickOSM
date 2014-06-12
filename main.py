# -*- coding: utf-8 -*-

'''
Created on 10 juin 2014

@author: etienne
'''

from QueryOverpass.connexion_OAPI import ConnexionOAPI
from QueryOverpass.osm_parser import OsmParser
from QueryOverpass.Nominatim import Nominatim

if __name__ == '__main__':
    
    
    
    #nominatim = Nominatim()
    #print nominatim.getFirstPolygonFromQuery("Baume les dames")
    
    
    oapi = ConnexionOAPI(url="http://overpass-api.de/api/interpreter",output="xml")
    req = '[out:json];area(3600028722)->.area;(node["amenity"="school"](area.area);way["amenity"="school"](area.area);relation["amenity"="school"](area.area););out body;>;out skel qt;'
    
    osmFile = oapi.getFileFromQuery(req)
    print req
    print osmFile
    
    parser = OsmParser("/home/etienne/addr.osm")
    layers = parser.parse()
    
    for key, values in layers.iteritems() :
        print key
        for value in values.iteritems():
            print "    " + str(value)