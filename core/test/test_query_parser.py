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

import unittest

# This import is to enable SIP API V2
# noinspection PyUnresolvedReferences
import qgis  # pylint: disable=unused-import

from test.utilities import get_qgis_app

QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()

from qgis.core import QgsRectangle


class TestQueryParser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_oql(self):
        """Test if OQL or XML."""
        self.assertTrue(is_oql('out skel qt;'))
        self.assertFalse(is_oql('</osm-script>'))

    def test_replace_center(self):
        """Test {{center}}."""
        extent = QgsRectangle(10.00, 0.5, 20.00, 1.5)

        # No center.
        fake_query = 'foobar{{bbox}}foobar'
        expected = 'foobar{{bbox}}foobar'
        self.assertEqual(replace_center(extent, fake_query), expected)

        # One center in XML.
        fake_query = 'foobar{{center}}foobar'
        expected = 'foobarlat="1.0" lon="15.0"foobar'
        self.assertEqual(replace_center(extent, fake_query), expected)

        # One center in OQL.
        fake_query = 'foobar{{center}}foobar;'
        expected = 'foobar1.0,15.0foobar;'
        self.assertEqual(replace_center(extent, fake_query), expected)

        # Two centers in OQL.
        fake_query = 'foobar{{center}}foobar{{center}}foobar;'
        expected = 'foobar1.0,15.0foobar1.0,15.0foobar;'
        self.assertEqual(replace_center(extent, fake_query), expected)

        # One center and one OQL in OQL.
        fake_query = 'foobar{{center}}foobar{{bbox}}foobar;'
        expected = 'foobar1.0,15.0foobar{{bbox}}foobar;'
        self.assertEqual(replace_center(extent, fake_query), expected)

    def test_replace_bbox(self):
        """Test {{bbox}}."""
        extent = QgsRectangle(10.00, 0.5, 20.00, 1.5)

        # One bbox.
        fake_query = 'foobar{{bbox}}foobar'
        expected = 'foobare="20.0" n="1.5" s="0.5" w="10.0"foobar'
        self.assertEqual(replace_bbox(extent, fake_query), expected)

        # Two bbox.
        fake_query = 'foo{{bbox}}foo{{bbox}}foo'
        expected = 'fooe="20.0" n="1.5" s="0.5" w="10.0"fooe="20.0" n="1.5" ' \
                   's="0.5" w="10.0"foo'
        self.assertEqual(replace_bbox(extent, fake_query), expected)

        # One bbox in OQL.
        fake_query = 'foobar{{bbox}}foobar;'
        expected = 'foobar0.5,10.0,1.5,20.0foobar;'
        self.assertEqual(replace_bbox(extent, fake_query), expected)

        # One center and one OQL in OQL.
        fake_query = 'foobar{{center}}foobar{{bbox}}foobar;'
        expected = 'foobar{{center}}foobar0.5,10.0,1.5,20.0foobar;'
        self.assertEqual(replace_bbox(extent, fake_query), expected)

    def test_replace_geocode_coords(self):
        """Test {{geocodeCoords}}.

        Test using the internet.

        New-York or Paris may change their position. You should check that
        coordinates are nearly the same or implement a fake access manager.

        19/02/16 : New-York and Paris updated, need to change these tests.
        """
        nominatim = 'new york'

        # Test with New-York.
        fake_query = 'foobar{{geocodeCoords:Paris,France}}foobar'
        expected = 'foobarlat="40.7647714" lon="-73.9807639"foobar'
        result = replace_geocode_coords(nominatim, fake_query)
        self.assertEqual(result, expected)

        # Test with Paris, as point (not the capital) in XML.
        fake_query = 'foobar{{geocodeCoords:Paris,France}}foobar'
        expected = 'foobarlat="44.491379" lon="0.3940874"foobar'
        result = replace_geocode_coords(None, fake_query)
        self.assertEqual(result, expected)

        # Test with Paris, as point (not the capital) in OQL.
        fake_query = 'foobar{{geocodeCoords:Paris,France}}foobar;'
        expected = 'foobar44.491379,0.3940874foobar;'
        result = replace_geocode_coords(None, fake_query)
        self.assertEqual(result, expected)

        # Test with Paris and Montpellier.
        fake_query = 'foo{{geocodeCoords:Paris,France}}bar' \
                     'foo{{geocodeCoords:Montpellier}}bar'
        expected = 'foolat="44.491379" lon="0.3940874"bar' \
                   'foolat="47.3746883" lon="-0.8451944"bar'
        result = replace_geocode_coords(None, fake_query)
        self.assertEqual(result, expected)

    def test_replace_geocode_area(self):
        """Test {{geocodeArea}}.

        Test using the internet.

        New-York or Paris may change their position. You should check that
        coordinates are nearly the same or implement a fake access manager.
        """
        nominatim = 'new york'

        # Test with New-York.
        fake_query = 'foobar{{geocodeArea:Paris,France}}foobar'
        expected = 'foobarref="3600175905" type="area"foobar'
        result = replace_geocode_area(nominatim, fake_query)
        self.assertEqual(result, expected)

        # Test with Paris.
        fake_query = 'foobar{{geocodeArea:Paris,France}}foobar'
        expected = 'foobarref="3600007444" type="area"foobar'
        result = replace_geocode_area(None, fake_query)
        self.assertEqual(result, expected)

        # Test with Paris in XML.
        fake_query = 'foobar{{geocodeArea:Paris,France}}foobar'
        expected = 'foobarref="3600007444" type="area"foobar'
        result = replace_geocode_area('', fake_query)
        self.assertEqual(result, expected)

        # Test with Paris in OQL.
        fake_query = 'foobar{{geocodeArea:Paris,France}}foobar;'
        expected = 'foobararea(3600007444)foobar;'
        result = replace_geocode_area('', fake_query)
        self.assertEqual(result, expected)

        # Test with a fake OSM relation.
        fake_query = 'foobar{{geocodeArea:123456}}foobar'
        expected = 'foobarref="3600123456" type="area"foobar'
        result = replace_geocode_area('', fake_query)
        self.assertEqual(result, expected)

        # Test with Paris and Montpellier.
        fake_query = 'foo{{geocodeArea:Paris,France}}bar' \
                     'foo{{geocodeArea:Montpellier}}bar'
        expected = 'fooref="3600007444" type="area"bar' \
                   'fooref="3600028722" type="area"bar'
        result = replace_geocode_area(None, fake_query)
        self.assertEqual(result, expected)

    def test_clean_query(self):
        """Test clean query."""
        self.assertEqual(clean_query('  foo;;   '), 'foo;')
        self.assertEqual(clean_query('	foo;	'), 'foo;')
        self.assertEqual(clean_query('   	foo	   '), 'foo')

    def test_prepare_query(self):
        """Test prepare query."""
        # Test geocodeArea simple.
        query = '<osm-script output="xml" timeout="25">    <id-query {{geoco' \
                'deArea:paris}} into="area_0"/>    <union>        <query typ' \
                'e="node">            <has-kv k="a" v="b"/>            <area' \
                '-query from="area_0"/>        </query>        <query type="' \
                'way">            <has-kv k="a" v="b"/>            <area-que' \
                'ry from="area_0"/>        </query>        <query type="rela' \
                'tion">            <has-kv k="a" v="b"/>            <area-qu' \
                'ery from="area_0"/>        </query>    </union>    <union> ' \
                '       <item/>        <recurse type="down"/>    </union>   ' \
                ' <print mode="body"/></osm-script>'
        expected = '<osm-script output="xml" timeout="25">    <id-query ref=' \
                   '"3600007444" type="area" into="area_0"/>    <union>     ' \
                   '   <query type="node">            <has-kv k="a" v="b"/> ' \
                   '           <area-query from="area_0"/>        </query>  ' \
                   '      <query type="way">            <has-kv k="a" v="b"/' \
                   '>            <area-query from="area_0"/>        </query>' \
                   '        <query type="relation">            <has-kv k="a"' \
                   ' v="b"/>            <area-query from="area_0"/>        <' \
                   '/query>    </union>    <union>        <item/>        <re' \
                   'curse type="down"/>    </union>    <print mode="body"/><' \
                   '/osm-script>'
        self.assertEqual(prepare_query(query), expected)

if __name__ == '__main__':
    suite = unittest.makeSuite(TestQueryParser)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
