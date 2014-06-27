'''
Created on 27 juin 2014

@author: etienne
'''

class QueryFactory():
    
    OSM_TYPES = ['node','way','relation']

    def __init__(self,key = None,value = None,bbox = None,nominatim = None,osmObjects = OSM_TYPES, output = 'xml', timeout='25', printMode = 'body'):
        self.__key = key
        self.__value = value
        self.__bbox = bbox
        self.__nominatim = nominatim
        self.__osmObjects = osmObjects
        self.__timeout = timeout
        self.__output = output
        self.__printMode = printMode
        
    def make(self):
        
        '''
        if not self.__nominatim and not self.__bbox:
            return False, "Nominatim or bbox required"'''
        
        if self.__nominatim and self.__bbox:
            return False, "Nominatim OR bbox, not both"
        
        if self.__nominatim == '{{nominatim}}' or self.__nominatim == True:
            self.__nominatim = '{{nominatim}}'
            
        if self.__bbox == '{{bbox}}' or self.__bbox == True:
            self.__bbox = '{{bbox}}'
        
        if not self.__key:
            return False, "Key required"
        
        for osmObject in self.__osmObjects:
            if osmObject not in QueryFactory.OSM_TYPES:
                return False, "Wrong OSM object"
          
        #TEST OK, so continue  
        query = '<osm-script output="'+self.__output+'" timeout="'+self.__timeout+'"> \n'
        
        if self.__nominatim:
            query += '\t<id-query {{nominatimArea:'+self.__nominatim+'}} into="area"/> \n'
            
        query += '\t<union>\n'
        
        for osmObject in self.__osmObjects:
            query += '\t\t<query type="'+osmObject+'"><has-kv k="'+self.__key+'" '
            if self.__value:
                query += 'v="'+self.__value+'"'
            query += '/> \n'
            
            if self.__nominatim:
                query += '\t\t\t<area-query from="area"/>\n'
            elif self.__bbox:
                query += '\t\t<bbox-query '+self.__bbox+'/>\n'
            query += '\t\t</query>\n'
        
        query += '\t</union>\n\t<union>\n\t\t<item />\n\t\t<recurse type="down"/>\n\t</union>\n'
        query += '\t<print mode="'+self.__printMode+'" />\n</osm-script>'
        
        return query