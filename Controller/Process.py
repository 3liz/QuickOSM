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
from os.path import dirname,abspath,join

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
    def Query(dialog = None, query=None, osmObjects=None, timeout=25, outputDir=None, prefixFile=None,outputGeomTypes=None):
        
        #Set the layername
        layerName = 'test'
        
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
        
        
        #Replace Nominatim or BBOX
        #missing extent, nominatim
        query = Tools.PrepareQueryOqlXml(query=query)
        
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
                
                #Loading default styles
                fields = newlayer.pendingFields()
                if fields.indexFromName("colour") > 0:
                    newlayer.loadNamedStyle(join(dirname(dirname(abspath(__file__))),"styles","colour.qml"))
                
                #Add action about OpenStreetMap
                actions = newlayer.actions()
                actions.addAction(QgsAction.OpenUrl,"OpenStreetMap Browser",'http://www.openstreetmap.org/browse/[% "osm_type" %]/[% "osm_id" %]',False)
                actions.addAction(QgsAction.OpenUrl,"JOSM",'http://localhost:8111/load_object?objects=[% "full_id" %]',False)
                actions.addAction(QgsAction.OpenUrl,"User default editor",'http://www.openstreetmap.org/edit?[% "osm_type" %]=[% "osm_id" %]',False)
                #actions.addAction(QgsAction.OpenUrl,"Edit directly",'http://rawedit.openstreetmap.fr/edit/[% "osm_type" %]/[% "osm_id" %]',False)
                actions.addAction(QgsAction.GenericPython,"Edit directly",'from PyQt4.QtCore import QUrl; from PyQt4.QtWebKit import QWebView;  myWV = QWebView(None); myWV.load(QUrl("http://rawedit.openstreetmap.fr/edit/[% "osm_type" %]/[% "osm_id" %]")); myWV.show()',False)
                
                if 'url' in item['tags']:
                    actions.addAction(QgsAction.GenericPython,"Website",'var = QtGui.QDesktopServices(); var.openUrl(QtCore.QUrl("[% "url" %]")) if "[% "url" %]"!="" else QtGui.QMessageBox.information(None, "Sorry", "Sorry man, no website")',False)
                    
                if 'wikipedia' in item['tags']:
                    actions.addAction(QgsAction.GenericPython,"Wikipedia",'var = QtGui.QDesktopServices(); var.openUrl(QtCore.QUrl("http://en.wikipedia.org/wiki/[% "wikipedia" %]")) if "[% "wikipedia" %]"!="" else QtGui.QMessageBox.information(None, "Sorry", "Sorry man, no wikipedia")',False)
                
                if 'website' in item['tags']:
                    actions.addAction(QgsAction.GenericPython,"Website",'var = QtGui.QDesktopServices(); var.openUrl(QtCore.QUrl("[% "website" %]")) if "[% "website" %]"!="" else QtGui.QMessageBox.information(None, "Sorry", "Sorry man, no website")',False)
                 
                if 'ref:UAI' in item['tags']:
                    actions.addAction(QgsAction.GenericPython,"ref UAI",'var = QtGui.QDesktopServices(); var.openUrl(QtCore.QUrl("http://www.education.gouv.fr/pid24302/annuaire-resultat-recherche.html?lycee_name=[% "ref_UAI" %]")) if "[% "ref_UAI" %]"!="" else QtGui.QMessageBox.information(None, "Sorry", "Sorry man, no ref UAI")',False)
                
                QgsMapLayerRegistry.instance().addMapLayer(newlayer)
                numLayers += 1
                
        return numLayers
    
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
                
                #Loading default styles
                fields = newlayer.pendingFields()
                if fields.indexFromName("colour") > 0:
                    newlayer.loadNamedStyle(join(dirname(dirname(abspath(__file__))),"styles","colour.qml"))
                
                #Add action about OpenStreetMap
                actions = newlayer.actions()
                actions.addAction(QgsAction.OpenUrl,"OpenStreetMap Browser",'http://www.openstreetmap.org/browse/[% "osm_type" %]/[% "osm_id" %]',False)
                actions.addAction(QgsAction.OpenUrl,"JOSM",'http://localhost:8111/load_object?objects=[% "full_id" %]',False)
                actions.addAction(QgsAction.OpenUrl,"User default editor",'http://www.openstreetmap.org/edit?[% "osm_type" %]=[% "osm_id" %]',False)
                #actions.addAction(QgsAction.OpenUrl,"Edit directly",'http://rawedit.openstreetmap.fr/edit/[% "osm_type" %]/[% "osm_id" %]',False)
                actions.addAction(QgsAction.GenericPython,"Edit directly",'from PyQt4.QtCore import QUrl; from PyQt4.QtWebKit import QWebView;  myWV = QWebView(None); myWV.load(QUrl("http://rawedit.openstreetmap.fr/edit/[% "osm_type" %]/[% "osm_id" %]")); myWV.show()',False)
                
                if 'url' in item['tags']:
                    actions.addAction(QgsAction.GenericPython,"Website",'var = QtGui.QDesktopServices(); var.openUrl(QtCore.QUrl("[% "url" %]")) if "[% "url" %]"!="" else QtGui.QMessageBox.information(None, "Sorry", "Sorry man, no website")',False)
                    
                if 'wikipedia' in item['tags']:
                    actions.addAction(QgsAction.GenericPython,"Wikipedia",'var = QtGui.QDesktopServices(); var.openUrl(QtCore.QUrl("http://en.wikipedia.org/wiki/[% "wikipedia" %]")) if "[% "wikipedia" %]"!="" else QtGui.QMessageBox.information(None, "Sorry", "Sorry man, no wikipedia")',False)
                
                if 'website' in item['tags']:
                    actions.addAction(QgsAction.GenericPython,"Website",'var = QtGui.QDesktopServices(); var.openUrl(QtCore.QUrl("[% "website" %]")) if "[% "website" %]"!="" else QtGui.QMessageBox.information(None, "Sorry", "Sorry man, no website")',False)
                 
                if 'ref:UAI' in item['tags']:
                    actions.addAction(QgsAction.GenericPython,"ref UAI",'var = QtGui.QDesktopServices(); var.openUrl(QtCore.QUrl("http://www.education.gouv.fr/pid24302/annuaire-resultat-recherche.html?lycee_name=[% "ref_UAI" %]")) if "[% "ref_UAI" %]"!="" else QtGui.QMessageBox.information(None, "Sorry", "Sorry man, no ref UAI")',False)
                
                QgsMapLayerRegistry.instance().addMapLayer(newlayer)
                numLayers += 1
                
        return numLayers