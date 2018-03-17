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

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QSettings
from processing.core.GeoAlgorithm import GeoAlgorithm

from QuickOSM.quick_osm_processing import *
from QuickOSM.core.api.nominatim import Nominatim
from QuickOSM.core.exceptions import NominatimAreaException


class NominatimQueryGeoAlgorithm(GeoAlgorithm):

    SERVER = 'SERVER'
    NOMINATIM_STRING = 'NOMINATIM_STRING'
    OSM_ID = 'OSM_ID'

    def defineCharacteristics(self):
        self.name = 'Query nominatim API with a string'
        self.group = 'API'

        self.addParameter(
            ParameterString(
                self.SERVER,
                'Nominatim server',
                'http://nominatim.openstreetmap.org/search?format=json',
                False,
                False))
        self.addParameter(
            ParameterString(
                self.NOMINATIM_STRING,
                'Search',
                '',
                False,
                False))
        self.addOutput(OutputNumber(self.OSM_ID, 'OSM id'))

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

        server = self.getParameterValue(self.SERVER)
        query = self.getParameterValue(self.NOMINATIM_STRING)

        nominatim = Nominatim(url=server)
        try:
            osm_id = nominatim.get_first_polygon_from_query(query)
            progress.setInfo(
                "Getting first OSM relation ID from Nominatim :", osm_id)
        except:
            raise NominatimAreaException

        self.setOutputValue("OSM_ID", osm_id)
