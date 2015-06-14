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

from CoreQuickOSM.API.Nominatim import Nominatim


def is_oql(query):
    return True if query[-1] == ";" else False


def replace_center(extent, query):
    template = r'{{center}}'
    if not re.search(template, query):
        return query

    y = extent.center().y()
    x = extent.center().x()
    if is_oql(query):
        new_string = '%s,%s' % (y, x)
    else:
        new_string = 'lat="%s" lon="%s"' % (y, x)

    query = re.sub(template, new_string, query)
    return query


def replace_bbox(extent, query):
    template = r'{{bbox}}'
    if not re.search(template, query):
        return query

    y_min = extent.yMinimum()
    y_max = extent.yMaximum()
    x_min = extent.xMinimum()
    x_max = extent.xMaximum()

    if is_oql(query):
        new_string = '%s,%s,%s,%s' % (y_min, x_min, y_max, x_max)
    else:
        new_string = 'e="%s" n="%s" s="%s" w="%s"' % \
                     (x_max, y_max, y_min, x_min)
    query = re.sub(template, new_string, query)
    return query


def replace_geocode_coords(nominatim_name, query):
    template = r'{{(geocodeCoords):(.*)}}'
    nominatim_query = re.search(template, query)
    if not nominatim_query:
        return query

    result = nominatim_query.groups()
    search = result[1]

    if nominatim_name:
        search = nominatim_name

    nominatim = Nominatim()
    lon, lat = nominatim.get_first_point_from_query(search)

    if is_oql(query):
        new_string = '%s,%s' % (lat, lon)
    else:
        new_string = 'lat="%s" lon="%s"' % (lat, lon)

    query = re.sub(template, new_string, query)
    return query


def replace_geocode_area(nominatim_name, query):
    template = r'{{(nominatimArea|geocodeArea):(.*)}}'
    nominatim_query = re.search(template, query)
    if not nominatim_query:
        return query

    result = nominatim_query.groups()
    search = result[1]

    if nominatim_name:
        search = nominatim_name

    # if the result is already a number, it's a relation ID.
    # we don't perform a nominatim query
    if search.isdigit():
        osm_id = search
    else:
        # We perform a nominatim query
        nominatim = Nominatim()
        osm_id = nominatim.get_first_polygon_from_query(search)

    area = int(osm_id) + 3600000000

    if is_oql(query):
        new_string = 'area(%s)' % area
    else:
        new_string = 'ref="%s" type="area"' % area

    query = re.sub(template, new_string, query)
    return query


def clean_query(query):
    query = query.strip()

    # Correction of ; in the OQL at the end
    query = re.sub(r';;$', ';', query)
    return query


def prepare_query(query, extent=None, nominatim_name=None):
    """Prepare the query before sending it to Overpass.

    @param query: the query, in XML or OQL
    @type query: str

    @param extent: the extent
    @type extent: QgsRectangle

    @param nominatim_name: the city, town ...
    @type nominatim_name: str

    @return: the final query
    @rtype: str
    """

    query = clean_query(query)
    query = replace_geocode_area(nominatim_name, query)
    query = replace_geocode_coords(nominatim_name, query)
    query = replace_bbox(extent, query)
    query = replace_center(extent, query)

    return query
