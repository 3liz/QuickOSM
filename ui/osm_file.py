# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'osm_file.ui'
#
# Created: Wed Jul 30 11:36:52 2014
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
        ui_osm_file.resize(694, 537)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ui_osm_file)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.scrollArea = QtGui.QScrollArea(ui_osm_file)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 680, 523))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_osmFile = QtGui.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_osmFile.setObjectName(_fromUtf8("lineEdit_osmFile"))
        self.horizontalLayout.addWidget(self.lineEdit_osmFile)
        self.pushButton_browseOsmFile = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_browseOsmFile.setObjectName(_fromUtf8("pushButton_browseOsmFile"))
        self.horizontalLayout.addWidget(self.pushButton_browseOsmFile)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_2 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEdit_osmConf = QtGui.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_osmConf.setObjectName(_fromUtf8("lineEdit_osmConf"))
        self.horizontalLayout_2.addWidget(self.lineEdit_osmConf)
        self.pushButton_browseOsmConf = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_browseOsmConf.setObjectName(_fromUtf8("pushButton_browseOsmConf"))
        self.horizontalLayout_2.addWidget(self.pushButton_browseOsmConf)
        self.pushButton_resetIni = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_resetIni.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/QuickOSM/resources/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_resetIni.setIcon(icon)
        self.pushButton_resetIni.setObjectName(_fromUtf8("pushButton_resetIni"))
        self.horizontalLayout_2.addWidget(self.pushButton_resetIni)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_3 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_6)
        self.checkBox_points = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_points.setText(_fromUtf8(""))
        self.checkBox_points.setChecked(True)
        self.checkBox_points.setObjectName(_fromUtf8("checkBox_points"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.checkBox_points)
        self.checkBox_lines = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_lines.setText(_fromUtf8(""))
        self.checkBox_lines.setChecked(True)
        self.checkBox_lines.setObjectName(_fromUtf8("checkBox_lines"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.checkBox_lines)
        self.checkBox_multilinestrings = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_multilinestrings.setText(_fromUtf8(""))
        self.checkBox_multilinestrings.setChecked(True)
        self.checkBox_multilinestrings.setObjectName(_fromUtf8("checkBox_multilinestrings"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.checkBox_multilinestrings)
        self.checkBox_multipolygons = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_multipolygons.setText(_fromUtf8(""))
        self.checkBox_multipolygons.setChecked(True)
        self.checkBox_multipolygons.setObjectName(_fromUtf8("checkBox_multipolygons"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.checkBox_multipolygons)
        self.verticalLayout.addLayout(self.formLayout)
        self.pushButton_openOsmFile = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_openOsmFile.setObjectName(_fromUtf8("pushButton_openOsmFile"))
        self.verticalLayout.addWidget(self.pushButton_openOsmFile)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)

        self.retranslateUi(ui_osm_file)
        QtCore.QMetaObject.connectSlotsByName(ui_osm_file)

    def retranslateUi(self, ui_osm_file):
        ui_osm_file.setWindowTitle(_translate("ui_osm_file", "QuickOSM - OSM File", None))
        self.label.setText(_translate("ui_osm_file", "OSM File", None))
        self.pushButton_browseOsmFile.setText(_translate("ui_osm_file", "Browse", None))
        self.label_2.setText(_translate("ui_osm_file", "OSMConf", None))
        self.pushButton_browseOsmConf.setText(_translate("ui_osm_file", "Browse", None))
        self.label_3.setText(_translate("ui_osm_file", "Points", None))
        self.label_4.setText(_translate("ui_osm_file", "Lines", None))
        self.label_5.setText(_translate("ui_osm_file", "Multilinestrings", None))
        self.label_6.setText(_translate("ui_osm_file", "Multipolygons", None))
        self.pushButton_openOsmFile.setText(_translate("ui_osm_file", "Open", None))

from QuickOSM import resources_rc

