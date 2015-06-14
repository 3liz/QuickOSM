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

from QuickOSM import *
from QuickOSM.ProcessingQuickOSM import *

from operating_system.path import isfile,join,basename,dirname,abspath

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
        self.addParameter(ParameterString(self.FIELD, 'Field','', False, False))
        
        self.addOutput(OutputString(self.OUTPUT_VALUE,"Value"))

    def help(self):
        locale = QSettings().value("locale/userLocale")[0:2]
        locale += "."

        current_file = __file__
        if current_file.endswith('pyc'):
            current_file = current_file[:-1]
        current_file = basename(current_file)

        helps = [current_file + locale + ".html", current_file + ".html"]

        doc_path = join(dirname(dirname(dirname(abspath(__file__)))), 'doc')
        for helpFileName in helps:
            file_help_path = join(doc_path, helpFileName)
            if isfile(file_help_path):
                return False, file_help_path
        
        return False, None
    
    def getIcon(self):
        return QIcon(dirname(__file__) + '/../../icon.png')

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