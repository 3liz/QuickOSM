"""Query factory, for building queries."""

import re
from xml.dom.minidom import parseString

from .exceptions import QueryFactoryException
from ..definitions.osm import OsmType, QueryType
from ..qgis_plugin_tools.tools.i18n import tr

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


SPACE_INDENT = '    '

ALL_VALUES = tr(
    'All OSM objects with the key {key} in {extent} are going to be downloaded.')
ALL_VALUES_WITH_DISTANCE = tr(
    'All OSM objects with the key {key} in {dist} meters of {extent} are going to be downloaded.')
NO_KEY = tr('All OSM objects in {extent} are going to be downloaded.')
NO_KEY_WITH_DISTANCE = tr(
    'All OSM objects in {dist} meters of {extent} are going to be downloaded.')
ATTRIBUTE_ONLY = tr(
    'All OSM objects with the key {key} are going to be downloaded.')


class QueryFactory:

    """Build a XML or OQL query."""

    def __init__(
            self,
            query_type=None,
            key=None,
            value=None,
            area=None,
            around_distance=None,
            osm_objects=None,
            output='xml',
            timeout=25,
            print_mode='body',
    ):
        """
        Query Factory constructor according to Overpass API.

        :param query_type: The type of query to build.
        :type query_type: QueryType

        :param key: OSM key or None.
        :type key: str,None

        :param value: OSM value or None.
        :type value: str,None

        :param area: A place name if needed or None.
        :type area: str,None

        :param around_distance: Distance to use if it's an around query or None
        :type around_distance: int,None

        :param osm_objects: List of osm objects to query on (node/way/relation)
        :type osm_objects: list(OsmType)

        :param output:output of overpass : XML or JSON
        :type output: str

        :param timeout: Timeout of the query
        :type timeout: int

        :param print_mode: Print type of the overpass query (read overpass doc)
        :type print_mode: str
        """
        self._query_type = query_type

        if isinstance(key, str):
            key = [key]
        elif key is None:
            key = []

        # The initial key might be an empty key, remove it.
        self._key = [x for x in key if x]

        if isinstance(value, str):
            if value == '':
                value = []
            else:
                value = [value]
        elif value is None:
            value = []
        self._value = value

        # Nominatim might be:
        # a list of places or
        # a single place or
        # not defined (None)
        self._area = None
        if area:
            self._area = [name.strip() for name in area.split(';')]

        self._distance_around = around_distance

        if osm_objects is None:
            # If None, we had all OSM Types from the enum
            # noinspection PyTypeChecker
            osm_objects = list(OsmType)

        self._osm_objects = osm_objects
        self._timeout = timeout
        self._output = output
        self._print_mode = print_mode

        self._checked = False

    @property
    def area(self):
        """Return the area defined for the query.

        Either None if no area or a list of areas.

        :rtype: list
        """
        return self._area

    def _check_parameters(self):
        """Internal function to check that the query can be built.

        :raise QueryFactoryException
        :return True if everything went fine.
        """
        if type(self._query_type) != QueryType:
            raise QueryFactoryException(tr('Wrong query type.'))

        for osmObject in self._osm_objects:
            if type(osmObject) != OsmType:
                raise QueryFactoryException(tr('Wrong OSM object.'))

        if self._query_type == QueryType.AroundArea:
            if not self._distance_around:
                raise QueryFactoryException(
                    tr('No distance provided with the "around" query.'))

            try:
                int(self._distance_around)
            except ValueError:
                raise QueryFactoryException(
                    tr('Wrong distance parameter.'))

        if self._distance_around and self._query_type == QueryType.InArea:
            raise QueryFactoryException(
                tr('Distance parameter is incompatible with this query.'))

        if self._query_type == QueryType.InArea and not self._area:
            raise QueryFactoryException(
                tr('Named area is required when the query is "In".'))

        if self._query_type == QueryType.AroundArea and not self._area:
            raise QueryFactoryException(
                tr('Named area or a WKT is required when the query is "Around".'))

        if not self._key and self._value:
            raise QueryFactoryException(
                tr('Not possible to query a specific value without a key.'))

        if self._query_type == QueryType.NotSpatial:
            if not self._key:
                raise QueryFactoryException(
                    tr('A key is required.'))

        if len(self._key) > len(self._value):
            if len(self._key) != 1:
                raise QueryFactoryException(
                    tr('Missing some values for some keys.'))

        if len(self._key) < len(self._value):
            raise QueryFactoryException(
                tr('Missing some keys for some values.'))

        self._checked = True
        return True

    @staticmethod
    def get_pretty_xml(query):
        """Helper to get a good indentation of the query."""
        xml = parseString(query)
        return xml.toprettyxml()

    @staticmethod
    def replace_template(query):
        """Add some templates tags to the query {{ }}.

        This is a hack to get pretty XML working, because templates are not a
        valid XML !
        """
        query = re.sub(
            r' area_coords="(.*?)"', r' {{geocodeCoords:\1}}', query)
        query = re.sub(
            r' area="(.*?)"', r' {{geocodeArea:\1}}', query)
        query = query.replace(' bbox="custom"', ' {{bbox}}')
        return query

    def generate_xml(self):
        """Generate the XML.

        The query will not be valid because of Overpass templates !
        """
        query = '<osm-script output="{}" timeout="{}">'.format(
            self._output, self._timeout)

        if self._area:
            nominatim = self._area
        else:
            nominatim = None

        if nominatim and self._query_type != QueryType.AroundArea:

            for i, one_place in enumerate(nominatim):
                query += '<id-query area="{}" into="area_{}"/>'.format(
                    one_place, i)

        query += '<union>'

        loop = 1 if not nominatim else len(nominatim)

        for osm_object in self._osm_objects:
            for i in range(0, loop):
                query += '<query type="{}">'.format(osm_object.value.lower())
                for j, key in enumerate(self._key):
                    query += '<has-kv k="{}" '.format(key)
                    if j < len(self._value) and self._value[j] is not None:
                        query += 'v="{}"'.format(self._value[j])

                    query += '/>'

                if self._area and self._query_type != QueryType.AroundArea:
                    query += '<area-query from="area_{}" />'.format(i)

                elif self._area and self._query_type == QueryType.AroundArea:
                    query += '<around area_coords="{}" radius="{}" />'.format(
                        nominatim[i], self._distance_around)

                elif self._query_type == QueryType.BBox:
                    query = '{}<bbox-query bbox="custom" />'.format(query)

                query += '</query>'

        query += '</union>'
        query += '<union>'
        query += '<item />'
        query += '<recurse type="down"/>'
        query += '</union>'
        query += '<print mode="{}" />'.format(self._print_mode)
        query += '</osm-script>'

        return query

    def make(self):
        """Make the query.

        @return: query
        @rtype: str
        """
        self._check_parameters()
        query = self.generate_xml()

        # get_pretty_xml works only with a valid XML, no template {{}}
        # So we replace fake XML after
        query = QueryFactory.get_pretty_xml(query)

        # get_pretty_xml add on XML header, let's remove the first line
        query = '\n'.join(query.split('\n')[1:])

        query = QueryFactory.replace_template(query)
        query = query.replace('	', SPACE_INDENT)

        return query

    def _make_for_test(self):
        """Helper for tests only!

        Without indentation and lines.
        """
        query = self.make()
        query = query.replace(SPACE_INDENT, '').replace('\n', '')
        return query

    def friendly_message(self):
        """Create a friendly/human message about what the query will do.

        @return: The message
        @rtype: str
        """
        self._check_parameters()

        place = self._area
        if self._area is not None:
            # human format a list
            if len(self._area) == 1:
                place = self._area[0]  # simply unwrap the list
            elif len(self._area) == 2:
                place = ' {} '.format(tr('and')).join(self._area)
            else:
                place = ', '.join(self._area[:-2]) + ', '
                place = place + ' {} '.format(tr('and')).join(self._area[-2:])

        extent_lbl = ''
        dist_lbl = ''
        key_lbl = ''
        use_with_dist = False
        use_all_vals = False
        attrib_only = False
        
        # first translate the location information
        if self._query_type == QueryType.InArea:
            extent_lbl = place
                
        elif self._query_type == QueryType.AroundArea:
            extent_lbl = place
            dist_lbl = self._distance_around
            use_with_dist = True

        elif self._query_type == QueryType.BBox:
            extent_lbl = tr('the canvas or layer extent')
            
        elif self._query_type == QueryType.NotSpatial:
            attrib_only = True

        # Next get the key / values
        if len(self._key) == 0:
            key = None
        else:
            key = self._key[0]

        if len(self._value) == 0:
            val = None
        else:
            val = self._value[0]
                
        if key is not None:
            # Do we have a value?
            use_all_vals = True
            if val is not None:
                # provide both the key and value
                key_lbl = "'{key}'='{val}'".format(key=key, val=val)
            else:
                # provide just the key
                key_lbl = "'{key}'".format(key=key)

        if attrib_only:
            msg = ATTRIBUTE_ONLY.format(key=key_lbl)
            
        elif use_all_vals:
            if use_with_dist:
                msg = ALL_VALUES_WITH_DISTANCE.format(key=key_lbl, dist=dist_lbl, extent=extent_lbl)
            else:
                msg = ALL_VALUES.format(key=key_lbl,extent=extent_lbl)
        else:
            if use_with_dist:
                msg = NO_KEY_WITH_DISTANCE.format(dist=dist_lbl, extent=extent_lbl)
            else:
                msg = NO_KEY.format(extent=extent_lbl)

        return msg
