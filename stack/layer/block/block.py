'''se
Created on Jun 4, 2013

@author: tel
'''

from prim.prim import Prim
from prim.joint import RoundJoint
from port import Port, Loc
from block_error import *

class Block(Prim):
    def __init__(self, loc=None, prev=None, innum=0, outnum=0, **kwargs):
        self.prev = prev
        self.innum = innum
        self.outnum = outnum
        self.inports = []
        self.outports = []
        if loc!=None:
            self.loc = loc
        elif prev!=None:
            self.loc = self.GetPrevOutport()
        else:
            raise UnpositionedBlockError
        super(Block, self).__init__(**kwargs)
    
    def SetInport(self, v0, v1):
        self.inports.append(Port(self, v0, v1))
    
    def GetInport(self, i=0):
        return self.inports[i]
        
    def SetOutport(self, v0, v1):
        self.outports.append(Port(self, v0, v1))
    
    def GetOutport(self, i=0):
        return self.outports[i]
    
    def GetPrevOutport(self, i=None):
        if i==None:
            i = self.outnum
        return self.prev.GetOutport(i)
    
    def __add__(self, other):
        comboblock = Block()
        joint = other.Joint(self)
        comboblock.hedra = self.hedra + other.hedra.RetTransform(joint.tmat) + joint.mortar
    
    def AddHedra(self, other):
        joint = other.Joint(self)
        return self.hedra + other.hedra.RetTransform(joint.tmat) + joint.mortar
        
    def AddPorts(self, other):
        toutports = self.outports[:]
        tinports = other.inports[:]
        for portlist,portnum in zip((toutports, tinports),(self.outnum, other.innum)):
            try:
                for i in reversed(portnum):
                    portlist.pop(i)
            except TypeError:
                portlist.pop(portnum)
        
        
        
class Channel(Block):
    def __init__(self, length, width, ang, **kwargs):
        super(Channel, self).__init__(**kwargs)
        self.length = length
        self.width = width
        self.ang = ang
        self.Build()
    
    def Build(self):
        self.hedra.make_box(self.length, self.width, 10)
        self.SetInport(0,3)
        self.SetOutport(1,2)
        
    def SetJoint(self):
        self.joint = RoundJoint(self.loc, self.GetInport(self.innum), ang=self.ang)
