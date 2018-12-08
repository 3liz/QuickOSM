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


from qgis.testing import start_app, unittest

from QuickOSM.definitions.osm import QueryType
from QuickOSM.core.exceptions import QueryFactoryException
from QuickOSM.core.query_factory import QueryFactory

start_app()


class TestQueryFactory(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        pass

    def tearDown(self):
        pass

    def test_check_parameters(self):
        """Test check parameters query."""
        # Fake query type
        query = QueryFactory(area='foo', query_type='fake_query_type')
        self.assertRaises(QueryFactoryException, query._check_parameters)
    #
    #     # Missing key.
    #     query = QueryFactory(nominatim='foo')
    #     self.assertRaises(QueryFactoryException, query._check_parameters)
    #
    #     # Missing osm object
    #     query = QueryFactory(key='foo', osm_objects=[])
    #     self.assertRaises(QueryFactoryException, query._check_parameters)
    #
    #     # Wrong osm object.
    #     query = QueryFactory(key='foo', osm_objects=['bar'])
    #     self.assertRaises(QueryFactoryException, query._check_parameters)
    #
    #     # Missing distance if "around".
    #     query = QueryFactory(key='foo', osm_objects=['node'], is_around=True)
    #     self.assertRaises(QueryFactoryException, query._check_parameters)
    #
    #     # Missing nominatim if "around".
    #     query = QueryFactory(
    #         key='foo', osm_objects=['node'], is_around=True, distance=10)
    #     self.assertRaises(QueryFactoryException, query._check_parameters)
    #
    #     # Good query.
    #     query = QueryFactory('foo', 'bar')
    #     try:
    #         query._check_parameters()
    #     except QueryFactoryException as e:
    #         self.fail(e.msg)
    #
    #     query = QueryFactory('foo', nominatim='bar')
    #     try:
    #         query._check_parameters()
    #     except QueryFactoryException as e:
    #         self.fail(e.msg)
    #
    #     query = QueryFactory('foo', bbox=True)
    #     try:
    #         query._check_parameters()
    #     except QueryFactoryException as e:
    #         self.fail(e.msg)
    #
    #     query = QueryFactory('foo', is_around=True, distance=50, nominatim='a')
    #     try:
    #         query._check_parameters()
    #     except QueryFactoryException as e:
    #         self.fail(e.msg)
    #
    # def test_replace_template(self):
    #     """Test replace template."""
    #     query = ' area="paris"'
    #     expected = ' {{geocodeArea:paris}}'
    #     self.assertEqual(QueryFactory.replace_template(query), expected)
    #
    #     query = ' area_coords="paris,france"'
    #     expected = ' {{geocodeCoords:paris,france}}'
    #     self.assertEqual(QueryFactory.replace_template(query), expected)
    #
    #     query = ' bbox="custom"'
    #     expected = ' {{bbox}}'
    #     self.assertEqual(QueryFactory.replace_template(query), expected)
    #
    # def test_generate_xml(self):
    #     """Test generate XML."""
    #     query = QueryFactory(key='foo', value='bar', nominatim='paris')
    #     expected = '<osm-script output="xml" timeout="25">' \
    #                '<id-query area="paris" into="area_0"/><union>' \
    #                '<query type="node"><has-kv k="foo" v="bar"/>' \
    #                '<area-query from="area_0" /></query><query type="way">' \
    #                '<has-kv k="foo" v="bar"/><area-query from="area_0" />' \
    #                '</query><query type="relation">' \
    #                '<has-kv k="foo" v="bar"/><area-query from="area_0" />' \
    #                '</query></union><union><item /><recurse type="down"/>' \
    #                '</union><print mode="body" /></osm-script>'
    #     self.assertEqual(query.generate_xml(), expected)
    #
    #     query = QueryFactory(key='foo', bbox=True, timeout=35)
    #     expected = '<osm-script output="xml" timeout="35"><union>' \
    #                '<query type="node"><has-kv k="foo" />' \
    #                '<bbox-query bbox="custom" /></query><query type="way">' \
    #                '<has-kv k="foo" /><bbox-query bbox="custom" /></query>' \
    #                '<query type="relation"><has-kv k="foo" />' \
    #                '<bbox-query bbox="custom" /></query></union><union>' \
    #                '<item /><recurse type="down"/></union>' \
    #                '<print mode="body" /></osm-script>'
    #     self.assertEqual(query.generate_xml(), expected)
    #
    #     query = QueryFactory(
    #         key='foo', nominatim='paris;dubai', osm_objects=['node'])
    #     expected = '<osm-script output="xml" timeout="25">' \
    #                '<id-query area="paris" into="area_0"/>' \
    #                '<id-query area="dubai" into="area_1"/><union>' \
    #                '<query type="node"><has-kv k="foo" />' \
    #                '<area-query from="area_0" /></query><query type="node">' \
    #                '<has-kv k="foo" /><area-query from="area_1" /></query>' \
    #                '</union><union><item /><recurse type="down"/></union>' \
    #                '<print mode="body" /></osm-script>'
    #     self.assertEqual(query.generate_xml(), expected)
    #
    #     query = QueryFactory(
    #         key='foo',
    #         is_around=True,
    #         distance=1000,
    #         print_mode='meta',
    #         nominatim='a')
    #     expected = '<osm-script output="xml" timeout="25"><union>' \
    #                '<query type="node"><has-kv k="foo" />' \
    #                '<around area_coords="a" radius="1000" /></query>' \
    #                '<query type="way"><has-kv k="foo" />' \
    #                '<around area_coords="a" radius="1000" /></query>' \
    #                '<query type="relation"><has-kv k="foo" />' \
    #                '<around area_coords="a" radius="1000" /></query>' \
    #                '</union>' \
    #                '<union><item /><recurse type="down"/></union>' \
    #                '<print mode="meta" /></osm-script>'
    #     self.assertEqual(query.generate_xml(), expected)
    #
    # def test_make(self):
    #     """Test make query."""
    #     query = QueryFactory('foo', 'bar', True)
    #     expected = '<osm-script output="xml" timeout="25">\n    ' \
    #                '<union>\n        <query type="node">\n            ' \
    #                '<has-kv k="foo" v="bar"/>\n            ' \
    #                '<bbox-query {{bbox}}/>\n        </query>\n        ' \
    #                '<query type="way">\n            ' \
    #                '<has-kv k="foo" v="bar"/>\n            ' \
    #                '<bbox-query {{bbox}}/>\n        </query>\n        ' \
    #                '<query type="relation">\n            ' \
    #                '<has-kv k="foo" v="bar"/>\n            ' \
    #                '<bbox-query {{bbox}}/>\n        </query>\n    ' \
    #                '</union>\n    <union>\n        <item/>\n        ' \
    #                '<recurse type="down"/>\n    </union>\n    ' \
    #                '<print mode="body"/>\n</osm-script>\n'
    #     self.assertEqual(query.make(), expected)


if __name__ == '__main__':
    suite = unittest.makeSuite(TestQueryFactory)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
