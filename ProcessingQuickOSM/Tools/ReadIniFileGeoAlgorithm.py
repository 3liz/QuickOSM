# -*- coding: utf-8 -*-

'''
Created on 10 juin 2014

@author: etienne
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from processing.core.Processing import Processing
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.parameters.ParameterFile import ParameterFile
from processing.outputs.OutputString import OutputString
from os.path import dirname,abspath
from QuickOSM.CoreQuickOSM.IniFile import IniFile

class ReadIniFileGeoAlgorithm(GeoAlgorithm):
    '''
    Read an INI file 
    '''
    
    def __init__(self):
        self.INI_FILE = 'QUERY_FILE'
        self.LAYERS = ['multipolygons', 'multilinestrings', 'lines', 'points']
        self.WHITE_LIST = {}
        for layer in self.LAYERS:
            self.WHITE_LIST[layer] = 'WHITE_LIST_'+layer
        GeoAlgorithm.__init__(self)

    def defineCharacteristics(self):
        self.name = "Read an ini file"
        self.group = "Tools"
        
        self.addParameter(ParameterFile(self.INI_FILE, 'Query file (ini)', False, False))
        
        for layer in self.LAYERS:
            self.addOutput(OutputString(self.WHITE_LIST[layer],'White list '+ layer +' layer'))
        
        self.addOutput(OutputString('QUERY_STRING',"Query string"))

    def help(self):
        return True, 'Help soon'
    
    '''def getIcon(self):
        return QIcon(dirname(dirname(dirname(abspath(__file__))))+"/icon.png")'''

    def processAlgorithm(self, progress):
        self.progress = progress
        self.progress.setInfo("Reading the ini file")
                
        filePath = self.getParameterValue(self.INI_FILE)
        iniFile = IniFile(filePath)
        iniDict = None
        if iniFile.isValid():
            iniDict = iniFile.getContent()

        self.setOutputValue('QUERY_STRING',iniDict['metadata']['query'])
        
        for layer in self.LAYERS:
            csv = iniDict[layer]['columns']
            self.setOutputValue(self.WHITE_LIST[layer],csv)