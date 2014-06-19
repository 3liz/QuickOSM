'''
Created on 4 juin 2014

@author: etienne
'''

import urllib2
import urllib
import re
import tempfile

class ConnexionOAPI:
    '''
    Manage connexion to the overpass API
    '''

    def __init__(self,url="http://overpass-api.de/api/", output = None):
        self.__url = url

        if output not in (None, "json","xml"):
            raise Exception, "Output not available"
        self.__output = output
        
    def query(self,req):
        '''
        Make a query to the overpass
        '''
        req = req.encode('utf8')
        urlQuery = self.__url + 'interpreter'
        
        #The output format can be forced (JSON or XML)
        if self.__output:
            req = re.sub(r'output="[a-z]*"','output="'+self.__output+'"', req)
            req = re.sub(r'\[out:[a-z]*','[out:'+self.__output, req)
        
        queryString = urllib.urlencode({'data':req})
        
        try:
            data = urllib2.urlopen(url=urlQuery, data=queryString).read()
        except urllib2.HTTPError as e:
            if e.code == 400:
                raise Exception, "Bad request OverpassAPI"
        #print req 
        result = re.search('<remark> runtime error: Query timed out in "[a-z]+" at line [\d]+ after ([\d]+) seconds. </remark>', data)
        if result:
            result = result.groups()
            #print "Timeout : " + result[0]
            raise Exception, "Timeout OverpassAPI"
            
        return data
            
    def getFileFromQuery(self,req):
        '''
        Make a query to the overpass and put the result in a temp file
        '''
        req = self.query(req)
        tf = tempfile.NamedTemporaryFile(delete=False,suffix=".osm")
        tf.write(req)
        namefile = tf.name
        tf.flush()
        tf.close()
        return namefile
    
    def getTimestamp(self):
        '''
        Get the timestamp of the OSM data on the server
        '''
        urlQuery = self.__url + 'timestamp'
        try:
            return urllib2.urlopen(url=urlQuery).read()
        except urllib2.HTTPError as e:
            if e.code == 400:
                raise Exception, "Bad request OverpassAPI"