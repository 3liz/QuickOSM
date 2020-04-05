"""Configuration panel."""

import logging

from json import load

from .base_panel import BasePanel
from ..core.utilities.tools import (
    get_setting,
    set_setting,
    custom_config_file,
)
from ..definitions.gui import Panels
from ..definitions.overpass import OVERPASS_SERVERS


__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'

LOGGER = logging.getLogger('QuickOSM')


class ConfigurationPanel(BasePanel):

    """Final implementation for the panel."""

    def __init__(self, dialog):
        super().__init__(dialog)
        self.panel = Panels.Configuration

    def setup_panel(self):
        """Set UI related the configuration panel."""
        # noinspection PyUnresolvedReferences
        self.dialog.combo_default_overpass.currentIndexChanged.connect(
            self.set_server_overpass_api)

        # Set settings about the overpass API
        default_server = get_setting('defaultOAPI')
        if default_server:
            index = self.dialog.combo_default_overpass.findText(default_server)
            self.dialog.combo_default_overpass.setCurrentIndex(index)
        else:
            default_server = self.dialog.combo_default_overpass.currentText()
            set_setting('defaultOAPI', default_server)

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

    def set_server_overpass_api(self):
        """Save the new Overpass server."""
        default_server = self.dialog.combo_default_overpass.currentText()
        set_setting('defaultOAPI', default_server)
