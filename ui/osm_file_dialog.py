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

from os.path import isdir, dirname, abspath, join, isfile

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QFileDialog, QApplication, QDockWidget
from qgis.core import QgsProject

from QuickOSM.core.utilities.tools import tr
from QuickOSM.core.exceptions import (
    QuickOsmException,
    OutPutGeomTypesException,
    FileDoesntExistException,
    DirectoryOutPutException,
    GDALVersion,
    OsmDriverNotFound)
from QuickOSM.core.utilities.utilities_qgis import \
    is_osm_driver_enabled, is_ogr_version_ok
from QuickOSM.core.parser.osm_parser import OsmParser
from QuickOSM.controller.process import open_file
from .QuickOSMWidget import QuickOSMWidget
from .osm_file import Ui_ui_osm_file


class OsmFileWidget(QuickOSMWidget, Ui_ui_osm_file):
    # noinspection PyUnresolvedReferences
    def __init__(self, parent=None):
        """
        OsmFileWidget constructor
        """
        QuickOSMWidget.__init__(self, parent)
        self.setupUi(self)

        # Set UI
        self.radioButton_osmConf.setChecked(False)
        self.label_progress.setText("")
        self.lineEdit_filePrefix.setDisabled(True)

        # Set default osm conf
        self.defaultOsmConf = join(
            dirname(dirname(abspath(__file__))), 'osmconf.ini')
        if not isfile(self.defaultOsmConf):
            self.defaultOsmConf = ''
        self.lineEdit_osmConf.setText(self.defaultOsmConf)
        self.pushButton_runQuery.setEnabled(False)

        # Connect
        self.pushButton_browseOsmFile.clicked.connect(self.set_osm_file_path)
        self.pushButton_browseOsmConf.clicked.connect(self.set_osm_conf_path)
        self.lineEdit_osmConf.textEdited.connect(self.disable_run_button)
        self.lineEdit_osmFile.textEdited.connect(self.disable_run_button)
        self.radioButton_osmConf.toggled.connect(self.disable_run_button)
        self.pushButton_runQuery.clicked.connect(self.open_file)
        self.pushButton_resetIni.clicked.connect(self.reset_ini)
        self.lineEdit_browseDir.textEdited.connect(self.disable_prefix_file)

    def set_osm_file_path(self):
        """
        Fill the osm file
        """
        osm_file, __ = QFileDialog.getOpenFileName(
            parent=None,
            caption=tr("QuickOSM", 'Select *.osm or *.pbf'),
            filter="OSM file (*.osm *.pbf)")
        self.lineEdit_osmFile.setText(osm_file)
        self.disable_run_button()

    def set_osm_conf_path(self):
        """
        Fill the osmConf file
        """
        osm_conf, __ = QFileDialog.getOpenFileName(
            parent=None,
            caption=tr("QuickOSM", 'Select osm conf'),
            filter="OsmConf file (*.ini)")
        if osm_conf:
            self.lineEdit_osmConf.setText(osm_conf)
        self.disable_run_button()

    def reset_ini(self):
        """
        Reset the default osmConf file
        """
        self.lineEdit_osmConf.setText(self.defaultOsmConf)

    def disable_run_button(self):
        """
        If the two fields are empty or allTags
        """
        if self.lineEdit_osmFile.text():
            self.pushButton_runQuery.setEnabled(False)

        if self.radioButton_osmConf.isChecked():
            if self.lineEdit_osmConf.text():
                self.pushButton_runQuery.setEnabled(True)
            else:
                self.pushButton_runQuery.setEnabled(False)
        else:
            self.pushButton_runQuery.setEnabled(True)

    def open_file(self):
        """
        Open the osm file with the osmconf
        """

        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.start_process()
        QApplication.processEvents()

        # Get fields
        osm_file = self.lineEdit_osmFile.text()
        osm_conf = self.lineEdit_osmConf.text()
        output_directory = self.lineEdit_browseDir.text()
        prefix_file = self.lineEdit_filePrefix.text()
        load_only = self.radioButton_osmConf.isChecked()

        # Which geometry at the end ?
        output_geometry_types = self.get_output_geometry_types()

        try:
            if not output_geometry_types:
                raise OutPutGeomTypesException

            if not isfile(osm_file):
                raise FileDoesntExistException(suffix="*.osm or *.pbf")

            if load_only:
                if not isfile(osm_conf):
                    raise FileDoesntExistException(suffix="*.ini")

            if output_directory and not isdir(output_directory):
                raise DirectoryOutPutException

            # Check OGR
            if not is_ogr_version_ok():
                raise GDALVersion

            if not is_osm_driver_enabled():
                raise OsmDriverNotFound

            if load_only:
                osm_parser = OsmParser(
                    osm_file,
                    load_only=True,
                    osm_conf=osm_conf,
                    layers=output_geometry_types)
                layers = osm_parser.parse()

                for item in list(layers.values()):
                    QgsProject.instance().addMapLayer(item)

            else:
                open_file(
                    dialog=self,
                    osm_file=osm_file,
                    output_geom_types=output_geometry_types,
                    output_dir=output_directory,
                    prefix_file=prefix_file)

        except QuickOsmException as e:
            self.display_geo_algorithm_exception(e)
        except Exception as e:  # pylint: disable=broad-except
            self.display_exception(e)
        finally:
            QApplication.restoreOverrideCursor()
            self.end_process()
            QApplication.processEvents()


class OsmFileDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self, parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(OsmFileWidget())
        self.setWindowTitle(tr("ui_osm_file", "QuickOSM - OSM File"))
