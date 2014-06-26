'''
Created on 25 juin 2014

@author: etienne
'''

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
                existingFiles.append(filePath)
        return existingFiles
    
    @staticmethod
    def getNamesAndPathsFromFolder(folder):
        existingIniFiles = IniFile.getIniFilesFromFolder(folder)
        result = []
        for filePath in existingIniFiles:
            ini = IniFile(filePath)
            ini.isValid()
            dic = {}
            dic['name'] = ini.__name
            dic['path'] = filePath
            result.append(dic)
        return result

    def __init__(self,filePath):
        self.__filePath = filePath
        self.__bboxTemplate = False
        self.__nominatimTemplate = False

    def isValid(self):
        #Is it an ini file ?    
        tab = (ntpath.basename(self.__filePath)).split('.')
        if tab[1] != "ini":
            #raise Exception, "Not an ini file"
            return False
        
        #Is there another file with the query ?
        directory = dirname(self.__filePath)
        queryFile = [join(directory, tab[0] + '.' + ext) for ext in IniFile.QUERY_EXTENSIONS if isfile(join(directory, tab[0] + '.' + ext))]
        
        if queryFile[0]:
            self.__queryFile = queryFile[0]
        else:
            #raise Exception, "No query file (.xml or .oql)"
            return False
        
        try:
            self.__configParser
        except AttributeError:
            self.__configParser = ConfigParser.ConfigParser()
            self.__configParser.read(self.__filePath)
        
        #Set the name
        self.__name = self.__configSectionMap('metadata')['name']
        
        query = unicode(open(self.__queryFile, 'r').read(), "utf-8")
        print query
        #Check if there is a BBOX template
        bboxQuery = re.search('<bbox-query {{bbox}}/>',query)
        if bboxQuery:
            self.__bboxTemplate = True
            self.__name = self.__name + " [extent required]"
            
        nominatimQuery = re.search('{{nominatimArea:{{nominatim}}}}', query)
        if nominatimQuery:
            self.__nominatimTemplate = True
            self.__name = self.__name + " [PLACENAME required]"
            
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
        
        print self.__name
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