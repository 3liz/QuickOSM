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
import configparser
from os.path import join, dirname, abspath, pardir

from QuickOSM.core.utilities.operating_system import copy_tree
from qgis.PyQt.QtCore import QDir, QSettings
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsApplication


def tr(text):
    return QApplication.translate('@default', text)


def read_metadata(section, item):
    root = dirname(dirname(dirname(__file__)))
    metadata = join(root, 'metadata.txt')
    parser = configparser.ConfigParser()
    parser.read(metadata)
    return parser.get(section, item)


def get_current_version():
    return read_metadata('general', 'version')


def new_queries_available():
    status = read_metadata('general', 'newQueries')
    if status == 'True':
        return True
    else:
        return False


def quickosm_user_folder():
    """
    Get the user folder, ~/.qgis2/QuickOSM on linux for instance

    @rtype: str
    @return: path
    """
    return abspath(join(QgsApplication.qgisSettingsDirPath(), 'QuickOSM'))


def resources_path(*args):
    """Get the path to our resources folder.

    .. versionadded:: 1.5.3

    Note that in version 1.5.3 we removed the use of Qt Resource files in
    favour of directly accessing on-disk resources.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: str

    :return: Absolute path to the resources folder.
    :rtype: str
    """
    path = dirname(dirname(__file__))
    path = abspath(join(path, pardir, 'resources'))
    for item in args:
        path = abspath(join(path, item))

    return path


def get_user_query_folder(over_write=False):
    """
    Get the user folder for queries.
    For instance on linux : ~/.qgis2/QuickOSM/queries

    @rtype: str
    @return: path
    """
    folder = quickosm_user_folder()
    queries_folder = join(folder, 'queries')
    if not QDir(queries_folder).exists() or over_write:
        folder = join(dirname(dirname(dirname(abspath(__file__)))), 'queries')
        copy_tree(folder, QDir.toNativeSeparators(queries_folder))
    return str(QDir.toNativeSeparators(queries_folder))


def get_setting(key, default=None):
    """Get a value in the QSettings.

    :param key: The key to fetch in the QSettings
    :type key: basestring

    :param default: The default value if the key is not found.
    :type default: basestring

    :return: The value or the default value.
    :rtype: basestring
    """
    qs = QSettings()
    prefix = '/QuickOSM/'
    value = qs.value(prefix + key)

    if value:
        return value
    else:
        return default


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
