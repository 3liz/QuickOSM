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
from os.path import isfile, join, basename, dirname, abspath

from PyQt4.QtCore import QSettings, SLOT
from PyQt4.QtGui import QIcon
from qgis.core import QgsVectorLayer
from processing.core.GeoAlgorithm import GeoAlgorithm

from QuickOSM.quick_osm_processing import *
from QuickOSM.core.parser.osm_parser import OsmParser


class OsmParserGeoAlgorithm(GeoAlgorithm):
    """
    Parse an OSM file with OGR and return each layer
    """

    def __init__(self):
        self.slotOsmParser = SLOT("osmParser()")

        self.FILE = 'FILE'

        self.LAYERS = ['multipolygons', 'multilinestrings', 'lines', 'points']
        self.WHITE_LIST = {}
        self.OUTPUT_LAYERS = {}
        for layer in self.LAYERS:
            self.WHITE_LIST[layer] = 'WHITE_LIST_' + layer
            self.OUTPUT_LAYERS[layer] = layer + "_LAYER"

        self.progress = None

        GeoAlgorithm.__init__(self)

    def defineCharacteristics(self):
        self.name = "OGR default"
        self.group = "OSM Parser"

        self.addParameter(ParameterFile(self.FILE, 'OSM file', False, False))

        for layer in self.LAYERS:
            self.addParameter(
                ParameterString(
                    self.WHITE_LIST[layer],
                    layer + '\'s whitelist column (csv)',
                    '',
                    False,
                    True))

            self.addOutput(
                OutputVector(
                    self.OUTPUT_LAYERS[layer],
                    'Output ' + layer + ' layer'))

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
        self.progress = progress
        self.progress.setPercentage(0)

        file_path = self.getParameterValue(self.FILE)

        # Creating the dict for columns
        white_list_values = {}
        for layer in self.LAYERS:
            value = self.getParameterValue(self.WHITE_LIST[layer])

            # Delete space and tabs in OSM keys
            # Processing return a 'None' value as unicode
            value = re.sub('\s', '', value)
            if value == '' or value == 'None':
                value = None

            if value:
                if value != ',':
                    white_list_values[layer] = value.split(',')
                else:
                    white_list_values[layer] = ','
            else:
                white_list_values[layer] = None

        # Call the OSM Parser and connect signals
        parser = OsmParser(file_path, self.LAYERS, white_list_values)
        parser.signalText.connect(self.set_info)
        parser.signalPercentage.connect(self.set_percentage)

        # Start to parse
        layers = parser.parse()

        layers_outputs = {}
        for key, values in layers.iteritems():
            layer = QgsVectorLayer(values['geojsonFile'], "test", "ogr")

            output_parameter = self.getOutputFromName(self.OUTPUT_LAYERS[key])
            layers_outputs[key] = output_parameter.getVectorWriter(
                layer.pendingFields(),
                values['geomType'],
                layer.crs())

            for feature in layer.getFeatures():
                layers_outputs[key].addFeature(feature)

    def set_info(self, text):
        self.progress.setInfo(text)

    def set_percentage(self, percent):
        self.progress.setPercentage(percent)
