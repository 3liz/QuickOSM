# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quick_query.ui'
#
# Created: Wed Jul 23 18:07:53 2014
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

class Ui_ui_quick_query(object):
    def setupUi(self, ui_quick_query):
        ui_quick_query.setObjectName(_fromUtf8("ui_quick_query"))
        ui_quick_query.resize(609, 565)
        self.verticalLayout = QtGui.QVBoxLayout(ui_quick_query)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(ui_quick_query)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEdit_key = QtGui.QLineEdit(ui_quick_query)
        self.lineEdit_key.setText(_fromUtf8(""))
        self.lineEdit_key.setObjectName(_fromUtf8("lineEdit_key"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_key)
        self.label_2 = QtGui.QLabel(ui_quick_query)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_value = QtGui.QLineEdit(ui_quick_query)
        self.lineEdit_value.setText(_fromUtf8(""))
        self.lineEdit_value.setObjectName(_fromUtf8("lineEdit_value"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_value)
        self.label_3 = QtGui.QLabel(ui_quick_query)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.radioButton_place = QtGui.QRadioButton(ui_quick_query)
        self.radioButton_place.setText(_fromUtf8(""))
        self.radioButton_place.setChecked(True)
        self.radioButton_place.setObjectName(_fromUtf8("radioButton_place"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.radioButton_place)
        self.lineEdit_nominatim = QtGui.QLineEdit(ui_quick_query)
        self.lineEdit_nominatim.setText(_fromUtf8(""))
        self.lineEdit_nominatim.setObjectName(_fromUtf8("lineEdit_nominatim"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_nominatim)
        self.radioButton_extentMapCanvas = QtGui.QRadioButton(ui_quick_query)
        self.radioButton_extentMapCanvas.setText(_fromUtf8(""))
        self.radioButton_extentMapCanvas.setObjectName(_fromUtf8("radioButton_extentMapCanvas"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.radioButton_extentMapCanvas)
        self.label_13 = QtGui.QLabel(ui_quick_query)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.label_13)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_15 = QtGui.QLabel(ui_quick_query)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_5.addWidget(self.label_15)
        self.comboBox_extentLayer = QtGui.QComboBox(ui_quick_query)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_extentLayer.sizePolicy().hasHeightForWidth())
        self.comboBox_extentLayer.setSizePolicy(sizePolicy)
        self.comboBox_extentLayer.setObjectName(_fromUtf8("comboBox_extentLayer"))
        self.horizontalLayout_5.addWidget(self.comboBox_extentLayer)
        self.pushButton_refreshLayers = QtGui.QPushButton(ui_quick_query)
        self.pushButton_refreshLayers.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/QuickOSM/resources/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_refreshLayers.setIcon(icon)
        self.pushButton_refreshLayers.setObjectName(_fromUtf8("pushButton_refreshLayers"))
        self.horizontalLayout_5.addWidget(self.pushButton_refreshLayers)
        self.formLayout.setLayout(5, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.radioButton_extentLayer = QtGui.QRadioButton(ui_quick_query)
        self.radioButton_extentLayer.setText(_fromUtf8(""))
        self.radioButton_extentLayer.setObjectName(_fromUtf8("radioButton_extentLayer"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.radioButton_extentLayer)
        self.verticalLayout.addLayout(self.formLayout)
        self.groupBox = QgsCollapsibleGroupBox(ui_quick_query)
        self.groupBox.setChecked(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_7)
        self.checkBox_node = QtGui.QCheckBox(self.groupBox)
        self.checkBox_node.setText(_fromUtf8(""))
        self.checkBox_node.setChecked(True)
        self.checkBox_node.setObjectName(_fromUtf8("checkBox_node"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.checkBox_node)
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_8)
        self.checkBox_way = QtGui.QCheckBox(self.groupBox)
        self.checkBox_way.setText(_fromUtf8(""))
        self.checkBox_way.setChecked(True)
        self.checkBox_way.setObjectName(_fromUtf8("checkBox_way"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.checkBox_way)
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_9)
        self.checkBox_relation = QtGui.QCheckBox(self.groupBox)
        self.checkBox_relation.setText(_fromUtf8(""))
        self.checkBox_relation.setChecked(True)
        self.checkBox_relation.setObjectName(_fromUtf8("checkBox_relation"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.checkBox_relation)
        self.horizontalLayout_3.addLayout(self.formLayout_3)
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.label_10 = QtGui.QLabel(self.groupBox)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_10)
        self.checkBox_points = QtGui.QCheckBox(self.groupBox)
        self.checkBox_points.setText(_fromUtf8(""))
        self.checkBox_points.setChecked(True)
        self.checkBox_points.setObjectName(_fromUtf8("checkBox_points"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.checkBox_points)
        self.checkBox_lines = QtGui.QCheckBox(self.groupBox)
        self.checkBox_lines.setText(_fromUtf8(""))
        self.checkBox_lines.setChecked(True)
        self.checkBox_lines.setObjectName(_fromUtf8("checkBox_lines"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.checkBox_lines)
        self.label_11 = QtGui.QLabel(self.groupBox)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_11)
        self.label_12 = QtGui.QLabel(self.groupBox)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_12)
        self.checkBox_multipolygons = QtGui.QCheckBox(self.groupBox)
        self.checkBox_multipolygons.setText(_fromUtf8(""))
        self.checkBox_multipolygons.setChecked(True)
        self.checkBox_multipolygons.setObjectName(_fromUtf8("checkBox_multipolygons"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.FieldRole, self.checkBox_multipolygons)
        self.label_14 = QtGui.QLabel(self.groupBox)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_14)
        self.checkBox_linestrings = QtGui.QCheckBox(self.groupBox)
        self.checkBox_linestrings.setText(_fromUtf8(""))
        self.checkBox_linestrings.setChecked(True)
        self.checkBox_linestrings.setObjectName(_fromUtf8("checkBox_linestrings"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.checkBox_linestrings)
        self.horizontalLayout_3.addLayout(self.formLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.spinBox_timeout = QtGui.QSpinBox(self.groupBox)
        self.spinBox_timeout.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.spinBox_timeout.setMinimum(25)
        self.spinBox_timeout.setMaximum(2000)
        self.spinBox_timeout.setSingleStep(25)
        self.spinBox_timeout.setObjectName(_fromUtf8("spinBox_timeout"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.spinBox_timeout)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_browseDir = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_browseDir.setObjectName(_fromUtf8("lineEdit_browseDir"))
        self.horizontalLayout.addWidget(self.lineEdit_browseDir)
        self.pushButton_browse_output_file = QtGui.QPushButton(self.groupBox)
        self.pushButton_browse_output_file.setObjectName(_fromUtf8("pushButton_browse_output_file"))
        self.horizontalLayout.addWidget(self.pushButton_browse_output_file)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_filePrefix = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_filePrefix.setObjectName(_fromUtf8("lineEdit_filePrefix"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_filePrefix)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_showQuery = QtGui.QPushButton(ui_quick_query)
        self.pushButton_showQuery.setObjectName(_fromUtf8("pushButton_showQuery"))
        self.horizontalLayout_2.addWidget(self.pushButton_showQuery)
        self.pushButton_runQuery = QtGui.QPushButton(ui_quick_query)
        self.pushButton_runQuery.setDefault(True)
        self.pushButton_runQuery.setObjectName(_fromUtf8("pushButton_runQuery"))
        self.horizontalLayout_2.addWidget(self.pushButton_runQuery)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_progress = QtGui.QLabel(ui_quick_query)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_progress.sizePolicy().hasHeightForWidth())
        self.label_progress.setSizePolicy(sizePolicy)
        self.label_progress.setText(_fromUtf8(""))
        self.label_progress.setObjectName(_fromUtf8("label_progress"))
        self.verticalLayout.addWidget(self.label_progress)
        self.progressBar_execution = QtGui.QProgressBar(ui_quick_query)
        self.progressBar_execution.setProperty("value", 0)
        self.progressBar_execution.setObjectName(_fromUtf8("progressBar_execution"))
        self.verticalLayout.addWidget(self.progressBar_execution)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(ui_quick_query)
        QtCore.QMetaObject.connectSlotsByName(ui_quick_query)

    def retranslateUi(self, ui_quick_query):
        ui_quick_query.setWindowTitle(_translate("ui_quick_query", "QuickOSM - Quick query", None))
        self.label.setText(_translate("ui_quick_query", "Key", None))
        self.label_2.setText(_translate("ui_quick_query", "Value", None))
        self.label_3.setText(_translate("ui_quick_query", "In", None))
        self.label_13.setText(_translate("ui_quick_query", "Extent of the map canvas", None))
        self.label_15.setText(_translate("ui_quick_query", "Extent of a layer", None))
        self.groupBox.setTitle(_translate("ui_quick_query", "Advanced", None))
        self.label_7.setText(_translate("ui_quick_query", "Node", None))
        self.label_8.setText(_translate("ui_quick_query", "Way", None))
        self.label_9.setText(_translate("ui_quick_query", "Relation", None))
        self.label_10.setText(_translate("ui_quick_query", "Points", None))
        self.label_11.setText(_translate("ui_quick_query", "Lines", None))
        self.label_12.setText(_translate("ui_quick_query", "Multipolygons", None))
        self.label_14.setText(_translate("ui_quick_query", "Multilinestrings", None))
        self.label_5.setText(_translate("ui_quick_query", "Timeout", None))
        self.label_4.setText(_translate("ui_quick_query", "Directory", None))
        self.lineEdit_browseDir.setPlaceholderText(_translate("ui_quick_query", "Save to temporary file", None))
        self.pushButton_browse_output_file.setText(_translate("ui_quick_query", "Browse", None))
        self.label_6.setText(_translate("ui_quick_query", "File prefix", None))
        self.pushButton_showQuery.setText(_translate("ui_quick_query", "Show query", None))
        self.pushButton_runQuery.setText(_translate("ui_quick_query", "Run query", None))

from qgis.gui import QgsCollapsibleGroupBox
from QuickOSM import resources_rc