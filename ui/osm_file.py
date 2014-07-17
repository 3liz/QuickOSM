# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'osm_file.ui'
#
# Created: Thu Jul 17 12:21:30 2014
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
        ui_osm_file.resize(316, 303)
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
        self.lineEdit_osmFile = QtGui.QLineEdit(ui_osm_file)
        self.lineEdit_osmFile.setObjectName(_fromUtf8("lineEdit_osmFile"))
        self.horizontalLayout.addWidget(self.lineEdit_osmFile)
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
        self.label_3 = QtGui.QLabel(ui_osm_file)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(ui_osm_file)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtGui.QLabel(ui_osm_file)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtGui.QLabel(ui_osm_file)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.checkBox_points = QtGui.QCheckBox(ui_osm_file)
        self.checkBox_points.setText(_fromUtf8(""))
        self.checkBox_points.setChecked(True)
        self.checkBox_points.setObjectName(_fromUtf8("checkBox_points"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.checkBox_points)
        self.checkBox_lines = QtGui.QCheckBox(ui_osm_file)
        self.checkBox_lines.setText(_fromUtf8(""))
        self.checkBox_lines.setChecked(True)
        self.checkBox_lines.setObjectName(_fromUtf8("checkBox_lines"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.checkBox_lines)
        self.checkBox_multilinestrings = QtGui.QCheckBox(ui_osm_file)
        self.checkBox_multilinestrings.setText(_fromUtf8(""))
        self.checkBox_multilinestrings.setChecked(True)
        self.checkBox_multilinestrings.setObjectName(_fromUtf8("checkBox_multilinestrings"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.checkBox_multilinestrings)
        self.checkBox_multipolygons = QtGui.QCheckBox(ui_osm_file)
        self.checkBox_multipolygons.setText(_fromUtf8(""))
        self.checkBox_multipolygons.setChecked(True)
        self.checkBox_multipolygons.setObjectName(_fromUtf8("checkBox_multipolygons"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.checkBox_multipolygons)
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
        self.label_3.setText(_translate("ui_osm_file", "Points", None))
        self.label_4.setText(_translate("ui_osm_file", "Lines", None))
        self.label_5.setText(_translate("ui_osm_file", "Multilinestrings", None))
        self.label_6.setText(_translate("ui_osm_file", "Multipolygons", None))
        self.pushButton_openOsmFile.setText(_translate("ui_osm_file", "Open", None))

