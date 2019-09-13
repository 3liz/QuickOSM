from osgeo import gdal
from qgis.PyQt import Qt
from qgis.core import Qgis

"""Configuration file for PyTest."""


def pytest_report_header(config):
    message = 'QGIS : {}\n'.format(Qgis.QGIS_VERSION_INT)
    message += 'Python GDAL : {}\n'.format(gdal.VersionInfo('VERSION_NUM'))
    message += 'QT : {}'.format(Qt.QT_VERSION_STR)
    return message
