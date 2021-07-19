"""Wizard of the preset."""

from qgis.PyQt.QtWidgets import QDialog

from QuickOSM.definitions.gui import Panels
from QuickOSM.qgis_plugin_tools.tools.resources import load_ui

FORM_CLASS = load_ui('wizard_preset.ui')


class Wizard(QDialog, FORM_CLASS):
    """Dialog that help with the preset"""

    def __init__(self, parent=None):
        """Constructor."""
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.button_select.clicked.connect(self.end_search)

        self.search_preset.textChanged.connect(self.search_edited)

        for item in parent.external_panels[Panels.QuickQuery].preset_items:
            item_clone = item.clone()
            self.list_preset.addItem(item_clone)

        self.list_preset.itemDoubleClicked.connect(self.end_search)
        self.nb_preset = self.list_preset.count()

    def search_edited(self):
        """ Show or hide items """
        search = self.search_preset.text().lower()
        for row in range(self.nb_preset):
            item = self.list_preset.item(row)
            if search in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def end_search(self):
        """Process the end of the dialog"""
        if self.list_preset.selectedItems():
            preset = self.list_preset.selectedItems()[0].text()
            self.parent().external_panels[Panels.QuickQuery].choice_preset(preset)

        self.close()
