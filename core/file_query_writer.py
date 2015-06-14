# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
 A QGIS plugin
 OSM Overpass API frontend
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

import ConfigParser
import codecs
from os.path import join, isfile

from QuickOSM.core.exceptions import QueryAlreadyExistsException


class FileQueryWriter:
    """
    Write a query and metadata into files
    """
    LAYERS = ['multipolygons', 'multilinestrings', 'lines', 'points']
    
    def __init__(
            self,
            path,
            name,
            category,
            query,
            white_list_values,
            output_geometry_types):
        """
        Constructor
        @param path:Folder where to save the query
        @type path:str
        @param name:Query's name
        @type name:str
        @param category:Query's category
        @type category:str
        @param query:query
        @type query:str
        @param white_list_values:doc of layers with columns
        @type white_list_values:dic
        @param output_geometry_types:list of layers
        @type output_geometry_types:list
        """

        self.path = path
        self.name = name
        self.category = category
        self.query = query
        self.outputGeomTypes = output_geometry_types
        self.whiteListValues = white_list_values
        self.iniFile = self.category + "-" + self.name + ".ini"
        self.queryFile = self.category + "-" + self.name + ".xml"
        
        # Set the INI writer
        self.config = ConfigParser.ConfigParser()
        
        # Write metadata
        info = {
            "name": self.name,
            "category": self.category}

        self.config.add_section('metadata')
        for key in info.keys():
            self.config.set('metadata', key, info[key])

        # Write every config for each layers
        for layer in FileQueryWriter.LAYERS:
            self.config.add_section(layer)

            load = True if layer in self.outputGeomTypes else False

            if layer not in self.whiteListValues:
                csv = ""
            else:
                csv = self.whiteListValues[layer]

            info_layer = {
                "load": load,
                "namelayer": "",
                "columns": csv,
                "style": ""}

            for key in info_layer.keys():
                self.config.set(layer, key, info_layer[key])
    
    def save(self):
        """
        Write the 2 files on disk
        
        @raise QueryAlreadyExistsException
        @return: True if success
        @rtype: bool
        """
        # ini file
        file_path = join(self.path, self.iniFile)
        if not isfile(file_path):
            fh = open(file_path, "w")
            self.config.write(fh)
            fh.close()
        else:
            raise QueryAlreadyExistsException

        # query file
        file_path = join(self.path, self.queryFile)
        if not isfile(file_path):
            fh = open(file_path, "w")
            fh.write(codecs.BOM_UTF8)
            fh.write(self.query.encode('utf8'))
            fh.close()
            return True
        else:
            raise QueryAlreadyExistsException        