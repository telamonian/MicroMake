'''
Created on Jun 5, 2013

@author: tel
'''
import numpy as np
import pyPolyCSG as csg

from hedra_error import UnpositionedHedraError
from transmat import rotation_matrix, translation_matrix

class Hedra(object):
    def __init__(self, layer, loc=None, prev=None, innum=None, outnum=None):
        self.hedra = csg.polyhedron()
        self.layer = layer
        self.prev = prev
        self.innum = innum
        self.outnum = outnum
        if loc!=None:
            self.loc = loc
        elif prev!=None:
            self.loc = self.GetPrevOutlet(outnum)
        else:
            raise UnpositionedHedrasError
    
    def Union(self, other):
        '''union of two hedra'''
        self.hedra = self.hedra + other.hedra

    def Diff(self, other):
        '''difference of two hedra'''
        self.hedra = self.hedra - other.hedra
        
    def SymDiff(self, other):
        '''symmetric difference of two hedra
        equivalent to the difference of the union and the intersection'''
        self.hedra = self.hedra ^ other.hedra
        
    def Intersect(self, other):
        '''intersection of two hedra'''
        self.hedra = self.hedra * other.hedra
        
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
            
    @property
    def curzpos(self):
        return self.GetInlet()[0][2]
    
    def Level(self):
        zmov = self.zpos - self.curzpos
        self.hedra = self.hedra.translate(0,0,zmov)
    
    def SegToSeg(self, seg1, seg2, offang=0):
        '''define a transformation based on moving one line segment to overlap with another, then apply it'''
        tmat = [a for b in Hedra.SegTransform(seg1, seg2, offang).tolist() for a in b]  #format transformation matrix as flat row-major list
        self.hedra = self.hedra.mult_matrix_4(tmat)
    
    def MoveToPos(self, inletnum=None, offang=0):
        '''position self based on line seg in self.loc'''
        try:
            self.SegToSeg(self.GetInlet(inletnum), self.GetPrevOutlet(self.outnum), offang)
        except AttributeError:
            self.SegToSeg(self.GetInlet(inletnum), self.loc, offang)
    
    @staticmethod
    def SegTransform(seg1, seg2, offang=0):
        vec1 = np.array(seg1[1]) - np.array(seg1[0])
        vec2 = np.array(seg2[1]) - np.array(seg2[0])
        ang = np.arccos(np.dot(vec1, vec2)/(np.sqrt(np.dot(vec1, vec1))*np.sqrt(np.dot(vec2, vec2))))
        if np.allclose(vec1,vec2):
            axis = (0,0,1)
        else:
            axis = np.cross(vec1, vec2)
        trans = np.array(seg2[0]) - np.array(seg1[0])
        #perpunittrans = .1*(np.array((-vec2[1],vec2[0],vec2[2]))/(np.sqrt(np.sum(vec2**2))))
        return rotation_matrix(offang, axis, point=Hedra.Midpoint(seg2)).dot(translation_matrix(trans)).dot(rotation_matrix(ang, axis, point=seg1[0]))#.dot(translation_matrix(perpunittrans))
    
    @staticmethod
    def Midpoint(seg):
        return (np.array(seg[0]) + np.array(seg[1]))/2