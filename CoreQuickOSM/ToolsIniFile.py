'''
Created on 25 juin 2014

@author: etienne
'''

import ntpath
import ConfigParser
from genericpath import isfile
from os.path import dirname, join

def ConfigSectionMap(configParser,section):
    iniDict = {}
    for option in configParser.options(section):
        try:
            iniDict[option] = configParser.get(section, option)
        except:
            iniDict[option] = None
    return iniDict

def ParseIniFile(filePath):

    dic = {}
    LAYERS = ['multipolygons', 'multilinestrings', 'lines', 'points']
    
    #Is it an ini file ?    
    tab = (ntpath.basename(filePath)).split('.')
    if tab[1] != "ini":
        raise Exception, "Not an ini file"
    
    #Is there another file with the query ?
    directory = dirname(filePath)
    queryFile = [join(directory, tab[0] + '.' + ext) for ext in ['oql','xml'] if isfile(join(directory, tab[0] + '.' + ext))]
    try:
        queryFile = queryFile[0]
    except IndexError:
        raise Exception, "No query file (.xml or .oql)"
    
    #Ini Parser
    configParser = ConfigParser.ConfigParser()
    configParser.read(filePath)
    
    dic['metadata'] = {}
    dic['metadata']['query'] = open(queryFile, 'r').read()
    
    for item in ['name', 'description','logo']:
        dic['metadata'][item] = ConfigSectionMap(configParser,'metadata')[item]
    
    for layer in LAYERS:
        dic[layer] = {}
        for item in ['namelayer', 'columns','style']:
            dic[layer][item] = ConfigSectionMap(configParser,layer)[item]
        
    return dic