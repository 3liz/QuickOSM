# -*- coding: utf-8 -*-

'''
Created on 10 juin 2014

@author: etienne
'''

from connexion_OAPI import ConnexionOAPI
from osm_parser import OsmParser

if __name__ == '__main__':
    
    oapi = ConnexionOAPI(url="http://overpass-api.de/api/interpreter",output="xml")
    req = '[out:json];way(around:300.0,44.0,8.0)["highway"];(._;node(w););out;'
    osmFile = oapi.getFileFromQuery(req)
    print req
    print osmFile
    
    parser = OsmParser(osmFile)
    layers = parser.parse()
    
    for key, values in layers.iteritems() :
        print key
        for value in values.iteritems():
            print "    " + str(value)