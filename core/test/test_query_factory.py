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

from QuickOSM.core.query_factory import QueryFactory
from QuickOSM.core.exceptions import QueryFactoryException


class TestQueryFactory(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        pass

    def tearDown(self):
        pass

    def test_check_parameters(self):
        """Test check parameters query."""
        # Nominatim and BBOX.
        query = QueryFactory(nominatim='foo', bbox=True)
        self.assertRaises(QueryFactoryException, query.check_parameters)

        # Missing key.
        query = QueryFactory(nominatim='foo')
        self.assertRaises(QueryFactoryException, query.check_parameters)

        # Missing osm object
        query = QueryFactory(key='foo', osm_objects=[])
        self.assertRaises(QueryFactoryException, query.check_parameters)

        # Wrong osm object.
        query = QueryFactory(key='foo', osm_objects=['bar'])
        self.assertRaises(QueryFactoryException, query.check_parameters)

        # Missing distance if "around".
        query = QueryFactory(key='foo', osm_objects=['node'], is_around=True)
        self.assertRaises(QueryFactoryException, query.check_parameters)

        # Missing nominatim if "around".
        query = QueryFactory(
            key='foo', osm_objects=['node'], is_around=True, distance=10)
        self.assertRaises(QueryFactoryException, query.check_parameters)

        # Good query.
        query = QueryFactory('foo', 'bar')
        try:
            query.check_parameters()
        except QueryFactoryException as e:
            self.fail(e.msg)

        query = QueryFactory('foo', nominatim='bar')
        try:
            query.check_parameters()
        except QueryFactoryException as e:
            self.fail(e.msg)

        query = QueryFactory('foo', bbox=True)
        try:
            query.check_parameters()
        except QueryFactoryException as e:
            self.fail(e.msg)

        query = QueryFactory('foo', is_around=True, distance=50, nominatim='a')
        try:
            query.check_parameters()
        except QueryFactoryException as e:
            self.fail(e.msg)

    def test_replace_template(self):
        """Test replace template."""
        query = ' area="paris"'
        expected = ' {{geocodeArea:paris}}'
        self.assertEqual(QueryFactory.replace_template(query), expected)

        query = ' area_coords="paris,france"'
        expected = ' {{geocodeCoords:paris,france}}'
        self.assertEqual(QueryFactory.replace_template(query), expected)

        query = ' bbox="custom"'
        expected = ' {{bbox}}'
        self.assertEqual(QueryFactory.replace_template(query), expected)

    def test_generate_xml(self):
        """Test generate XML."""
        query = QueryFactory(key='foo', value='bar', nominatim='paris')
        expected = u'<osm-script output="xml" timeout="25">' \
                   u'<id-query area="paris" into="area_0"/><union>' \
                   u'<query type="node"><has-kv k="foo" v="bar"/>' \
                   u'<area-query from="area_0" /></query><query type="way">' \
                   u'<has-kv k="foo" v="bar"/><area-query from="area_0" />' \
                   u'</query><query type="relation">' \
                   u'<has-kv k="foo" v="bar"/><area-query from="area_0" />' \
                   u'</query></union><union><item /><recurse type="down"/>' \
                   u'</union><print mode="body" /></osm-script>'
        self.assertEqual(query.generate_xml(), expected)

        query = QueryFactory(key='foo', bbox=True, timeout=35)
        expected = u'<osm-script output="xml" timeout="35"><union>' \
                   u'<query type="node"><has-kv k="foo" />' \
                   u'<bbox-query bbox="custom" /></query><query type="way">' \
                   u'<has-kv k="foo" /><bbox-query bbox="custom" /></query>' \
                   u'<query type="relation"><has-kv k="foo" />' \
                   u'<bbox-query bbox="custom" /></query></union><union>' \
                   u'<item /><recurse type="down"/></union>' \
                   u'<print mode="body" /></osm-script>'
        self.assertEqual(query.generate_xml(), expected)

        query = QueryFactory(
            key='foo', nominatim='paris;dubai', osm_objects=['node'])
        expected = u'<osm-script output="xml" timeout="25">' \
                   u'<id-query area="paris" into="area_0"/>' \
                   u'<id-query area="dubai" into="area_1"/><union>' \
                   u'<query type="node"><has-kv k="foo" />' \
                   u'<area-query from="area_0" /></query><query type="node">' \
                   u'<has-kv k="foo" /><area-query from="area_1" /></query>' \
                   u'</union><union><item /><recurse type="down"/></union>' \
                   u'<print mode="body" /></osm-script>'
        self.assertEqual(query.generate_xml(), expected)

        query = QueryFactory(
            key='foo',
            is_around=True,
            distance=1000,
            print_mode='meta',
            nominatim='a')
        expected = u'<osm-script output="xml" timeout="25"><union>' \
                   u'<query type="node"><has-kv k="foo" />' \
                   u'<around area_coords="a" radius="1000" /></query>' \
                   u'<query type="way"><has-kv k="foo" />' \
                   u'<around area_coords="a" radius="1000" /></query>' \
                   u'<query type="relation"><has-kv k="foo" />' \
                   u'<around area_coords="a" radius="1000" /></query>' \
                   u'</union>' \
                   u'<union><item /><recurse type="down"/></union>' \
                   u'<print mode="meta" /></osm-script>'
        self.assertEqual(query.generate_xml(), expected)

    def test_make(self):
        """Test make query."""
        query = QueryFactory('foo', 'bar', True)
        expected = u'<osm-script output="xml" timeout="25">\n    ' \
                   u'<union>\n        <query type="node">\n            ' \
                   u'<has-kv k="foo" v="bar"/>\n            ' \
                   u'<bbox-query {{bbox}}/>\n        </query>\n        ' \
                   u'<query type="way">\n            ' \
                   u'<has-kv k="foo" v="bar"/>\n            ' \
                   u'<bbox-query {{bbox}}/>\n        </query>\n        ' \
                   u'<query type="relation">\n            ' \
                   u'<has-kv k="foo" v="bar"/>\n            ' \
                   u'<bbox-query {{bbox}}/>\n        </query>\n    ' \
                   u'</union>\n    <union>\n        <item/>\n        ' \
                   u'<recurse type="down"/>\n    </union>\n    ' \
                   u'<print mode="body"/>\n</osm-script>\n'
        self.assertEqual(query.make(), expected)

if __name__ == '__main__':
    suite = unittest.makeSuite(TestQueryFactory)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
