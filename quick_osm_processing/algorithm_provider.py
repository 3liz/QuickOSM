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
from __future__ import absolute_import

from processing.core.AlgorithmProvider import AlgorithmProvider
from qgis.PyQt.QtGui import QIcon

from .api.nominatim_query import NominatimQueryGeoAlgorithm
from .api.overpass_query import OverpassQueryGeoAlgorithm
from .parser.osm_member_parser import OsmMemberParserGeoAlgorithm
from .parser.osm_parser import OsmParserGeoAlgorithm
from .parser.osm_relation_parser import OsmRelationParserGeoAlgorithm
from .tools.get_first_field import GetFirstFieldGeoAlgorithm
from .tools.list_ini_files import ListIniFilesGeoAlgorithm
from .tools.query_factory import QueryFactoryGeoAlgorithm
from .tools.read_ini_file import ReadIniFileGeoAlgorithm
from .tools.read_ini_file_path import ReadIniFilePathGeoAlgorithm


class QuickOSMAlgorithmProvider(AlgorithmProvider):
    """
    QuickOSM provides some GeoAlgorithms
    """

    def __init__(self):
        AlgorithmProvider.__init__(self)

        self.activate = True

        # Load algorithms
        self.alglist = [
            OverpassQueryGeoAlgorithm(),
            NominatimQueryGeoAlgorithm(),
            OsmParserGeoAlgorithm(),
            ReadIniFileGeoAlgorithm(),
            ReadIniFilePathGeoAlgorithm(),
            ListIniFilesGeoAlgorithm(),
            QueryFactoryGeoAlgorithm(),
            OsmMemberParserGeoAlgorithm(),
            OsmRelationParserGeoAlgorithm(),
            GetFirstFieldGeoAlgorithm()
            ]

        for alg in self.alglist:
            alg.provider = self

    def initializeSettings(self):
        AlgorithmProvider.initializeSettings(self)

    def unload(self):
        AlgorithmProvider.unload(self)

    def getName(self):
        return 'QuickOSM'

    def getDescription(self):
        return 'QuickOSM'

    def getIcon(self):
        return QIcon(":/plugins/QuickOSM/icon.png")

    def _loadAlgorithms(self):
        self.algs = self.alglist

    def getSupportedOutputTableExtensions(self):
        return ['csv']
