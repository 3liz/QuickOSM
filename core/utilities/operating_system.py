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

import platform
import sys
from shutil import copy2, copystat, Error, WindowsError
from exceptions import OSError
from os import listdir, makedirs, readlink, symlink
from os.path import join, isdir, islink

from PyQt4.QtCore import QSettings
from PyQt4.QtNetwork import QNetworkProxy


def get_proxy():
    """
    Get a proxy according to QSettings
    @return: proxy
    @rtype: QNetworkProxy
    """
    s = QSettings()
    if s.value('proxy/proxyEnabled', '') == 'true':

        proxy_type = s.value('proxy/proxyType', '')
        proxy_host = s.value('proxy/proxyHost', '')
        proxy_port = s.value('proxy/proxyPort', '')
        proxy_user = s.value('proxy/proxyUser', '')
        proxy_password = s.value('proxy/proxyPassword', '')

        proxy = QNetworkProxy()

        if proxy_type == 'DefaultProxy':
            proxy.setType(QNetworkProxy.DefaultProxy)
        elif proxy_type == 'Socks5Proxy':
            proxy.setType(QNetworkProxy.Socks5Proxy)
        elif proxy_type == 'HttpProxy':
            proxy.setType(QNetworkProxy.HttpProxy)
        elif proxy_type == 'HttpCachingProxy':
            proxy.setType(QNetworkProxy.HttpCachingProxy)
        elif proxy_type == 'FtpCachingProxy':
            proxy.setType(QNetworkProxy.FtpCachingProxy)

        proxy.setHostName(proxy_host)
        proxy.setPort(int(proxy_port))
        proxy.setUser(proxy_user)
        proxy.setPassword(proxy_password)
        return proxy
    else:
        return None


def copy_tree(src, dst, symlinks=False, ignore=None):
    names = listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    if not isdir(dst):  # This one line does the trick
        makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        source_name = join(src, name)
        destination_name = join(dst, name)
        try:
            if symlinks and islink(source_name):
                link_to = readlink(source_name)
                symlink(link_to, destination_name)
            elif isdir(source_name):
                copy_tree(source_name, destination_name, symlinks, ignore)
            else:
                # Will raise a SpecialFileError for unsupported file types
                copy2(source_name, destination_name)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error, err:
            errors.extend(err.args[0])
        except EnvironmentError, why:
            errors.append((source_name, destination_name, str(why)))
    try:
        copystat(src, dst)
    except OSError, why:
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying file access times may fail on Windows
            pass
        else:
            errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)


def is_windows():
    return True if platform.system() == 'Windows' else False


def get_default_encoding():
    if is_windows():
        return sys.getdefaultencoding()
    else:
        return 'UTF-8'
