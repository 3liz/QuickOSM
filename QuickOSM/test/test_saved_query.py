"""Tests for the bookmark and the history of queries."""
import json
import os

from qgis.core import QgsCoordinateReferenceSystem, QgsRectangle
from qgis.testing import unittest

from QuickOSM.core.utilities.json_encoder import as_enum
from QuickOSM.core.utilities.tools import query_bookmark
from QuickOSM.definitions.format import Format
from QuickOSM.definitions.gui import Panels
from QuickOSM.ui.dialog import Dialog
from QuickOSM.ui.edit_bookmark import EditBookmark

__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class TestBookmarkQuery(unittest.TestCase):
    """Tests for the bookmark and the history of queries."""

    def setUp(self):
        """Set up the tests"""
        self.maxDiff = None
        self.bookmark_folder = query_bookmark()

        self.dialog = Dialog()

        index = self.dialog.table_keys_values_qq.cellWidget(0, 1).findText('amenity')
        self.dialog.table_keys_values_qq.cellWidget(0, 1).setCurrentIndex(index)
        index = self.dialog.table_keys_values_qq.cellWidget(0, 2).findText('bench')
        self.dialog.table_keys_values_qq.cellWidget(0, 2).setCurrentIndex(index)
        self.dialog.places_edits[Panels.QuickQuery].setText('foo')
        self.dialog.save_query.click()

        self.bookmark = self.dialog.list_bookmark_mp.item(0)
        layout_label = self.dialog.list_bookmark_mp.itemWidget(self.bookmark).layout()
        self.name_bookmark = layout_label.itemAt(0).itemAt(0).widget().text()

    def set_up_bookmark_data_text(self) -> dict:
        """Load the data save in the json file linked to the bookmark."""
        bookmark_file = os.path.join(
            self.bookmark_folder, self.name_bookmark, self.name_bookmark + '.json')
        with open(bookmark_file, encoding='utf8') as json_file:
            data_bookmark = json.load(json_file)

        return data_bookmark

    def set_up_bookmark_data(self) -> dict:
        """Load the data save in the json file linked to the bookmark."""
        bookmark_folder = query_bookmark()
        bookmark_file = os.path.join(
            bookmark_folder, self.name_bookmark, self.name_bookmark + '.json')
        with open(bookmark_file, encoding='utf8') as json_file:
            data_bookmark = json.load(json_file, object_hook=as_enum)

        return data_bookmark

    def tearDown(self):
        """End of the tests"""
        self.dialog.external_panels[Panels.MapPreset].remove_bookmark(self.bookmark, self.name_bookmark)

    def test_save_in_bookmark(self):
        """Test if the file is save in bookmark."""
        nb_bookmark = self.dialog.list_bookmark_mp.count()
        self.assertEqual(nb_bookmark, 1)
        self.assertEqual(self.name_bookmark, 'amenity_bench_foo')

    def test_bookmark_format(self):
        """Test if the file in bookmark is as expected."""
        data_bookmark = self.set_up_bookmark_data_text()

        expected_json = {
            "query":
                [
                    "[out:xml] [timeout:25];\n {{geocodeArea:foo}} -> .area_0;\n(\n"
                    "    node[\"amenity\"=\"bench\"](area.area_0);\n    "
                    "way[\"amenity\"=\"bench\"](area.area_0);\n    "
                    "relation[\"amenity\"=\"bench\"](area.area_0);\n);\n"
                    "(._;>;);\nout body;"
                ],
            "description":
                ["All OSM objects with the key 'amenity'='bench' in foo are going to be downloaded."],
            "advanced": False,
            "file_name": "amenity_bench_foo",
            "query_layer_name": ["amenity_bench_foo"],
            "query_name": ["Query 1"],
            "type_multi_request": [[]],
            "keys": [["amenity"]],
            "values": [["bench"]],
            "area": ["foo"],
            "bbox": [""],
            "output_geom_type":
                [
                    [
                        {"__enum__": "LayerType.Points"},
                        {"__enum__": "LayerType.Lines"},
                        {"__enum__": "LayerType.Multilinestrings"},
                        {"__enum__": "LayerType.Multipolygons"}
                    ]
                ],
            "white_list_column":
                [{"multilinestrings": None, "points": None, "lines": None, "multipolygons": None}],
            "output_directory": [""],
            "output_format": [{"__enum__": "Format.GeoPackage"}]
        }

        self.assertDictEqual(expected_json, data_bookmark)

    def test_view_bookmark(self):
        """Test if we can display a bookmark."""
        data_bookmark = self.set_up_bookmark_data()

        edit_dialog = EditBookmark(self.dialog, data_bookmark)

        self.assertEqual(data_bookmark['file_name'], edit_dialog.bookmark_name.text())
        self.assertEqual(
            data_bookmark['description'], edit_dialog.description.toPlainText().split('\\n')
        )
        self.assertEqual(data_bookmark['query_layer_name'][0], edit_dialog.layer_name.text())
        self.assertEqual(data_bookmark['query'][0], edit_dialog.query.toPlainText())
        self.assertEqual(data_bookmark['area'][0], edit_dialog.area.text())
        self.assertFalse(edit_dialog.bbox.outputExtent().xMinimum())
        self.assertFalse(edit_dialog.bbox.outputExtent().yMinimum())
        self.assertTrue(edit_dialog.checkbox_points.isChecked())
        self.assertTrue(edit_dialog.checkbox_lines.isChecked())
        self.assertTrue(edit_dialog.checkbox_multilinestrings.isChecked())
        self.assertTrue(edit_dialog.checkbox_multipolygons.isChecked())
        self.assertFalse(edit_dialog.white_points.text())
        self.assertFalse(edit_dialog.white_lines.text())
        self.assertFalse(edit_dialog.white_multilinestrings.text())
        self.assertFalse(edit_dialog.white_multipolygons.text())
        self.assertEqual(edit_dialog.combo_output_format.currentData(), Format.GeoPackage)
        self.assertEqual(
            data_bookmark['output_directory'][0], edit_dialog.output_directory.filePath()
        )

        nb_queries = edit_dialog.list_queries.count()
        self.assertEqual(nb_queries, 1)

        edit_dialog.bookmark_name.setText('Test a new name')
        edit_dialog.button_cancel.click()

        self.dialog.external_panels[Panels.MapPreset].update_bookmark_view()

        self.bookmark = self.dialog.list_bookmark_mp.item(0)
        layout_label = self.dialog.list_bookmark_mp.itemWidget(self.bookmark).layout()
        self.name_bookmark = layout_label.itemAt(0).itemAt(0).widget().text()
        self.assertNotEqual(self.name_bookmark, 'Test a new name')

    def test_edit_rename_bookmark(self):
        """Test if we can edit and rename a bookmark."""
        data_bookmark = self.set_up_bookmark_data()

        edit_dialog = EditBookmark(self.dialog, data_bookmark)
        edit_dialog.bookmark_name.setText('Test a new name')
        edit_dialog.button_validate.click()

        self.dialog.external_panels[Panels.MapPreset].update_bookmark_view()

        self.bookmark = self.dialog.list_bookmark_mp.item(0)
        layout_label = self.dialog.list_bookmark_mp.itemWidget(self.bookmark).layout()
        self.name_bookmark = layout_label.itemAt(0).itemAt(0).widget().text()
        self.assertEqual(self.name_bookmark, 'Test a new name')

    def test_edited_bookmark_file(self):
        """Test if we can edit a bookmark and check the edited json file."""
        data_bookmark = self.set_up_bookmark_data()

        edit_dialog = EditBookmark(self.dialog, data_bookmark)

        edit_dialog.description.setPlainText('Be or not to be...\\nShakespear')
        edit_dialog.layer_name.setText('Misery')
        edit_dialog.query.setPlainText('I would like two pencils please.')
        edit_dialog.checkbox_points.setChecked(True)
        edit_dialog.checkbox_lines.setChecked(True)
        edit_dialog.checkbox_multilinestrings.setChecked(False)
        edit_dialog.checkbox_multipolygons.setChecked(False)
        edit_dialog.white_points.setText('name')
        index = edit_dialog.combo_output_format.findData(Format.Kml)
        edit_dialog.combo_output_format.setCurrentIndex(index)

        edit_dialog.button_validate.click()
        self.bookmark = self.dialog.list_bookmark_mp.item(0)

        new_data = self.set_up_bookmark_data_text()

        expected_json = {
            "query":
                [
                    "I would like two pencils please."
                ],
            "description":
                ["Be or not to be...", "Shakespear"],
            "advanced": False,
            "file_name": "amenity_bench_foo",
            "query_layer_name": ["Misery"],
            "query_name": ["Query 1"],
            "type_multi_request": [[]],
            "keys": [["amenity"]],
            "values": [["bench"]],
            "area": ["foo"],
            "bbox": [{'__extent__': '0.0 0.0 0.0 0.0'}],
            "output_geom_type":
                [
                    [
                        {"__enum__": "LayerType.Points"},
                        {"__enum__": "LayerType.Lines"}
                    ]
                ],
            "white_list_column":
                [{"multilinestrings": None, "points": 'name', "lines": None, "multipolygons": None}],
            "output_directory": [""],
            "output_format": [{"__enum__": "Format.Kml"}]
        }

        self.assertDictEqual(expected_json, new_data)

    def test_bookmark_several_query(self):
        """Test if we can manage (add and remove) several queries in a bookmark."""
        data_bookmark = self.set_up_bookmark_data()

        edit_dialog = EditBookmark(self.dialog, data_bookmark)

        self.assertEqual(edit_dialog.current_query, 0)
        edit_dialog.button_add.click()

        nb_queries = edit_dialog.list_queries.count()
        self.assertEqual(nb_queries, 2)
        self.assertEqual(edit_dialog.current_query, 1)
        self.assertEqual(edit_dialog.layer_name.text(), '')

        edit_dialog.layer_name.setText('Query 2')

        edit_dialog.button_validate.click()
        self.bookmark = self.dialog.list_bookmark_mp.item(0)

        new_data = self.set_up_bookmark_data_text()

        expected_json = {
            "query":
                [
                    "[out:xml] [timeout:25];\n {{geocodeArea:foo}} -> .area_0;\n(\n"
                    "    node[\"amenity\"=\"bench\"](area.area_0);\n    "
                    "way[\"amenity\"=\"bench\"](area.area_0);\n    "
                    "relation[\"amenity\"=\"bench\"](area.area_0);\n);\n"
                    "(._;>;);\nout body;",
                    ""
                ],
            "description":
                ["All OSM objects with the key 'amenity'='bench' in foo are going to be downloaded."],
            "advanced": False,
            "file_name": "amenity_bench_foo",
            "query_layer_name": ["amenity_bench_foo", "Query 2"],
            "query_name": ["Query 1", "Query 2"],
            "type_multi_request": [[], []],
            "keys": [["amenity"], [""]],
            "values": [["bench"], [""]],
            "area": ["foo", ""],
            "bbox": [{'__extent__': '0.0 0.0 0.0 0.0'}, {'__extent__': '0.0 0.0 0.0 0.0'}],
            "output_geom_type":
                [
                    [
                        {"__enum__": "LayerType.Points"},
                        {"__enum__": "LayerType.Lines"},
                        {"__enum__": "LayerType.Multilinestrings"},
                        {"__enum__": "LayerType.Multipolygons"}
                    ], [
                        {"__enum__": "LayerType.Points"},
                        {"__enum__": "LayerType.Lines"},
                        {"__enum__": "LayerType.Multilinestrings"},
                        {"__enum__": "LayerType.Multipolygons"}
                    ]
                ],
            "white_list_column":
                [
                    {"multilinestrings": None, "points": None, "lines": None, "multipolygons": None},
                    {"multilinestrings": None, "points": None, "lines": None, "multipolygons": None}
                ],
            "output_directory": ["", ""],
            "output_format": [{"__enum__": "Format.GeoPackage"}, None]
        }

        self.assertDictEqual(expected_json, new_data)

        edit_dialog.list_queries.setCurrentRow(0)
        self.assertEqual(edit_dialog.current_query, 0)
        self.assertEqual(edit_dialog.layer_name.text(), 'amenity_bench_foo')

        edit_dialog.delete_query(0)

        nb_queries = edit_dialog.list_queries.count()
        self.assertEqual(nb_queries, 1)
        self.assertEqual(edit_dialog.layer_name.text(), 'Query 2')

        crs = QgsCoordinateReferenceSystem('EPSG:4326')
        x_min = 2.71828
        x_max = 3.1415926
        y_min = 0.0
        y_max = 1.6180339
        rect = QgsRectangle(x_min, y_min, x_max, y_max)
        edit_dialog.bbox.setOutputExtentFromUser(rect, crs)

        self.assertEqual(
            edit_dialog.stacked_parameters_bookmark.currentWidget(), edit_dialog.basic_parameters)
        edit_dialog.radio_advanced.setChecked(True)
        self.assertEqual(
            edit_dialog.stacked_parameters_bookmark.currentWidget(), edit_dialog.advanced_parameters)

        edit_dialog.button_validate.click()
        self.bookmark = self.dialog.list_bookmark_mp.item(0)

        new_data = self.set_up_bookmark_data_text()

        expected_json = {
            "query":
                [
                    ""
                ],
            "description":
                ["All OSM objects with the key 'amenity'='bench' in foo are going to be downloaded."],
            "advanced": True,
            "file_name": "amenity_bench_foo",
            "query_layer_name": ["Query 2"],
            "query_name": ["Query 1"],
            "type_multi_request": [[]],
            "keys": [[""]],
            "values": [[""]],
            "area": [""],
            "bbox": [{'__extent__': '2.71828 0.0 3.1415926 1.6180339'}],
            "output_geom_type":
                [
                    [
                        {"__enum__": "LayerType.Points"},
                        {"__enum__": "LayerType.Lines"},
                        {"__enum__": "LayerType.Multilinestrings"},
                        {"__enum__": "LayerType.Multipolygons"}
                    ]
                ],
            "white_list_column":
                [{"multilinestrings": None, "points": None, "lines": None, "multipolygons": None}],
            "output_directory": [""],
            "output_format": [None]
        }

        self.assertDictEqual(expected_json, new_data)
