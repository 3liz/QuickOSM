'''
Created on 17 juin 2014

@author: etienne
'''

from QuickOSM.CoreQuickOSM.QueryFactory import QueryFactory
from QuickOSM.CoreQuickOSM.Tools import Tools
from QuickOSM.CoreQuickOSM.API.ConnexionOAPI import ConnexionOAPI
from QuickOSM.CoreQuickOSM.Parser.OsmParser import OsmParser
from QuickOSM.CoreQuickOSM.ExceptionQuickOSM import FileOutPutException,Ogr2OgrException
from processing.tools.system import *
from qgis.core import QgsMapLayerRegistry
from PyQt4.QtGui import *
import ntpath

#Processing >=2.4
try:
    from processing.algs.gdal.pyogr.ogr2ogr import main as ogr2ogr
except ImportError:
    pass

#Processing >=2.0
try:
    from processing.gdal.pyogr.ogr2ogr import main as ogr2ogr
except ImportError:
    pass


class Process:

    '''
    @staticmethod
    def execute(query,\
                url = "http://overpass-api.de/api/",\
                layers = ['points','lines','multilinestrings','multipolygons','other_relations'],\
                whiteList = None):
        
        query = PrepareQueryOqlXml(query)
        oapi = ConnexionOAPI()
        osmFile = oapi.getFileFromQuery(query)
        parser = OsmParser(osmFile)
        layers = parser.parse()
        
        return layers
    '''
    
    @staticmethod
    def ProcessQuickQuery(dialog = None, key = None,value = None,bbox = None,nominatim = None,osmObjects = None, timeout=25, outputDir=None, prefixFile=None, outputGeomTypes=None):
        
        #Set the layername
        layerName = ''
        for i in [key,value,nominatim]:
            if i:
                layerName += i + "_"
        #Delete last "_"
        layerName = layerName[:-1]
        
        #Prepare outputs
        dialog.setProgressText(QApplication.translate("QuickOSM",u"Prepare outputs"))
        #If a file already exist, we avoid downloading data for nothing
        outputs = {}
        for layer in ['points','lines','multilinestrings','multipolygons']:
            QApplication.processEvents()
            if not outputDir:
                #if no directory, get a temporary shapefile
                outputs[layer] = getTempFilenameInTempFolder("_"+layer+"_quickosm.shp")
            else:
                if not prefixFile:
                    prefixFile = layerName
                    
                outputs[layer] = os.path.join(outputDir,prefixFile + "_" + layer + ".shp")
                
                if os.path.isfile(outputs[layer]):
                    raise FileOutPutException(suffix="("+outputs[layer]+")")
        
        #Building the query
        queryFactory = QueryFactory(key=key,value=value,bbox=bbox,nominatim=nominatim,osmObjects=osmObjects)
        query = queryFactory.make()
        
        #Replace Nominatim or BBOX
        #missing extent
        query = Tools.PrepareQueryOqlXml(query=query, nominatimName = nominatim, extent=bbox)
        
        #Getting the default OAPI and running the query
        server = Tools.getSetting('defaultOAPI')
        dialog.setProgressText(QApplication.translate("QuickOSM",u"Downloading data from Overpass"))
        QApplication.processEvents()
        connexionOAPI = ConnexionOAPI(url=server,output = "xml")
        osmFile = connexionOAPI.getFileFromQuery(query)
        
        #Parsing the file
        osmParser = OsmParser(osmFile, layers=outputGeomTypes)
        osmParser.signalText.connect(dialog.setProgressText)
        osmParser.signalPercentage.connect(dialog.setProgressPercentage)
        layers = osmParser.parse()
        
        #Geojson to shapefile
        numLayers = 0
        dialog.setProgressText(QApplication.translate("QuickOSM",u"From GeoJSON to Shapefile"))
        for i, (layer,item) in enumerate(layers.iteritems()):
            dialog.setProgressPercentage(i/len(layers)*100)  
            QApplication.processEvents()
            if item['featureCount'] and layer in outputGeomTypes:
                #Transforming the vector file
                if not ogr2ogr(["","-f", "ESRI Shapefile", outputs[layer], item["geojsonFile"]]):
                    raise Ogr2OgrException               
                
                #Loading the final vector file
                newlayer = QgsVectorLayer(outputs[layer],layerName,"ogr")
                QgsMapLayerRegistry.instance().addMapLayer(newlayer)
                numLayers += 1
                
        return numLayers