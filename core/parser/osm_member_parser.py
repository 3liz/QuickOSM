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

from xml.sax import make_parser
from xml.sax.handler import ContentHandler


class OsmMemberParser(object):

    def __init__(self, osm_file):
        """
        Constructor
        """
        self.osm_file = osm_file

    @staticmethod
    def get_fields():
        fields = [
            "r_full_id",
            "relation",
            "m_full_id",
            "ref",
            "type",
            "role",
            "sequence"]
        return fields

    def parse(self):
        sax_parser = make_parser()
        relations = OsmHandler()
        sax_parser.setContentHandler(relations)
        f = open(self.osm_file)
        sax_parser.parse(f)

        for m in relations.members:
            yield m


class OsmHandler(ContentHandler):

    DIC_OSM_TYPE = {'node': 'n', 'way': 'w', 'relation': 'r'}

    def __init__(self):
        ContentHandler.__init__(self)
        self.type = ""
        self.id = ""
        self.sequence = 0
        self.members = []

    def startElement(self, name, attributes):
        if name == "relation":
            self.type = "relation"
            self.id = attributes.get("id")
        elif name == "member":
            self.sequence += 1
            osm_type = self.DIC_OSM_TYPE[attributes.get("type")]
            tab = [
                'r%s' % self.id,
                self.id,
                '%s%s' % (osm_type, attributes.get("ref")),
                attributes.get("ref"),
                attributes.get("type"),
                attributes.get("role"),
                self.sequence]
            self.members.append(tab)

    def endElement(self, name):
        if name == "relation":
            self.type = ""
            self.id = ""
            self.sequence = 0
