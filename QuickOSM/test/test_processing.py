"""Tests for processing algorithms."""

import processing

from qgis.core import QgsApplication, QgsVectorLayer
from qgis.testing import unittest

from QuickOSM.quick_osm_processing.provider import Provider

__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class TestProcessing(unittest.TestCase):
    """Tests for processing algorithms."""

    def setUp(self) -> None:
        self.provider = Provider()
        QgsApplication.processingRegistry().addProvider(self.provider)
        self.maxDiff = None

    def test_build_not_spatial_query(self):
        """Test for the build of a not spatial query algorithm."""
        result = processing.run(
            'quickosm:buildquerybyattributeonly',
            {
                'KEY': 'amenity',
                'SERVER': 'https://lz4.overpass-api.de/api/interpreter',
                'TIMEOUT': 25,
                'VALUE': 'bench'
            }
        )

        result_expected = {
            'OUTPUT_URL': 'https://lz4.overpass-api.de/api/interpreter?data=[out:xml]'
                          ' [timeout:25];%0A(%0A    node[%22amenity%22%3D%22bench%22];%0A'
                          '    way[%22amenity%22%3D%22bench%22];%0A    '
                          'relation[%22amenity%22%3D%22bench%22];%0A);%0A(._;%3E;);'
                          '%0Aout body;&info=QgisQuickOSMPlugin',
            'OUTPUT_OQL_QUERY':
                '[out:xml] [timeout:25];\n(\n    node["amenity"="bench"];\n'
                '    way["amenity"="bench"];\n    relation["amenity"="bench"];'
                '\n);\n(._;>;);\nout body;'
        }

        self.assertEqual(result_expected, result)

    def test_build_in_area_query(self):
        """Test for the build of a in area query algorithm."""
        result = processing.run(
            'quickosm:buildqueryinsidearea',
            {
                'AREA': 'La Souterraine',
                'KEY': 'amenity',
                'SERVER': 'https://lz4.overpass-api.de/api/interpreter',
                'TIMEOUT': 25,
                'VALUE': 'bench'
            }
        )

        result_expected = {
            'OUTPUT_URL':
                'https://lz4.overpass-api.de/api/interpreter?data=[out:xml]'
                ' [timeout:25];%0A area(3600118810) -%3E .area_0;%0A(%0A    '
                'node[%22amenity%22%3D%22bench%22](area.area_0);%0A    '
                'way[%22amenity%22%3D%22bench%22](area.area_0);%0A    '
                'relation[%22amenity%22%3D%22bench%22](area.area_0);%0A);'
                '%0A(._;%3E;);%0Aout body;&info=QgisQuickOSMPlugin',
            'OUTPUT_OQL_QUERY':
                '[out:xml] [timeout:25];\n area(3600118810) -> .area_0;\n'
                '(\n    node["amenity"="bench"](area.area_0);\n    '
                'way["amenity"="bench"](area.area_0);\n    '
                'relation["amenity"="bench"](area.area_0);\n);'
                '\n(._;>;);\nout body;'
        }

        self.assertEqual(result_expected, result)

    def test_build_around_area_query(self):
        """Test for the build of an around area query algorithm."""
        result = processing.run(
            'quickosm:buildqueryaroundarea',
            {
                'AREA': 'La Souterraine',
                'DISTANCE': 1000,
                'KEY': 'amenity',
                'SERVER': 'https://lz4.overpass-api.de/api/interpreter',
                'TIMEOUT': 25,
                'VALUE': 'bench'
            }
        )

        result_expected = {
            'OUTPUT_URL':
                'https://lz4.overpass-api.de/api/interpreter?data=[out:xml]'
                ' [timeout:25];%0A(%0A    node[%22amenity%22%3D%22bench%22]'
                '(around:1000, 46.2383347,1.4861387);%0A    way[%22amenity%22%3D%22bench%22]'
                '(around:1000, 46.2383347,1.4861387);%0A    relation[%22amenity%22%3D%22bench%22]'
                '(around:1000, 46.2383347,1.4861387);%0A);%0A(._;%3E;);%0Aout'
                ' body;&info=QgisQuickOSMPlugin',
            'OUTPUT_OQL_QUERY':
                '[out:xml] [timeout:25];\n(\n'
                '    node["amenity"="bench"](around:1000, 46.2383347,1.4861387);\n'
                '    way["amenity"="bench"](around:1000, 46.2383347,1.4861387);\n'
                '    relation["amenity"="bench"](around:1000, 46.2383347,1.4861387);'
                '\n);\n(._;>;);\nout body;'
        }

        self.assertEqual(result_expected, result)

    def test_build_in_extent_query(self):
        """Test for the build of a in extent query algorithm."""
        result = processing.run(
            'quickosm:buildqueryextent',
            {
                'EXTENT': '3.809971100,3.963647400,43.557942300,43.654612100 [EPSG:4326]',
                'KEY': 'amenity',
                'SERVER': 'https://lz4.overpass-api.de/api/interpreter',
                'TIMEOUT': 25,
                'VALUE': 'bench'
            }
        )

        result_expected = {
            'OUTPUT_URL':
                'https://lz4.overpass-api.de/api/interpreter?data=[out:xml]'
                ' [timeout:25];%0A(%0A    node[%22amenity%22%3D%22bench%22]'
                '( 43.5579423,3.8099711,43.6546121,3.9636474);%0A    '
                'way[%22amenity%22%3D%22bench%22]( 43.5579423,3.8099711,43.6546121,3.9636474);%0A'
                '    relation[%22amenity%22%3D%22bench%22]'
                '( 43.5579423,3.8099711,43.6546121,3.9636474);%0A);'
                '%0A(._;%3E;);%0Aout body;&info=QgisQuickOSMPlugin',
            'OUTPUT_OQL_QUERY':
                '[out:xml] [timeout:25];\n(\n    node["amenity"="bench"]'
                '( 43.5579423,3.8099711,43.6546121,3.9636474);\n    '
                'way["amenity"="bench"]( 43.5579423,3.8099711,43.6546121,3.9636474);\n'
                '    relation["amenity"="bench"]( 43.5579423,3.8099711,43.6546121,3.9636474);'
                '\n);\n(._;>;);\nout body;'
        }

        self.assertEqual(result_expected, result)

    def test_build_raw_query(self):
        """Test for the build of a raw query algorithm."""
        result = processing.run(
            'quickosm:buildrawquery',
            {
                'AREA': 'La Souterraine',
                'EXTENT': '3.809971100,3.963647400,43.557942300,43.654612100 [EPSG:4326]',
                'QUERY':
                    '[out:xml] [timeout:25];\n {{geocodeArea:La Souterraine}}'
                    ' -> .area_0;\n(\n    node[\"amenity\"=\"bench\"]'
                    '(area.area_0);\n    way[\"amenity\"=\"bench\"]'
                    '(area.area_0);\n    relation[\"amenity\"=\"bench\"]'
                    '(area.area_0);\n);\n(._;>;);\nout body;',
                'SERVER': 'server Overpass'
            }
        )

        result_expected = {
            'OUTPUT_URL':
                'server Overpass?data=[out:xml] [timeout:25];%0A '
                'area(3600118810) -%3E .area_0;%0A(%0A    '
                'node[%22amenity%22%3D%22bench%22](area.area_0);'
                '%0A    way[%22amenity%22%3D%22bench%22](area.area_0);'
                '%0A    relation[%22amenity%22%3D%22bench%22](area.area_0);'
                '%0A);%0A(._;%3E;);%0Aout body;&info=QgisQuickOSMPlugin',
            'OUTPUT_OQL_QUERY':
                '[out:xml] [timeout:25];\n area(3600118810) -> .area_0;\n'
                '(\n    node["amenity"="bench"](area.area_0);\n    '
                'way["amenity"="bench"](area.area_0);\n    '
                'relation["amenity"="bench"](area.area_0);\n);'
                '\n(._;>;);\nout body;'
        }

        self.assertEqual(result_expected, result)

    def test_open_osm_file(self):
        """Test for the opening of an osm file."""
        result = processing.run(
            'quickosm:openosmfile',
            {
                'FILE': '\\path\\to\\a\\file.osm',
                'OSM_CONF': ''
            }
        )

        self.assertIsInstance(result['OUTPUT_POINTS'], QgsVectorLayer)
        self.assertIn('|layername=points', result['OUTPUT_POINTS'].source())
        self.assertIsInstance(result['OUTPUT_LINES'], QgsVectorLayer)
        self.assertIn('|layername=lines', result['OUTPUT_LINES'].source())
        self.assertIsInstance(result['OUTPUT_MULTILINESTRINGS'], QgsVectorLayer)
        self.assertIn('|layername=multilinestrings', result['OUTPUT_MULTILINESTRINGS'].source())
        self.assertIsInstance(result['OUTPUT_MULTIPOLYGONS'], QgsVectorLayer)
        self.assertIn('|layername=multipolygons', result['OUTPUT_MULTIPOLYGONS'].source())
        self.assertIsInstance(result['OUTPUT_OTHER_RELATIONS'], QgsVectorLayer)
        self.assertIn('|layername=other_relations', result['OUTPUT_OTHER_RELATIONS'].source())


if __name__ == '__main__':
    unittest.main()
