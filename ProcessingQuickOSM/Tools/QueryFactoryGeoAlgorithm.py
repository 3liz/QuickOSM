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
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.parameters.ParameterSelection import ParameterSelection
from processing.parameters.ParameterString import ParameterString
from processing.parameters.ParameterExtent import ParameterExtent
from processing.parameters.ParameterNumber import ParameterNumber
from processing.outputs.OutputString import OutputString
from os.path import dirname,abspath,isfile, join
from os import listdir
from QuickOSM.CoreQuickOSM.QueryFactory import QueryFactory


class QueryFactoryGeoAlgorithm(GeoAlgorithm):
    '''
    Build a query with parameters 
    '''
    
    def __init__(self):
        self.FIELD_KEY = 'FIELD_KEY'
        self.FIELD_VALUE = 'FIELD_VALUE'
        self.FIELD_EXTENT = 'FIELD_EXTENT'
        self.FIELD_NOMINATIM = 'FIELD_NOMINATIM'
        self.FIELD_OSM_OBJECTS = 'FIELD_OSM_OBJECTS'
        self.FIELD_TIMEOUT = 'FIELD_TIMEOUT'
        self.OUTPUT_QUERY = 'OUTPUT_QUERY'
        GeoAlgorithm.__init__(self)
        
    def defineCharacteristics(self):
        self.name = "Query factory"
        self.group = "Tools"
        
        self.addParameter(ParameterString(self.FIELD_KEY, 'Key','ref:INSEE',optional=False))
        self.addParameter(ParameterString(self.FIELD_VALUE, 'Value','25047',optional=True))
        self.addParameter(ParameterExtent(self.FIELD_EXTENT, 'Extent',))
        self.addParameter(ParameterString(self.FIELD_NOMINATIM, 'Nominatim',optional=True))
        
        #osm_objects = ['node','way','relation','all']
        #self.addParameter(ParameterSelection(self.FIELD_OSM_OBJECTS, 'OSM objects', osm_objects, default=3))
        
        self.addParameter(ParameterNumber(self.FIELD_TIMEOUT, 'Timeout',minValue=20, default=25))        
        
        self.addOutput(OutputString(self.OUTPUT_QUERY,"Query"))

    def help(self):
        return True, 'Help soon'
    
    '''def getIcon(self):
        return QIcon(dirname(dirname(abspath(__file__)))+"/icon.png")'''

    def processAlgorithm(self, progress):
        key = self.getParameterValue(self.FIELD_KEY)
        value = self.getParameterValue(self.FIELD_VALUE)
        extent = self.getParameterValue(self.FIELD_EXTENT)
        nominatim = self.getParameterValue(self.FIELD_NOMINATIM)
        
        if nominatim == '' or nominatim == 'None':
            nominatim = None
        
        if value == '' or value =='None':
            value = None
            
        if extent == "0,1,0,1" or extent == None or extent == u"None":
            extent = None
        
        #osmObjects = self.getParameterValue(self.FIELD_OSM_OBJECTS)
        timeout = self.getParameterValue(self.FIELD_TIMEOUT)
        
        #Missing OSMObjects
        queryFactory = QueryFactory(key = key, value = value, nominatim = nominatim, bbox=extent,timeout=timeout)
        query = queryFactory.make()
        
        self.setOutputValue(self.OUTPUT_QUERY,query)