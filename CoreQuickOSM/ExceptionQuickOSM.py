'''
Created on 4 juil. 2014

@author: etienne
'''

from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException

class QuickOsmException(GeoAlgorithmExecutionException):
    def __init__(self,msg):
        GeoAlgorithmExecutionException.__init__(self,msg)

class DirectoryException(Exception):
    def __init__(self, msg):
        QuickOsmException.__init__(self,msg)