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

import ntpath
import ConfigParser
from genericpath import isfile
from os.path import dirname, join
from os import listdir
import re

class IniFile():
    '''
    Read an INI file
    '''

    LAYERS = ['multipolygons', 'multilinestrings', 'lines', 'points']
    QUERY_EXTENSIONS = ['oql','xml']
    
    @staticmethod
    def getIniFilesFromFolder(folder):
        existingFiles = []
        files = [ join(folder,f) for f in listdir(folder) if isfile(join(folder,f))]
        for filePath in files:
            ini = IniFile(filePath)
            if ini.isValid():
                existingFiles.append(ini)
        return existingFiles
    
    @staticmethod
    def getNamesAndPathsFromFolder(folder):
        existingIniFiles = IniFile.getIniFilesFromFolder(folder)
        result = []
        for ini in existingIniFiles:
            result.append({'name': ini.__name,'nameFull': ini.__nameFull, 'category':ini.__category,'path' : ini.__filePath, 'bbox': ini.__bboxTemplate, 'nominatim':ini.__nominatimTemplate })
        return result

    def __init__(self,filePath):
        self.__filePath = filePath
        self.__bboxTemplate = None
        self.__nominatimTemplate = None

    def isValid(self):
        #Is it an ini file ?    
        tab = (ntpath.basename(self.__filePath)).split('.')
        filename = tab[0]
        if tab[1] != "ini":
            #raise Exception, "Not an ini file"
            return False
        
        #Is there another file with the query ?
        directory = dirname(self.__filePath)
        self.__queryExtension = None
        self.__queryFile = None
        for ext in IniFile.QUERY_EXTENSIONS:
            if isfile(join(directory, filename + '.' + ext)):
                self.__queryFile = join(directory, filename + '.' + ext)
                self.__queryExtension = ext
        if not self.__queryExtension and not self.__queryFile:
            #raise Exception, "No query file (.xml or .oql)"
            return False
        
        try:
            self.__configParser
        except AttributeError:
            self.__configParser = ConfigParser.ConfigParser()
            self.__configParser.read(self.__filePath)
        
        #Set the name
        self.__name = self.__configSectionMap('metadata')['name']
        self.__nameFull = self.__name
        self.__category = self.__configSectionMap('metadata')['category']
        
        #If XML, check for templates
        if self.__queryExtension == 'xml':
            query = unicode(open(self.__queryFile, 'r').read(), "utf-8")
            
            #Check if there is a BBOX template
            bboxQuery = re.search('<bbox-query {{bbox}}/>',query)
            if bboxQuery:
                self.__bboxTemplate = True
                self.__nameFull = self.__nameFull + " [extent required]"
            
            #Check if there is a Nominatim template    
            nominatimQuery = re.search('{{nominatimArea:{{nominatim}}}}', query)
            if nominatimQuery:
                self.__nominatimTemplate = True
                self.__nameFull = self.__nameFull + " [PLACENAME required]"
        else:
            self.__bboxTemplate = False
            self.__nominatimTemplate = False
            
        return True
        
        
    def getContent(self):
        
        try:
            self.__configParser
        except AttributeError:
            self.__configParser = ConfigParser.ConfigParser()
            self.__configParser.read(self.__filePath)
        
        dic = {}
        dic['metadata'] = {}
        dic['metadata']['query'] = unicode(open(self.__queryFile, 'r').read(), "utf-8")
        
        for item in ['description','logo']:
            dic['metadata'][item] = self.__configSectionMap('metadata')[item]
        
        dic['metadata']['name'] = self.__name
        
        for layer in IniFile.LAYERS:
            dic[layer] = {}
            for item in ['namelayer', 'columns','style']:
                dic[layer][item] = self.__configSectionMap(layer)[item]
            
        return dic

    def getValue(self,section,item):
        try:
            self.__configParser
        except AttributeError:
            self.__configParser = ConfigParser.ConfigParser()
            self.__configParser.read(self.__filePath)
        
        for var in self.__configParser.options(section):
            if var == item:
                try:
                    return unicode(self.__configParser.get(section, var), "utf-8")
                except:
                    return False
        return False
    
    def __configSectionMap(self,section):
        
        iniDict = {}
        for option in self.__configParser.options(section):
            try:
                iniDict[option] = unicode(self.__configParser.get(section, option), "utf-8")
            except:
                iniDict[option] = None
        return iniDict