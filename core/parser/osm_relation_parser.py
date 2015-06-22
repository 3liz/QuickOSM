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


class OsmRelationParser(object):

    def __init__(self, osm_file):
        """
        Constructor
        """
        self.osm_file = osm_file
        self.fields = ['full_id', 'osm_id', 'osm_type']

    def get_fields(self):
        return self.fields

    def parse(self):
        sax_parser = make_parser()
        relations = OsmHandler()
        sax_parser.setContentHandler(relations)
        f = open(self.osm_file)
        sax_parser.parse(f)

        self.fields = relations.fields
        for elem in relations.elements:
            e = []
            for f in self.fields:
                if f in elem:
                    e.append(elem[f])
                else:
                    e.append('')
            yield e


class OsmHandler(ContentHandler):

    DIC_OSM_TYPE = {'node': 'n', 'way': 'w', 'relation': 'r'}

    def __init__(self):
        ContentHandler.__init__(self)
        self.type = ""
        self.id = ""
        self.tags = {}
        self.fields = ['full_id', 'osm_id', 'osm_type']
        self.elements = []

    def startElement(self, name, attributes):
        if name == "relation":
            self.type = "relation"
            self.id = attributes.get("id")
        elif name == "tag" and self.type == "relation":
            k = attributes.get("k").replace(":", "_")
            if k not in self.fields:
                self.fields.append(k)
            self.tags[k] = attributes.get("v")

    def endElement(self, name):
        if name == "relation":
            self.tags['full_id'] = 'r'+self.id
            self.tags['osm_id'] = self.id
            self.tags['osm_type'] = 'relation'
            self.elements.append(self.tags)

            self.type = ""
            self.id = ""
            self.tags = {}
