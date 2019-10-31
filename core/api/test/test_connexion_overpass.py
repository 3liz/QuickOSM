"""Tests for Overpass API requests."""

from qgis.testing import unittest
from qgis.PyQt.QtCore import QUrl, QUrlQuery

from ..connexion_oapi import ConnexionOAPI
from ...exceptions import (
    OverpassBadRequestException,
    OverpassTimeoutException,
    OverpassMemoryException,
    OverpassRuntimeError,
)
from ....definitions.overpass import OVERPASS_SERVERS
from ....qgis_plugin_tools.tools.resources import plugin_test_data_path

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class TestOverpass(unittest.TestCase):

    def test_real_wrong_request(self):
        """Test wrong request.

        This is test is using internet.
        """
        url = QUrl(OVERPASS_SERVERS[0])
        query_string = QUrlQuery()
        query_string.addQueryItem('data', 'fake_query')
        url.setQuery(query_string)
        overpass = ConnexionOAPI(url.toString())

        self.assertListEqual(overpass.errors, [])

        # We don't want the FileNotFoundError
        try:
            overpass.run()
        except OverpassBadRequestException:
            self.assertTrue(True)
        except FileNotFoundError:
            self.assertFalse(True)
        else:
            self.assertFalse(True)

        self.assertEqual(len(overpass.errors), 1)

    def test_parsing_http_string(self):
        """Test we can parse the HTTP return string from QGIS for timing out."""
        string = (
            'Network request http://www.overpass-api.de/api/interpreter?data='
            '%3Cosm-script output%3D%22xml%22 timeout%3D%2225%22%3E%0A %3Cid-'
            'query ref%3D%223600171496%22 type%3D%22area%22 into%3D%22area_0%'
            '22/%3E%0A %3Cunion%3E%0A %3Cquery type%3D%22node%22%3E%0A %3Chas'
            '-kv k%3D%22admin_level%22 v%3D%222%22/%3E%0A %3Carea-query from%'
            '3D%22area_0%22/%3E%0A %3C/query%3E%0A %3Cquery type%3D%22way%22%'
            '3E%0A %3Chas-kv k%3D%22admin_level%22 v%3D%222%22/%3E%0A %3Carea'
            '-query from%3D%22area_0%22/%3E%0A %3C/query%3E%0A %3Cquery type%'
            '3D%22relation%22%3E%0A %3Chas-kv k%3D%22admin_level%22 v%3D%222%'
            '22/%3E%0A %3Carea-query from%3D%22area_0%22/%3E%0A %3C/query%3E%'
            '0A %3C/union%3E%0A %3Cunion%3E%0A %3Citem/%3E%0A %3Crecurse type'
            '%3D%22down%22/%3E%0A %3C/union%3E%0A %3Cprint mode%3D%22body%22/'
            '%3E%0A%3C/osm-script%3E&info=QgisQuickOSMPlugin timed out')
        try:
            ConnexionOAPI.is_query_timed_out(string)
        except OverpassTimeoutException:
            self.assertTrue(True)
        else:
            self.assertFalse(True)

    def test_xml_error(self):
        """Test we can parse Overpass error within a file."""

        timeout_file = plugin_test_data_path('overpass', 'query_timed_out.xml')
        try:
            ConnexionOAPI.check_file(timeout_file)
        except OverpassTimeoutException as e:
            self.assertEqual(
                e.message,
                'OverpassAPI timeout, try again later or a smaller query.')
        else:
            self.assertFalse(True)

        run_out_memory = plugin_test_data_path('overpass', 'run_out_memory.xml')
        try:
            ConnexionOAPI.check_file(run_out_memory)
        except OverpassMemoryException as e:
            self.assertEqual(
                e.message,
                'OverpassAPI is out of memory, try another query or a smaller area.')
            self.assertEqual(
                e.more_details,
                'The server would need more or less 513 MB of RAM.')
        else:
            self.assertFalse(True)

        generic_error = plugin_test_data_path('overpass', 'generic_error.xml')
        try:
            ConnexionOAPI.check_file(generic_error)
        except OverpassRuntimeError as e:
            self.assertEqual(e.message, 'Overpass error: FAKE error that I do not know')
        else:
            self.assertFalse(True)
