'''
Created on 23 juin 2014

@author: etienne
'''

import xml.etree.ElementTree as ET

class FirstRelationIdParser():
    
    def __init__(self,osmFile):
        self.__osmFile = osmFile

    def parse(self):
        tree = ET.parse(self.__osmFile)
        root = tree.getroot()
        for child in root: 
            if child.tag == "relation":
                return child.attrib['id']
        
        return False