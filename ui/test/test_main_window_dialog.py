from qgis.core import Qgis
from qgis.testing import unittest, start_app
from qgis.testing.mocked import get_iface
from QuickOSM.ui.main_window_dialog import MainDialog

start_app()


class TestUiMainWindow(unittest.TestCase):

    @unittest.skipIf(Qgis.QGIS_VERSION_INT < 30800, 'Somehow, test not working on QGIS 3.4')
    def test_show_query(self):
        """Test we can show a query by switching tab with all params."""
        # Empty query
        dialog = MainDialog(get_iface())
        dialog.button_show_query.click()
        self.assertEqual(dialog.stacked_panels_widget.currentIndex(), dialog.query_index)
