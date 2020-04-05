"""Tests for the query preparation."""

import unittest

from qgis.core import QgsRectangle

from ..query_preparation import QueryPreparation
from ..api.nominatim import Nominatim

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class FakeNominatim(Nominatim):
    """NOTE, because of the fake nominatim instance,
    latitude, longitude and relation ID are wrong and
    are replaced by the area name.
    """

    def get_first_polygon_from_query(self, fake_query):
        # It normally returns relation ID.
        return fake_query

    def get_first_point_from_query(self, fake_query):
        # It normally returns lat and lon
        return fake_query, fake_query


class TestQueryPreparation(unittest.TestCase):

    """Tests for the query preparation."""

    def setUp(self):
        self.maxDiff = None

    def test_is_oql(self):
        """Test if OQL or XML."""
        self.assertTrue(QueryPreparation('out skel qt;').is_oql_query())
        self.assertFalse(QueryPreparation('</osm-script>').is_oql_query())

    def test_replace_center(self):
        """Test we can replace {{center}} in a query."""
        extent = QgsRectangle(10.00, 0.5, 20.00, 1.5)

        def test(data, result, e=None):
            q = QueryPreparation(data, extent=e)
            q._replace_center()
            self.assertEqual(q._query_prepared, result)

        # No center.
        query = 'foobar{{bbox}}foobar'
        expected = 'foobar{{bbox}}foobar'
        test(query, expected)

        # One center in XML.
        query = 'foobar{{center}}foobar'
        expected = 'foobarlat="1.0" lon="15.0"foobar'
        test(query, expected, extent)

        # One center in OQL.
        query = 'foobar{{center}}foobar;'
        expected = 'foobar1.0,15.0foobar;'
        test(query, expected, extent)

        # Two centers in OQL.
        query = 'foobar{{center}}foobar{{center}}foobar;'
        expected = 'foobar1.0,15.0foobar1.0,15.0foobar;'
        test(query, expected, extent)

        # One center and one OQL in OQL.
        query = 'foobar{{center}}foobar{{bbox}}foobar;'
        expected = 'foobar1.0,15.0foobar{{bbox}}foobar;'
        test(query, expected, extent)

    def test_replace_bbox(self):
        """Test we can replace {{bbox}} in a query."""
        extent = QgsRectangle(10.00, 0.5, 20.00, 1.5)

        def test(data, result, e=None):
            q = QueryPreparation(data, extent=e)
            q.replace_bbox()
            self.assertEqual(q._query_prepared, result)

        # One bbox.
        query = 'foobar{{bbox}}foobar'
        expected = 'foobare="20.0" n="1.5" s="0.5" w="10.0"foobar'
        test(query, expected, extent)

        # Two bbox.
        query = 'foo{{bbox}}foo{{bbox}}foo'
        expected = 'fooe="20.0" n="1.5" s="0.5" w="10.0"fooe="20.0" n="1.5" ' \
                   's="0.5" w="10.0"foo'
        test(query, expected, extent)

        # One bbox in OQL.
        query = 'foobar{{bbox}}foobar;'
        expected = 'foobar0.5,10.0,1.5,20.0foobar;'
        test(query, expected, extent)

        # One center and one OQL in OQL.
        query = 'foobar{{center}}foobar{{bbox}}foobar;'
        expected = 'foobar{{center}}foobar0.5,10.0,1.5,20.0foobar;'
        test(query, expected, extent)

    def test_replace_geocode_coords(self):
        """Test we can replace {{geocodeCoords:}} in a query."""

        def test(data, result, nominatim=None):
            q = QueryPreparation(data, area=nominatim)
            q._nominatim = FakeNominatim()
            q._replace_geocode_coords()
            self.assertEqual(q._query_prepared, result)

        # Test with another area instead of Paris in XML
        query = 'foobar{{geocodeCoords:Paris,France}}foobar'
        expected = 'foobarlat="not_paris" lon="not_paris"foobar'
        test(query, expected, 'not_paris')

        # Test with Paris in XML
        query = 'foobar{{geocodeCoords:Paris,France}}foobar'
        expected = 'foobarlat="Paris,France" lon="Paris,France"foobar'
        test(query, expected)

        # Test with WKT in XML
        query = 'foobar{{geocodeCoords:POINT(6 10)}}foobar'
        expected = 'foobarlat="10.0" lon="6.0"foobar'
        test(query, expected)

        # Test with WKT in OQL.
        query = 'foobar{{geocodeCoords:POINT(6 10)}}foobar;'
        expected = 'foobar10.0,6.0foobar;'
        test(query, expected)

        # Test with Paris in OQL.
        query = 'foobar{{geocodeCoords:Paris,France}}foobar;'
        expected = 'foobarParis,France,Paris,Francefoobar;'
        test(query, expected)

        # Test with Paris and Montpellier.
        query = (
            'foo{{geocodeCoords:Paris,France}}bar'
            'foo{{geocodeCoords:Montpellier}}bar')
        expected = (
            'foolat="Paris,France" lon="Paris,France"bar'
            'foolat="Montpellier" lon="Montpellier"bar')
        test(query, expected)

    def test_replace_geocode_area(self):
        """Test we can replace {{geocodeArea}} in a query."""

        # There is a HACK in the code to return 12345 and 54321 in the code.

        def test(data, result, nominatim=None):
            q = QueryPreparation(data, area=nominatim)
            q._nominatim = FakeNominatim()
            q._replace_geocode_area()
            self.assertEqual(q._query_prepared, result)

        # Test with another place.
        query = 'foobar{{geocodeArea:foo_BAR}}foobar'
        expected = 'foobarref="3600054321" type="area"foobar'
        test(query, expected, 'bar_FOO')

        # Test with Paris.
        query = 'foobar{{geocodeArea:foo_BAR}}foobar'
        expected = 'foobarref="3600012345" type="area"foobar'
        test(query, expected)

        # Test with Paris in XML.
        query = 'foobar{{geocodeArea:foo_BAR}}foobar'
        expected = 'foobarref="3600012345" type="area"foobar'
        test(query, expected)

        # Test with Paris in OQL.
        query = 'foobar{{geocodeArea:foo_BAR}}foobar;'
        expected = 'foobararea(3600012345)foobar;'
        test(query, expected)

        # Test with a fake OSM relation.
        query = 'foobar{{geocodeArea:123456}}foobar'
        expected = 'foobarref="3600123456" type="area"foobar'
        test(query, expected)

        # Test with foo_BAR
        # and bar_FOO.
        query = (
            'foo{{geocodeArea:foo_BAR}}bar'
            'foo{{geocodeArea:bar_FOO}}bar')
        expected = (
            'fooref="3600012345" type="area"bar'
            'fooref="3600054321" type="area"bar')
        test(query, expected)

    def test_clean_query(self):
        """Test we can clean a query."""

        def test(data, result):
            q = QueryPreparation(data)
            q.clean_query()
            self.assertEqual(q._query_prepared, result)

        test('  foo;;   ', 'foo;')
        test('	foo;	', 'foo;')
        test('   	foo	   ', 'foo')

    def test_prepare_query(self):
        """Test we can prepare a query."""
        # Test geocodeArea simple.
        # There is a HACK in the code to return 12345
        query = (
            '<osm-script output="xml" timeout="25">    <id-query '
            '{{geocodeArea:foo_BAR}} into="area_0"/>    '
            '<union>        <query type="node">            '
            '<has-kv k="a" v="b"/>            '
            '<area-query from="area_0"/>        </query>        <query type='
            '"way">            <has-kv k="a" v="b"/>            <area-query '
            'from="area_0"/>        </query>        '
            '<query type="relation">            '
            '<has-kv k="a" v="b"/>            '
            '<area-query from="area_0"/>        </query>    </union>    '
            '<union>        <item/>        <recurse type="down"/>    '
            '</union>   <print mode="body"/></osm-script>'
        )
        expected = (
            '<osm-script output="xml" timeout="25">    <id-query '
            'ref="3600012345" type="area" into="area_0"/>    <union>        '
            '<query type="node">            <has-kv k="a" v="b"/>            '
            '<area-query from="area_0"/>        </query>        '
            '<query type="way">            <has-kv k="a" v="b"/>            '
            '<area-query from="area_0"/>        </query>        '
            '<query type="relation">            '
            '<has-kv k="a" v="b"/>            '
            '<area-query from="area_0"/>        </query>    </union>    '
            '<union>        <item/>        <recurse type="down"/>    '
            '</union>   <print mode="body"/></osm-script>'
        )
        q = QueryPreparation(query)
        q._nominatim = FakeNominatim()
        self.assertEqual(q.prepare_query(), expected)


if __name__ == '__main__':
    suite = unittest.makeSuite(TestQueryPreparation)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
