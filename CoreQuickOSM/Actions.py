'''
Created on 15 juil. 2014

@author: etienne
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import QWebView
from PyQt4.QtNetwork import *
from qgis.gui import QgsMessageBar
from qgis.utils import iface

class Actions:

    @staticmethod
    def run(field,value):
        
        if value == '':
            iface.messageBar().pushMessage(QApplication.translate("QuickOSM", u"Sorry man, this field is empty for this entity."), level=QgsMessageBar.WARNING , duration=7)
        else:
            if field in ["url","website","wikipedia"]:
                var = QDesktopServices()
                url = None
                
                if field == "url" or field =="website":
                    url = value
                    
                if field == "ref_UAI":
                    url = "http://www.education.gouv.fr/pid24302/annuaire-resultat-recherche.html?lycee_name="+value
                    
                if field == "wikipedia":
                    url = "http://en.wikipedia.org/wiki/" + value
                    
                var.openUrl(QUrl(url))
            
            elif field == "josm":
                import urllib2
                try:
                    url = "http://localhost:8111/load_object?objects="+value
                    data = urllib2.urlopen(url).read()
                except urllib2.URLError:
                    iface.messageBar().pushMessage(QApplication.translate("QuickOSM", u"Sorry man, the JOSM remote is not enabled."), level=QgsMessageBar.CRITICAL , duration=7)
            
            #NOT USED    
            elif field == "rawedit":
                url = QUrl("http://rawedit.openstreetmap.fr/edit/"+value)
                webBrowser = QWebView(None)
                webBrowser.load(url)
                webBrowser.show()
                
    @staticmethod
    def runSketchLine(network,ref):
        
        if network == '' or ref == '':
            iface.messageBar().pushMessage(QApplication.translate("QuickOSM", u"Sorry man, this field is empty for this entity."), level=QgsMessageBar.WARNING , duration=7)
        else:
            var = QDesktopServices()
            url = "http://www.overpass-api.de/api/sketch-line?network="+network+"&ref="+ref
            var.openUrl(QUrl(url))