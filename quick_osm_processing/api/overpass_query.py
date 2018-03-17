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

from os.path import isfile, join, basename, dirname, abspath

from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtGui import QIcon
from qgis.utils import iface
from qgis.core import (
    QgsGeometry,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsRectangle)
from processing.core.GeoAlgorithm import GeoAlgorithm

from QuickOSM.quick_osm_processing import *
from QuickOSM.core.api.connexion_oapi import ConnexionOAPI
from QuickOSM.core.query_parser import prepare_query


class OverpassQueryGeoAlgorithm(GeoAlgorithm):
    """
    Perform an OverPass query and get an OSM file.
    """

    SERVER = 'SERVER'
    QUERY_STRING = 'QUERY_STRING'
    EXTENT = 'EXTENT'
    NOMINATIM = 'NOMINATIM'
    OUTPUT_FILE = 'OUTPUT_FILE'

    def defineCharacteristics(self):
        self.name = "Query overpass API with a string"
        self.group = "API"

        self.addParameter(
            ParameterString(
                self.SERVER,
                'Overpass API',
                'http://overpass-api.de/api/',
                False,
                False))
        self.addParameter(
            ParameterString(
                self.QUERY_STRING,
                'Query (XML or OQL)',
                '',
                True,
                False))
        self.addParameter(
            ParameterExtent(
                self.EXTENT,
                'If {{bbox}} in the query, extent (0,0,0,0 is a wrong value)',
                default="0,0,0,0"))
        self.addParameter(
            ParameterString(
                self.NOMINATIM,
                'If {{nominatim}} in the query, place',
                '',
                False,
                True))

        self.addOutput(OutputFile(self.OUTPUT_FILE, 'OSM file'))

    def help(self):
        locale = QSettings().value("locale/userLocale")[0:2]
        locale += "."

        current_file = __file__
        if current_file.endswith('pyc'):
            current_file = current_file[:-1]
        current_file = basename(current_file)

        helps = [current_file + locale + ".html", current_file + ".html"]

        doc_path = join(dirname(dirname(dirname(abspath(__file__)))), 'doc')
        for helpFileName in helps:
            file_help_path = join(doc_path, helpFileName)
            if isfile(file_help_path):
                return False, file_help_path

        return False, None

    def getIcon(self):
        return QIcon(dirname(__file__) + '/../../icon.png')

    def processAlgorithm(self, progress):
        progress.setInfo("Preparing the Overpass query")
        progress.setPercentage(0)

        server = self.getParameterValue(self.SERVER)
        query = self.getParameterValue(self.QUERY_STRING)
        nominatim = self.getParameterValue(self.NOMINATIM)

        # Extent of the layer
        extent = self.getParameterValue(self.EXTENT)
        if extent != "0,0,0,0":
            # x_min, x_max, y_min, y_max
            extent = [float(i) for i in extent.split(',')]
            # noinspection PyCallByClass
            geometry_extent = QgsGeometry.fromRect(
                QgsRectangle(extent[0], extent[2], extent[1], extent[3]))
            source_crs = iface.mapCanvas().mapRenderer().destinationCrs()
            crs_transform = QgsCoordinateTransform(
                source_crs, QgsCoordinateReferenceSystem("EPSG:4326"))
            geometry_extent.transform(crs_transform)
            extent = geometry_extent.boundingBox()
        else:
            extent = None

        if nominatim == "":
            nominatim = None

        # Make some transformation on the query ({{box}}, Nominatim, ...
        query = prepare_query(query, extent, nominatim)

        overpass_api = ConnexionOAPI(url=server, output="xml")
        progress.setInfo("Downloading data from Overpass")
        progress.setPercentage(5)
        osm_file = overpass_api.get_file_from_query(query)

        # Set the output file for Processing
        progress.setPercentage(100)
        self.setOutputValue(self.OUTPUT_FILE, osm_file)
