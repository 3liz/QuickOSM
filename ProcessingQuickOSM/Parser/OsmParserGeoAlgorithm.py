# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
                             -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info at 3liz dot com
        contributor          : Etienne Trimaille
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.parameters.ParameterString import ParameterString
from processing.parameters.ParameterFile import ParameterFile
from processing.outputs.OutputVector import OutputVector
from processing.tools import vector
from QuickOSM.CoreQuickOSM.Parser.OsmParser import OsmParser
from os.path import dirname,abspath
import re



class OsmParserGeoAlgorithm(GeoAlgorithm):
    '''
    Parse an OSM file with OGR and return each layer
    '''
    
    def __init__(self):
        self.slotOsmParser = SLOT("osmParser()")
        
        self.FILE = 'FILE'
        
        self.LAYERS = ['multipolygons', 'multilinestrings', 'lines', 'points']
        self.WHITE_LIST = {}
        self.OUTPUT_LAYERS = {}
        for layer in self.LAYERS:
            self.WHITE_LIST[layer] = 'WHITE_LIST_'+layer
            self.OUTPUT_LAYERS[layer] = layer + "_LAYER"
        
        GeoAlgorithm.__init__(self)

    def defineCharacteristics(self):
        self.name = "OGR default"
        self.group = "OSM Parser"

        self.addParameter(ParameterFile(self.FILE, 'OSM file', False, False))
        
        for layer in self.LAYERS:
            self.addParameter(ParameterString(self.WHITE_LIST[layer], layer + '\'s whitelist column (csv)','', False, True))
            self.addOutput(OutputVector(self.OUTPUT_LAYERS[layer],'Output '+ layer +' layer'))

    def help(self):
        return True, 'Help soon'
    
    '''def getIcon(self):
        return QIcon(dirname(dirname(dirname(abspath(__file__))))+"/icon.png")'''

    def processAlgorithm(self, progress):
        self.progress = progress
        self.progress.setPercentage(0)
        
        filePath = self.getParameterValue(self.FILE)
        print filePath
        
        #Creating the dict for columns
        whiteListValues = {}
        for layer in self.LAYERS:
            value = self.getParameterValue(self.WHITE_LIST[layer])
            
            #Delete space and tabs in OSM's keys
            #Processing return a 'None' value as unicode
            value = re.sub ('\s', '', value)
            if value == '' or value == 'None':
                value = None
            
            if value:
                if value != ',':
                    whiteListValues[layer] = value.split(',')
                else:
                    whiteListValues[layer] = ','
            else:
                whiteListValues[layer] = None
        
        #Call the OSM Parser and connect signals
        parser = OsmParser(filePath, self.LAYERS, whiteListValues)
        parser.signalText.connect(self.setInfo)
        parser.signalPercentage.connect(self.setPercentage)
        
        #Start to parse
        layers = parser.parse()
        print layers
        
        layersOutputs = {}
        for key, values in layers.iteritems():
            layer = QgsVectorLayer(values['geojsonFile'],"test","ogr")
            outputParameter = self.getOutputValue(self.OUTPUT_LAYERS[key])
            layersOutputs[key] = QgsVectorFileWriter(outputParameter, 'UTF-8',layer.pendingFields(),values['geomType'], layer.crs())
            for feature in layer.getFeatures():
                layersOutputs[key].addFeature(feature)
                
    def setInfo(self,text):
        self.progress.setInfo(text)
    
    def setPercentage(self,percent):
        self.progress.setPercentage(percent)