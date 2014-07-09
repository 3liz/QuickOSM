'''
Created on 4 juil. 2014

@author: etienne
'''

from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from PyQt4.QtGui import QApplication

'''
Error 10-19 - Overpass
'''
class OverpassBadRequestException(GeoAlgorithmExecutionException):
    def __init__(self, msg = QApplication.translate("Exception", u"Bad request OverpassAPI")):
        GeoAlgorithmExecutionException.__init__(self,msg)
        self.errorNumber = 10
        
class OverpassTimeoutException(GeoAlgorithmExecutionException):
    def __init__(self,msg= QApplication.translate("Exception", u"OverpassAPI timeout")):
        GeoAlgorithmExecutionException.__init__(self,msg)
        self.errorNumber = 11

'''
Error 20-29 - Nominatim
'''
class NominatimAreaException(GeoAlgorithmExecutionException):
    def __init__(self,msg= QApplication.translate("Exception", u"No nominatim area")):
        GeoAlgorithmExecutionException.__init__(self,msg)
        self.errorNumber = 20

'''
Error 30-39 - Other
'''
class DirectoryOutPutException(GeoAlgorithmExecutionException):
    def __init__(self,msg= QApplication.translate("Exception", u"The output directory does not exist.")):
        GeoAlgorithmExecutionException.__init__(self,msg)
        self.errorNumber = 30
        
class FileOutPutException(GeoAlgorithmExecutionException):
    def __init__(self,msg= QApplication.translate("Exception", u"The output file already exist, set a prefix"), suffix=None):
        if suffix:
            msg = msg + " " + suffix
        GeoAlgorithmExecutionException.__init__(self,msg)
        self.errorNumber = 31
        
class OutPutFormatException(GeoAlgorithmExecutionException):
    def __init__(self,msg= QApplication.translate("Exception", u"Output not available")):
        GeoAlgorithmExecutionException.__init__(self,msg)
        self.errorNumber = 32

class Ogr2OgrException(GeoAlgorithmExecutionException):
    def __init__(self,msg= QApplication.translate("Exception", u"Error with ogr2ogr")):
        GeoAlgorithmExecutionException.__init__(self,msg)
        self.errorNumber = 33