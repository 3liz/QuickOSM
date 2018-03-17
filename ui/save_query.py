# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'save_query.ui'
#
# Created: Wed Jul 30 11:57:33 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from builtins import object
from qgis.PyQt import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ui_save_query(object):
    def setupUi(self, ui_save_query):
        ui_save_query.setObjectName(_fromUtf8("ui_save_query"))
        ui_save_query.resize(452, 108)
        self.verticalLayout = QtGui.QVBoxLayout(ui_save_query)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(ui_save_query)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(ui_save_query)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEdit_category = QtGui.QLineEdit(ui_save_query)
        self.lineEdit_category.setObjectName(_fromUtf8("lineEdit_category"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_category)
        self.label_2 = QtGui.QLabel(ui_save_query)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_name = QtGui.QLineEdit(ui_save_query)
        self.lineEdit_name.setObjectName(_fromUtf8("lineEdit_name"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_name)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(ui_save_query)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ui_save_query)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ui_save_query.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ui_save_query.reject)
        QtCore.QMetaObject.connectSlotsByName(ui_save_query)

    def retranslateUi(self, ui_save_query):
        ui_save_query.setWindowTitle(_translate("ui_save_query", "QuickOSM - Save query", None))
        self.label_3.setText(_translate("ui_save_query", "The styles and names of these layers won\'t be saved.", None))
        self.label.setText(_translate("ui_save_query", "Category", None))
        self.label_2.setText(_translate("ui_save_query", "Name", None))

