# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
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

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

class OsmMemberParser:

    def __init__(self,osmFile):
        '''
        Constructor
        '''
        self.osmFile = osmFile
        
    def getFields(self):
        fields = ["r_full_id","relation","m_full_id","ref","type","role","sequence"]
        return fields
        
    def parse(self):
        saxparser = make_parser()
        relations = osmHandler()
        saxparser.setContentHandler( relations )
        f = open(self.osmFile)
        saxparser.parse(f)
        
        for m in relations.members :
            yield m

class osmHandler(ContentHandler):
    
    DIC_OSM_TYPE = {'node':'n', 'way':'w', 'relation':'r'}
    
    def __init__(self):
        self.type = ""
        self.id = ""
        self.sequence = 0
        self.members = []
        
    def startElement(self, name, attrs):
        if name == "relation":
            self.type = "relation"
            self.id = attrs.get("id")
        elif name == "member":
            self.sequence += 1
            self.members.append( ['r'+self.id, self.id,self.DIC_OSM_TYPE[attrs.get("type")]+attrs.get("ref"),attrs.get("ref"),attrs.get("type"),attrs.get("role"),self.sequence] )
    
    def endElement(self, name):
        if name == "relation":
            self.type = ""
            self.id = ""
            self.sequence = 0