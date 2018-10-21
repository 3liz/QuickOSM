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

from qgis.PyQt.QtCore import QUrl, QUrlQuery

from QuickOSM.core.api.nominatim import Nominatim
from QuickOSM.definitions.overpass import OVERPASS_SERVERS
from QuickOSM.core.exceptions import (
    QueryNotSupported, QueryFactoryException)


class QueryPreparation:

    """Prepare the query before sending it to Overpass."""

    def __init__(
            self, query, extent=None, nominatim_place=None,
            overpass=None, output_format='xml'):
        """Constructor.

        :param query: The query to prepare.
        :type query: str

        :param extent: The extent to use in 4326, if needed. It can be None.
        :type extent: QgsRectangle

        :param nominatim_place: A name or a list of place names.
        :type nominatim_place: str, list(str)
        """
        if overpass is None:
            self._overpass = OVERPASS_SERVERS[0]
        else:
            self._overpass = overpass

        self._query = query
        self._query_prepared = query
        self._extent = extent
        self._nominatim_places = nominatim_place
        self._output_format = output_format

        self._query_is_ready = False

    @property
    def query(self):
        """The original query.

        :return: The original query.
        :rtype: str
        """
        return self._query

    @property
    def final_query(self):
        """The generated query or None if it's not yet generated.

        :return: The final query.
        :rtype: str
        """
        if self._query_is_ready:
            return self._query_prepared
        else:
            return None

    def is_oql_query(self):
        """Return if the query is written in OQL or not.

        :return: If the it's OQL query.
        :rtype: bool
        """
        return self._query[-1] == ';'

    def is_compatible(self):
        """The plugin doesn't support all special tags like Overpass Turbo.

        :return: A tuple (bool, reason).
        :rtype: tuple
        """
        # token to look for, error returned to the user
        incompatible_queries = {
            'geometry="center"': 'center',
            'out center;': 'center',
            '{{style': '{{style}}',
            '{{data': '{{data}}',
            '{{date': '{{date}}',
            '{{geocodeId:': '{{geocodeId:}}',
            '{{geocodeBbox:': '{{geocodeBbox:}}',
        }

        for expression, error in incompatible_queries.items():
            if re.search(expression, self._query):
                return False, error

        return True, None

    def _replace_center(self):
        """Replace {{center}} by the centroid of the extent if needed.

        The temporary query will be updated.
        """
        template = r'{{center}}'
        if not re.search(template, self._query_prepared):
            return
        else:
            if self._extent is None:
                raise QueryFactoryException('Missing extent parameter')

        y = self._extent.center().y()
        x = self._extent.center().x()
        if self.is_oql_query():
            new_string = '{},{}'.format(y, x)
        else:
            new_string = 'lat="{}" lon="{}"'.format(y, x)

        self._query_prepared = (
            re.sub(template, new_string, self._query_prepared))

    def replace_bbox(self):
        """Replace {{bbox}} by the extent BBOX if needed.

        The temporary query will be updated.
        """
        template = r'{{bbox}}'
        if not re.search(template, self._query_prepared):
            return
        else:
            if self._extent is None:
                raise QueryFactoryException('Missing extent parameter')

        y_min = self._extent.yMinimum()
        y_max = self._extent.yMaximum()
        x_min = self._extent.xMinimum()
        x_max = self._extent.xMaximum()

        if self.is_oql_query():
            new_string = '{},{},{},{}'.format(y_min, x_min, y_max, x_max)
        else:
            new_string = 'e="{}" n="{}" s="{}" w="{}"'.format(
                x_max, y_max, y_min, x_min)
        self._query_prepared = (
            re.sub(template, new_string, self._query_prepared))

    def _replace_geocode_coords(self):
        """Replace {{geocodeCoords}} by the centroid of the extent.

        The temporary query will be updated.
        """
        def replace(catch, default_nominatim):

            if default_nominatim:
                search = default_nominatim
            else:
                search = catch

            nominatim = Nominatim()
            lon, lat = nominatim.get_first_point_from_query(search)

            if self.is_oql_query():
                new_string = '{},{}'.format(lat, lon)
            else:
                new_string = 'lat="{}" lon="{}"'.format(lat, lon)

            return new_string

        template = r'{{(geocodeCoords):([^}]*)}}'
        self._query_prepared = re.sub(
            template, lambda m: replace(
                m.groups()[1], self._nominatim_places), self._query_prepared)

    def _replace_geocode_area(self):
        """Replace {{geocodeCoords}} by the centroid of the extent.

        The temporary query will be updated.
        """
        def replace(catch, default_nominatim):

            if default_nominatim:
                search = default_nominatim
            else:
                search = catch

            # if the result is already a number, it's a relation ID.
            # we don't perform a nominatim query
            if search.isdigit():
                osm_id = search
            else:
                # We perform a nominatim query
                nominatim = Nominatim()
                osm_id = nominatim.get_first_polygon_from_query(search)

            area = int(osm_id) + 3600000000

            if self.is_oql_query():
                new_string = 'area({})'.format(area)
            else:
                new_string = 'ref="{}" type="area"'.format(area)

            return new_string

        template = r'{{(nominatimArea|geocodeArea):([^}]*)}}'
        self._query_prepared = re.sub(template, lambda m: replace(
            m.groups()[1], self._nominatim_places), self._query_prepared)

        return self._query_prepared

    def clean_query(self):
        """Remove extra characters that might be present in the query.

        The temporary query will be updated.
        """
        query = self._query_prepared.strip()

        # Correction of ; in the OQL at the end
        self._query_prepared = re.sub(r';;$', ';', query)

    def prepare_query(self):
        """Prepare the query before sending it to Overpass.

        The temporary query will be updated.

        :return: The final query.
        :rtype: basestring
        """
        result, error = self.is_compatible()
        if not result:
            raise QueryNotSupported(error)

        self.clean_query()
        self.replace_bbox()
        self._replace_center()
        self._replace_geocode_area()
        self._replace_geocode_coords()

        self._query_is_ready = True
        return self._query_prepared

    def prepare_url(self):
        """Prepare a query to be as an URL.

        :return: The URL encoded with the query.
        :rtype: basestring
        """
        if not self._query_prepared:
            return ''

        if self._output_format:
            query = re.sub(
                r'output="[a-z]*"',
                'output="%s"' % self._output_format,
                self._query_prepared)
            query = re.sub(
                r'\[out:[a-z]*',
                '[out:%s' % self._output_format,
                query)
        else:
            query = self._query_prepared

        url_query = QUrl(self._overpass)
        query_string = QUrlQuery()
        query_string.addQueryItem('data', query)
        query_string.addQueryItem('info', 'QgisQuickOSMPlugin')
        url_query.setQuery(query_string)
        return url_query.toString()
