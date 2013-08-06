'''
Created on Jun 24, 2013

@author: tel
'''

import numpy as np
from transformable import Transformable

class Vertex(object):
    def __init__(self, x=0, y=0, z=0, d=1):
        self.xyzd = np.array((x, y, z, d))
    
    def Get(self, ndim=2):
        return self.xyzd[0:ndim]
    
    @property
    def xy(self):
        return self.Get()
    
    @property
    def xyz(self):
        return self.Get(3)
    
    def _Trans(self, tmat, garbage):
        self.xyzd = self.xyzd.dot(tmat.transpose())
        
    def _RetTrans(self, tmat):
        return Vertex(*self.xyzd.dot(tmat.transpose()))
    
    def Clean(self):
        pass