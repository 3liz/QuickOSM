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
import ntpath

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
    def ProcessQuickQuery(key = None,value = None,bbox = None,nominatim = None,osmObjects = None, timeout=25, outputDir=None, prefixFile=None):
        
        layerName = ''
        for i in [key,value,nominatim]:
            if i:
                layerName += i + "_"
        layerName = layerName[:-1]
        
        #Building the query
        queryFactory = QueryFactory(key=key,value=value,bbox=bbox,nominatim=nominatim,osmObjects=osmObjects)
        query = queryFactory.make()
        
        #Replace Nominatim or BBOX
        #missing extent
        query = Tools.PrepareQueryOqlXml(query=query, nominatimName = nominatim)
        
        #Getting the default OAPI and running the query
        server = Tools.getSetting('defaultOAPI')
        connexionOAPI = ConnexionOAPI(url=server,output = "xml")
        osmFile = connexionOAPI.getFileFromQuery(query)
        
        #Parsing the file
        osmParser = OsmParser(osmFile)
        layers = osmParser.parse()
                
        for layer,item in layers.iteritems():
            if item['featureCount']:
                
                #Setting the output
                outputLayerFile = None
                if not outputDir:
                    #if no directory, get a temporary shapefile
                    outputLayerFile = getTempFilenameInTempFolder("_"+layer+"_quickosm.shp")
                else:
                    if not prefixFile:
                        prefixFile = layerName
                        
                    outputLayerFile = os.path.join(outputDir,prefixFile + "_" + layer + ".shp")
                    
                    if os.path.isfile(outputLayerFile):
                        raise FileOutPutException
                  
                #Transforming the vector file
                if not ogr2ogr(["","-f", "ESRI Shapefile", outputLayerFile, item["geojsonFile"]]):
                    raise Ogr2OgrException               
                
                #Loading the final vector file
                newlayer = QgsVectorLayer(outputLayerFile,layerName,"ogr")
                QgsMapLayerRegistry.instance().addMapLayer(newlayer)
                
        return True