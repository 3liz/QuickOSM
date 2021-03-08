"""Panel core base class."""

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class BasePanel:

    """Base panel for QuickOSM dialog.

    This is a kind of virtual class.
    """

    def __init__(self, dialog):
        self._panel = None
        self._dialog = dialog

    @property
    def panel(self):
        if self._panel:
            return self._panel
        else:
            raise NotImplementedError

    @panel.setter
    def panel(self, panel):
        self._panel = panel

    @property
    def dialog(self):
        """Return the dialog.

        :rtype: QDialog
        """
        return self._dialog

    def setup_panel(self):
        """Setup the UI for the panel."""
        raise NotImplementedError
