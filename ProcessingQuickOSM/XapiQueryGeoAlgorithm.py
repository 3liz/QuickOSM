# -*- coding: utf-8 -*-

'''
Created on 10 juin 2014

@author: etienne
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import QgsMapCanvas
from qgis.core import *
from qgis.utils import iface

from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.parameters.ParameterExtent import ParameterExtent
from processing.parameters.ParameterString import ParameterString
from processing.outputs.OutputFile import OutputFile
from QuickOSM.CoreQuickOSM.ConnexionXAPI import ConnexionXAPI
from os.path import dirname,abspath


class XapiQueryGeoAlgorithm(GeoAlgorithm):
    '''
    Perform an OverPass query and get an OSM file
    '''

    SERVER = 'SERVER'
    QUERY_STRING = 'QUERY'
    OUTPUT_FILE = 'OUTPUT_FILE'

    def defineCharacteristics(self):
        self.name = "Query XAPI with a string"
        self.group = "API"

        self.addParameter(ParameterString(self.SERVER, 'XAPI','http://www.overpass-api.de/api/xapi?', False, False))
        self.addParameter(ParameterString(self.QUERY_STRING,'Query', 'relation[ref:INSEE=25047]', False,False))
        
        self.addOutput(OutputFile(self.OUTPUT_FILE,'OSM file'))

    def help(self):
        return True, 'Help soon'
    
    def getIcon(self):
        return QIcon(dirname(dirname(abspath(__file__)))+"/icon.png")

    def processAlgorithm(self, progress):
        
        server = self.getParameterValue(self.SERVER)
        query = self.getParameterValue(self.QUERY_STRING)
        
        xapi = ConnexionXAPI(url=server)
        osmFile = xapi.getFileFromQuery(query)
        
        print osmFile
        #Set the output file for Processing
        self.setOutputValue(self.OUTPUT_FILE,osmFile)
        