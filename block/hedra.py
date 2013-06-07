'''
Created on Jun 5, 2013

@author: tel
'''
import numpy as np
import pyPolyCSG as csg

from hedra_error import UnpositionedHedraError
from transmat import rotation_matrix, translation_matrix

class Hedra(object):
    def __init__(self, layer, loc=None, prev=None, outnum=None):
        self.hedra = csg.polyhedron()
        self.layer = layer
        self.prev = prev
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
        
    def SegToSeg(self, seg1, seg2):
        '''define a transformation based on moving one line segment to overlap with another, then apply it'''
        tmat = [a for b in Hedra.SegTransform(seg1, seg2).tolist() for a in b]  #format transformation matrix as flat row-major list
        self.hedra = self.hedra.mult_matrix_4(tmat)
    
    def Position(self, inletnum=None):
        '''position self based on line seg in self.loc'''
        self.SegToSeg(self.GetInlet(inletnum), self.GetPrevOutlet(self.outnum))
    
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
    
    @staticmethod
    def SegTransform(seg1, seg2):
        vec1 = seg1[1] - seg1[0]
        vec2 = seg2[1] - seg2[0]
        ang = np.arccos(np.dot(vec1, vec2)/(np.sqrt(np.dot(vec1, vec1))*np.sqrt(np.dot(vec2, vec2))))
        return translation_matrix(seg2[0] - seg1[0])*rotation_matrix(ang, np.cross(vec1, vec2), point=seg1[0])