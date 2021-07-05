"""Manage the saved query in history or bookmark."""
import json
import logging
import re

from os import listdir, remove, rename
from os.path import join
from typing import List, Union

from qgis.core import QgsRectangle

from QuickOSM.core.utilities.json_encoder import EnumEncoder
from QuickOSM.core.utilities.tools import query_bookmark, query_historic
from QuickOSM.definitions.format import Format
from QuickOSM.definitions.osm import OSM_LAYERS, WHITE_LIST, LayerType

__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

LOGGER = logging.getLogger('QuickOSM')


class QueryManagement:
    """Manage the saved query in history or bookmark."""

    def __init__(
            self,
            query: Union[str, List[str]] = '',
            name: str = '',
            description: Union[str, List[str]] = '',
            area: Union[str, List[str]] = None,
            bbox: Union[QgsRectangle, List[QgsRectangle]] = None,
            output_geometry_types: list = None,
            white_list_column: dict = None,
            output_directory: str = None,
            output_format: Format = None
    ):
        """Constructor"""
        if isinstance(query, str):
            self.query = [query]
        else:
            self.query = query

        if isinstance(name, str):
            self.name = [name]
        else:
            self.name = name

        if description is None:
            self.description = ['']
        elif isinstance(description, str):
            self.description = [description]
        else:
            self.description = description

        if area is None:
            self.area = ['']
        elif isinstance(area, str):
            self.area = [area]
        else:
            self.area = area

        if bbox is None:
            self.bbox = ['']
        elif isinstance(bbox, QgsRectangle):
            self.bbox = [bbox]
        elif isinstance(bbox, str):
            self.bbox = [bbox]
        else:
            self.bbox = bbox

        if output_geometry_types is None:
            self.output_geom_type = [OSM_LAYERS]
        elif isinstance(output_geometry_types[0], LayerType):
            self.output_geom_type = [output_geometry_types]
        else:
            self.output_geom_type = output_geometry_types

        if white_list_column is None:
            self.white_list = [WHITE_LIST]
        elif isinstance(white_list_column, dict):
            self.white_list = [white_list_column]
        else:
            self.white_list = white_list_column

        if output_directory is None:
            self.output_directory = ['']
        elif isinstance(output_directory, str):
            self.output_directory = [output_directory]
        else:
            self.output_directory = output_directory

        if output_format is None:
            self.output_format = ['']
        elif isinstance(output_format, Format):
            self.output_format = [output_format]
        else:
            self.output_format = output_format

    def write_query_historic(self):
        """Write new query in the history folder"""
        history_folder = query_historic()
        files = listdir(history_folder)
        nb_files = len(files)

        if nb_files == 10:
            remove(join(history_folder, 'query_saved_0.json'))
            files = listdir(history_folder)
            for k, file in enumerate(files):
                former_file = join(history_folder, file)
                new_file = join(history_folder, 'query_saved_{}.json'.format(k))
                rename(former_file, new_file)
            new_file = join(history_folder, 'query_saved_{}.json'.format(nb_files - 1))
        else:
            new_file = join(history_folder, 'query_saved_{}.json'.format(nb_files))

        self.write_json(new_file)

    def add_bookmark(self, name_bookmark: str):
        """Add a new query in the bookmark folder"""
        bookmark_folder = query_bookmark()
        files = listdir(bookmark_folder)
        nb_files = len(files)

        self.name[0] = name_bookmark if name_bookmark != "OsmQuery" else 'OsmQuery_{}'.format(nb_files)
        final_name = self.name[0] + '.json'

        new_file = join(bookmark_folder, final_name)
        self.write_json(new_file)

    def write_json(self, file: str):
        """Write the saved file in json"""
        data = {
            'query': self.query,
            'description': self.description,
            'file_name': self.name[0],
            'query_name': self.name,
            'area': self.area,
            'bbox': self.bbox,
            'output_geom_type': self.output_geom_type,
            'white_list_column': self.white_list,
            'output_directory': self.output_directory,
            'output_format': self.output_format
        }

        with open(file, 'w', encoding='utf8') as json_file:
            json.dump(data, json_file, cls=EnumEncoder)

    @staticmethod
    def remove_bookmark(name: str):
        """Remove a bookmark query"""
        bookmark_folder = query_bookmark()

        file = join(bookmark_folder, name + '.json')
        remove(file)
        if name.startswith('bookmark_'):
            list_bookmark = filter(lambda query_file: query_file.startswith('OsmQuery_'), name)
            num = re.findall('OsmQuery_(0-9)', name)[0]
            for k, file in enumerate(list_bookmark):
                if k >= num:
                    former_file = join(bookmark_folder, file + '.json')
                    new_file = join(bookmark_folder, 'OsmQuery_{}.json'.format(k))
                    rename(former_file, new_file)

    @staticmethod
    def add_empty_query_in_bookmark(data: dict) -> dict:
        """Add a query in a bookmark file"""
        data['query'].append('')
        data['query_name'].append('')
        data['area'].append('')
        data['bbox'].append('')
        data['output_geom_type'].append(OSM_LAYERS)
        data['white_list_column'].append(WHITE_LIST)
        data['output_format'].append(None)
        data['output_directory'].append(None)

        return data

    @staticmethod
    def remove_query_in_bookmark(data: dict, num_query: int) -> dict:
        """Remove a query in a bookmark file."""
        data['query_name'].pop(num_query)
        data['query'].pop(num_query)
        data['area'].pop(num_query)
        data['bbox'].pop(num_query)
        data['output_geom_type'].pop(num_query)
        data['white_list_column'].pop(num_query)
        data['output_format'].pop(num_query)
        data['output_directory'].pop(num_query)

        return data

    def rename_bookmark(self, former_name: str, new_name: str, data: dict):
        """Rename a bookmark query"""
        bookmark_folder = query_bookmark()

        new_file = join(bookmark_folder, new_name + '.json')

        with open(new_file, 'w', encoding='utf8') as new_json_file:
            json.dump(data, new_json_file, cls=EnumEncoder)

        self.remove_bookmark(former_name)

    @staticmethod
    def update_bookmark(data: dict):
        """Rename a bookmark query"""
        bookmark_folder = query_bookmark()

        bookmark_file = join(bookmark_folder, data['file_name'] + '.json')

        with open(bookmark_file, 'w', encoding='utf8') as json_file:
            json.dump(data, json_file, cls=EnumEncoder)
