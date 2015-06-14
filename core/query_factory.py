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

import re
from xml.dom.minidom import parseString

from QuickOSM.core.exceptions import QueryFactoryException
from QuickOSM.core.utilities.tools import tr


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

    @staticmethod
    def get_pretty_xml(query):
        xml = parseString(query)
        return xml.toprettyxml()

    @staticmethod
    def replace_template(query):
        query = re.sub(
            r' area="(.*?)" ', r' {{geocodeArea:\1}} ', query)
        query = query.replace('bbox="custom"', ' {{bbox}} ')
        return query

    def generate_xml(self):
        query = u'<osm-script output="%s" timeout="%s">' % \
                (self.__output, self.__timeout)

        if self.__nominatim:
            nominatim = [name.strip() for name in self.__nominatim.split(';')]
        else:
            nominatim = None

        if nominatim and not self.__is_around:

            for i, one_nominatim in enumerate(nominatim):
                query += u'<id-query area="%s" into="area_%s"/>' % \
                         (one_nominatim, i)

        query += u'<union>'

        loop = 1 if not nominatim else len(nominatim)

        for osmObject in self.__osm_objects:
            for i in range(0, loop):
                query += u'<query type="%s">' % osmObject
                query += u'<has-kv k="%s" ' % self.__key
                if self.__value:
                    query += u'v="%s"' % self.__value

                query += u'/>'

                if self.__nominatim and not self.__is_around:
                    query += u'<area-query from="area_%s"/>' % i

                elif self.__nominatim and self.__is_around:
                    query += u'<around area="%s" radius="%s" />' % \
                             self.__nominatim, self.__distance

                elif self.__bbox:
                    query = u'%s<bbox-query bbox="custom" />' % query

                query += u'</query>'

        query += u'</union>'
        query += u'<union>'
        query += u'<item />'
        query += u'<recurse type="down"/>'
        query += u'</union>'
        query += u'<print mode="%s" />' % self.__print_mode
        query += u'</osm-script>'

        return query

    def make(self):
        """
        Make the query

        @return: query
        @rtype: str
        """

        self.check_parameters()
        query = self.generate_xml()

        # get_pretty_xml works only with a valid XML, no template {{}}
        # So we replace fake XML after
        query = QueryFactory.get_pretty_xml(query)

        # get_pretty_xml add on XML header, let's remove the first line
        query = '\n'.join(query.split('\n')[1:])

        query = QueryFactory.replace_template(query)
        query = query.replace('	', '    ')
        return query