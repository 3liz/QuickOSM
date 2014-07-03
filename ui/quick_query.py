# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quick_query.ui'
#
# Created: Wed Jul  2 18:09:17 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(274, 201)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEdit_key = QtGui.QLineEdit(Form)
        self.lineEdit_key.setObjectName(_fromUtf8("lineEdit_key"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_key)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_value = QtGui.QLineEdit(Form)
        self.lineEdit_value.setObjectName(_fromUtf8("lineEdit_value"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_value)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_nominatim = QtGui.QLineEdit(Form)
        self.lineEdit_nominatim.setObjectName(_fromUtf8("lineEdit_nominatim"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_nominatim)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_browseFile = QtGui.QLineEdit(Form)
        self.lineEdit_browseFile.setObjectName(_fromUtf8("lineEdit_browseFile"))
        self.horizontalLayout.addWidget(self.lineEdit_browseFile)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.formLayout.setLayout(5, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_4)
        self.buttonBox = QtGui.QDialogButtonBox(Form)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.buttonBox)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.spinBox_timeout = QtGui.QSpinBox(Form)
        self.spinBox_timeout.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.spinBox_timeout.setMinimum(25)
        self.spinBox_timeout.setMaximum(2000)
        self.spinBox_timeout.setSingleStep(25)
        self.spinBox_timeout.setObjectName(_fromUtf8("spinBox_timeout"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.spinBox_timeout)
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_6)
        self.comboBox_osmObjects = QtGui.QComboBox(Form)
        self.comboBox_osmObjects.setObjectName(_fromUtf8("comboBox_osmObjects"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.comboBox_osmObjects)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Key", None))
        self.label_2.setText(_translate("Form", "Value", None))
        self.label_3.setText(_translate("Form", "Place", None))
        self.pushButton.setText(_translate("Form", "Browse", None))
        self.label_4.setText(_translate("Form", "File", None))
        self.label_5.setText(_translate("Form", "Timeout", None))
        self.label_6.setText(_translate("Form", "OSM objects", None))

