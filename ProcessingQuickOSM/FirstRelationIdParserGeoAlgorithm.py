# -*- coding: utf-8 -*-

'''
Created on 10 juin 2014

@author: etienne
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.parameters.ParameterFile import ParameterFile
from processing.outputs.OutputNumber import OutputNumber
from QuickOSM.CoreQuickOSM.FirstRelationIdParser import FirstRelationIdParser
from os.path import dirname,abspath


class FirstRelationIdParserGeoAlgorithm(GeoAlgorithm):

    OSM_FILE = 'OSM_FILE'
    OSM_ID = 'OSM_ID'

    def defineCharacteristics(self):
        self.name = "First relation ID"
        self.group = "OSM Parser"

        self.addParameter(ParameterFile(self.OSM_FILE, 'Osm file', False, False))
        self.addOutput(OutputNumber(self.OSM_ID, 'OSM id'))

    def help(self):
        return True, 'Help soon'
    
    def getIcon(self):
        return QIcon(dirname(dirname(abspath(__file__)))+"/icon.png")

    def processAlgorithm(self, progress):
        
        osmFile = self.getParameterValue(self.OSM_FILE)
        
        parser = FirstRelationIdParser(osmFile)
        try:
            osmID = parser.parse()
        except:
            raise
        self.setOutputValue("OSM_ID",osmID)