# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
 A QGIS plugin
 OSM Overpass API frontend
                             -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info at 3liz dot com
        contributor          : Etienne Trimaille
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtWebKit import QWebView
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtCore import QUrl
from qgis.utils import iface
from qgis.gui import QgsMessageBar

from QuickOSM.core.utilities.tools import tr


class Actions(object):
    """
    Manage actions available on layers
    """

    @staticmethod
    def run(field, value):
        """
        Run an action with only one value as parameter
        
        @param field:Type of the action
        @type field:str
        @param value:Value of the field for one entity
        @type value:str
        """
        
        if value == '':
            iface.messageBar().pushMessage(
                tr("QuickOSM",
                   u"Sorry man, this field is empty for this entity."),
                level=QgsMessageBar.WARNING, duration=7)
        else:
            field = unicode(field, "UTF-8")
            value = unicode(value, "UTF-8")
            
            if field in ["url", "website", "wikipedia"]:
                var = QDesktopServices()
                url = None
                
                if field == "url" or field == "website":
                    url = value
                    
                if field == "ref_UAI":
                    url = "http://www.education.gouv.fr/pid24302/annuaire-" \
                          "resultat-recherche.html?lycee_name=" + value
                    
                if field == "wikipedia":
                    url = "http://en.wikipedia.org/wiki/" + value
                    
                var.openUrl(QUrl(url))
            
            elif field == "josm":
                import urllib2
                try:
                    url = "http://localhost:8111/load_object?objects="+value
                    urllib2.urlopen(url).read()
                except urllib2.URLError:
                    iface.messageBar().pushMessage(
                        tr("QuickOSM",
                           u"The JOSM remote seems to be disabled."),
                        level=QgsMessageBar.CRITICAL,
                        duration=7)

            # NOT USED
            elif field == "rawedit":
                url = QUrl("http://rawedit.openstreetmap.fr/edit/"+value)
                web_browser = QWebView(None)
                web_browser.load(url)
                web_browser.show()
                
    @staticmethod
    def run_sketch_line(network, ref):
        """
        Run an action with two values for sketchline
        
        @param network:network of the bus
        @type network:str
        @param ref:ref of the bus
        @type ref:str
        """
        
        network = unicode(network, "UTF-8")
        ref = unicode(ref, "UTF-8")
        
        if network == '' or ref == '':
            iface.messageBar().pushMessage(
                tr("QuickOSM",
                   u"Sorry man, this field is empty for this entity."),
                level=QgsMessageBar.WARNING,
                duration=7)
        else:
            var = QDesktopServices()
            url = "http://www.overpass-api.de/api/sketch-line?" \
                  "network=" + network + "&ref=" + ref
            var.openUrl(QUrl(url))