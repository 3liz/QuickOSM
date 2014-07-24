# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
                             -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info at 3liz dot com
        contributor          : Etienne Trimaille
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import iface

from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.parameters.ParameterExtent import ParameterExtent
from processing.parameters.ParameterString import ParameterString
from processing.outputs.OutputFile import OutputFile
from QuickOSM.CoreQuickOSM.API.ConnexionOAPI import ConnexionOAPI
from QuickOSM.CoreQuickOSM.Tools import Tools
from os.path import dirname,abspath


class OverpassQueryGeoAlgorithm(GeoAlgorithm):
    '''
    Perform an OverPass query and get an OSM file
    '''

    SERVER = 'SERVER'
    QUERY_STRING = 'QUERY_STRING'
    EXTENT = 'EXTENT'
    NOMINATIM = 'NOMINATIM'
    OUTPUT_FILE = 'OUTPUT_FILE'

    def defineCharacteristics(self):
        self.name = "Query overpass API with a string"
        self.group = "API"

        self.addParameter(ParameterString(self.SERVER, 'Overpass API','http://overpass-api.de/api/', False, False))
        self.addParameter(ParameterString(self.QUERY_STRING,'Query (XML or OQL)', '', True,False))
        self.addParameter(ParameterExtent(self.EXTENT, 'If {{bbox}} in the query, extent :'))
        self.addParameter(ParameterString(self.NOMINATIM, 'If {{nominatim}} in the query, place :','', False, True))
        
        self.addOutput(OutputFile(self.OUTPUT_FILE, 'OSM file'))

    def help(self):
        return True, 'Help soon'
    
    '''def getIcon(self):
        return QIcon(dirname(dirname(dirname(abspath(__file__))))+"/icon.png")'''

    def processAlgorithm(self, progress):
        self.progress = progress
        self.progress.setInfo("Preparing the Overpass query")
        self.progress.setPercentage(0)
        
        server = self.getParameterValue(self.SERVER)
        query = self.getParameterValue(self.QUERY_STRING)
        
        nominatim = self.getParameterValue(self.NOMINATIM)
        
        #Extent of the layer
        extent = self.getParameterValue(self.EXTENT)
        #default value of processing : 0,1,0,1 
        if extent != "0,1,0,1":
            #xmin,xmax,ymin,ymax
            extent = [float(i) for i in extent.split(',')]
            geomExtent = QgsGeometry.fromRect(QgsRectangle(extent[0],extent[2],extent[1],extent[3]))
            sourceCrs = iface.mapCanvas().mapRenderer().destinationCrs()
            crsTransform = QgsCoordinateTransform(sourceCrs, QgsCoordinateReferenceSystem("EPSG:4326"))
            geomExtent.transform(crsTransform)
            extent = geomExtent.boundingBox()

        #Make some transformation on the query ({{box}}, Nominatim, ...
        query = Tools.PrepareQueryOqlXml(query,extent,nominatim)
        
        oapi = ConnexionOAPI(url=server,output="xml")
        self.progress.setInfo("Downloading data from Overpass")
        self.progress.setPercentage(5)
        osmFile = oapi.getFileFromQuery(query)
        
        self.progress.setPercentage(100)
        #Set the output file for Processing
        self.setOutputValue(self.OUTPUT_FILE,osmFile)
        