# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/quick_query.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ui_quick_query(object):
    def setupUi(self, ui_quick_query):
        ui_quick_query.setObjectName("ui_quick_query")
        ui_quick_query.resize(644, 805)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(ui_quick_query)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(ui_quick_query)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 626, 787))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_mapFeatures = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_mapFeatures.setObjectName("pushButton_mapFeatures")
        self.horizontalLayout_4.addWidget(self.pushButton_mapFeatures)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.scrollAreaWidgetContents)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_4.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox_key = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_key.sizePolicy().hasHeightForWidth())
        self.comboBox_key.setSizePolicy(sizePolicy)
        self.comboBox_key.setEditable(True)
        self.comboBox_key.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox_key.setObjectName("comboBox_key")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_key)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBox_value = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_value.sizePolicy().hasHeightForWidth())
        self.comboBox_value.setSizePolicy(sizePolicy)
        self.comboBox_value.setEditable(True)
        self.comboBox_value.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox_value.setObjectName("comboBox_value")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_value)
        self.radioButton_place = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_place.setText("")
        self.radioButton_place.setChecked(True)
        self.radioButton_place.setObjectName("radioButton_place")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.radioButton_place)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.comboBox_in_around = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_in_around.setObjectName("comboBox_in_around")
        self.horizontalLayout_8.addWidget(self.comboBox_in_around)
        self.lineEdit_nominatim = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_nominatim.setText("")
        self.lineEdit_nominatim.setObjectName("lineEdit_nominatim")
        self.horizontalLayout_8.addWidget(self.lineEdit_nominatim)
        self.spinBox_distance_point = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.spinBox_distance_point.setMinimum(1)
        self.spinBox_distance_point.setMaximum(999999999)
        self.spinBox_distance_point.setSingleStep(100)
        self.spinBox_distance_point.setProperty("value", 1000)
        self.spinBox_distance_point.setObjectName("spinBox_distance_point")
        self.horizontalLayout_8.addWidget(self.spinBox_distance_point)
        self.label_distance_point = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_distance_point.setText("m")
        self.label_distance_point.setObjectName("label_distance_point")
        self.horizontalLayout_8.addWidget(self.label_distance_point)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_8)
        self.radioButton_extentMapCanvas = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_extentMapCanvas.setText("")
        self.radioButton_extentMapCanvas.setObjectName("radioButton_extentMapCanvas")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.radioButton_extentMapCanvas)
        self.label_13 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.label_13)
        self.radioButton_extentLayer = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_extentLayer.setText("")
        self.radioButton_extentLayer.setObjectName("radioButton_extentLayer")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.radioButton_extentLayer)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_15 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_5.addWidget(self.label_15)
        self.comboBox_extentLayer = QgsMapLayerComboBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_extentLayer.sizePolicy().hasHeightForWidth())
        self.comboBox_extentLayer.setSizePolicy(sizePolicy)
        self.comboBox_extentLayer.setObjectName("comboBox_extentLayer")
        self.horizontalLayout_5.addWidget(self.comboBox_extentLayer)
        self.formLayout.setLayout(5, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.verticalLayout.addLayout(self.formLayout)
        self.advanced = QgsCollapsibleGroupBox(self.scrollAreaWidgetContents)
        self.advanced.setChecked(False)
        self.advanced.setObjectName("advanced")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.advanced)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_7 = QtWidgets.QLabel(self.advanced)
        self.label_7.setText("Node")
        self.label_7.setObjectName("label_7")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.checkBox_node = QtWidgets.QCheckBox(self.advanced)
        self.checkBox_node.setText("")
        self.checkBox_node.setChecked(True)
        self.checkBox_node.setObjectName("checkBox_node")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.checkBox_node)
        self.label_8 = QtWidgets.QLabel(self.advanced)
        self.label_8.setText("Way")
        self.label_8.setObjectName("label_8")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.checkBox_way = QtWidgets.QCheckBox(self.advanced)
        self.checkBox_way.setText("")
        self.checkBox_way.setChecked(True)
        self.checkBox_way.setObjectName("checkBox_way")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.checkBox_way)
        self.label_9 = QtWidgets.QLabel(self.advanced)
        self.label_9.setText("Relation")
        self.label_9.setObjectName("label_9")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.checkBox_relation = QtWidgets.QCheckBox(self.advanced)
        self.checkBox_relation.setText("")
        self.checkBox_relation.setChecked(True)
        self.checkBox_relation.setObjectName("checkBox_relation")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.checkBox_relation)
        self.horizontalLayout_3.addLayout(self.formLayout_3)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_10 = QtWidgets.QLabel(self.advanced)
        self.label_10.setText("Points")
        self.label_10.setObjectName("label_10")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.checkBox_points = QtWidgets.QCheckBox(self.advanced)
        self.checkBox_points.setText("")
        self.checkBox_points.setChecked(True)
        self.checkBox_points.setObjectName("checkBox_points")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.checkBox_points)
        self.checkBox_lines = QtWidgets.QCheckBox(self.advanced)
        self.checkBox_lines.setText("")
        self.checkBox_lines.setChecked(True)
        self.checkBox_lines.setObjectName("checkBox_lines")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.checkBox_lines)
        self.label_11 = QtWidgets.QLabel(self.advanced)
        self.label_11.setText("Lines")
        self.label_11.setObjectName("label_11")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.label_12 = QtWidgets.QLabel(self.advanced)
        self.label_12.setText("Multipolygons")
        self.label_12.setObjectName("label_12")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.checkBox_multipolygons = QtWidgets.QCheckBox(self.advanced)
        self.checkBox_multipolygons.setText("")
        self.checkBox_multipolygons.setChecked(True)
        self.checkBox_multipolygons.setObjectName("checkBox_multipolygons")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.checkBox_multipolygons)
        self.label_14 = QtWidgets.QLabel(self.advanced)
        self.label_14.setText("Multilinestrings")
        self.label_14.setObjectName("label_14")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.checkBox_multilinestrings = QtWidgets.QCheckBox(self.advanced)
        self.checkBox_multilinestrings.setText("")
        self.checkBox_multilinestrings.setChecked(True)
        self.checkBox_multilinestrings.setObjectName("checkBox_multilinestrings")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.checkBox_multilinestrings)
        self.horizontalLayout_3.addLayout(self.formLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_5 = QtWidgets.QLabel(self.advanced)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.spinBox_timeout = QtWidgets.QSpinBox(self.advanced)
        self.spinBox_timeout.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spinBox_timeout.setMinimum(25)
        self.spinBox_timeout.setMaximum(2000)
        self.spinBox_timeout.setSingleStep(25)
        self.spinBox_timeout.setObjectName("spinBox_timeout")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBox_timeout)
        self.label_4 = QtWidgets.QLabel(self.advanced)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.output_directory = QgsFileWidget(self.advanced)
        self.output_directory.setObjectName("output_directory")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.output_directory)
        self.label_6 = QtWidgets.QLabel(self.advanced)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_filePrefix = QtWidgets.QLineEdit(self.advanced)
        self.lineEdit_filePrefix.setObjectName("lineEdit_filePrefix")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_filePrefix)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.verticalLayout.addWidget(self.advanced)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_showQuery = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_showQuery.setObjectName("pushButton_showQuery")
        self.horizontalLayout_2.addWidget(self.pushButton_showQuery)
        self.pushButton_runQuery = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_runQuery.setDefault(True)
        self.pushButton_runQuery.setObjectName("pushButton_runQuery")
        self.horizontalLayout_2.addWidget(self.pushButton_runQuery)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_progress = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_progress.sizePolicy().hasHeightForWidth())
        self.label_progress.setSizePolicy(sizePolicy)
        self.label_progress.setText("progress text")
        self.label_progress.setObjectName("label_progress")
        self.verticalLayout.addWidget(self.label_progress)
        self.progressBar_execution = QtWidgets.QProgressBar(self.scrollAreaWidgetContents)
        self.progressBar_execution.setProperty("value", 0)
        self.progressBar_execution.setObjectName("progressBar_execution")
        self.verticalLayout.addWidget(self.progressBar_execution)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)

        self.retranslateUi(ui_quick_query)
        QtCore.QMetaObject.connectSlotsByName(ui_quick_query)

    def retranslateUi(self, ui_quick_query):
        _translate = QtCore.QCoreApplication.translate
        ui_quick_query.setWindowTitle(_translate("ui_quick_query", "QuickOSM - Quick query"))
        self.pushButton_mapFeatures.setText(_translate("ui_quick_query", "Help with key/value"))
        self.label.setText(_translate("ui_quick_query", "Key"))
        self.label_2.setText(_translate("ui_quick_query", "Value"))
        self.comboBox_in_around.setToolTip(_translate("ui_quick_query", "\"In\" will search the first multipolygon relation, however \"Around\" will get the first OSM node."))
        self.lineEdit_nominatim.setPlaceholderText(_translate("ui_quick_query", "A village, a town, ..."))
        self.label_13.setText(_translate("ui_quick_query", "Extent of the map canvas"))
        self.label_15.setText(_translate("ui_quick_query", "Extent of a layer"))
        self.advanced.setTitle(_translate("ui_quick_query", "Advanced"))
        self.label_5.setText(_translate("ui_quick_query", "Timeout"))
        self.label_4.setText(_translate("ui_quick_query", "Directory"))
        self.label_6.setText(_translate("ui_quick_query", "File prefix"))
        self.pushButton_showQuery.setText(_translate("ui_quick_query", "Show query"))
        self.pushButton_runQuery.setText(_translate("ui_quick_query", "Run query"))

from qgis.gui import QgsCollapsibleGroupBox, QgsFileWidget, QgsMapLayerComboBox
