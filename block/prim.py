'''
Created on Jun 4, 2013

@author: tel
'''
import numpy as np

from hedra import Hedra
from transmat import rotation_matrix

class Prim(Hedra):
    def Build():
        pass
    
    
            
class Channel(Prim):
    def __init__(self, xdim, ydim, **kwargs):
        '''
        layer
        loc
        prev
        innum
        outnum
        '''
        super(Channel, self).__init__(**kwargs)
        self.xdim = float(xdim)
        self.ydim = float(ydim)
        self.zpos = self.layer.zpos
        self.Build()
        
    def Build(self):
        self.hedra.make_box(self.xdim, self.ydim, 1.0)
        self.SetInlet((0,3))
        self.SetOutlet((1,2))

    
    