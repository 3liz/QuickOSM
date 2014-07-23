'''
Created on 22 juil. 2014

@author: etienne
'''

from PyQt4.QtCore import *
import ConfigParser
import os

class FileQueryWriter:
    
    LAYERS = ['multipolygons', 'multilinestrings', 'lines', 'points']
    
    def __init__(self,path,name,category,query,whiteListValues,outputGeomTypes):
        self.path = path
        self.name = name
        self.category = category
        self.query = query
        self.outputGeomTypes = outputGeomTypes
        self.whiteListValues = whiteListValues
        self.iniFile = self.category + "-" + self.name + ".ini"
        self.queryFile = self.category + "-" + self.name + ".xml"
        
        self.config = ConfigParser.ConfigParser()
        info = {"name":self.name,"category":self.category}

        self.config.add_section('metadata')
        for key in info.keys():
            self.config.set('metadata', key, info[key])

        for layer in FileQueryWriter.LAYERS:
            self.config.add_section(layer)
            load = True if layer in self.outputGeomTypes else False
            csv = "" if layer not in self.whiteListValues else self.whiteListValues[layer]
            infoLayer = {"load":load,"namelayer":"","columns":csv,"style":""}
            for key in infoLayer.keys():
                self.config.set(layer, key, infoLayer[key])
    
    def save(self):
        filePath = os.path.join(self.path,self.iniFile)
        if not os.path.isfile(filePath):
            fh = open(filePath,"w")
            self.config.write(fh)
            fh.close()
        else:
            return False
        
        filePath = os.path.join(self.path,self.queryFile)
        if not os.path.isfile(filePath):
            fh = open(filePath,"w")
            fh.write(self.query)
            fh.close()
            return True
        else:
            return False        