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


class OverpassQueryGeoAlgorithm(GeoAlgorithm):

    SERVER = 'SERVER'
    QUERY_STRING = 'QUERY_STRING'
    POINT_LAYER = 'POINT_LAYER'
    LINESTRING_LAYER = 'LINESTRING_LAYER'
    MULTILINESTRING_LAYER = 'MULTILINESTRING_LAYER'
    MULTIPOLYGON_LAYER = 'MULTIPOLYGON_LAYER'

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

        self.addOutput(OutputVector(self.POINT_LAYER,'Output point layer'))
        self.addOutput(OutputVector(self.LINESTRING_LAYER,'Output linestring layer'))
        self.addOutput(OutputVector(self.MULTILINESTRING_LAYER,'Output multilinestring layer'))
        self.addOutput(OutputVector(self.MULTIPOLYGON_LAYER,'Output multipolygon layer'))

    def help(self):
        return True, QApplication.translate("QuickOSM", 'Help soon')
    
    def getIcon(self):
        return QIcon(":/resources/icon")

    def processAlgorithm(self, progress):
        
        server = self.getParameterValue(self.SERVER)
        query = self.getParameterValue(self.QUERY_STRING)
        
        oapi = ConnexionOAPI(url=server,output="xml")
        osmFile = oapi.getFileFromQuery(query)
        parser = OsmParser(osmFile)
        layers = parser.parse()
        
        outputs = {}
        outputs['points'] = self.getOutputValue(self.POINT_LAYER)
        outputs['lines'] = self.getOutputValue(self.LINESTRING_LAYER)
        outputs['multilinestrings'] = self.getOutputValue(self.MULTILINESTRING_LAYER)
        outputs['multipolygons'] = self.getOutputValue(self.MULTIPOLYGON_LAYER)
        
        layersOutputs = {}
        for key, values in layers.iteritems():
            if key != "other_relations":
                layer = QgsVectorLayer(values['geojsonFile'],"test","ogr")
                layersOutputs[key] = QgsVectorFileWriter(outputs[key], 'UTF-8',layer.pendingFields(),values['geomType'], layer.crs())
                for feature in layer.getFeatures():
                    layersOutputs[key].addFeature(feature)