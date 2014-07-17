# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'osm_file.ui'
#
# Created: Thu Jul 17 08:29:56 2014
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

class Ui_ui_osm_file(object):
    def setupUi(self, ui_osm_file):
        ui_osm_file.setObjectName(_fromUtf8("ui_osm_file"))
        ui_osm_file.resize(316, 195)
        self.verticalLayout = QtGui.QVBoxLayout(ui_osm_file)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(ui_osm_file)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdi_osmFile = QtGui.QLineEdit(ui_osm_file)
        self.lineEdi_osmFile.setObjectName(_fromUtf8("lineEdi_osmFile"))
        self.horizontalLayout.addWidget(self.lineEdi_osmFile)
        self.pushButton_browseOsmFile = QtGui.QPushButton(ui_osm_file)
        self.pushButton_browseOsmFile.setObjectName(_fromUtf8("pushButton_browseOsmFile"))
        self.horizontalLayout.addWidget(self.pushButton_browseOsmFile)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_2 = QtGui.QLabel(ui_osm_file)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEdit_osmConf = QtGui.QLineEdit(ui_osm_file)
        self.lineEdit_osmConf.setObjectName(_fromUtf8("lineEdit_osmConf"))
        self.horizontalLayout_2.addWidget(self.lineEdit_osmConf)
        self.pushButton_browseOsmConf = QtGui.QPushButton(ui_osm_file)
        self.pushButton_browseOsmConf.setObjectName(_fromUtf8("pushButton_browseOsmConf"))
        self.horizontalLayout_2.addWidget(self.pushButton_browseOsmConf)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.formLayout)
        self.pushButton_openOsmFile = QtGui.QPushButton(ui_osm_file)
        self.pushButton_openOsmFile.setObjectName(_fromUtf8("pushButton_openOsmFile"))
        self.verticalLayout.addWidget(self.pushButton_openOsmFile)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(ui_osm_file)
        QtCore.QMetaObject.connectSlotsByName(ui_osm_file)

    def retranslateUi(self, ui_osm_file):
        ui_osm_file.setWindowTitle(_translate("ui_osm_file", "Form", None))
        self.label.setText(_translate("ui_osm_file", "OSM File", None))
        self.pushButton_browseOsmFile.setText(_translate("ui_osm_file", "Browse", None))
        self.label_2.setText(_translate("ui_osm_file", "OSMConf", None))
        self.pushButton_browseOsmConf.setText(_translate("ui_osm_file", "Browse", None))
        self.pushButton_openOsmFile.setText(_translate("ui_osm_file", "Open", None))

