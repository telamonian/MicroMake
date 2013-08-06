'''
Created on Jun 27, 2013

@author: tel
'''
from copy import deepcopy
import numpy as np
from collections import namedtuple
from clipper import Point, Clipper, PolyType, ClipType, PolyFillType
from block.block import Channel, RoundJoint
from block.prim.transformable.transformable import Transformable

class Branch(Transformable):
    name = 'Branch'
    
    def __init__(self, blocks, join='Round', tmat=None, noprev=False):
        self.blocks = blocks
        self.mortars = []
        self.join = 'Round'
        if tmat==None:
            self.tmat = np.identity(4)
        else:
            self.tmat = tmat
        #flag for branches whose first block is not part of another branch
        self.noprev = noprev
    
    def Copy(self):
        tmp = super(Branch, self).Copy()
        tmp.blocks[0] = self.blocks[0]
        return tmp
    
    def Build(self):
        join = self.__getattribute__(self.join)
        joint = Branch.Joint(*join(self.blocks[0], self.initport))
        self.blocks[0].Trans(joint.tmat)
        self.mortars.append(joint.mortar)
        for i,block in enumerate(self.blocks[1:]):
            joint = Branch.Joint(*join(block, self.blocks[i]))
            block.Trans(joint.tmat)
            self.mortars.append(joint.mortar)
        
    def GetInport(self, i=0):
        return self.blocks[0].GetInport(i)
    
    def GetOutport(self, i=0):
        return self.blocks[-1].GetOutport(i)
    
    @property
    def children(self):
        return self.blocks