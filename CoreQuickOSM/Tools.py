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
import re
from API.Nominatim import Nominatim
from os.path import join,dirname,abspath
import os
from shutil import *
from qgis.utils import iface

class Tools:
    '''
    Usefull tools
    '''

    @staticmethod
    def displayMessageBar(title = None, msg = None,level=QgsMessageBar.INFO,duration=5):
        '''
        Display the message at the good place
        '''
        if iface.QuickOSM_mainWindowDialog.isVisible():
            iface.QuickOSM_mainWindowDialog.messageBar.pushMessage(title, msg, level,duration)
        else:
            iface.messageBar().pushMessage(title, msg, level,duration)

    @staticmethod
    def getUserFolder():
        '''
        Get the user folder, ~/.qgis2/QuickOSM on linux for instance
        @rtype: str
        @return: path
        '''
        userDir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path()+'QuickOSM'
        return unicode(QDir.toNativeSeparators(userDir))

    @staticmethod
    def getUserQueryFolder(overWrite = False):
        '''
        Get the user folder for queries, ~/.qgis2/QuickOSM/queries on linux for instance
        @rtype: str
        @return: path
        '''
        folder = Tools.getUserFolder()
        queriesFolder = os.path.join(folder, 'queries')
        if not QDir(queriesFolder).exists() or overWrite:
            folder = join(dirname(dirname(abspath(__file__))),"queries")
            Tools.copytree(folder, QDir.toNativeSeparators(queriesFolder))
        return unicode(QDir.toNativeSeparators(queriesFolder))

    @staticmethod
    def getSetting(key):
        '''
        Get a value in the QSettings
        @param key: key
        @type key: str
        @return: value
        @rtype: str 
        '''
        qs = QSettings()
        prefix = "/QuickOSM/"
        return qs.value(prefix + key)
    
    @staticmethod
    def setSetting(key,value):
        '''
        Set a value in the QSettings
        @param key: key
        @type key: str
        @param value: value
        @type value: str
        @return: result
        @rtype: bool
        '''
        qs = QSettings()
        prefix = "/QuickOSM/"
        return qs.setValue(prefix + key, value)
    
    @staticmethod
    def PrepareQueryOqlXml(query,extent = None, nominatimName = None):
        '''
        Prepare the query before sending it to Overpass
        @param query: the query, in XML or OQL
        @type query: str
        @param extent: the extent if {{bbox}}
        @type extent: QgsRectangle
        @param nominatimName: the city if {{nominatimArea:}}
        @type nominatimName: str
        @return: the final query
        @rtype: str  
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
    
    @staticmethod
    def copytree(src, dst, symlinks=False, ignore=None):
        names = os.listdir(src)
        if ignore is not None:
            ignored_names = ignore(src, names)
        else:
            ignored_names = set()
    
        if not os.path.isdir(dst): # This one line does the trick
            os.makedirs(dst)
        errors = []
        for name in names:
            if name in ignored_names:
                continue
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            try:
                if symlinks and os.path.islink(srcname):
                    linkto = os.readlink(srcname)
                    os.symlink(linkto, dstname)
                elif os.path.isdir(srcname):
                    copytree(srcname, dstname, symlinks, ignore)
                else:
                    # Will raise a SpecialFileError for unsupported file types
                    copy2(srcname, dstname)
            # catch the Error from the recursive copytree so that we can
            # continue with other files
            except Error, err:
                errors.extend(err.args[0])
            except EnvironmentError, why:
                errors.append((srcname, dstname, str(why)))
        try:
            copystat(src, dst)
        except OSError, why:
            if WindowsError is not None and isinstance(why, WindowsError):
                # Copying file access times may fail on Windows
                pass
            else:
                errors.extend((src, dst, str(why)))
        if errors:
            raise Error, errors