from qgis.testing import unittest, start_app
from qgis.testing.mocked import get_iface

from ...definitions.gui import Panels
from ..dialog import Dialog

start_app()

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class TestQuickOSMWidget(unittest.TestCase):

    def test_sort_nominatim_places(self):
        """Test if reorder last nominatim places works."""
        dialog = Dialog(get_iface())

        existing_places = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        new_list = dialog.external_panels[Panels.QuickQuery].sort_nominatim_places(existing_places, '3')
        expected = ['3', '1', '2', '4', '5', '6', '7', '8', '9', '10']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        new_list = dialog.external_panels[Panels.QuickQuery].sort_nominatim_places(existing_places, '11')
        expected = ['11', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5']
        new_list = dialog.external_panels[Panels.QuickQuery].sort_nominatim_places(existing_places, '3')
        expected = ['3', '1', '2', '4', '5']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5']
        new_list = dialog.external_panels[Panels.QuickQuery].sort_nominatim_places(existing_places, '6')
        expected = ['6', '1', '2', '3', '4', '5']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5']
        new_list = dialog.external_panels[Panels.QuickQuery].sort_nominatim_places(existing_places, '1')
        expected = ['1', '2', '3', '4', '5']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        new_list = dialog.external_panels[Panels.QuickQuery].sort_nominatim_places(existing_places, '1')
        expected = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.assertListEqual(expected, new_list)


if __name__ == '__main__':
    suite = unittest.makeSuite(TestQuickOSMWidget)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
