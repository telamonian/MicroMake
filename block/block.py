'''
Created on Jun 4, 2013

@author: tel
'''

import pyPolyCSG as csg

from block_error import *

class Block(object):
    def __init__(self, layer, prims, loc=None, prev=None):
        self.layer = layer
        if loc!=None:
            self.inlet = loc
        elif prev!=None:
            self.inlet = layer.GetBlock(prev.name).GetOutlet(prev.outlet_name)
        else:
            raise UnpositionedBlockError
        if prev!=None:
            self.prev = layer.GetBlock(prev.name)
        self.prims = prims
        self.Build()
    
    def Build(self):
        pass
    
    