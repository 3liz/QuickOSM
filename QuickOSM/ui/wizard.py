from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDialog, QListWidgetItem

from QuickOSM.qgis_plugin_tools.tools.resources import load_ui, resources_path

FORM_CLASS = load_ui('wizard_preset.ui')


class Wizard(QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.button_select.clicked.connect(self.end_search)

        self.search_preset.textChanged.connect(self.search_edited)

        for key in parent.keys_preset:
            icon_path = parent.preset_data.elements[key].icon
            icon_path = resources_path('icons', icon_path)
            icon = QIcon(icon_path)
            item = QListWidgetItem(icon, key)
            self.list_preset.addItem(item)

        self.list_preset.itemDoubleClicked.connect(self.end_search)
        self.nb_preset = self.list_preset.count()

    def search_edited(self):

        search = self.search_preset.text().lower()
        for row in range(self.nb_preset):
            item = self.list_preset.item(row)
            if search in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def end_search(self):
        preset = self.list_preset.selectedItems()[0].text()
        self.parent().combo_preset.setCurrentText(preset)
        self.close()
