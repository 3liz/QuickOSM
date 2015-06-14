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

import ConfigParser
from os.path import join, dirname, abspath
from PyQt4.QtCore import QDir, QSettings
from PyQt4.QtGui import QApplication

from utilities_qgis import get_user_folder
from operating_system import copy_tree


def tr(section, text):
    return QApplication.translate(section, text)


def read_metadata(section, item):
    root = dirname(dirname(__file__))
    metadata = join(root, 'metadata.txt')
    parser = ConfigParser.ConfigParser()
    parser.read(metadata)
    return parser.get(section, item)


def get_current_version():
    return read_metadata('general', 'version')


def new_queries_available():
    status = read_metadata('general', 'newQueries')
    if status == u'True':
        return True
    else:
        return False


def get_user_query_folder(overwrite=False):
    """
    Get the user folder for queries.
    For instance on linux : ~/.qgis2/QuickOSM/queries

    @rtype: str
    @return: path
    """
    folder = get_user_folder()
    queries_folder = join(folder, 'queries')
    if not QDir(queries_folder).exists() or overwrite:
        folder = join(dirname(dirname(abspath(__file__))), 'queries')
        copy_tree(folder, QDir.toNativeSeparators(queries_folder))
    return unicode(QDir.toNativeSeparators(queries_folder))


def get_setting(key):
    """
    Get a value in the QSettings
    @param key: key
    @type key: str
    @return: value
    @rtype: str
    """
    qs = QSettings()
    prefix = '/QuickOSM/'
    return qs.value(prefix + key)


def set_setting(key, value):
    """
    Set a value in the QSettings
    @param key: key
    @type key: str
    @param value: value
    @type value: str
    @return: result
    @rtype: bool
    """
    qs = QSettings()
    prefix = '/QuickOSM/'
    return qs.setValue(prefix + key, value)
