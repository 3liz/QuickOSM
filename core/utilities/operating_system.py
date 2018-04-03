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
from os import listdir, makedirs, stat
from os.path import join, isdir, exists
from shutil import copytree, copy2


def copy_tree(src, dst, symlinks=False, ignore=None):
    if not exists(dst):
        makedirs(dst)
    for item in listdir(src):
        s = join(src, item)
        d = join(dst, item)
        if isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not exists(d) or stat(s).st_mtime - stat(d).st_mtime > 1:
                copy2(s, d)


def get_default_encoding():
    if platform.system() == 'Windows':
        return sys.getdefaultencoding()
    else:
        return 'UTF-8'
