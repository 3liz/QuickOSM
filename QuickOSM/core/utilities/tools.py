"""Tools for QuickOSM."""

import io
import platform
import sys

from os import mkdir
from os.path import abspath, isdir, isfile, join

from qgis.core import QgsApplication, QgsSettings
from qgis.PyQt.QtCore import QDir

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


def custom_config_file() -> str:
    """Get the custom config file or None."""
    filepath = join(quickosm_user_folder(), 'custom_config.json')
    if isfile(filepath):
        return filepath


def nominatim_file() -> str:
    """Get the nominatim history file."""
    path = join(quickosm_user_folder(), 'nominatim.txt')
    if not path or not isfile(path):
        io.open(path, 'a').close()

    return path


def query_historic() -> str:
    """Get the query history folder"""
    path = join(quickosm_user_folder(), 'query_history')
    if not isdir(path):
        mkdir(path)

    return path


def query_preset() -> str:
    """Get the query preset folder"""
    path = join(quickosm_user_folder(), 'query_preset')
    if not isdir(path):
        mkdir(path)

    return path


def get_default_encoding() -> str:
    """Get the default encoding."""
    if platform.system() == 'Windows':
        return sys.getdefaultencoding()

    return 'UTF-8'


def quickosm_user_folder() -> str:
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


def get_setting(key: str, default: str = None) -> str:
    """Get a value in the QgsSettings.

    :param key: The key to fetch in the QgsSettings
    :type key: basestring

    :param default: The default value if the key is not found.
    :type default: basestring

    :return: The value or the default value.
    :rtype: basestring
    """
    q_setting = QgsSettings()
    prefix = '/QuickOSM/'
    value = q_setting.value(prefix + key)

    if value:
        return value

    return default


def set_setting(key: str, value: str) -> bool:
    """
    Set a value in the QgsSettings
    @param key: key
    @type key: str

    @param value: value
    @type value: str

    @return: result
    @rtype: bool
    """
    q_setting = QgsSettings()
    prefix = '/QuickOSM/'
    return q_setting.setValue(prefix + key, value)
