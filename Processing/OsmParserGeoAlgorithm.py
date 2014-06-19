# -*- coding: utf-8 -*-

'''
Created on 10 juin 2014

@author: etienne
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import QuickOSM.resources

from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.parameters.ParameterString import ParameterString
from processing.parameters.ParameterFile import ParameterFile
from processing.outputs.OutputVector import OutputVector
from processing.tools import vector
from QuickOSM.Core.OsmParser import OsmParser


class OsmParserGeoAlgorithm(GeoAlgorithm):
    '''
    Parse an OSM file with OGR and return each layer
    '''
    
    def __init__(self):
        self.FILE = 'FILE'
        
        self.LAYERS = ['multipolygons', 'multilinestrings', 'lines', 'points']
        self.WHITE_LIST = {}
        self.OUTPUT_LAYERS = {}
        for layer in self.LAYERS:
            self.WHITE_LIST[layer] = 'WHITE_LIST_'+layer
            self.OUTPUT_LAYERS[layer] = layer + "_LAYER"
        
        GeoAlgorithm.__init__(self)

    def defineCharacteristics(self):
        self.name = "OGR default OSM parser"
        self.group = "OSM Parser"

        self.addParameter(ParameterFile(self.FILE, 'OSM file', False, False))
        
        for layer in self.LAYERS:
            self.addParameter(ParameterString(self.WHITE_LIST[layer], layer + '\'s whitelist column (csv)','', False, True))
            self.addOutput(OutputVector(self.OUTPUT_LAYERS[layer],'Output '+ layer +' layer'))

    def help(self):
        return True, QApplication.translate("QuickOSM", 'Help soon')
    
    def getIcon(self):
        return QIcon(":/resources/icon")

    def processAlgorithm(self, progress):
        
        filePath = self.getParameterValue(self.FILE)
        print filePath
        
        #Creating the dict for columns
        whiteListValues = {}
        for layer in self.LAYERS:
            value = self.getParameterValue(self.WHITE_LIST[layer])
            
            #Delete space in OSM's keys
            value = value.replace(" ","")
            
            if value != '':
                whiteListValues[layer] = value.split(',')
            else:
                whiteListValues[layer] = None
        
        #Call the OSM Parser
        parser = OsmParser(filePath, self.LAYERS, whiteListValues)
        layers = parser.parse()
        print layers
        
        layersOutputs = {}
        for key, values in layers.iteritems():
            layer = QgsVectorLayer(values['geojsonFile'],"test","ogr")
            print "tada"
            print self.OUTPUT_LAYERS[key]
            outputParameter = self.getOutputValue(self.OUTPUT_LAYERS[key])
            layersOutputs[key] = QgsVectorFileWriter(outputParameter, 'UTF-8',layer.pendingFields(),values['geomType'], layer.crs())
            for feature in layer.getFeatures():
                layersOutputs[key].addFeature(feature)