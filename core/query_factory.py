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

from QuickOSM.definitions.osm import ALL_OSM_TYPES, QueryType
from QuickOSM.core.exceptions import QueryFactoryException
from QuickOSM.core.utilities.tools import tr


class QueryFactory:

    """Build a XML or OQL query."""

    def __init__(
            self,
            query_type=None,
            key=None,
            value=None,
            nominatim_place=None,
            around_distance=None,
            osm_objects=ALL_OSM_TYPES,
            output='xml',
            timeout=25,
            print_mode='body',
    ):
        """
        Query Factory constructor according to Overpass API.

        :param query_type: The type of query to build.
        :type query_type: QueryType

        :param key: OSM key or None.
        :type key: str,None

        :param value: OSM value or None.
        :type value: str,None

        :param nominatim_place: A place name if needed or None
        :type nominatim_place: str,None

        :param around_distance: Distance to use if it's an around query or None
        :type around_distance: int,None

        :param osm_objects: List of osm objects to query on (node/way/relation)
        :type osm_objects: list

        :param output:output of overpass : XML or JSON
        :type output: str

        :param timeout: Timeout of the query
        :type timeout: int

        :param print_mode: Print type of the overpass query (read overpass doc)
        :type print_mode: str
        """
        self._query_type = query_type
        self._key = key
        self._value = value
        self._nominatim_place = nominatim_place
        self._distance_around = around_distance
        self._osm_objects = osm_objects
        self._timeout = timeout
        self._output = output
        self._print_mode = print_mode

    def _check_parameters(self):
        """Internal function to check that the query can be built."""
        if self._query_type not in QueryType:
            raise QueryFactoryException(tr('Wrong query type'))

        if len(self._osm_objects) < 1:
            raise QueryFactoryException(tr('OSM object required'))

        for osmObject in self._osm_objects:
            if osmObject not in ALL_OSM_TYPES:
                raise QueryFactoryException(tr('Wrong OSM object'))

        if self._query_type == QueryType.AroundNominatimPlace and not self._distance_around:
            raise QueryFactoryException(tr('No distance provided with "around".'))

        nominatim = [
            QueryType.InNominatimPlace, QueryType.AroundNominatimPlace]
        if self._query_type in nominatim and not self._nominatim_place:
            raise QueryFactoryException(tr('Nominatim place required.'))

    @staticmethod
    def get_pretty_xml(query):
        """Helper to get a good indentation of the query."""
        xml = parseString(query)
        return xml.toprettyxml()

    @staticmethod
    def replace_template(query):
        """Add some templates tags to the query {{ }}."""
        query = re.sub(
            r' area_coords="(.*?)"', r' {{geocodeCoords:\1}}', query)
        query = re.sub(
            r' area="(.*?)"', r' {{geocodeArea:\1}}', query)
        query = query.replace(' bbox="custom"', ' {{bbox}}')
        return query

    def generate_xml(self):
        """Generate the XML."""
        query = '<osm-script output="%s" timeout="%s">' % \
                (self._output, self._timeout)

        # Nominatim might be a list of places or a single place, or not defined
        if self._nominatim_place:
            nominatim = [
                name.strip() for name in self._nominatim_place.split(';')]
        else:
            nominatim = None

        if nominatim and self._query_type != QueryType.AroundNominatimPlace:

            for i, one_place in enumerate(nominatim):
                query += '<id-query area="%s" into="area_%s"/>' % (one_place, i)

        query += '<union>'

        loop = 1 if not nominatim else len(nominatim)

        for osm_object in self._osm_objects:
            for i in range(0, loop):
                query += '<query type="%s">' % osm_object.value
                if self._key:
                    query += '<has-kv k="%s" ' % self._key
                    if self._value:
                        query += 'v="%s"' % self._value

                    query += '/>'

                if self._nominatim_place and self._query_type != QueryType.AroundNominatimPlace:
                    query += '<area-query from="area_%s" />' % i

                elif self._nominatim_place and self._query_type == QueryType.AroundNominatimPlace:
                    query += '<around area_coords="%s" radius="%s" />' % \
                             (nominatim[i], self._distance_around)

                elif self._query_type == QueryType.BBox:
                    query = '%s<bbox-query bbox="custom" />' % query

                query += '</query>'

        query += '</union>'
        query += '<union>'
        query += '<item />'
        query += '<recurse type="down"/>'
        query += '</union>'
        query += '<print mode="%s" />' % self._print_mode
        query += '</osm-script>'

        return query

    def make(self):
        """Make the query.

        @return: query
        @rtype: str
        """
        self._check_parameters()
        query = self.generate_xml()

        # get_pretty_xml works only with a valid XML, no template {{}}
        # So we replace fake XML after
        query = QueryFactory.get_pretty_xml(query)

        # get_pretty_xml add on XML header, let's remove the first line
        query = '\n'.join(query.split('\n')[1:])

        query = QueryFactory.replace_template(query)
        query = query.replace('	', '    ')

        return query
