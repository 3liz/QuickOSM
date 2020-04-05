"""Tests for Query factory."""

from qgis.testing import unittest

from ..exceptions import QueryFactoryException
from ..query_factory import QueryFactory
from ...definitions.osm import QueryType, OsmType

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class TestQueryFactory(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_impossible_queries(self):
        """Test queries which are not possible and must raise an exception."""
        # Query type
        # noinspection PyTypeChecker
        query = QueryFactory('fake_query_type', area='foo')
        msg = 'Wrong query type.'
        with self.assertRaisesRegex(QueryFactoryException, msg):
            query._check_parameters()

        # Missing query type
        query = QueryFactory(key='foo', value='bar', area='paris')
        msg = 'Wrong query type.'
        with self.assertRaisesRegex(QueryFactoryException, msg):
            query._check_parameters()

        # OSM object
        query = QueryFactory(QueryType.BBox)
        self.assertEqual(3, len(query._osm_objects))
        query = QueryFactory(QueryType.BBox, osm_objects=[OsmType.Node])
        self.assertEqual(1, len(query._osm_objects))
        query = QueryFactory(QueryType.BBox, osm_objects=['foo'])
        msg = 'Wrong OSM object.'
        with self.assertRaisesRegex(QueryFactoryException, msg):
            query._check_parameters()

        # Query type with distance
        query = QueryFactory(QueryType.AroundArea)
        msg = 'No distance provided with the "around" query.'
        with self.assertRaisesRegex(QueryFactoryException, msg):
            query._check_parameters()

        query = QueryFactory(QueryType.AroundArea, around_distance='foo')
        msg = 'Wrong distance parameter.'
        with self.assertRaisesRegex(QueryFactoryException, msg):
            query._check_parameters()

        # One value but no key, bbox
        query = QueryFactory(query_type=QueryType.BBox, value='b')
        msg = 'Not possible to query a specific value without a key.'
        with self.assertRaisesRegex(QueryFactoryException, msg):
            query._check_parameters()

        # One value but no key, attributes only
        query = QueryFactory(
            query_type=QueryType.NotSpatial, value='b')
        msg = 'Not possible to query a specific value without a key.'
        with self.assertRaisesRegex(QueryFactoryException, msg):
            query._check_parameters()

        # Attributes only
        query = QueryFactory(query_type=QueryType.NotSpatial)
        msg = 'A key is required.'
        with self.assertRaisesRegex(QueryFactoryException, msg):
            query._check_parameters()

        # Query with named area
        query = QueryFactory(QueryType.InArea)
        msg = 'Named area is required when the query is "In".'
        with self.assertRaisesRegex(QueryFactoryException, msg):
            query._check_parameters()
        query = QueryFactory(QueryType.InArea, around_distance=500)
        msg = 'Distance parameter is incompatible with this query.'
        with self.assertRaisesRegex(QueryFactoryException, msg):
            query._check_parameters()

        # Many keys with one value
        query = QueryFactory(
            query_type=QueryType.BBox,
            key=['foo', 'bar'],
            value='not possible')
        msg = 'Missing some values for some keys'
        with self.assertRaisesRegex(QueryFactoryException, msg):
            query._check_parameters()

        # Many keys with one value
        query = QueryFactory(
            query_type=QueryType.BBox,
            key=['foo', 'bar'],
            value=['not possible'])
        msg = 'Missing some values for some keys'
        with self.assertRaisesRegex(QueryFactoryException, msg):
            query._check_parameters()

        # Many values with one key
        query = QueryFactory(
            query_type=QueryType.BBox,
            key=['bar'],
            value=['foo', 'bar'])
        msg = 'Missing some keys for some values'
        with self.assertRaisesRegex(QueryFactoryException, msg):
            query._check_parameters()

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

    def test_possible_queries(self):
        """Test queries which are possible and must return a XML query."""

        def test_query(q, xml, xml_with_template, human_label):
            """Internal helper for testing queries."""
            self.assertTrue(q._check_parameters())
            self.assertEqual(q.generate_xml(), xml)
            self.assertEqual(q.friendly_message(), human_label)
            self.assertEqual(q._make_for_test(), xml_with_template)

        # All keys in extent
        query = QueryFactory(
            query_type=QueryType.BBox)
        expected_xml = (
            '<osm-script output="xml" timeout="25">'
            '<union>'
            '<query type="node">'
            '<bbox-query bbox="custom" />'
            '</query>'
            '<query type="way">'
            '<bbox-query bbox="custom" />'
            '</query>'
            '<query type="relation">'
            '<bbox-query bbox="custom" />'
            '</query>'
            '</union>'
            '<union>'
            '<item />'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body" />'
            '</osm-script>'
        )
        expected_xml_with_template = (
            '<osm-script output="xml" timeout="25">'
            '<union>'
            '<query type="node">'
            '<bbox-query {{bbox}}/>'
            '</query>'
            '<query type="way">'
            '<bbox-query {{bbox}}/>'
            '</query>'
            '<query type="relation">'
            '<bbox-query {{bbox}}/>'
            '</query>'
            '</union>'
            '<union>'
            '<item/>'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body"/>'
            '</osm-script>'
        )
        human = 'All OSM objects in the canvas or layer extent are going to be downloaded.'
        test_query(query, expected_xml, expected_xml_with_template, human)

        # Key value and named place
        query = QueryFactory(
            query_type=QueryType.InArea, key='foo', value='bar', area='paris')
        self.assertListEqual(query.area, ['paris'])
        expected_xml = (
            '<osm-script output="xml" timeout="25">'
            '<id-query area="paris" into="area_0"/>'
            '<union>'
            '<query type="node">'
            '<has-kv k="foo" v="bar"/>'
            '<area-query from="area_0" />'
            '</query>'
            '<query type="way">'
            '<has-kv k="foo" v="bar"/>'
            '<area-query from="area_0" />'
            '</query>'
            '<query type="relation">'
            '<has-kv k="foo" v="bar"/>'
            '<area-query from="area_0" />'
            '</query>'
            '</union>'
            '<union>'
            '<item />'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body" />'
            '</osm-script>')
        expected_xml_with_template = (
            '<osm-script output="xml" timeout="25">'
            '<id-query {{geocodeArea:paris}} into="area_0"/>'
            '<union>'
            '<query type="node">'
            '<has-kv k="foo" v="bar"/>'
            '<area-query from="area_0"/>'
            '</query>'
            '<query type="way">'
            '<has-kv k="foo" v="bar"/>'
            '<area-query from="area_0"/>'
            '</query>'
            '<query type="relation">'
            '<has-kv k="foo" v="bar"/>'
            '<area-query from="area_0"/>'
            '</query>'
            '</union>'
            '<union>'
            '<item/>'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body"/>'
            '</osm-script>'
        )
        human = 'All OSM objects with the key \'foo\'=\'bar\' in paris are going to be downloaded.'
        test_query(query, expected_xml, expected_xml_with_template, human)

        # Key in bbox
        query = QueryFactory(query_type=QueryType.BBox, key='foo', timeout=35)
        self.assertIsNone(query.area)
        expected_xml = (
            '<osm-script output="xml" timeout="35">'
            '<union>'
            '<query type="node">'
            '<has-kv k="foo" />'
            '<bbox-query bbox="custom" />'
            '</query>'
            '<query type="way">'
            '<has-kv k="foo" />'
            '<bbox-query bbox="custom" />'
            '</query>'
            '<query type="relation">'
            '<has-kv k="foo" />'
            '<bbox-query bbox="custom" />'
            '</query>'
            '</union>'
            '<union>'
            '<item />'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body" />'
            '</osm-script>'
        )
        expected_xml_with_template = (
            '<osm-script output="xml" timeout="35">'
            '<union>'
            '<query type="node">'
            '<has-kv k="foo"/>'
            '<bbox-query {{bbox}}/>'
            '</query>'
            '<query type="way">'
            '<has-kv k="foo"/>'
            '<bbox-query {{bbox}}/>'
            '</query>'
            '<query type="relation">'
            '<has-kv k="foo"/>'
            '<bbox-query {{bbox}}/>'
            '</query>'
            '</union>'
            '<union>'
            '<item/>'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body"/>'
            '</osm-script>'
        )
        human = 'All OSM objects with the key \'foo\' in the canvas or layer extent are going to be downloaded.'
        test_query(query, expected_xml, expected_xml_with_template, human)

        # Attribute only
        query = QueryFactory(query_type=QueryType.NotSpatial, key='foo', timeout=35)
        self.assertIsNone(query.area)
        expected_xml = (
            '<osm-script output="xml" timeout="35">'
            '<union>'
            '<query type="node">'
            '<has-kv k="foo" />'
            '</query>'
            '<query type="way">'
            '<has-kv k="foo" />'
            '</query>'
            '<query type="relation">'
            '<has-kv k="foo" />'
            '</query>'
            '</union>'
            '<union>'
            '<item />'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body" />'
            '</osm-script>'
        )
        expected_xml_with_template = (
            '<osm-script output="xml" timeout="35">'
            '<union>'
            '<query type="node">'
            '<has-kv k="foo"/>'
            '</query>'
            '<query type="way">'
            '<has-kv k="foo"/>'
            '</query>'
            '<query type="relation">'
            '<has-kv k="foo"/>'
            '</query>'
            '</union>'
            '<union>'
            '<item/>'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body"/>'
            '</osm-script>'
        )
        human = 'All OSM objects with the key \'foo\' are going to be downloaded.'
        test_query(query, expected_xml, expected_xml_with_template, human)

        # Double place name, with node only
        query = QueryFactory(
            query_type=QueryType.InArea,
            key='foo',
            area='paris;dubai',
            osm_objects=[OsmType.Node],
        )
        self.assertListEqual(query.area, ['paris', 'dubai'])
        expected_xml = (
            '<osm-script output="xml" timeout="25">'
            '<id-query area="paris" into="area_0"/>'
            '<id-query area="dubai" into="area_1"/>'
            '<union>'
            '<query type="node">'
            '<has-kv k="foo" />'
            '<area-query from="area_0" />'
            '</query>'
            '<query type="node">'
            '<has-kv k="foo" />'
            '<area-query from="area_1" />'
            '</query>'
            '</union>'
            '<union>'
            '<item />'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body" />'
            '</osm-script>'
        )
        expected_xml_with_template = (
            '<osm-script output="xml" timeout="25">'
            '<id-query {{geocodeArea:paris}} into="area_0"/>'
            '<id-query {{geocodeArea:dubai}} into="area_1"/>'
            '<union>'
            '<query type="node">'
            '<has-kv k="foo"/>'
            '<area-query from="area_0"/>'
            '</query>'
            '<query type="node">'
            '<has-kv k="foo"/>'
            '<area-query from="area_1"/>'
            '</query>'
            '</union>'
            '<union>'
            '<item/>'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body"/>'
            '</osm-script>'
        )
        human = 'All OSM objects with the key \'foo\' in paris and dubai are going to be downloaded.'
        test_query(query, expected_xml, expected_xml_with_template, human)

        # Not testing the XML or OQL
        query = QueryFactory(
            query_type=QueryType.InArea,
            key='foo',
            area='paris;dubai;new york',
            osm_objects=[OsmType.Node],
        )
        human = 'All OSM objects with the key \'foo\' in paris, dubai and new york are going to be downloaded.'
        self.assertEqual(query.friendly_message(), human)

        # Around query with meta and one key
        query = QueryFactory(
            query_type=QueryType.AroundArea,
            key='foo',
            around_distance=1000,
            print_mode='meta',
            area='a')
        self.assertListEqual(query.area, ['a'])
        expected_xml = (
            '<osm-script output="xml" timeout="25">'
            '<union>'
            '<query type="node">'
            '<has-kv k="foo" />'
            '<around area_coords="a" radius="1000" />'
            '</query>'
            '<query type="way">'
            '<has-kv k="foo" />'
            '<around area_coords="a" radius="1000" />'
            '</query>'
            '<query type="relation">'
            '<has-kv k="foo" />'
            '<around area_coords="a" radius="1000" />'
            '</query>'
            '</union>'
            '<union>'
            '<item />'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="meta" />'
            '</osm-script>'
        )
        expected_xml_with_template = (
            '<osm-script output="xml" timeout="25">'
            '<union>'
            '<query type="node">'
            '<has-kv k="foo"/>'
            '<around {{geocodeCoords:a}} radius="1000"/>'
            '</query>'
            '<query type="way">'
            '<has-kv k="foo"/>'
            '<around {{geocodeCoords:a}} radius="1000"/>'
            '</query>'
            '<query type="relation">'
            '<has-kv k="foo"/>'
            '<around {{geocodeCoords:a}} radius="1000"/>'
            '</query>'
            '</union>'
            '<union>'
            '<item/>'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="meta"/>'
            '</osm-script>'
        )
        human = 'All OSM objects with the key \'foo\' in 1000 meters of a are going to be downloaded.'
        test_query(query, expected_xml, expected_xml_with_template, human)

        # No key, no value, one object
        query = QueryFactory(
            query_type=QueryType.AroundArea,
            around_distance=1000,
            print_mode='meta',
            osm_objects=[OsmType.Node],
            area='a')
        self.assertListEqual(query.area, ['a'])
        expected_xml = (
            '<osm-script output="xml" timeout="25"><union>'
            '<query type="node">'
            '<around area_coords="a" radius="1000" />'
            '</query>'
            '</union>'
            '<union>'
            '<item /><recurse type="down"/>'
            '</union><print mode="meta" /></osm-script>')
        expected_xml_with_template = (
            '<osm-script output="xml" timeout="25">'
            '<union>'
            '<query type="node">'
            '<around {{geocodeCoords:a}} radius="1000"/>'
            '</query>'
            '</union>'
            '<union>'
            '<item/>'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="meta"/>'
            '</osm-script>'
        )
        human = 'All OSM objects in 1000 meters of a are going to be downloaded.'
        test_query(query, expected_xml, expected_xml_with_template, human)

        # Many keys with many values
        query = QueryFactory(
            query_type=QueryType.BBox,
            osm_objects=[OsmType.Node],
            key=['a', 'c'],
            value=['b', 'd']
        )
        self.assertIsNone(query.area)
        expected_xml = (
            '<osm-script output="xml" timeout="25">'
            '<union>'
            '<query type="node">'
            '<has-kv k="a" v="b"/>'
            '<has-kv k="c" v="d"/>'
            '<bbox-query bbox="custom" />'
            '</query>'
            '</union>'
            '<union>'
            '<item />'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body" />'
            '</osm-script>'
        )
        expected_xml_with_template = (
            '<osm-script output="xml" timeout="25">'
            '<union>'
            '<query type="node">'
            '<has-kv k="a" v="b"/>'
            '<has-kv k="c" v="d"/>'
            '<bbox-query {{bbox}}/>'
            '</query>'
            '</union>'
            '<union>'
            '<item/>'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body"/>'
            '</osm-script>'
        )
        # TODO, fix many keys
        human = 'All OSM objects with the key \'a\'=\'b\' in the canvas or layer extent are going to be downloaded.'
        test_query(query, expected_xml, expected_xml_with_template, human)

        # Many keys with None values
        query = QueryFactory(
            query_type=QueryType.BBox,
            osm_objects=[OsmType.Node],
            key=['a', 'c'],
            value=[None, None]
        )
        self.assertIsNone(query.area)
        expected_xml = (
            '<osm-script output="xml" timeout="25">'
            '<union>'
            '<query type="node">'
            '<has-kv k="a" />'
            '<has-kv k="c" />'
            '<bbox-query bbox="custom" />'
            '</query>'
            '</union>'
            '<union>'
            '<item />'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body" />'
            '</osm-script>'
        )
        expected_xml_with_template = (
            '<osm-script output="xml" timeout="25">'
            '<union>'
            '<query type="node">'
            '<has-kv k="a"/>'
            '<has-kv k="c"/>'
            '<bbox-query {{bbox}}/>'
            '</query>'
            '</union>'
            '<union>'
            '<item/>'
            '<recurse type="down"/>'
            '</union>'
            '<print mode="body"/>'
            '</osm-script>'
        )
        human = 'All OSM objects with the key \'a\' in the canvas or layer extent are going to be downloaded.'
        test_query(query, expected_xml, expected_xml_with_template, human)

    def test_make(self):
        """Test make query wuth valid indentation and lines."""
        query = QueryFactory(
            query_type=QueryType.BBox, key='foo', value='bar')
        self.assertIsNone(query.area)
        expected = (
            '<osm-script output="xml" timeout="25">\n    '
            '<union>\n        <query type="node">\n            '
            '<has-kv k="foo" v="bar"/>\n            '
            '<bbox-query {{bbox}}/>\n        </query>\n        '
            '<query type="way">\n            '
            '<has-kv k="foo" v="bar"/>\n            '
            '<bbox-query {{bbox}}/>\n        </query>\n        '
            '<query type="relation">\n            '
            '<has-kv k="foo" v="bar"/>\n            '
            '<bbox-query {{bbox}}/>\n        </query>\n    '
            '</union>\n    <union>\n        <item/>\n        '
            '<recurse type="down"/>\n    </union>\n    '
            '<print mode="body"/>\n</osm-script>\n')
        self.assertEqual(query.make(), expected)


if __name__ == '__main__':
    unittest.main()
