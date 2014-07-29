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
from QuickOSM.CoreQuickOSM.API.Nominatim import Nominatim
from QuickOSM.CoreQuickOSM.ExceptionQuickOSM import NominatimAreaException
from os.path import isfile,join,basename,dirname,abspath

class NominatimQueryGeoAlgorithm(GeoAlgorithm):

    SERVER = 'SERVER'
    NOMINATIM_STRING = 'NOMINATIM_STRING'
    OSM_ID = 'OSM_ID'

    def defineCharacteristics(self):
        self.name = "Query nominatim API with a string"
        self.group = "API"

        self.addParameter(ParameterString(self.SERVER, 'Nominatim server', 'http://nominatim.openstreetmap.org/search?format=json', False, False))
        self.addParameter(ParameterString(self.NOMINATIM_STRING, 'Search','', False, False))
        self.addOutput(OutputNumber(self.OSM_ID,'OSM id'))

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
        return QIcon(dirname(__file__) + '/../../icon.png')

    def processAlgorithm(self, progress):
        
        server = self.getParameterValue(self.SERVER)
        query = self.getParameterValue(self.NOMINATIM_STRING)
        
        nominatim = Nominatim(url = server)
        try:
            osmID = nominatim.getFirstPolygonFromQuery(query)
            progress.setInfo("Getting first OSM relation ID from Nominatim :",osmID)
        except:
            raise NominatimAreaException
        self.setOutputValue("OSM_ID",osmID)