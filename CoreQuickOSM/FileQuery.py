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
from os.path import dirname, join,isfile
from os import listdir
import re

class FileQuery:
    '''
    Read an INI file
    '''

    LAYERS = ['multipolygons', 'multilinestrings', 'lines', 'points']
    QUERY_EXTENSIONS = ['oql','xml']
    FILES = {}

    @staticmethod
    def getIniFilesFromFolder(folder,force=False):
        if force:
            FileQuery.FILES = {}
        if not FileQuery.FILES:
            files = [ join(folder,f) for f in listdir(folder) if isfile(join(folder,f))]
            for filePath in files:
                ini = FileQuery(filePath)
                ini.isValid()
        return FileQuery.FILES

    def __init__(self,filePath):
        self.__filePath = filePath
        self.__queryFile = None
        self.__name = None
        self.__category = None
        self.__bboxTemplate = None
        self.__nominatimTemplate = None
        self.__icon = None

    def getName(self):
        return self.__name

    def getCategory(self):
        return self.__category
    
    def getIcon(self):
        return self.__icon
    
    def getQueryFile(self):
        return self.__queryFile
    
    def getFilePath(self):
        return self.__filePath

    def isValid(self):
        #Is it an ini file ?    
        tab = (ntpath.basename(self.__filePath)).split('.')
        if len(tab)<2:
            return False
        
        filename = tab[0]
        if tab[1] != "ini":
            return False
        
        #Get the ini parser
        try:
            self.__configParser
        except AttributeError:
            self.__configParser = ConfigParser.ConfigParser()
            self.__configParser.read(self.__filePath)
        
        #Set the name
        try:
            #metadata-name and
            #metadata-category and
            #(layers)-load (bool) are compulsory
            self.__name = self.__configSectionMap('metadata')['name']
            self.__category = self.__configSectionMap('metadata')['category']
        
            #Check if layers are presents in the ini file
            for layer in FileQuery.LAYERS:
                if not isinstance(self.__configSectionMap(layer)['load'], bool):
                    return False
            
            #Is there another file with the query ?
            self.directory = dirname(self.__filePath)
            self.__queryExtension = None
            for ext in FileQuery.QUERY_EXTENSIONS:
                if isfile(join(self.directory, filename + '.' + ext)):
                    self.__queryFile = join(self.directory, filename + '.' + ext)
                    self.__queryExtension = ext
            if not self.__queryExtension and not self.__queryFile:
                return False
            
            #Test OK, so add it to the list
            if self.__category not in FileQuery.FILES:
                FileQuery.FILES[self.__category] = []
            
            FileQuery.FILES[self.__category].append(self)
            return True
        except Exception:
            return False

    def isTemplate(self):
        self.__bboxTemplate = False
        self.__nominatimTemplate = False
        self.__nominatimDefaultValue = None
        
        #If XML, check for templates
        if self.__queryExtension == 'xml':
            query = unicode(open(self.__queryFile, 'r').read(), "utf-8")
            
            #Check if there is a BBOX template
            if re.search('<bbox-query {{bbox}}/>',query):
                self.__bboxTemplate = True
            
            #Check if there is a Nominatim template    
            if re.search('{{nominatim}}', query):
                self.__nominatimTemplate = True
                self.__nominatimDefaultValue = False
            m = re.search('{{(nominatimArea|geocodeArea):(.*)}}', query)
            if m:
                self.__nominatimTemplate = True
                self.__nominatimDefaultValue = m.groups(1)[1]
                
        return {"nominatim" : self.__nominatimTemplate, "nominatimDefaultValue" : self.__nominatimDefaultValue, "bbox":self.__bboxTemplate}
        
    def getContent(self):
        try:
            return self.__dic
        except AttributeError:
            try:
                self.__configParser
            except AttributeError:
                self.__configParser = ConfigParser.ConfigParser()
                self.__configParser.read(self.__filePath)
            
            dic = {}
            dic['metadata'] = {}
            dic['metadata']['query'] = unicode(open(self.__queryFile, 'r').read(), "utf-8")
            
            dic['metadata']['name'] = self.__name
            
            dic['layers'] = {}
            for layer in FileQuery.LAYERS:
                dic['layers'][layer] = {}
                for item in ['namelayer', 'columns','style','load']:
                    dic['layers'][layer][item] = self.__configSectionMap(layer)[item]
                    
                    if item == 'style':
                        if isfile(join(self.directory,dic['layers'][layer][item])):
                            dic['layers'][layer][item] = join(self.directory,dic['layers'][layer][item])
                        else:
                            dic['layers'][layer][item] = None
            self.__dic = dic
            return self.__dic

    def getValue(self,section,item):
        try:
            self.__configParser
        except AttributeError:
            self.__configParser = ConfigParser.ConfigParser()
            self.__configParser.read(self.__filePath)
        
        for var in self.__configParser.options(section):
            if var == item:
                try:
                    value = unicode(self.__configParser.get(section, var), "utf-8") 
                    if value == u"True":
                        return True
                    elif value == u"False":
                        return False
                    else:
                        return value
                except:
                    return False
        return False
    
    def __configSectionMap(self,section):
        
        iniDict = {}
        for option in self.__configParser.options(section):
            try:
                value = unicode(self.__configParser.get(section, option), "utf-8")
                if value == u"True":
                    iniDict[option] = True
                elif value == u"False":
                    iniDict[option] = False
                else:
                    iniDict[option] = value   
            except:
                iniDict[option] = None
        return iniDict