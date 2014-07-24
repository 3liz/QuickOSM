# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
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

from processing.core.AlgorithmProvider import AlgorithmProvider
from processing.core.ProcessingConfig import Setting, ProcessingConfig
from API.OverpassQueryGeoAlgorithm import OverpassQueryGeoAlgorithm
from API.XapiQueryGeoAlgorithm import XapiQueryGeoAlgorithm
from API.NominatimQueryGeoAlgorithm import NominatimQueryGeoAlgorithm
from Tools.ListIniFilesGeoAlgorithm import ListIniFilesGeoAlgorithm
from Tools.ReadIniFileGeoAlgorithm import ReadIniFileGeoAlgorithm
from Tools.ReadIniFilePathGeoAlgorithm import ReadIniFilePathGeoAlgorithm
from Tools.QueryFactoryGeoAlgorithm import QueryFactoryGeoAlgorithm
from Parser.OsmParserGeoAlgorithm import OsmParserGeoAlgorithm
from Tools.GetFirstFieldGeoAlgorithm import GetFirstFieldGeoAlgorithm
from PyQt4.QtGui import QIcon
from os.path import dirname,abspath,join


class QuickOSMAlgorithmProvider(AlgorithmProvider):
    '''
    QuickOSM provide some GeoAlgorithms
    '''

    QUERIES_FOLDER = 'QUERIES_FOLDER'

    def __init__(self):
        AlgorithmProvider.__init__(self)

        self.activate = True

        # Load algorithms
        self.alglist = [OverpassQueryGeoAlgorithm(),
                        NominatimQueryGeoAlgorithm(),
                        OsmParserGeoAlgorithm(),
                        XapiQueryGeoAlgorithm(),
                        ReadIniFileGeoAlgorithm(),
                        ReadIniFilePathGeoAlgorithm(),
                        ListIniFilesGeoAlgorithm(),
                        QueryFactoryGeoAlgorithm(),
                        GetFirstFieldGeoAlgorithm()
                        ]
        
        for alg in self.alglist:
            alg.provider = self

    def initializeSettings(self):
        AlgorithmProvider.initializeSettings(self)
        directory = join(dirname(dirname(abspath(__file__))),'queries')       
        ProcessingConfig.addSetting(Setting(self.getDescription(),self.QUERIES_FOLDER,'Queries folder',directory))

    def unload(self):
        AlgorithmProvider.unload(self)
        ProcessingConfig.removeSetting(self.QUERIES_FOLDER)

    def getName(self):
        return 'QuickOSM'

    def getDescription(self):
        return 'QuickOSM'

    def getIcon(self):
        return QIcon(dirname(dirname(abspath(__file__)))+"/icon.png")
    
    def _loadAlgorithms(self):
        self.algs = self.alglist
