""" Parser of the presets file. """

import collections as col
import xml.dom.minidom as xml

from QuickOSM.qgis_plugin_tools.tools.resources import resources_path

PRESET_PATH = resources_path('JOSM_preset', 'defaultpresets.xml')

__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class PresetsParser:
    """Management of the presets file."""

    def __init__(self):

        self.file = xml.parse(PRESET_PATH)
        self.items = None

    def parser(self) -> col.namedtuple:
        """
        Parse the presets file

        :return: a dictionary of two dictionaries.
        Elements contains the data needed for the completer
        Items contains the data needed for the preset
        Items_combo contains couples key/value needed to specify more the query
        :rtype: namedTuple of two dictionaries
        """

        def fetch_keys(group, heirs_name: list) -> list:
            """
            This is a recursive function that dig into the file to find items inside groups

            Ancestors represents the path to the item/group
            Heirs contains all the items accessible from the item/group

            :group: an xml elements

            :return: the list of heirs.
            :rtype: list[str]
            """
            ancestors_name.append(group.getAttribute('name'))

            children = filter(lambda child: self.node_filter(child), group.childNodes)
            for inner_group in children:
                heirs_item_name = fetch_keys(inner_group, [])

                name_completion = ancestors_name[0]
                if len(ancestors_name) != 1:
                    for ancestor in ancestors_name[1:]:
                        name_completion += '/' + ancestor
                ancestors_name.pop(-1)
                data_group = data('group', ancestors_name, heirs_item_name)
                elements[name_completion] = data_group

                heirs_name += heirs_item_name

            children = filter(lambda child: self.node_filter(child, 'item'), group.childNodes)
            for item in children:
                data_item = {}
                name = item.getAttribute('name')

                for keys in item.getElementsByTagName('key'):
                    key = keys.getAttribute('key')
                    value = keys.getAttribute('value')

                    data_item[key] = value

                items[name] = data_item

                children = filter(lambda child: self.node_filter(child, 'combo'), item.childNodes)
                for combo in children:
                    key = combo.getAttribute('key')
                    value = combo.getAttribute('values').split(',')

                    data_item[key] = value

                items_combo[name] = data_item
                heirs_name.append(name)

                name_completion = ''
                ancestors = []
                for ancestor in ancestors_name:
                    name_completion += ancestor + '/'
                    ancestors.append(ancestor)
                name_completion += name

                data_item = data('item', ancestors, [name])
                elements[name_completion] = data_item

            return heirs_name

        elements = {}
        items = {}
        items_combo = {}

        data = col.namedtuple('data', ['type', 'ancestors', 'heirs'])

        root = self.file.firstChild
        children = filter(lambda child: self.node_filter(child), root.childNodes)

        for group in children:

            ancestors_name = []

            heirs_name = fetch_keys(group, [])

            name_completion = group.getAttribute('name')
            data_group = data('group', ancestors_name[:-1], heirs_name)
            elements[name_completion] = data_group

        results = col.namedtuple('results', ['elements', 'items'])
        results = results(elements, items)

        self.items = items_combo

        return results

    @staticmethod
    def node_filter(node, search: str = 'group') -> bool:
        """
        Test if the node has the tag we search
        """
        if isinstance(node, xml.Element):
            return node.tagName == search

    def osm_keys_values(self) -> dict:
        """ Retrieval of key/value couple """
        couple = {}

        key = []
        for item in self.items:
            for k in list(self.items[item].keys()):
                value = self.items[item][k]
                if k in key:
                    if isinstance(value, list):
                        for val in value:
                            if val not in couple[k]:
                                couple[k].append(val)
                    elif value not in couple[k]:
                        couple[k].append(value)
                elif isinstance(value, str):
                    key.append(k)
                    couple[k] = [value]
                elif isinstance(value, list):
                    couple[k] = [value[0]]
                    for val in value[1:]:
                        couple[k].append(val)

        return couple
