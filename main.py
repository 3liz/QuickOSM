# -*- coding: utf-8 -*-

'''
Created on 10 juin 2014

@author: etienne
'''
from qgis.core import QgsApplication
from QueryOverpass.connexion_OAPI import ConnexionOAPI
from QueryOverpass.osm_parser import OsmParser
from QueryOverpass.QueryParser import *

if __name__ == '__main__':
    
    QgsApplication.setPrefixPath('/usr', True)  
    QgsApplication.initQgis()
    
    layers = ['points','lines','multilinestrings','multipolygons','other_relations']
    
    
    oapi = ConnexionOAPI(url="http://overpass-api.de/api/interpreter",output="xml")
    req = '"<osm-script output="json" timeout="25"> \
  <id-query {{nominatimArea:Baume les dames}} into="area"/> \
  <union> \
    <query type="node">\
      <has-kv k="shop" v="supermarket"/>\
      <area-query from="area"/>\
    </query>\
    <query type="way">\
      <has-kv k="shop" v="supermarket"/>\
      <area-query from="area"/>\
    </query>\
    <query type="relation">\
      <has-kv k="shop" v="supermarket"/>\
      <area-query from="area"/>\
    </query>\
  </union>\
  <print mode="body"/>\
  <recurse type="down"/>\
  <print mode="skeleton" order="quadtile"/>\
</osm-script>"'
    print req
    query = queryParser(req)
    osmFile = oapi.getFileFromQuery(query)
    
    
    #req = '[out:json];area(3600028722)->.area;(node["amenity"="school"](area.area);way["amenity"="school"](area.area);relation["amenity"="school"](area.area););out body;>;out skel qt;'
    
    #osmFile = oapi.getFileFromQuery(req)
    #print req
    """
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
            
    """
    QgsApplication.exitQgis()