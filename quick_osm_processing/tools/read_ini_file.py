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
from processing.core.GeoAlgorithm import GeoAlgorithm

from QuickOSM.quick_osm_processing import *
from QuickOSM.core.file_query import FileQuery


class ReadIniFileGeoAlgorithm(GeoAlgorithm):
    """
    Read an INI file.
    """

    def __init__(self):
        self.INI_FILE = 'QUERY_FILE'
        self.LAYERS = ['multipolygons', 'multilinestrings', 'lines', 'points']
        self.WHITE_LIST = {}

        for layer in self.LAYERS:
            self.WHITE_LIST[layer] = 'WHITE_LIST_' + layer

        GeoAlgorithm.__init__(self)

    def defineCharacteristics(self):
        self.name = "Read an ini file"
        self.group = "Tools"

        self.addParameter(
            ParameterFile(
                self.INI_FILE,
                'Query file (ini)',
                False,
                False))

        for layer in self.LAYERS:
            self.addOutput(
                OutputString(
                    self.WHITE_LIST[layer],
                    'White list ' + layer + ' layer'))

        self.addOutput(OutputString('QUERY_STRING', "Query string"))

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
        progress.setInfo("Reading the ini file")

        file_path = self.getParameterValue(self.INI_FILE)
        ini_file = FileQuery(file_path)
        ini_dict = None
        if ini_file.isValid():
            ini_dict = ini_file.getContent()

        self.setOutputValue('QUERY_STRING', ini_dict['metadata']['query'])

        for layer in self.LAYERS:
            csv = ini_dict['layers'][layer]['columns']
            self.setOutputValue(self.WHITE_LIST[layer], csv)
