import sys

from qgis.testing import unittest, start_app
from qgis.testing.mocked import get_iface

from ..main_window_dialog import MainDialog
from ...core.utilities.tools import (
    get_setting,
)
from ...definitions.overpass import OVERPASS_SERVERS

if not hasattr(sys, 'argv'):
    sys.argv = ['']

start_app()


class TestUiMainWindow(unittest.TestCase):

    def configuration_panel(self):
        """Test we can save the custom server."""
        servers = len(OVERPASS_SERVERS)

        dialog = MainDialog(get_iface())
        self.assertEqual(dialog.combo_default_overpass.count(), servers)
        default_server = get_setting('defaultOAPI')
        self.assertEqual(default_server, OVERPASS_SERVERS[0])

        dialog.combo_default_overpass.setCurrentIndex(1)
        default_server = get_setting('defaultOAPI')
        self.assertEqual(default_server, OVERPASS_SERVERS[1])
