"""Tests for the parser of the osm data."""

import unittest

from qgis.core import QgsWkbTypes

from QuickOSM.core.parser.osm_parser import OsmParser
from QuickOSM.qgis_plugin_tools.tools.resources import plugin_test_data_path

__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class TestOsmParser(unittest.TestCase):
    """Tests for the parser of the osm data."""

    def setUp(self):
        self.maxDiff = None

    def test_parser(self):
        """Test if the osm parser output is as expected."""
        file = plugin_test_data_path('osm_parser', 'map.osm')

        parser = OsmParser(
            osm_file=file,
            layers=['points'],
            layer_name='layer_name',
        )

        layers = parser.processing_parse()

        tags_expected = [
            'full_id', 'osm_id', 'osm_type', 'osm_version', 'osm_timestamp',
            'osm_uid', 'osm_user', 'osm_changeset', 'entrance',
            'website', 'official_name', 'office', 'contact:street',
            'contact:postcode', 'contact:phone', 'contact:housenumber',
            'contact:city', 'recycling_type', 'recycling:green_waste',
            'material', 'emergency', 'telecom:medium', 'telecom',
            'street_cabinet', 'ref:FR:Orange:NRO', 'ref:FR:Orange',
            'ref', 'owner', 'man_made', 'natural', 'shelter', 'network',
            'covered', 'bench', 'wheelchair', 'stamping_machine',
            'ref:FR:LaPoste', 'opening_hours', 'atm', 'recycling:paper',
            'recycling:glass', 'motor_vehicle', 'foot', 'bollard', 'bicycle',
            'ref:FR:FINESS', 'opening_hours:covid19', 'healthcare',
            'dispensing', 'amenity', 'shop', 'operator', 'brand:wikipedia',
            'brand:wikidata', 'brand', 'addr:street', 'addr:postcode',
            'addr:city', 'public_transport', 'name', 'highway', 'bus',
            'barrier'
        ]
        features_expected = 52
        geom_type_expected = QgsWkbTypes.Point

        self.assertEqual(layers['points']['tags'], tags_expected)
        self.assertEqual(layers['points']['featureCount'], features_expected)
        self.assertEqual(layers['points']['geomType'], geom_type_expected)


if __name__ == '__main__':
    unittest.main()
