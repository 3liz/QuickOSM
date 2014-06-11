# -*- coding: utf-8 -*-

'''
Created on 10 juin 2014

@author: etienne
'''

from processing.core.AlgorithmProvider import AlgorithmProvider
from processing.core.ProcessingConfig import Setting, ProcessingConfig
from OverpassQueryGeoAlgorithm import OverpassQueryGeoAlgorithm
from PyQt4.QtGui import QIcon
import resources

class QuickOSMAlgorithmProvider(AlgorithmProvider):

    def __init__(self):
        AlgorithmProvider.__init__(self)

        self.activate = True

        # Load algorithms
        self.alglist = [OverpassQueryGeoAlgorithm()]
        for alg in self.alglist:
            alg.provider = self

    def initializeSettings(self):
        AlgorithmProvider.initializeSettings(self)

    def unload(self):
        AlgorithmProvider.unload(self)

    def getName(self):
        return 'QuickOSM'

    def getDescription(self):
        return 'QuickOSM'

    def getIcon(self):
        return QIcon(":/resources/icon")
    
    def _loadAlgorithms(self):
        self.algs = self.alglist
