# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Thu Jul  3 10:52:42 2014
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(701, 513)
        self.gridLayout = QtGui.QGridLayout(MainWindow)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listWidget = QtGui.QListWidget(MainWindow)
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
        item.setIcon(icon)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon)
        self.listWidget.addItem(item)
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)
        self.stackedWidget = QtGui.QStackedWidget(MainWindow)
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

        self.retranslateUi(MainWindow)
        self.listWidget.setCurrentRow(-1)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("currentRowChanged(int)")), self.stackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Quick OSM", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "My queries", None))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Quick query", None))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "Parameters", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("MainWindow", "Overpass API", None))
        self.pushButton_OAPI_timestamp.setText(_translate("MainWindow", "Get timestamp", None))
        self.label_timestamp_oapi.setText(_translate("MainWindow", "unknow", None))
        self.comboBox_default_OAPI.setItemText(0, _translate("MainWindow", "http://www.overpass-api.de/api/", None))
        self.comboBox_default_OAPI.setItemText(1, _translate("MainWindow", "http://overpass.osm.rambler.ru/cgi/", None))
        self.comboBox_default_OAPI.setItemText(2, _translate("MainWindow", "http://api.openstreetmap.fr/oapi/", None))
        self.label.setText(_translate("MainWindow", "Server", None))

from quick_query_dialog import QuickQueryWidget
from my_queries_dialog import MyQueriesWidget
