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

from QuickOSM.core.exceptions import QueryFactoryException
from QuickOSM.core.utilities.tools import tr

TAB = '     '


class QueryFactory(object):
    """
    Build a XML query
    """
    
    OSM_TYPES = ['node', 'way', 'relation']

    def __init__(
            self,
            key=None,
            value=None,
            bbox=None,
            nominatim=None,
            is_around=None,
            distance=None,
            osm_objects=OSM_TYPES,
            output='xml',
            timeout=25,
            print_mode='body'):
        """
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
        @param is_around: around or in
        @type is_around: bool
        @param osm_objects: list of osm objects to query on (node/way/relation)
        @type osm_objects: list
        @param output:output of overpass : xml or json
        @type output: str
        @param timeout: timeout of the query
        @type timeout: int
        @param print_mode: print type of the overpass query (read overpass doc)
        @type print_mode: str
        """
        self.__key = key
        self.__value = value
        self.__bbox = bbox
        self.__nominatim = nominatim
        self.__is_around = is_around
        self.__distance = distance
        self.__osm_objects = osm_objects
        self.__timeout = timeout
        self.__output = output
        self.__print_mode = print_mode

    def check_parameters(self):
        if self.__nominatim and self.__bbox:
            raise QueryFactoryException(
                suffix=tr('QuickOSM', 'nominatim OR bbox, not both'))

        if not self.__key:
            raise QueryFactoryException(suffix=tr('QuickOSM', 'key required'))

        for osmObject in self.__osm_objects:
            if osmObject not in QueryFactory.OSM_TYPES:
                raise QueryFactoryException(
                    suffix=tr('QuickOSM', 'wrong OSM object'))

    def make(self):
        """
        Make the query

        @return: query
        @rtype: str
        """

        self.check_parameters()

        query = '<osm-script output="%s" timeout="%s">\n' % \
                (self.__output, self.__timeout)
        
        if self.__nominatim and not self.__is_around:
            template = '{{geocodeArea:%s}}' % self.__nominatim
            query += TAB + '<id-query %s into="area"/> \n' % template
            
        query += TAB + '<union>\n'
        
        for osmObject in self.__osm_objects:

            query += TAB + TAB + '<query type="' + osmObject + '">\n'
            query += TAB + TAB + TAB + '<has-kv k="' + self.__key + '" '

            if self.__value:
                query += 'v="' + self.__value + '"'

            query += '/> \n'
            
            if self.__nominatim and not self.__is_around:
                query += TAB + TAB + TAB + '<area-query from="area"/>\n'

            elif self.__nominatim and self.__is_around:
                template = '{{geocodeCoords:%s}}' % self.__nominatim
                query += TAB + TAB + TAB + '<around %s radius="%s" />\n' % \
                    (template, self.__distance)

            elif self.__bbox:
                query += TAB + TAB + TAB + '<bbox-query {{bbox}} />\n'

            query += TAB + TAB + '</query>\n'
        
        query += TAB + '</union>\n'
        query += TAB + '<union>\n'
        query += TAB + TAB + '<item />\n'
        query += TAB + TAB + '<recurse type="down"/>\n'
        query += TAB + '</union>\n'
        query += TAB + '<print mode="%s" />\n' % self.__print_mode
        query += '</osm-script>'
        
        return query