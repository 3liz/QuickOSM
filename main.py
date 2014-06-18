# -*- coding: utf-8 -*-

'''
Created on 10 juin 2014

@author: etienne
'''
from qgis.core import QgsApplication,QgsProviderRegistry

from Core.Process import execute

if __name__ == '__main__':
    
    QgsApplication.setPrefixPath('/usr', True)  
    QgsApplication.initQgis()
    print QgsApplication.showSettings()
    providers = QgsProviderRegistry.instance().providerList()
    for provider in providers:
        print provider
    
    #req = '[out:json];area(3600028722)->.area;(node["amenity"="school"](area.area);way["amenity"="school"](area.area);relation["amenity"="school"](area.area););out body;>;out skel qt;'

    req = '<osm-script output="json" timeout="25"> \
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
</osm-script>'
    print req
    
    whiteList = {}
    whiteList['points'] = None
    whiteList['lines'] = None
    whiteList['multilinestrings'] = None
    whiteList['multipolygons'] = ('wikipedia')
    whiteList['other_relations'] = None

    layers = execute(req,"http://overpass-api.de/api/interpreter",['points','lines','multilinestrings','multipolygons','other_relations'],whiteList)
    
    for key, values in layers.iteritems() :
        print key
        for value in values.iteritems():
            print "    " + str(value)

    QgsApplication.exitQgis()