# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
                              -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info@3liz.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from processing.core.Processing import Processing
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from quick_osm_dialog import QuickOSMDialog
from QuickOSMAlgorithmProvider import QuickOSMAlgorithmProvider
import os.path


class QuickOSM:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'QuickOSM_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = QuickOSMDialog()

        # Declare instance attributes
        self.action = None

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/resources/icon"),
            u"Quick OSM",
            self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(
            u"&Quick OSM",
            self.action)
        
        #Add to processing
        self.provider = QuickOSMAlgorithmProvider()
        Processing.addProvider(self.provider, True)
        

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.iface.removePluginMenu(
            u"&Quick OSM",
            self.action)
        self.iface.removeToolBarIcon(self.action)
        Processing.removeProvider(self.provider)

    
    def run(self):
        # show the dialog
        self.dlg.show()
    