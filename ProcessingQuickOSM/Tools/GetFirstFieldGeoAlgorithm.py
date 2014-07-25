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
from processing.parameters.ParameterVector import ParameterVector
from processing.parameters.ParameterString import ParameterString
from processing.outputs.OutputString import OutputString
from processing.tools import dataobjects, vector
from os.path import isfile
from os import listdir
from QuickOSM import resources_rc
from QuickOSM.CoreQuickOSM.QueryFactory import QueryFactory


class GetFirstFieldGeoAlgorithm(GeoAlgorithm):
    '''
    Get first field of a vector layer 
    '''
    
    VECTOR_LAYER = 'VECTOR_LAYER'
    FIELD = 'FIELD'
    OUTPUT_VALUE = 'OUTPUT_VALUE'
        
    def defineCharacteristics(self):
        self.name = "Get first field of an attribute"
        self.group = "Tools"
        
        self.addParameter(ParameterVector(self.VECTOR_LAYER, 'Vector layer',[ParameterVector.VECTOR_TYPE_ANY], True))
        self.addParameter(ParameterString(self.FIELD, 'Field','ref:INSEE', False, False))
        
        self.addOutput(OutputString(self.OUTPUT_VALUE,"Value"))

    def help(self):
        if isfile(__file__+".html"):
            return False, __file__+".html"
        return False, None
    
    def getIcon(self):
        return QIcon(":/plugins/QuickOSM/icon.png")

    def processAlgorithm(self, progress):
        field = self.getParameterValue(self.FIELD)
        layer = self.getParameterValue(self.VECTOR_LAYER)
        
        vectorLayer = dataobjects.getObjectFromUri(layer)
        features = vector.features(vectorLayer)
        fieldIndex = vector.resolveFieldIndex(vectorLayer, field)
        
        '''HACK, need to be corrected'''
        for feature in features:
            value = unicode(feature.attributes()[fieldIndex])
            self.setOutputValue(self.OUTPUT_VALUE,value)
            break