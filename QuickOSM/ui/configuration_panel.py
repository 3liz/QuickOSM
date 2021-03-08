"""Configuration panel."""

import logging

from json import load

from QuickOSM.core.utilities.tools import (
    custom_config_file,
    get_setting,
    set_setting,
)
from QuickOSM.definitions.gui import Panels
from QuickOSM.definitions.overpass import OVERPASS_SERVERS
from QuickOSM.ui.base_panel import BasePanel

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

LOGGER = logging.getLogger('QuickOSM')


class ConfigurationPanel(BasePanel):

    """Final implementation for the panel."""

    def __init__(self, dialog):
        super().__init__(dialog)
        self.panel = Panels.Configuration

    def setup_panel(self):
        """Set UI related the configuration panel."""
        self.dialog.save_config.clicked.connect(self.set_server_overpass_api)

        for server in OVERPASS_SERVERS:
            self.dialog.combo_default_overpass.addItem(server)

        # Read the config file
        custom_config = custom_config_file()
        if custom_config:
            with open(custom_config) as f:
                config_json = load(f)
                for server in config_json.get('overpass_servers'):
                    if server not in OVERPASS_SERVERS:
                        LOGGER.info(
                            'Custom overpass server list added: {}'.format(
                                server))
                        self.dialog.combo_default_overpass.addItem(server)

        # Set settings about the overpass API
        # Set it after populating the combobox #235
        default_server = get_setting('defaultOAPI')
        if default_server:
            index = self.dialog.combo_default_overpass.findText(default_server)
            self.dialog.combo_default_overpass.setCurrentIndex(index)
        else:
            default_server = self.dialog.combo_default_overpass.currentText()
            set_setting('defaultOAPI', default_server)

    def set_server_overpass_api(self):
        """Save the new Overpass server."""
        default_server = self.dialog.combo_default_overpass.currentText()
        set_setting('defaultOAPI', default_server)
