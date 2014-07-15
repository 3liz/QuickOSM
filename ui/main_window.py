# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Tue Jul 15 17:56:38 2014
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

class Ui_ui_main_window(object):
    def setupUi(self, ui_main_window):
        ui_main_window.setObjectName(_fromUtf8("ui_main_window"))
        ui_main_window.setWindowModality(QtCore.Qt.NonModal)
        ui_main_window.resize(701, 513)
        self.gridLayout = QtGui.QGridLayout(ui_main_window)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listWidget = QtGui.QListWidget(ui_main_window)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMinimumSize(QtCore.QSize(100, 200))
        self.listWidget.setMaximumSize(QtCore.QSize(153, 16777215))
        self.listWidget.setStyleSheet(_fromUtf8("background:rgb(74, 74, 74)"))
        self.listWidget.setIconSize(QtCore.QSize(32, 32))
        self.listWidget.setUniformItemSizes(True)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        item = QtGui.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/QuickOSM/resources/general.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon)
        self.listWidget.addItem(item)
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)
        self.stackedWidget = QtGui.QStackedWidget(ui_main_window)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QtCore.QSize(300, 200))
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.my_queries = MyQueriesWidget()
        self.my_queries.setObjectName(_fromUtf8("my_queries"))
        self.stackedWidget.addWidget(self.my_queries)
        self.query = QueryWidget()
        self.query.setObjectName(_fromUtf8("query"))
        self.stackedWidget.addWidget(self.query)
        self.quick_query = QuickQueryWidget()
        self.quick_query.setObjectName(_fromUtf8("quick_query"))
        self.stackedWidget.addWidget(self.quick_query)
        self.parameters = QtGui.QWidget()
        self.parameters.setObjectName(_fromUtf8("parameters"))
        self.groupBox = QtGui.QGroupBox(self.parameters)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 501, 381))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 70, 321, 27))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_OAPI_timestamp = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_OAPI_timestamp.setObjectName(_fromUtf8("pushButton_OAPI_timestamp"))
        self.horizontalLayout_2.addWidget(self.pushButton_OAPI_timestamp)
        self.label_timestamp_oapi = QtGui.QLabel(self.layoutWidget)
        self.label_timestamp_oapi.setObjectName(_fromUtf8("label_timestamp_oapi"))
        self.horizontalLayout_2.addWidget(self.label_timestamp_oapi)
        self.comboBox_default_OAPI = QtGui.QComboBox(self.groupBox)
        self.comboBox_default_OAPI.setGeometry(QtCore.QRect(60, 40, 261, 24))
        self.comboBox_default_OAPI.setObjectName(_fromUtf8("comboBox_default_OAPI"))
        self.comboBox_default_OAPI.addItem(_fromUtf8(""))
        self.comboBox_default_OAPI.addItem(_fromUtf8(""))
        self.comboBox_default_OAPI.addItem(_fromUtf8(""))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 40, 61, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.stackedWidget.addWidget(self.parameters)
        self.gridLayout.addWidget(self.stackedWidget, 0, 1, 1, 1)

        self.retranslateUi(ui_main_window)
        self.listWidget.setCurrentRow(-1)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("currentRowChanged(int)")), self.stackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(ui_main_window)
        ui_main_window.setTabOrder(self.pushButton_OAPI_timestamp, self.comboBox_default_OAPI)
        ui_main_window.setTabOrder(self.comboBox_default_OAPI, self.listWidget)

    def retranslateUi(self, ui_main_window):
        ui_main_window.setWindowTitle(_translate("ui_main_window", "Quick OSM", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("ui_main_window", "My queries", None))
        item = self.listWidget.item(1)
        item.setText(_translate("ui_main_window", "Query", None))
        item = self.listWidget.item(2)
        item.setText(_translate("ui_main_window", "Quick query", None))
        item = self.listWidget.item(3)
        item.setText(_translate("ui_main_window", "Parameters", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("ui_main_window", "Overpass API", None))
        self.pushButton_OAPI_timestamp.setText(_translate("ui_main_window", "Get timestamp", None))
        self.label_timestamp_oapi.setText(_translate("ui_main_window", "unknow", None))
        self.comboBox_default_OAPI.setItemText(0, _translate("ui_main_window", "http://www.overpass-api.de/api/", None))
        self.comboBox_default_OAPI.setItemText(1, _translate("ui_main_window", "http://overpass.osm.rambler.ru/cgi/", None))
        self.comboBox_default_OAPI.setItemText(2, _translate("ui_main_window", "http://api.openstreetmap.fr/oapi/", None))
        self.label.setText(_translate("ui_main_window", "Server", None))

from query_dialog import QueryWidget
from quick_query_dialog import QuickQueryWidget
from my_queries_dialog import MyQueriesWidget
