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

from PyQt4.QtCore import QSettings
import re
from API.Nominatim import Nominatim
import shutil
from PyQt4.QtCore import *
from qgis.core import *
from os.path import join,dirname,abspath

class Tools:

    @staticmethod
    def userFolder():
        userDir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path()+'QuickOSM'
        if not QDir(userDir).exists():
            folder = join(dirname(dirname(abspath(__file__))),"queries")
            shutil.copytree(folder, QDir.toNativeSeparators(userDir))
        return unicode(QDir.toNativeSeparators(userDir))

    @staticmethod
    def getSetting(key):
        qs = QSettings()
        prefix = "/QuickOSM/"
        return qs.value(prefix + key)
    
    @staticmethod
    def setSetting(key,value):
        qs = QSettings()
        prefix = "/QuickOSM/"
        return qs.setValue(prefix + key, value)
    
    @staticmethod
    def PrepareQueryOqlXml(query,extent = None, nominatimName = None):
        '''
        Prepare the query before sending it to Overpass
        '''
        
        #Delete spaces and tabs at the beginning and at the end
        query = query.strip()
        
        #Correction of ; in the OQL at the end
        query = re.sub(r';;$',';', query)
    
        #Replace nominatimArea by <id-query />
        nominatimQuery = re.search('{{nominatimArea:(.*)}}', query)
        if nominatimQuery:
            result = nominatimQuery.groups()
            search = result[0]
            
            osmid = None
            
            #if the result is already a number, it's a relation ID, we don't perform a nominatim query
            if search.isdigit():
                osmid = search
            else:
                nominatim = Nominatim()
                
                #If {{nominatim}}, it's a template, we use the parameter
                if search == "{{nominatim}}" or nominatimName:
                    search = nominatimName
                    
                    
                #We perform a nominatim query
                osmid = nominatim.getFirstPolygonFromQuery(search)
            
            area = int(osmid) + 3600000000
            newString = '<id-query into="area" ref="'+str(area)+'" type="area"/>'
            query = re.sub(r'<id-query {{nominatimArea:(.*)}} into="area"/>',newString, query)
        
        #Replace {{bbox}} by <bbox-query />
        bboxQuery = re.search('<bbox-query {{bbox}}/>',query)
        if bboxQuery:
            newString = '<bbox-query e="'+str(extent.xMaximum())+'" n="'+str(extent.yMaximum())+'" s="'+str(extent.yMinimum())+'" w="'+str(extent.xMinimum())+'"/>'
            query = re.sub(r'<bbox-query {{bbox}}/>',newString, query)
        
        return query