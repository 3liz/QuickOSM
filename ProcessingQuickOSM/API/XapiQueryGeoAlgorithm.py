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

from QuickOSM import *
from QuickOSM.ProcessingQuickOSM import *

from qgis.utils import iface

from QuickOSM.CoreQuickOSM.API.ConnexionXAPI import ConnexionXAPI
from operating_system.path import isfile,join,basename,dirname,abspath


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
        locale += "."

        current_file = __file__
        if current_file.endswith('pyc'):
            current_file = current_file[:-1]
        current_file = basename(current_file)

        helps = [current_file + locale + ".html", current_file + ".html"]

        doc_path = join(dirname(dirname(dirname(abspath(__file__)))), 'doc')
        for helpFileName in helps:
            file_help_path = join(doc_path, helpFileName)
            if isfile(file_help_path):
                return False, file_help_path
        
        return False, None
    
    def getIcon(self):
        return QIcon(dirname(__file__) + '/../../icon.png')

    def processAlgorithm(self, progress):
        self.progress = progress
        self.progress.setInfo("Downloading data from XAPI")
        
        server = self.getParameterValue(self.SERVER)
        query = self.getParameterValue(self.QUERY_STRING)
        
        xapi = ConnexionXAPI(url=server)
        osmFile = xapi.get_file_from_query(query)
        
        #Set the output file for Processing
        self.setOutputValue(self.OUTPUT_FILE,osmFile)
        