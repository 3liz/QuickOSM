from qgis.testing import start_app, unittest
from qgis.testing.mocked import get_iface

from QuickOSM.definitions.gui import Panels
from QuickOSM.definitions.osm import QueryLanguage
from QuickOSM.ui.dialog import Dialog

start_app()

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class TestUiMainWindow(unittest.TestCase):

    def test_show_query_empty(self):
        """Test we can show a query by switching tab with all params."""
        dialog = Dialog(get_iface())
        index = dialog.combo_query_type_qq.findData('canvas')
        dialog.combo_query_type_qq.setCurrentIndex(index)
        dialog.button_show_query.click()
        expected_index = dialog.stacked_panels_widget.indexOf(dialog.query_page)
        self.assertEqual(dialog.stacked_panels_widget.currentIndex(), expected_index)
        self.assertNotEqual(dialog.text_query.toPlainText(), '')

    def test_show_query_key_value_in(self):
        """Test we can show a query by switching tab with key value in params."""
        dialog = Dialog(get_iface())
        dialog.combo_key.lineEdit().setText('amenity')
        dialog.combo_value.lineEdit().setText('value')
        dialog.places_edits[Panels.QuickQuery].setText('foo')
        dialog.button_show_query.click()
        expected_index = dialog.stacked_panels_widget.indexOf(dialog.query_page)
        self.assertEqual(dialog.stacked_panels_widget.currentIndex(), expected_index)
        self.assertNotEqual(dialog.text_query.toPlainText(), '')

    def test_show_query_oql(self):
        """Test we can show a query in OQL by switching tab."""
        dialog = Dialog(get_iface())
        dialog.combo_key.lineEdit().setText('amenity')
        dialog.combo_value.lineEdit().setText('value')
        dialog.places_edits[Panels.QuickQuery].setText('foo')
        index = dialog.combo_query_language_qq.findData(QueryLanguage.OQL)
        dialog.combo_query_language_qq.setCurrentIndex(index)
        dialog.button_show_query.click()
        expected_index = dialog.stacked_panels_widget.indexOf(dialog.query_page)
        self.assertEqual(dialog.stacked_panels_widget.currentIndex(), expected_index)
        self.assertNotEqual(dialog.text_query.toPlainText(), '')
        self.assertEqual(dialog.text_query.toPlainText()[-1], ';')

    def test_show_query_xml(self):
        """Test we can show a query in XML by switching tab."""
        dialog = Dialog(get_iface())
        dialog.combo_key.lineEdit().setText('amenity')
        dialog.combo_value.lineEdit().setText('value')
        dialog.places_edits[Panels.QuickQuery].setText('foo')
        index = dialog.combo_query_language_qq.findData(QueryLanguage.XML)
        dialog.combo_query_language_qq.setCurrentIndex(index)
        dialog.button_show_query.click()
        expected_index = dialog.stacked_panels_widget.indexOf(dialog.query_page)
        self.assertEqual(dialog.stacked_panels_widget.currentIndex(), expected_index)
        self.assertNotEqual(dialog.text_query.toPlainText(), '')
        self.assertEqual(dialog.text_query.toPlainText()[-2], '>')
