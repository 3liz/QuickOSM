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

from PyQt4.QtCore import *
from QuickOSM.CoreQuickOSM.ExceptionQuickOSM import QueryAlreadyExistsException
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
            raise QueryAlreadyExistsException
        
        filePath = os.path.join(self.path,self.queryFile)
        if not os.path.isfile(filePath):
            fh = open(filePath,"w")
            fh.write(self.query)
            fh.close()
            return True
        else:
            raise QueryAlreadyExistsException        