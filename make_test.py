'''
Created on 17 juin 2014

@author: etienne
'''

# According http://snorf.net/blog/2014/01/04/writing-unit-tests-for-qgis-python-plugins/

from qgis.core import *
from qgis.gui import *

from PyQt4 import QtCore, QtGui, QtTest

import unittest

QgsApplication.setPrefixPath("/usr/local", True)
QgsApplication.initQgis()

if len(QgsProviderRegistry.instance().providerList()) == 0:
    raise RuntimeError('No data providers available.')

QgsApplication.exitQgis()
