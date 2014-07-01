'''
Created on 25 juin 2014

@author: etienne
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from processing.core.Processing import Processing
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.parameters.ParameterVector import ParameterVector
from processing.parameters.ParameterString import ParameterString
from processing.outputs.OutputString import OutputString
from processing.tools import dataobjects, vector
from os.path import dirname,abspath,isfile, join
from os import listdir
from QuickOSM.CoreQuickOSM.QueryFactory import QueryFactory


class GetFirstFieldGeoAlgorithm(GeoAlgorithm):
    '''
    Get first field of a vector layer 
    '''
    
    VECTOR_LAYER = 'VECTOR_LAYER'
    FIELD = 'FIELD'
    OUTPUT_VALUE = 'OUTPUT_VALUE'
        
    def defineCharacteristics(self):
        self.name = "Get first field of an attribue"
        self.group = "Tools"
        
        self.addParameter(ParameterVector(self.VECTOR_LAYER, 'Vector layer',[ParameterVector.VECTOR_TYPE_ANY], True))
        self.addParameter(ParameterString(self.FIELD, 'Field','ref:INSEE', False, False))
        
        self.addOutput(OutputString(self.OUTPUT_VALUE,"Value"))

    def help(self):
        return True, 'Help soon'
    
    '''def getIcon(self):
        return QIcon(dirname(dirname(abspath(__file__)))+"/icon.png")'''

    def processAlgorithm(self, progress):
        field = self.getParameterValue(self.FIELD)
        layer = self.getParameterValue(self.VECTOR_LAYER)
        
        print "layer getFirstField",layer
        vectorLayer = dataobjects.getObjectFromUri(layer)
        features = vector.features(vectorLayer)
        fieldIndex = vector.resolveFieldIndex(vectorLayer, field)
        
        '''HACK, need to be corrected'''
        for feature in features:
            value = unicode(feature.attributes()[fieldIndex])
            self.setOutputValue(self.OUTPUT_VALUE,value)
            break