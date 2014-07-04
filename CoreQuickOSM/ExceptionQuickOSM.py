'''
Created on 4 juil. 2014

@author: etienne
'''

class QuickOsmException(Exception):
    def __init__(self,msg):
        Exception.__init__(self)
        self.msg = msg

class DirectoryException(Exception):
    def __init__(self, msg):
        QuickOsmException.__init__(self,msg)