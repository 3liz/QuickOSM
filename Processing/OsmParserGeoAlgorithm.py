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
        self.name = "Parse an OSM file"
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
        
        whiteListValues = {}
        for layer in self.LAYERS:
            value = self.getParameterValue(self.WHITE_LIST[layer])
            value = value.replace(" ","")
            if value != '':
                whiteListValues[layer] = value.split(',')
            else:
                whiteListValues[layer] = None
        
        parser = OsmParser(filePath, self.LAYERS, whiteListValues)
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