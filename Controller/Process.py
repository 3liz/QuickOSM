'''
Created on 17 juin 2014

@author: etienne
'''

from QuickOSM.CoreQuickOSM.QueryFactory import QueryFactory
from QuickOSM.CoreQuickOSM.Tools import Tools
from QuickOSM.CoreQuickOSM.API.ConnexionOAPI import ConnexionOAPI
from QuickOSM.CoreQuickOSM.Parser.OsmParser import OsmParser
from processing.tools.system import *
from qgis.core import QgsMapLayerRegistry
from processing.algs.gdal.pyogr.ogr2ogr import main as ogr2ogr
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
    def ProcessQuickQuery(key = None,value = None,bbox = None,nominatim = None,osmObjects = None, timeout=25, output=None):
        
        queryFactory = QueryFactory(key=key,value=value,bbox=bbox,nominatim=nominatim,osmObjects=osmObjects)
        query = queryFactory.make()
        
        #missing extent
        query = Tools.PrepareQueryOqlXml(query=query, nominatimName = nominatim)
        
        connexionOAPI = ConnexionOAPI(output = "xml")
        osmFile = connexionOAPI.getFileFromQuery(query)
        print osmFile
        osmParser = OsmParser(osmFile)
        layers = osmParser.parse()
                
        for layer,item in layers.iteritems():
            if item['featureCount']:
                outputLayerFile = None
                if not output:
                    outputLayerFile = getTempFilenameInTempFolder("_"+layer+"_quickosm.shp")
                else:
                    tab = (ntpath.basename(output)).split('.')
                    outputLayerFile = tab[0] + "_" + layer + "." + tab[1]
                    
                layerName = ''
                for i in [key,value,nominatim]:
                    if i:
                        layerName += i + " "
                    
                ogr2ogr(["","-f", "ESRI Shapefile", outputLayerFile, item["geojsonFile"]])
                newlayer = QgsVectorLayer(outputLayerFile,layerName,"ogr")
                QgsMapLayerRegistry.instance().addMapLayer(newlayer)
                
        return True