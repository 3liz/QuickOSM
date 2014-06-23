'''
Created on 4 juin 2014

@author: etienne
'''

#from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
import urllib2
import tempfile

class ConnexionXAPI:
    '''
    Manage connexion to the eXtend API (XAPI)
    '''

    def __init__(self,url="api.openstreetmap.fr/xapi?"):
        self.__url = url
        
    def query(self,req):
        '''
        Make a query to the xapi
        '''
        req = req.encode('utf8')
        urlQuery = self.__url + req
        
        print urlQuery
        try:
            data = urllib2.urlopen(url=urlQuery).read()
        except urllib2.HTTPError as e:
            if e.code == 400:
                raise Exception
                #raise GeoAlgorithmExecutionException, "Bad request XAPI"
        
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