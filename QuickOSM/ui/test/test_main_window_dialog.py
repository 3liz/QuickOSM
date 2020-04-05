from qgis.testing import unittest, start_app
from qgis.testing.mocked import get_iface

from ...definitions.gui import Panels
from ..dialog import Dialog


start_app()

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


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
