"""Set up a completer that ignore diacritics and accents"""

import unicodedata

from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtWidgets import QCompleter


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


class DiacriticFreeCompleter(QCompleter):

    def splitPath(self, path):
        return [strip_accents(path).lower()]

    def pathFromIndex(self, index):
        return index.data()


class DiactricFreeStringListModel(QStringListModel):

    def __init__(self, *args, **kwargs):
        super(DiactricFreeStringListModel, self).__init__(*args, **kwargs)
        self.setDiactricFreeRole(Qt.UserRole + 10)

    def data(self, index, role):
        if role == self.diactricFreeRole():
            value = super(DiactricFreeStringListModel, self).data(index, Qt.DisplayRole)
            return strip_accents(value).lower()
        else:
            return super(DiactricFreeStringListModel, self).data(index, role)

    def setDiactricFreeRole(self, role):
        self.mDiactricFreeRole = role

    def diactricFreeRole(self):
        return self.mDiactricFreeRole
