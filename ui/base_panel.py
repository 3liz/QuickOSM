"""Panel core base class."""

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class BasePanel:

    def __init__(self, dialog):
        self.panel = None

    def setup_panel(self):
        """Setup the UI for the panel."""
        raise NotImplemented
