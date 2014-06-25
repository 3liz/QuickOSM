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
from processing.parameters.ParameterSelection import ParameterSelection
from processing.outputs.OutputString import OutputString
from os.path import dirname,abspath,isfile, join
from os import listdir
from QuickOSM.CoreQuickOSM.IniFile import IniFile


class ListIniFilesGeoAlgorithm(GeoAlgorithm):
    '''
    List all the INI files 
    '''
    
    def __init__(self):
        self.NAME_FILE = 'NAME'
        self.OUTPUT_INI = 'INI'
        GeoAlgorithm.__init__(self)
        
    def defineCharacteristics(self):
        self.name = "Queries available"
        self.group = "Tools"
        
        folder = join(dirname(dirname(dirname(abspath(__file__)))),"queries")
        self.__files = IniFile.getNamesAndPathsFromFolder(folder)
        names = [ f['name'] for f in self.__files]
        
        self.addParameter(ParameterSelection(self.NAME_FILE, 'Queries available', names))
        
        self.addOutput(OutputString(self.OUTPUT_INI,"Ini filepath as string"))

    def help(self):
        return True, 'Help soon'
    
    '''def getIcon(self):
        return QIcon(dirname(dirname(abspath(__file__)))+"/icon.png")'''

    def processAlgorithm(self, progress):
        index = self.getParameterValue(self.NAME_FILE)
        ini = self.__files[index]
        self.setOutputValue(self.OUTPUT_INI,ini['path'])