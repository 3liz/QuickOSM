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
import ConfigParser
from os.path import dirname,abspath,join
import ntpath
from macpath import basename
from genericpath import isfile

class ReadIniFileGeoAlgorithm(GeoAlgorithm):
    '''
    Read an INI file 
    '''
    
    def __ConfigSectionMap(self,section):
        iniDict = {}
        for option in self.configParser.options(section):
            try:
                iniDict[option] = self.configParser.get(section, option)
            except:
                iniDict[option] = None
        return iniDict
    
    def __init__(self):
        self.INI_FILE = 'QUERY_FILE'
        self.LAYERS = ['multipolygons', 'multilinestrings', 'lines', 'points']
        self.WHITE_LIST = {}
        for layer in self.LAYERS:
            self.WHITE_LIST[layer] = 'WHITE_LIST_'+layer
        GeoAlgorithm.__init__(self)

    def defineCharacteristics(self):
        self.name = "Read an ini file"
        self.group = "API"
        
        self.addParameter(ParameterFile(self.INI_FILE, 'Query file (ini)', False, False))
        
        for layer in self.LAYERS:
            self.addOutput(OutputString(self.WHITE_LIST[layer],'White list '+ layer +' layer'))
        
        self.addOutput(OutputString('QUERY_STRING',"Query string"))

    def help(self):
        return True, 'Help soon'
    
    def getIcon(self):
        return QIcon(dirname(dirname(abspath(__file__)))+"/icon.png")

    def processAlgorithm(self, progress):
        self.configParser = ConfigParser.ConfigParser()
        
        filePath = self.getParameterValue(self.INI_FILE)
        tab = (ntpath.basename(filePath)).split('.')
        
        if tab[1] != "ini":
            raise GeoAlgorithmExecutionException, "Not an ini file"
        
        directory = dirname(filePath)
        
        queryFile = [join(directory, tab[0] + '.' + ext) for ext in ['oql','xml'] if isfile(join(directory, tab[0] + '.' + ext))]
        try:
            queryFile = queryFile[0]
        except IndexError:
            raise GeoAlgorithmExecutionException, "No query file (.xml or .oql)"
        
        query = open(queryFile, 'r').read()
        self.setOutputValue('QUERY_STRING',query)
        
        self.configParser.read(filePath)
        for layer in self.LAYERS:
            csv = self.__ConfigSectionMap(layer)['columns']
            self.setOutputValue(self.WHITE_LIST[layer],csv)