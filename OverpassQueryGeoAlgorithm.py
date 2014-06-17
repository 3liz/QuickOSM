# -*- coding: utf-8 -*-

'''
Created on 10 juin 2014

@author: etienne
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import resources

from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.parameters.ParameterString import ParameterString
from processing.outputs.OutputVector import OutputVector
from processing.outputs.OutputHTML import OutputHTML
from processing.tools import vector
from QueryOverpass.connexion_OAPI import ConnexionOAPI
from QueryOverpass.osm_parser import OsmParser
from QueryOverpass.QueryParser import queryParser


class OverpassQueryGeoAlgorithm(GeoAlgorithm):

    def __init__(self):
        self.SERVER = 'SERVER'
        self.QUERY_STRING = 'QUERY_STRING'
        
        self.LAYERS = ['multipolygons', 'multilinestrings', 'lines', 'points']
        self.WHITE_LIST = {}
        self.OUTPUT_LAYERS = {}
        for layer in self.LAYERS:
            self.WHITE_LIST[layer] = 'WHITE_LIST_'+layer
            self.OUTPUT_LAYERS[layer] = layer + "_LAYER"
        
        GeoAlgorithm.__init__(self)

    def defineCharacteristics(self):
        self.name = "Query overpass API with a string"
        self.group = "Query overpass API"

        self.addParameter(ParameterString(self.SERVER, 'Overpass API','http://overpass-api.de/api/interpreter', False, False))
        self.addParameter(ParameterString(self.QUERY_STRING,'Query (XML or OQL)', '<osm-script output="json">\n \
              <id-query into="area" ref="3600028722" type="area"/>\n \
              <union into="_">\n \
                <query into="_" type="node">\n \
                  <has-kv k="amenity" modv="" v="school"/>\n \
                  <area-query from="area" into="_" ref=""/>\n \
                </query>\n \
                <query into="_" type="way">\n \
                  <has-kv k="amenity" modv="" v="school"/>\n \
                  <area-query from="area" into="_" ref=""/>\n \
                </query>\n \
                <query into="_" type="relation">\n \
                  <has-kv k="amenity" modv="" v="school"/>\n \
                  <area-query from="area" into="_" ref=""/>\n \
                </query>\n \
              </union>\n \
              <print from="_" limit="" mode="body" order="id"/>\n \
              <recurse from="_" into="_" type="down"/>\n \
              <print from="_" limit="" mode="skeleton" order="quadtile"/>\n \
            </osm-script>', True,False))
        
        for layer in self.LAYERS:
            self.addParameter(ParameterString(self.WHITE_LIST[layer], layer + '\'s whitelist column (csv)','', False, True))
            self.addOutput(OutputVector(self.OUTPUT_LAYERS[layer],'Output '+ layer +' layer'))


    def help(self):
        return True, QApplication.translate("QuickOSM", 'Help soon')
    
    def getIcon(self):
        return QIcon(":/resources/icon")

    def processAlgorithm(self, progress):
        
        server = self.getParameterValue(self.SERVER)
        query = self.getParameterValue(self.QUERY_STRING)
        
        whiteListValues = {}
        for layer in self.LAYERS:
            value = self.getParameterValue(self.WHITE_LIST[layer])
            value = value.replace(" ","")
            if value != '':
                whiteListValues[layer] = value.split(',')
            else:
                whiteListValues[layer] = None
        
        query = queryParser(query)
        
        oapi = ConnexionOAPI(url=server,output="xml")
        osmFile = oapi.getFileFromQuery(query)
        print osmFile
        parser = OsmParser(osmFile, self.LAYERS, whiteListValues)
        layers = parser.parse()
        print layers
        outputs = {}
        for layer in self.LAYERS:
            outputs[layer] = self.getOutputValue(self.OUTPUT_LAYERS[layer])
        
        layersOutputs = {}
        for key, values in layers.iteritems():
            layer = QgsVectorLayer(values['geojsonFile'],"test","ogr")
            layersOutputs[key] = QgsVectorFileWriter(outputs[key], 'UTF-8',layer.pendingFields(),values['geomType'], layer.crs())
            for feature in layer.getFeatures():
                layersOutputs[key].addFeature(feature)