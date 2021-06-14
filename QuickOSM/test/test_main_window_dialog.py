"""Tests for the main window."""

from qgis.testing import unittest

from QuickOSM.definitions.gui import Panels
from QuickOSM.ui.dialog import Dialog

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class TestUiMainWindow(unittest.TestCase):
    """Tests for the main window."""

    def test_show_query_empty(self):
        """Test we can show a query by switching tab with all params."""
        dialog = Dialog()
        index = dialog.combo_query_type_qq.findData('canvas')
        dialog.combo_query_type_qq.setCurrentIndex(index)
        dialog.button_show_query.click()
        expected_index = dialog.stacked_panels_widget.indexOf(dialog.query_page)
        self.assertEqual(dialog.stacked_panels_widget.currentIndex(), expected_index)
        self.assertNotEqual(dialog.text_query.toPlainText(), '')

    @unittest.skip("Bug first setText l.27")
    def test_show_query_key_value_in(self):
        """Test we can show a query by switching tab with key value in params."""
        dialog = Dialog()
        dialog.table_keys_values.cellWidget(0, 1).lineEdit().setText('amenity')
        dialog.table_keys_values.cellWidget(0, 2).lineEdit().setText('value')
        dialog.places_edits[Panels.QuickQuery].setText('foo')
        dialog.button_show_query.click()
        expected_index = dialog.stacked_panels_widget.indexOf(dialog.query_page)
        self.assertEqual(dialog.stacked_panels_widget.currentIndex(), expected_index)
        self.assertNotEqual(dialog.text_query.toPlainText(), '')

    @unittest.skip("Bug first setText l.39")
    def test_show_query_oql(self):
        """Test we can show a query in OQL by switching tab."""
        dialog = Dialog()
        dialog.table_keys_values.cellWidget(0, 1).lineEdit().setText('amenity')
        dialog.table_keys_values.cellWidget(0, 2).lineEdit().setText('value')
        dialog.places_edits[Panels.QuickQuery].setText('foo')
        dialog.action_oql_qq.trigger()
        dialog.button_show_query.click()
        expected_index = dialog.stacked_panels_widget.indexOf(dialog.query_page)
        self.assertEqual(dialog.stacked_panels_widget.currentIndex(), expected_index)
        self.assertNotEqual(dialog.text_query.toPlainText(), '')
        self.assertEqual(dialog.text_query.toPlainText()[-1], ';')

    @unittest.skip("Bug first setText l.53")
    def test_show_query_xml(self):
        """Test we can show a query in XML by switching tab."""
        dialog = Dialog()
        dialog.table_keys_values.cellWidget(0, 1).lineEdit().setText('amenity')
        dialog.table_keys_values.cellWidget(0, 1).lineEdit().setText('value')
        dialog.places_edits[Panels.QuickQuery].setText('foo')
        dialog.action_xml_qq.trigger()
        dialog.button_show_query.click()
        expected_index = dialog.stacked_panels_widget.indexOf(dialog.query_page)
        self.assertEqual(dialog.stacked_panels_widget.currentIndex(), expected_index)
        self.assertNotEqual(dialog.text_query.toPlainText(), '')
        self.assertEqual(dialog.text_query.toPlainText()[-2], '>')
