"""Test the osm file loader panel."""

import unittest

from QuickOSM.definitions.osm import MultiType
from QuickOSM.qgis_plugin_tools.tools.resources import plugin_test_data_path
from QuickOSM.ui.osm_file_panel import OsmFilePanel

__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class TestFileLoader(unittest.TestCase):
    """Test the osm file loader panel."""

    def setUp(self):
        self.file = plugin_test_data_path('osm_parser', 'map.osm')

    def test_generate_filter(self):
        """Test if we can obtain a valid filter expression"""

        # 1 couple key/value
        properties = {
            'key': ['foo'],
            'value': ['bar'],
            'type_multi_request': []
        }

        expression = OsmFilePanel.generate_sql(properties)
        expected_exp = '\"foo\"=\'bar\''
        self.assertEqual(expected_exp, expression)

        # 2 couples key/value, AND
        properties = {
            'key': ['foo', 'foofoo'],
            'value': ['bar', 'barbar'],
            'type_multi_request': [MultiType.AND]
        }

        expression = OsmFilePanel.generate_sql(properties)
        expected_exp = '(\"foo\"=\'bar\' AND \"foofoo\"=\'barbar\')'
        self.assertEqual(expected_exp, expression)

        # 2 couples key/value, OR
        properties = {
            'key': ['foo', 'foofoo'],
            'value': ['bar', 'barbar'],
            'type_multi_request': [MultiType.OR]
        }

        expression = OsmFilePanel.generate_sql(properties)
        expected_exp = '\"foo\"=\'bar\' OR \"foofoo\"=\'barbar\''
        self.assertEqual(expected_exp, expression)


if __name__ == '__main__':
    unittest.main()
