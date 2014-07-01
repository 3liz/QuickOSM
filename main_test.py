'''
Created on 20 juin 2014

@author: etienne
'''

from CoreQuickOSM.QueryFactory import QueryFactory

if __name__ == '__main__':
    queryFactory = QueryFactory(key = 'ref:INSEE', value='25047', osmObjects=['relation'])
    print queryFactory.make()