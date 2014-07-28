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
from qgis.gui import QgsMapCanvas
from qgis.core import *
from qgis.utils import iface

from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.parameters.ParameterExtent import ParameterExtent
from processing.parameters.ParameterString import ParameterString
from processing.outputs.OutputFile import OutputFile
from QuickOSM.CoreQuickOSM.API.ConnexionXAPI import ConnexionXAPI
from QuickOSM import resources_rc
from os.path import isfile,join,basename,dirname,abspath


class XapiQueryGeoAlgorithm(GeoAlgorithm):
    '''
    Perform an OverPass query and get an OSM file
    '''

    SERVER = 'SERVER'
    QUERY_STRING = 'QUERY'
    OUTPUT_FILE = 'OUTPUT_FILE'

    def defineCharacteristics(self):
        self.name = "Query XAPI with a string"
        self.group = "API"

        self.addParameter(ParameterString(self.SERVER, 'XAPI','http://www.overpass-api.de/api/xapi?', False, False))
        self.addParameter(ParameterString(self.QUERY_STRING,'Query', '', False,False))
        
        self.addOutput(OutputFile(self.OUTPUT_FILE,'OSM file'))

    def help(self):
        locale = QSettings().value("locale/userLocale")[0:2]
        locale = "." + locale

        currentFile = __file__
        if currentFile.endswith('pyc'):
            currentFile = currentFile[:-1]
        currentFile = basename(currentFile)
        
        helps = [currentFile + locale +".html", currentFile + ".html"]
        
        docPath = join(dirname(dirname(dirname(abspath(__file__)))),'doc')
        for helpFileName in helps :
            fileHelpPath = join(docPath,helpFileName)
            if isfile(fileHelpPath):
                return False, fileHelpPath
        
        return False, None
    
    def getIcon(self):
        return QIcon(":/plugins/QuickOSM/icon.png")

    def processAlgorithm(self, progress):
        self.progress = progress
        self.progress.setInfo("Downloading data from XAPI")
        
        server = self.getParameterValue(self.SERVER)
        query = self.getParameterValue(self.QUERY_STRING)
        
        xapi = ConnexionXAPI(url=server)
        osmFile = xapi.getFileFromQuery(query)
        
        #Set the output file for Processing
        self.setOutputValue(self.OUTPUT_FILE,osmFile)
        