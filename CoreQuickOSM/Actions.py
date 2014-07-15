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
                    
                var.openUrl(QUrl(url))
            
            #NOT USED    
            elif field == "rawedit":
                url = QUrl("http://rawedit.openstreetmap.fr/edit/"+value)
                webBrowser = QWebView(None)
                webBrowser.load(url)
                webBrowser.show()