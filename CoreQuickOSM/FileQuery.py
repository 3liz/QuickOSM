'''
Created on 25 juin 2014

@author: etienne
'''

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
    def getIniFilesFromFolder(folder):
        if not FileQuery.FILES:
            files = [ join(folder,f) for f in listdir(folder) if isfile(join(folder,f))]
            for filePath in files:
                ini = FileQuery(filePath)
                ini.isValid()
        return FileQuery.FILES

    def __init__(self,filePath):
        self.__filePath = filePath
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

    def isValid(self):
        #Is it an ini file ?    
        tab = (ntpath.basename(self.__filePath)).split('.')
        filename = tab[0]
        if tab[1] != "ini":
            #raise Exception, "Not an ini file"
            return False
        
        #Get the ini parser
        try:
            self.__configParser
        except AttributeError:
            self.__configParser = ConfigParser.ConfigParser()
            self.__configParser.read(self.__filePath)
        
        #Set the name
        self.__name = self.__configSectionMap('metadata')['name']
        self.__category = self.__configSectionMap('metadata')['category']
        if not self.__name or not self.__category:
            return False
        
        #Is there another file with the query ?
        directory = dirname(self.__filePath)
        self.__queryExtension = None
        self.__queryFile = None
        for ext in FileQuery.QUERY_EXTENSIONS:
            if isfile(join(directory, filename + '.' + ext)):
                self.__queryFile = join(directory, filename + '.' + ext)
                self.__queryExtension = ext
        if not self.__queryExtension and not self.__queryFile:
            return False
        
        #Test OK, so add it to the list
        if self.__category not in FileQuery.FILES:
            FileQuery.FILES[self.__category] = []
        
        FileQuery.FILES[self.__category].append(self)  
        return True

    def isTemplate(self):
        self.__bboxTemplate = False
        self.__nominatimTemplate = False
        
        #If XML, check for templates
        if self.__queryExtension == 'xml':
            query = unicode(open(self.__queryFile, 'r').read(), "utf-8")
            
            #Check if there is a BBOX template
            if re.search('<bbox-query {{bbox}}/>',query):
                self.__bboxTemplate = True
            
            #Check if there is a Nominatim template    
            if re.search('{{nominatim}}', query) or re.search('{{nominatimArea:(.*)}}', query):
                self.__nominatimTemplate = True

        return {"nominatim" : self.__nominatimTemplate, "bbox":self.__bboxTemplate}
        
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
        
        dic['layers'] = {}
        for layer in FileQuery.LAYERS:
            dic['layers'][layer] = {}
            for item in ['namelayer', 'columns','style','load','alias']:
                dic['layers'][layer][item] = self.__configSectionMap(layer)[item]
            
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