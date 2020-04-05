"""File for custom UI widgets."""

from qgis.PyQt.QtWidgets import (
    QStyledItemDelegate, QComboBox, QCompleter, QTableView, QLineEdit)
from qgis.PyQt.QtCore import QStringListModel

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class TableKeyValue(QTableView):
    def __init__(self, parent):
        super(TableKeyValue, self).__init__(parent)
        self.osm_keys = None

    def set_osm_keys(self, keys):
        self.osm_keys = keys

    def add_new_row(self):
        row = self.model().rowCount()

        keys = list(self.osm_keys.keys())
        keys.append('')  # All keys request #118
        keys.sort()
        keys_completer = QCompleter(keys)

        key_editor = QComboBox()
        key_editor.setEditable(True)
        key_editor.addItems(keys)
        key_editor.setCompleter(keys_completer)
        key_editor.completer().setCompletionMode(
            QCompleter.PopupCompletion)
        key_editor.lineEdit().setPlaceholderText(
            self.tr('Query on all keys'))

        self.model().setItem(row, 0, key_editor)
        self.model().setItem(row, 1, QComboBox())

    def dataChanged(self, top_left, bottom_right, roles):
        print(top_left.data())
        if top_left.data() == 'a':
            widget = QLineEdit()
            widget.setPlaceholderText('ahhhhhhhh')
            self.setIndexWidget(top_left, widget)
        else:
            self.setIndexWidget(top_left, None)


class QueryItemDelegate(QStyledItemDelegate):

    def __init__(self, osm_keys):
        super(QueryItemDelegate, self).__init__()
        self.osm_keys = osm_keys

    def createEditor(self, parent, option, index):
        if index.column() == 0:
            keys = list(self.osm_keys.keys())
            keys.append('')  # All keys request #118
            keys.sort()
            keys_completer = QCompleter(keys)

            key_editor = QComboBox(parent)
            key_editor.setEditable(True)
            key_editor.addItems(keys)
            key_editor.setCompleter(keys_completer)
            key_editor.completer().setCompletionMode(
                QCompleter.PopupCompletion)
            key_editor.lineEdit().setPlaceholderText(
                self.tr('Query on all keys'))
            return key_editor

        elif index.column() == 1:
            model = QStringListModel(parent)
            model.setStringList(['11111', '22222', '33333'])

            value_editor = QComboBox(parent)
            value_editor.setEditable(True)
            value_editor.setModel(model)
            value_editor.lineEdit().setPlaceholderText(
                self.tr('Query on all values'))
            return value_editor
