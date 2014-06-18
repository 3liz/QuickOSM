'''
Created on 16 juin 2014

@author: etienne
'''

import re
from Nominatim import Nominatim

def PrepareQuery(query):
    
    '''Delete spaces at the beginning and at the end'''
    query = query.strip()
    
    '''Correction of ; in the OQL at the end'''
    query = re.sub(r';;$',';', query)

    '''Replace nominatimArea by query area with osm id'''
    nominatimQuery = re.search('{{nominatimArea:(.*)}}', query)
    nominatim = Nominatim()
    if nominatimQuery:
        result = nominatimQuery.groups()
        osmid = nominatim.getFirstPolygonFromQuery(result[0])
        print result[0] + " : " + osmid
        area = int(osmid) + 3600000000
        newString = '<id-query into="area" ref="'+str(area)+'" type="area"/>'
        query = re.sub(r'<id-query {{nominatimArea:(.*)}} into="area"/>',newString, query)
    
    return query