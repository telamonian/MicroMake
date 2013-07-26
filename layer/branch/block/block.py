'''se
Created on Jun 4, 2013

@author: tel
'''
import numpy as np
import math
from copy import deepcopy
from collections import namedtuple

from prim.prim import Prim, Rect, Ngon, Circ
from prim.transformable.vertex import Vertex
from prim.transformable.transformable import Transformable
from port import Port, MidPort
from block_error import *

Joint = namedtuple('Joint', 'tmat, mortar')

class Block(Transformable):
    def __init__(self, props, inspec=None, outspec=None, innum=0, outnum=0, tmat=None, join='Round', **kwargs):
        self.prims = []
        self.props = props
        for key in kwargs:
            self.props[key] = kwargs[key]
        self.inspec = inspec
        self.outspec = outspec
        self.innum = innum
        self.outnum = outnum
        if tmat==None:
            self.tmat = np.identity(4)
        else:
            self.tmat = tmat
        self.join = join
        self.placed = False
        self.go = False
    
    def Go(self):
        self.go = True
        self.InitPorts()
    
    def InitPorts(self):
        self.inports = []
        self.outports = []
        for spec,func in zip((self.inspec, self.outspec),(self.SetInport, self.SetOutport)):
            if spec==None:
                func()
            else:
                for ptups in spec:
                    func(ptups)
    
    def SetInport(self, ptups):
        vecs = []
        for ptup in ptups:
            vecs.append(self.prims[ptup[0]].vertices[ptup[1]])
        self.inports.append(Port(vecs))
    
    def GetInport(self, i=0):
        return self.inports[i]
        
    def SetOutport(self, ptups):
        vecs = []
        for ptup in ptups:
            vecs.append(self.prims[ptup[0]].vertices[ptup[1]])
        self.outports.append(Port(vecs))
    
    def GetOutport(self, i=0):
        return self.outports[i]
    
    def GetPrevOutport(self, i=None):
        if i==None:
            i = self.outnum
        return self.prev.GetOutport(i)
    
    def Join(self, prev):
        join = self.__getattribute__(self.join)
        joint = Joint(*join(prev))
        self.Trans(joint.tmat)
        self.mortar = joint.mortar
        
    def Round(self, prev):
        outport = prev.GetOutport(self.outnum)
        inport = self.GetInport(self.innum)
        try:
            ang = self.props['ang']
        except KeyError:
            ang = 0
        tmat = inport.MidpointRotate(outport, ang=ang).dot(inport.Overlay(outport))
        try:
            width = prev.props['width']
        except AttributeError:
            width = prev.width
        mortar = RoundJoint(width/2)
        mortar.Go()
        for prim in mortar.prims:
            prim.SelfTrans()
        mtmat = mortar.GetInport().OverlayMidpoint(outport)
        mortar.Trans(mtmat)
        return tmat, mortar.prims[0]
    
    def Place(self, seg):
        self.placed = True
        self.Go()
        segport = Port([Vertex(*pnt) for pnt in seg])
        tmat = self.GetInport(self.innum).Overlay(segport)
        for prim in self.prims:
            prim.SelfTrans()
        self.Trans(tmat)
    
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
    
    def GetPrimCentroids(self, primtrans=False):
        return [prim.GetCentroid(primtrans) for prim in self.prims]
    
    def GetCentroid(self, primtrans=False):
        return np.mean(self.GetPrimCentroids(primtrans), 0)
    
    @property
    def children(self):
        return self.prims
    
class Channel(Block):
    def __init__(self, length, width, **kwargs):
        props = {'length':length, 'width':width}
        inspec = [((0,0),(0,1))]
        outspec = [((0,3),(0,2))]
        super(Channel, self).__init__(props, inspec, outspec, **kwargs)

    def Go(self):
        length = self.props['length']
        width = self.props['width']
        self.prims = [Rect(length, width)]
        super(Channel, self).Go()
        
class Split(Block):
    def __init__(self, width, length, sang=math.pi/3, **kwargs):
        props = {'length':length, 'width':width, 'sang':sang}
        inspec = [((0,0),(0,1))]
        outspec = [((1,1),(1,0)), 
                   ((2,1),(2,0))]
        super(Split, self).__init__(props, inspec, outspec, **kwargs)
        
    def Go(self):
        length = self.props['length']
        width = self.props['width']
        sang = self.props['sang']
        '''initialize necessary prims'''
        trib = Rect(length, width)
        dist0 = trib.Copy()
        dist1 = trib.Copy()
        '''using chamber as the central shape, generate and assign tmats'''
        cen = Prim.Midpoint([trib.GetVertex(2).xyz, trib.GetVertex(3).xyz])
        dist0.tmat = Prim.RotatePointMat(math.pi - sang/2, cen)
        dist1.tmat = Prim.RotatePointMat(math.pi + sang/2, cen)
        '''standard prim setup'''
        self.prims = [trib, dist0, dist1]
        super(Split, self).Go()

class Pinhole(Block):
    def __init__(self, width, rad=400, out=False, **kwargs):
        props = {'width':width, 'rad':rad, 'out':out}
        inspec = [((1,0),(1,1))]
        outspec = [((1,3),(1,2))]
        if out:
            inspec,outspec = [pspec[::-1] for pspec in outspec],[pspec[::-1] for pspec in inspec]
        super(Pinhole, self).__init__(props, inspec, outspec, **kwargs)
        
    def Go(self):
        rad = self.props['rad']
        width = self.props['width']
        self.prims = [Circ(rad), 
                 Rect(rad+2*width, width, tmat=Rect.TranslateMat((0,width/2,0), (rad,rad,0)))]
        super(Pinhole, self).Go()

class RoundJoint(Block):
    def __init__(self, rad, **kwargs):
        props = {'rad':rad}
        super(RoundJoint, self).__init__(props, **kwargs)
        
    def Go(self):
        rad = self.props['rad']
        self.prims = [Circ(rad)]
        super(RoundJoint, self).Go()
        
    def SetInport(self):
        self.inports.append(MidPort(self))
    
    def SetOutport(self):
        self.outports.append(MidPort(self))
        
class HexWell(Block):
    def __init__(self, width, rad=400, cmult=3, **kwargs):
        props = {'width':width, 'rad':rad, 'cmult':cmult}
        inspec = [((0,1),(0,0)),
                   ((1,1),(1,0)), 
                   ((2,1),(2,0)), 
                   ((0,2),(0,3)),
                   ((1,2),(1,3)),
                   ((2,2),(2,3))]
        outspec = [((0,1),(0,0)),
                   ((1,1),(1,0)), 
                   ((2,1),(2,0)), 
                   ((0,2),(0,3)),
                   ((1,2),(1,3)),
                   ((2,2),(2,3))]
        super(HexWell, self).__init__(props, inspec, outspec, **kwargs)
        
    def Go(self):
        rad = self.props['rad']
        width = self.props['width']
        cmult = self.props['cmult']

        '''initialize prims'''
        chan0 = Rect(cmult*rad, width)
        chan1 = chan0.Copy()
        chan2 = chan0.Copy()
        well = Ngon(rad, 6)
        '''using well as the central shape, generate and assign tmats'''
        cen = Vertex(*well.GetCentroid())
        for i,chan in enumerate((chan0, chan1, chan2)):
            chan.tmat = Prim.RotatePointMat((.5 + i/3.0)*math.pi, cen.xyz).dot(Prim.TranslateMat(chan.GetCentroid()[0:3], cen.xyz))
        '''standard prim setup'''
        self.prims = [chan0, chan1, chan2, well]
        super(HexWell, self).Go()
        
class RectTrap(Block):
    def __init__(self, width, rad, mwidth, mdepth, tang=0, **kwargs):
        props = {'width':width, 'rad':rad, 'mwidth':mwidth, 'mdepth':mdepth, 'tang':tang}
        inspec = [((0,0),(0,1))]
        outspec = [((0,3),(0,2))]
        super(RectTrap, self).__init__(props, inspec, outspec, **kwargs)
        
    def Go(self):
        rad = self.props['rad']
        width = self.props['width']
        mwidth = self.props['mwidth']
        mdepth = self.props['mdepth']
        tang = self.props['tang']
        
        '''initialize necessary prims'''
        chan = Rect(2*rad, width)
        chamber = Circ(rad)
        trap = Rect(np.sin(math.pi/4)*rad, np.sin(math.pi/4)*rad)
        trap.neg = True
        mouth = Rect(mwidth, mdepth)
        '''using chamber as the central shape, generate and assign tmats'''
        cen = Vertex(*chamber.GetCentroid(True))
        chan.tmat = Prim.RotatePointMat(math.pi/2, cen.xyz).dot(Prim.TranslateMat(chan.GetCentroid()[0:3], cen.xyz))
        trap.tmat = Prim.TranslateMat(trap.GetCentroid()[0:3], cen.xyz)
        midpoint_mouth_top = Prim.Midpoint([mouth.vertices[1].xyz, mouth.vertices[2].xyz])
        midpoint_trap_top = Prim.Midpoint([trap.GetVertex(1, True).xyz, trap.GetVertex(2, True).xyz])
        mouth.tmat = Prim.TranslateMat(midpoint_mouth_top, midpoint_trap_top)
        traprot = Prim.RotatePointMat(tang, cen.xyz)
        trap.tmat = traprot.dot(trap.tmat)
        mouth.tmat = traprot.dot(mouth.tmat)
        '''standard prim setup'''
        self.prims = [chan, chamber, trap, mouth]
        super(RectTrap, self).Go()