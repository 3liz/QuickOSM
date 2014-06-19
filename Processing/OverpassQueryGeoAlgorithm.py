# -*- coding: utf-8 -*-

'''
Created on 10 juin 2014

@author: etienne
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import QgsMapCanvas
from qgis.core import *
from qgis.utils import iface
import QuickOSM.resources

from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.parameters.ParameterExtent import ParameterExtent
from processing.parameters.ParameterString import ParameterString
from processing.outputs.OutputFile import OutputFile
from QuickOSM.Core.ConnexionOAPI import ConnexionOAPI
from QuickOSM.Core.PrepareQuery import PrepareQuery


class OverpassQueryGeoAlgorithm(GeoAlgorithm):
    '''
    Perform an OverPass query and get an OSM file
    '''

    SERVER = 'SERVER'
    QUERY_STRING = 'QUERY_STRING'
    EXTENT = 'EXTENT'
    OUTPUT_FILE = 'OUTPUT_FILE'

    def defineCharacteristics(self):
        self.name = "Query overpass API with a string"
        self.group = "Query overpass API"

        self.addParameter(ParameterString(self.SERVER, 'Overpass API','http://overpass-api.de/api/interpreter', False, False))
        self.addParameter(ParameterString(self.QUERY_STRING,'Query (XML or OQL)', '<osm-script output="json">\n \
              <id-query into="area" ref="3600028722" type="area"/>\n \
              <union into="_">\n \
                <query into="_" type="node">\n \
                  <has-kv k="amenity" modv="" v="school"/>\n \
                  <area-query from="area" into="_" ref=""/>\n \
                </query>\n \
                <query into="_" type="way">\n \
                  <has-kv k="amenity" modv="" v="school"/>\n \
                  <area-query from="area" into="_" ref=""/>\n \
                </query>\n \
                <query into="_" type="relation">\n \
                  <has-kv k="amenity" modv="" v="school"/>\n \
                  <area-query from="area" into="_" ref=""/>\n \
                </query>\n \
              </union>\n \
              <print from="_" limit="" mode="body" order="id"/>\n \
              <recurse from="_" into="_" type="down"/>\n \
              <print from="_" limit="" mode="skeleton" order="quadtile"/>\n \
            </osm-script>', True,False))
        self.addParameter(ParameterExtent(self.EXTENT, 'Extent for {{bbox}} '))
        
        self.addOutput(OutputFile(self.OUTPUT_FILE))

    def help(self):
        return True, QApplication.translate("QuickOSM", 'Help soon')
    
    def getIcon(self):
        return QIcon(":/resources/icon")

    def processAlgorithm(self, progress):
        
        server = self.getParameterValue(self.SERVER)
        query = self.getParameterValue(self.QUERY_STRING)
        
        #Extent of the layer
        extent = self.getParameterValue(self.EXTENT)
        #default value of processing : 0,1,0,1 
        if extent != "0,1,0,1":
            print extent
            #xmin,xmax,ymin,ymax
            extent = [float(i) for i in extent.split(',')]
            geomExtent = QgsGeometry.fromRect(QgsRectangle(extent[0],extent[2],extent[1],extent[3]))
            sourceCrs = iface.mapCanvas().mapRenderer().destinationCrs()
            crsTransform = QgsCoordinateTransform(sourceCrs, QgsCoordinateReferenceSystem("EPSG:4326"))
            geomExtent.transform(crsTransform)
            extent = geomExtent.boundingBox()

        #Make some transformation on the query ({{box}}, Nominatim, ...
        query = PrepareQuery(query,extent)
        
        oapi = ConnexionOAPI(url=server,output="xml")
        osmFile = oapi.getFileFromQuery(query)
        
        #Set the output file for Processing
        self.setOutputValue(self.OUTPUT_FILE,osmFile)
        