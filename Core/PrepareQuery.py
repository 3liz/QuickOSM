'''
Created on 16 juin 2014

@author: etienne
'''

import re
from Nominatim import Nominatim

def PrepareQuery(query,extent):
    
    '''Delete spaces at the beginning and at the end'''
    query = query.strip()
    
    '''Correction of ; in the OQL at the end'''
    query = re.sub(r';;$',';', query)

    '''Replace nominatimArea by query area with osm id'''
    nominatimQuery = re.search('{{nominatimArea:(.*)}}', query)
    if nominatimQuery:
        result = nominatimQuery.groups()
        nominatim = Nominatim()
        osmid = nominatim.getFirstPolygonFromQuery(result[0])
        print result[0] + " : " + osmid
        area = int(osmid) + 3600000000
        newString = '<id-query into="area" ref="'+str(area)+'" type="area"/>'
        query = re.sub(r'<id-query {{nominatimArea:(.*)}} into="area"/>',newString, query)
    
    '''Replace bbox-query'''
    bboxQuery = re.search('<bbox-query {{bbox}}/>',query)
    '''<bbox-query e="-1.81" n="52.55" s="52.55" w="-1.82"/>'''
    if bboxQuery:
        print "bbox"
        print extent.asWktPolygon()
        newString = '<bbox-query e="'+str(extent.xMaximum())+'" n="'+str(extent.yMaximum())+'" s="'+str(extent.yMinimum())+'" w="'+str(extent.xMinimum())+'"/>'
        query = re.sub(r'<bbox-query {{bbox}}/>',newString, query)
    
    print query
    return query