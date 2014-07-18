'''
Created on 27 juin 2014

@author: etienne
'''

from qgis.core import QgsRectangle

class QueryFactory():
    
    OSM_TYPES = ['node','way','relation']

    def __init__(self,key = None,value = None,bbox = None,nominatim = None,osmObjects = OSM_TYPES, output = 'xml', timeout=25, printMode = 'body'):
        self.__key = key
        self.__value = value
        self.__bbox = bbox
        self.__nominatim = nominatim
        self.__osmObjects = osmObjects
        self.__timeout = timeout
        self.__output = output
        self.__printMode = printMode
        
    def make(self):
        
        if self.__nominatim and self.__bbox:
            return False, "Nominatim OR bbox, not both"
        
        if self.__nominatim == '{{nominatim}}' or self.__nominatim == True:
            self.__nominatim = '{{nominatim}}'
            
        if self.__bbox == '{{bbox}}' or self.__bbox == True or isinstance(self.__bbox, QgsRectangle):
            self.__bbox = '{{bbox}}'
        
        if not self.__key:
            return False, "Key required"
        
        for osmObject in self.__osmObjects:
            if osmObject not in QueryFactory.OSM_TYPES:
                return False, "Wrong OSM object"
          
        #TEST OK, so continue
        TAB = '     '
        query = '<osm-script output="%s" timeout="%s"> \n' %(self.__output,self.__timeout)
        
        if self.__nominatim:
            query += TAB + '<id-query {{nominatimArea:'+self.__nominatim+'}} into="area"/> \n'
            
        query += TAB + '<union>\n'
        
        for osmObject in self.__osmObjects:
            query += TAB + TAB +'<query type="'+osmObject+'">\n'
            query += TAB + TAB + TAB +'<has-kv k="'+self.__key+'" '
            if self.__value:
                query += 'v="'+self.__value+'"'
            query += '/> \n'
            
            if self.__nominatim:
                query += TAB + TAB + TAB + '<area-query from="area"/>\n'
            elif self.__bbox:
                query += TAB + TAB + TAB + '<bbox-query '+self.__bbox+'/>\n'
            query += TAB + TAB + '</query>\n'
        
        query += TAB + '</union>\n'+TAB+'<union>\n'+TAB + TAB +'<item />\n'+TAB + TAB +'<recurse type="down"/>\n'+TAB +'</union>\n'
        query += TAB + '<print mode="'+self.__printMode+'" />\n</osm-script>'
        
        return query