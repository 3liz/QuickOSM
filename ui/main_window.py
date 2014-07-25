# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Fri Jul 25 14:53:27 2014
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
        ui_main_window.setWindowModality(QtCore.Qt.WindowModal)
        ui_main_window.resize(837, 659)
        self.horizontalLayout = QtGui.QHBoxLayout(ui_main_window)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(ui_main_window)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.listWidget = QtGui.QListWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMinimumSize(QtCore.QSize(100, 200))
        self.listWidget.setMaximumSize(QtCore.QSize(153, 16777215))
        self.listWidget.setStyleSheet(_fromUtf8("QListWidget{\n"
"    background-color: rgb(69, 69, 69, 220);\n"
"    outline: 0;\n"
"}\n"
"QListWidget::item {\n"
"    color: white;\n"
"    padding: 3px;\n"
"}\n"
"QListWidget::item::selected {\n"
"    color: black;\n"
"    background-color:palette(Window);\n"
"    padding-right: 0px;\n"
"}"))
        self.listWidget.setFrameShape(QtGui.QFrame.Box)
        self.listWidget.setLineWidth(0)
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
        item = QtGui.QListWidgetItem()
        item.setIcon(icon)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setIcon(icon)
        self.listWidget.addItem(item)
        self.stackedWidget = QtGui.QStackedWidget(self.splitter)
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
        self.query = QueryWidget()
        self.query.setObjectName(_fromUtf8("query"))
        self.stackedWidget.addWidget(self.query)
        self.osm_file = OsmFileWidget()
        self.osm_file.setObjectName(_fromUtf8("osm_file"))
        self.stackedWidget.addWidget(self.osm_file)
        self.parameters = QtGui.QWidget()
        self.parameters.setObjectName(_fromUtf8("parameters"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.parameters)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.parameters)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.comboBox_default_OAPI = QtGui.QComboBox(self.groupBox)
        self.comboBox_default_OAPI.setObjectName(_fromUtf8("comboBox_default_OAPI"))
        self.comboBox_default_OAPI.addItem(_fromUtf8(""))
        self.comboBox_default_OAPI.addItem(_fromUtf8(""))
        self.comboBox_default_OAPI.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.comboBox_default_OAPI)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_OAPI_timestamp = QtGui.QPushButton(self.groupBox)
        self.pushButton_OAPI_timestamp.setObjectName(_fromUtf8("pushButton_OAPI_timestamp"))
        self.horizontalLayout_2.addWidget(self.pushButton_OAPI_timestamp)
        self.label_timestamp_oapi = QtGui.QLabel(self.groupBox)
        self.label_timestamp_oapi.setObjectName(_fromUtf8("label_timestamp_oapi"))
        self.horizontalLayout_2.addWidget(self.label_timestamp_oapi)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.stackedWidget.addWidget(self.parameters)
        self.help = QtGui.QWidget()
        self.help.setObjectName(_fromUtf8("help"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.help)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.scrollArea = QtGui.QScrollArea(self.help)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 667, 645))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_help = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_help.setObjectName(_fromUtf8("label_help"))
        self.verticalLayout_5.addWidget(self.label_help)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.stackedWidget.addWidget(self.help)
        self.about = QtGui.QWidget()
        self.about.setObjectName(_fromUtf8("about"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.about)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.groupBox_2 = QtGui.QGroupBox(self.about)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.stackedWidget.addWidget(self.about)
        self.horizontalLayout.addWidget(self.splitter)

        self.retranslateUi(ui_main_window)
        self.listWidget.setCurrentRow(-1)
        self.stackedWidget.setCurrentIndex(5)
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
        item.setText(_translate("ui_main_window", "Quick query", None))
        item = self.listWidget.item(2)
        item.setText(_translate("ui_main_window", "Query", None))
        item = self.listWidget.item(3)
        item.setText(_translate("ui_main_window", "OSM File", None))
        item = self.listWidget.item(4)
        item.setText(_translate("ui_main_window", "Parameters", None))
        item = self.listWidget.item(5)
        item.setText(_translate("ui_main_window", "Help", None))
        item = self.listWidget.item(6)
        item.setText(_translate("ui_main_window", "About", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("ui_main_window", "Overpass API", None))
        self.comboBox_default_OAPI.setItemText(0, _translate("ui_main_window", "http://www.overpass-api.de/api/", None))
        self.comboBox_default_OAPI.setItemText(1, _translate("ui_main_window", "http://overpass.osm.rambler.ru/cgi/", None))
        self.comboBox_default_OAPI.setItemText(2, _translate("ui_main_window", "http://api.openstreetmap.fr/oapi/", None))
        self.pushButton_OAPI_timestamp.setText(_translate("ui_main_window", "Get timestamp", None))
        self.label_timestamp_oapi.setText(_translate("ui_main_window", "unknow", None))
        self.label_help.setText(_translate("ui_main_window", "Help", None))
        self.groupBox_2.setTitle(_translate("ui_main_window", "Blabla", None))

from query_dialog import QueryWidget
from osm_file_dialog import OsmFileWidget
from quick_query_dialog import QuickQueryWidget
from my_queries_dialog import MyQueriesWidget
from QuickOSM import resources_rc
