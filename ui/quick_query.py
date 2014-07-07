# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quick_query.ui'
#
# Created: Mon Jul  7 14:42:08 2014
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
        Form.resize(583, 344)
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
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_7)
        self.checkBox_node = QtGui.QCheckBox(Form)
        self.checkBox_node.setText(_fromUtf8(""))
        self.checkBox_node.setChecked(True)
        self.checkBox_node.setObjectName(_fromUtf8("checkBox_node"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.checkBox_node)
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_8)
        self.checkBox_way = QtGui.QCheckBox(Form)
        self.checkBox_way.setText(_fromUtf8(""))
        self.checkBox_way.setChecked(True)
        self.checkBox_way.setObjectName(_fromUtf8("checkBox_way"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.checkBox_way)
        self.label_9 = QtGui.QLabel(Form)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_9)
        self.checkBox_relation = QtGui.QCheckBox(Form)
        self.checkBox_relation.setText(_fromUtf8(""))
        self.checkBox_relation.setChecked(True)
        self.checkBox_relation.setObjectName(_fromUtf8("checkBox_relation"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.checkBox_relation)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_5)
        self.spinBox_timeout = QtGui.QSpinBox(Form)
        self.spinBox_timeout.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.spinBox_timeout.setMinimum(25)
        self.spinBox_timeout.setMaximum(2000)
        self.spinBox_timeout.setSingleStep(25)
        self.spinBox_timeout.setObjectName(_fromUtf8("spinBox_timeout"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.spinBox_timeout)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_browseDir = QtGui.QLineEdit(Form)
        self.lineEdit_browseDir.setObjectName(_fromUtf8("lineEdit_browseDir"))
        self.horizontalLayout.addWidget(self.lineEdit_browseDir)
        self.pushButton_browse_output_file = QtGui.QPushButton(Form)
        self.pushButton_browse_output_file.setObjectName(_fromUtf8("pushButton_browse_output_file"))
        self.horizontalLayout.addWidget(self.pushButton_browse_output_file)
        self.formLayout.setLayout(7, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_filePrefix = QtGui.QLineEdit(Form)
        self.lineEdit_filePrefix.setObjectName(_fromUtf8("lineEdit_filePrefix"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.lineEdit_filePrefix)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_showQuery = QtGui.QPushButton(Form)
        self.pushButton_showQuery.setObjectName(_fromUtf8("pushButton_showQuery"))
        self.horizontalLayout_2.addWidget(self.pushButton_showQuery)
        self.pushButton_runQuery = QtGui.QPushButton(Form)
        self.pushButton_runQuery.setObjectName(_fromUtf8("pushButton_runQuery"))
        self.horizontalLayout_2.addWidget(self.pushButton_runQuery)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.progressBar_execution = QtGui.QProgressBar(Form)
        self.progressBar_execution.setProperty("value", 0)
        self.progressBar_execution.setObjectName(_fromUtf8("progressBar_execution"))
        self.verticalLayout.addWidget(self.progressBar_execution)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Key", None))
        self.lineEdit_key.setText(_translate("Form", "shop", None))
        self.label_2.setText(_translate("Form", "Value", None))
        self.lineEdit_value.setText(_translate("Form", "supermarket", None))
        self.label_3.setText(_translate("Form", "Place", None))
        self.lineEdit_nominatim.setText(_translate("Form", "montpellier", None))
        self.label_7.setText(_translate("Form", "Node", None))
        self.label_8.setText(_translate("Form", "Way", None))
        self.label_9.setText(_translate("Form", "Relation", None))
        self.label_5.setText(_translate("Form", "Timeout", None))
        self.label_4.setText(_translate("Form", "Directory", None))
        self.lineEdit_browseDir.setPlaceholderText(_translate("Form", "Save to temporary file", None))
        self.pushButton_browse_output_file.setText(_translate("Form", "Browse", None))
        self.label_6.setText(_translate("Form", "File prefix", None))
        self.pushButton_showQuery.setText(_translate("Form", "Show query", None))
        self.pushButton_runQuery.setText(_translate("Form", "Run query", None))

