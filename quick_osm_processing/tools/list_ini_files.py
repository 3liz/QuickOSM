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
from QuickOSM.core.utilities.tools import get_user_query_folder


class ListIniFilesGeoAlgorithm(GeoAlgorithm):
    """
    List all the INI files.
    """

    def __init__(self):
        self.NAME_FILE = 'NAME'
        self.OUTPUT_INI = 'INI'

        self.__queries = {}
        self.__names = []

        GeoAlgorithm.__init__(self)

    def defineCharacteristics(self):
        self.name = "Queries available"
        self.group = "Tools"

        # Get the folder and all files queries
        folder = get_user_query_folder()
        cat_files = FileQuery.get_ini_files_from_folder(folder, force=False)

        for cat in cat_files:
            for query in cat_files[cat]:
                self.__queries[cat + " : " + query.getName()] = query

        self.__names = list(self.__queries.keys())

        self.addParameter(
            ParameterSelection(
                self.NAME_FILE,
                'Queries available',
                self.__names))

        self.addOutput(OutputString(self.OUTPUT_INI, "Ini filepath as string"))

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

        index = self.getParameterValue(self.NAME_FILE)
        for query in self.__queries:
            if query == self.__names[index]:
                path = self.__queries[query].getFilePath()
                self.setOutputValue(self.OUTPUT_INI, path)
