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

class QueryFactory():
    '''
    Build a XML query
    '''
    
    OSM_TYPES = ['node','way','relation']

    def __init__(self,key = None,value = None,bbox = None,nominatim = None,osmObjects = OSM_TYPES, output = 'xml', timeout=25, printMode = 'body'):
        '''
        Constructor with key=value according to OpenStreetMap
        A bbox or nominatim can be provided
        
        @param key: key
        @type key: str
        @param value: value
        @type value: str
        @param bbox: if we want a {{bbox}}
        @type bbox: QgsRectangle or bool or "{{bbox}}"
        @param nominatim: a place
        @type nominatim: str
        @param osmObjects: list of osm objects to query on (node/way/relation)
        @type osmObjects: list
        @param output:output of overpass : xml or json
        @type output: str
        @param timeout: timeout of the query
        @type timeout: int
        @param printMode: print type of the overpass query (read overpass doc)
        @type printMode: str 
        '''
        self.__key = key
        self.__value = value
        self.__bbox = bbox
        self.__nominatim = nominatim
        self.__osmObjects = osmObjects
        self.__timeout = timeout
        self.__output = output
        self.__printMode = printMode
        
    def make(self):
        '''
        Make the query
        @return: query
        @rtype: str
        '''
        
        #Check if is ok ?
        if self.__nominatim and self.__bbox:
            return False, "Nominatim OR bbox, not both"
        
        if self.__nominatim == '{{nominatim}}' or self.__nominatim == True:
            self.__nominatim = '{{nominatim}}'
            
        if self.__bbox == '{{bbox}}' or self.__bbox == True or isinstance(self.__bbox, QgsRectangle):
            self.__bbox = '{{bbox}}'
        
        if not self.__key:
            return False, "Key required"
        
        for osmObject in self.__osmObjects:
            if osmObject not in QueryFactory.OSM_TYPES:
                return False, "Wrong OSM object"
          
        #TEST OK, so continue and build the query
        TAB = '     '
        query = '<osm-script output="%s" timeout="%s"> \n' %(self.__output,self.__timeout)
        
        if self.__nominatim:
            query += TAB + '<id-query {{nominatimArea:'+self.__nominatim+'}} into="area"/> \n'
            
        query += TAB + '<union>\n'
        
        for osmObject in self.__osmObjects:
            query += TAB + TAB +'<query type="'+osmObject+'">\n'
            query += TAB + TAB + TAB +'<has-kv k="'+self.__key+'" '
            if self.__value:
                query += 'v="'+self.__value+'"'
            query += '/> \n'
            
            if self.__nominatim:
                query += TAB + TAB + TAB + '<area-query from="area"/>\n'
            elif self.__bbox:
                query += TAB + TAB + TAB + '<bbox-query '+self.__bbox+'/>\n'
            query += TAB + TAB + '</query>\n'
        
        query += TAB + '</union>\n'+TAB+'<union>\n'+TAB + TAB +'<item />\n'+TAB + TAB +'<recurse type="down"/>\n'+TAB +'</union>\n'
        query += TAB + '<print mode="'+self.__printMode+'" />\n</osm-script>'
        
        return query