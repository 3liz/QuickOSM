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
from processing.outputs.OutputNumber import OutputNumber
from QuickOSM.Core.Nominatim import Nominatim


class NominatimQueryGeoAlgorithm(GeoAlgorithm):

    NOMINATIM_STRING = 'NOMINATIM_STRING'
    OSM_ID = 'OSM_ID'

    def defineCharacteristics(self):
        self.name = "Query nominatim API with a string"
        self.group = "Query nominatim API"

        self.addParameter(ParameterString(self.NOMINATIM_STRING, 'Search','Montpellier', False, False))
        self.addOutput(OutputNumber(self.OSM_ID))


    def help(self):
        return True, QApplication.translate("QuickOSM", 'Help soon')
    
    def getIcon(self):
        return QIcon(":/resources/icon")

    def processAlgorithm(self, progress):
        
        query = self.getParameterValue(self.NOMINATIM_STRING)
        
        nominatim = Nominatim()
        osmID = nominatim.getFirstPolygonFromQuery(query)
        self.setOutputValue("OSM_ID",osmID)
        print self.getOutputValue("OSM_ID")
        