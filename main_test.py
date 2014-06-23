'''
Created on 20 juin 2014

@author: etienne
'''

#from Core.ConnexionXAPI import ConnexionXAPI

def myfunc(a=None,b=None,c=None, d='d'):
    print a
    print b
    print c
    print d


if __name__ == '__main__':
    #connexion = ConnexionXAPI("http://www.overpass-api.de/api/xapi?")
    #req = "relation[ref:INSEE=25047]"
    #print connexion.query(req)
    myfunc(d='tata')