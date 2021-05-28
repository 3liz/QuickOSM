"""Panel core base class."""

from qgis.PyQt.QtWidgets import QDialog

from QuickOSM.definitions.gui import Panels

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class BasePanel:

    """Base panel for QuickOSM dialog.

    This is a kind of virtual class.
    """

    def __init__(self, dialog: QDialog):
        self._panel = None
        self._dialog = dialog

    @property
    def panel(self) -> Panels:
        if self._panel:
            return self._panel
        else:
            raise NotImplementedError

    @panel.setter
    def panel(self, panel: str):
        self._panel = panel

    @property
    def dialog(self) -> QDialog:
        """Return the dialog.

        :rtype: QDialog
        """
        return self._dialog

    def setup_panel(self):
        """Setup the UI for the panel."""
        raise NotImplementedError
