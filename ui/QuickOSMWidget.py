'''
Created on 24 juil. 2014

@author: etienne
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface
from QuickOSM.CoreQuickOSM.ExceptionQuickOSM import *

class QuickOSMWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

    def fillLayerCombobox(self):
        '''
        Fill the combobox with layers which are in the legend
        '''
        layers = iface.legendInterface().layers()
        self.comboBox_extentLayer.clear()
        for layer in layers:
            self.comboBox_extentLayer.addItem(layer.name(),layer)
            
        if self.comboBox_extentLayer.count() < 1:
            self.radioButton_extentLayer.setCheckable(False)
            self.radioButton_extentMapCanvas.setChecked(True)
            
    def disablePrefixFile(self):
        '''
        If the directory is empty, we disable the file prefix
        '''
        if self.lineEdit_browseDir.text():
            self.lineEdit_filePrefix.setDisabled(False)
        else:
            self.lineEdit_filePrefix.setText("")
            self.lineEdit_filePrefix.setDisabled(True)
            
    def setOutDirPath(self):
        '''
        Fill the output directory path
        '''
        outputFile = QFileDialog.getExistingDirectory(None, caption=QApplication.translate("QuickOSM", 'Select directory'))
        self.lineEdit_browseDir.setText(outputFile)
        self.disablePrefixFile()
        
    def extentRadio(self):
        '''
        Disable or enable the comboxbox
        '''
        if self.radioButton_extentLayer.isChecked():
            self.comboBox_extentLayer.setDisabled(False)
        else:
            self.comboBox_extentLayer.setDisabled(True)

    def getOutputGeomTypes(self):
        outputGeomTypes = []
        if self.checkBox_points.isChecked():
            outputGeomTypes.append('points')
        if self.checkBox_lines.isChecked():
            outputGeomTypes.append('lines')
        if self.checkBox_multilinestrings.isChecked():
            outputGeomTypes.append('multilinestrings')
        if self.checkBox_multipolygons.isChecked():
            outputGeomTypes.append('multipolygons')
        return outputGeomTypes
    
    def getWhiteListValues(self):
        whiteListValues = {}
        if self.checkBox_points.isChecked():
            whiteListValues['points'] = self.lineEdit_csv_points.text()
        if self.checkBox_lines.isChecked():
            whiteListValues['lines'] = self.lineEdit_csv_lines.text()
        if self.checkBox_multilinestrings.isChecked():
            whiteListValues['multilinestrings'] = self.lineEdit_csv_multilinestrings.text()
        if self.checkBox_multipolygons.isChecked():
            whiteListValues['multipolygons'] = self.lineEdit_csv_multipolygons.text()
        return whiteListValues
    
    def getBBox(self):
        '''
        Get the geometry of the bbox in WGS84
        '''
        geomExtent = None
        sourceCrs = None
        
        #If mapCanvas is checked
        if self.radioButton_extentMapCanvas.isChecked():
            geomExtent = iface.mapCanvas().extent()
            sourceCrs = iface.mapCanvas().mapRenderer().destinationCrs()
        else:
            #Else if a layer is checked
            index = self.comboBox_extentLayer.currentIndex()
            layerID = self.comboBox_extentLayer.itemData(index)
            layerName = self.comboBox_extentLayer.itemText(index)
            layers = iface.legendInterface().layers()
            for layer in layers:
                if layer.id() == layerID:
                    geomExtent = layer.extent()
                    sourceCrs = layer.crs()
                    break
            else:
                #the layer could be deleted before
                raise NoLayerException(suffix=layerName)
        
        geomExtent = QgsGeometry.fromRect(geomExtent)
        crsTransform = QgsCoordinateTransform(sourceCrs, QgsCoordinateReferenceSystem("EPSG:4326"))
        geomExtent.transform(crsTransform)
        return geomExtent.boundingBox()

    def startProcess(self):
        self.pushButton_runQuery.setDisabled(True)
        self.pushButton_runQuery.initialText = self.pushButton_runQuery.text()
        self.pushButton_runQuery.setText(QApplication.translate("QuickOSM","Running query ..."))
        self.progressBar_execution.setMinimum(0)
        self.progressBar_execution.setMaximum(0)
        self.progressBar_execution.setValue(0)
        self.label_progress.setText("")
        
        
    def endProcess(self):
        self.pushButton_runQuery.setDisabled(False)
        self.pushButton_runQuery.setText(self.pushButton_runQuery.initialText)
        self.progressBar_execution.setMinimum(0)
        self.progressBar_execution.setMaximum(100)
        self.progressBar_execution.setValue(100)
        QApplication.processEvents()      
    
    def setProgressPercentage(self,percent):
        '''
        Slot to update percentage during process
        '''
        self.progressBar_execution.setValue(percent)
        QApplication.processEvents()
        
    def setProgressText(self,text):
        '''
        Slot to update text during process
        '''
        self.label_progress.setText(text)
        QApplication.processEvents()
    
    def displayGeoAlgorithmException(self,e):
        self.label_progress.setText("")
        iface.messageBar().pushMessage(e.msg, level=QgsMessageBar.CRITICAL , duration=7)

    def displayException(self,e):
        import sys,os
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        ex_type, ex, tb = sys.exc_info()
        import traceback
        traceback.print_tb(tb)
        iface.messageBar().pushMessage("Error in the python console, please report it", level=QgsMessageBar.CRITICAL , duration=5)