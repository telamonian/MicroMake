'''
Created on Jun 4, 2013

@author: tel
'''

from prim.prim import Prim
from prim.joint import Joint
from block_error import *

class Block(Prim):
    def __init__(self, layer, loc=None, prev=None, innum=None, outnum=None, **kwargs):
        self.layer = layer
        self.prev = prev
        self.innum = innum
        self.outnum = outnum
        if loc!=None:
            self.loc = loc
        elif prev!=None:
            self.loc = self.GetPrevOutlet(outnum)
        else:
            raise UnpositionedBlockError
        super(Block, self).__init__(**kwargs)
    
    def GetOutlet(self, i=None):
        if i==None:
            i=0
        return [self.hedra.get_vertex(j) for j in self._outlets[i]]
    
    def GetPrevOutlet(self, i=None):
        return self.prev.GetOutlet(i)
        
    def SetOutlet(self, seg, i=None):
        if i==None:
            i=0
        try:
            self._outlets[i] = seg
        except AttributeError:
            self._outlets = {}
            self._outlets[i] = seg
    
    def GetInlet(self, i=None):
        if i==None:
            i=0
        return [self.hedra.get_vertex(j) for j in self._inlets[i]]
        
    def SetInlet(self, seg, i=None):
        if i==None:
            i=0
        try:
            self._inlets[i] = seg
        except AttributeError:
            self._inlets = {}
            self._inlets[i] = seg
    
class Channel(Block):
    def __init__(self, **kwargs):
        super(Channel, self).__init__(**kwargs)
    
    def Build(self):
        self.hedra.make_box(self.xdim, self.ydim, 1.0)
        self.SetInlet((0,3))
        self.SetOutlet((1,2))    
    
    def Join(self, static, mobile, joint):

