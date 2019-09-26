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
import io

from os.path import join, abspath, isfile

from qgis.PyQt.QtCore import QDir
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsApplication, QgsSettings


def tr(text):
    return QApplication.translate('@default', text)


def custom_config_file():
    """Get the custom config file or None."""
    filepath = join(quickosm_user_folder(), 'custom_config.json')
    if isfile(filepath):
        return filepath
    else:
        return None


def nominatim_file():
    path = join(quickosm_user_folder(), 'nominatim.txt')
    if not path or not isfile(path):
        io.open(path, 'a').close()

    return path


def quickosm_user_folder():
    """
    Get the QuickOSM user folder.

    If the folder does not exist, it will create it.

    On Linux: .local/share/QGIS/QGIS3/profiles/default/QuickOSM

    @rtype: str
    @return: path
    """
    path = abspath(join(QgsApplication.qgisSettingsDirPath(), 'QuickOSM'))

    if not QDir(path).exists():
        QDir().mkdir(path)

    return path


def get_setting(key, default=None):
    """Get a value in the QgsSettings.

    :param key: The key to fetch in the QgsSettings
    :type key: basestring

    :param default: The default value if the key is not found.
    :type default: basestring

    :return: The value or the default value.
    :rtype: basestring
    """
    qs = QgsSettings()
    prefix = '/QuickOSM/'
    value = qs.value(prefix + key)

    if value:
        return value
    else:
        return default


def set_setting(key, value):
    """
    Set a value in the QgsSettings
    @param key: key
    @type key: str

    @param value: value
    @type value: str

    @return: result
    @rtype: bool
    """
    qs = QgsSettings()
    prefix = '/QuickOSM/'
    return qs.setValue(prefix + key, value)
