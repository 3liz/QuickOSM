from qgis.testing import unittest, start_app
from qgis.testing.mocked import get_iface

from ..dialog import Dialog
from ...core.utilities.tools import (
    get_setting,
)
from ...definitions.overpass import OVERPASS_SERVERS


start_app()

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class TestUiMainWindow(unittest.TestCase):

    def test_configuration_panel(self):
        """Test we can save the custom server."""
        servers = len(OVERPASS_SERVERS)

        dialog = Dialog(get_iface())
        self.assertEqual(dialog.combo_default_overpass.count(), servers)
        default_server = get_setting('defaultOAPI')
        self.assertEqual(default_server, OVERPASS_SERVERS[0])

        dialog.combo_default_overpass.setCurrentIndex(1)
        default_server = get_setting('defaultOAPI')
        self.assertEqual(default_server, OVERPASS_SERVERS[1])
