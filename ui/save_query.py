# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'save_query.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ui_save_query(object):
    def setupUi(self, ui_save_query):
        ui_save_query.setObjectName("ui_save_query")
        ui_save_query.resize(452, 108)
        self.verticalLayout = QtWidgets.QVBoxLayout(ui_save_query)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(ui_save_query)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(ui_save_query)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit_category = QtWidgets.QLineEdit(ui_save_query)
        self.lineEdit_category.setObjectName("lineEdit_category")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_category)
        self.label_2 = QtWidgets.QLabel(ui_save_query)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_name = QtWidgets.QLineEdit(ui_save_query)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_name)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(ui_save_query)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ui_save_query)
        self.buttonBox.accepted.connect(ui_save_query.accept)
        self.buttonBox.rejected.connect(ui_save_query.reject)
        QtCore.QMetaObject.connectSlotsByName(ui_save_query)

    def retranslateUi(self, ui_save_query):
        _translate = QtCore.QCoreApplication.translate
        ui_save_query.setWindowTitle(_translate("ui_save_query", "QuickOSM - Save query"))
        self.label_3.setText(_translate("ui_save_query", "The styles and names of these layers won\'t be saved."))
        self.label.setText(_translate("ui_save_query", "Category"))
        self.label_2.setText(_translate("ui_save_query", "Name"))

