'''
Created on Jun 5, 2013

@author: tel
'''
import numpy as np
import pyPolyCSG as csg

from transmat import rotation_matrix, translation_matrix

class Hedra(object):
    def __init__(self):
        self.hedra = csg.polyhedron()
    
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
        
    @staticmethod
    def SegTransform(seg1, seg2):
        vec1 = seg1[1] - seg1[0]
        vec2 = seg2[1] - seg2[0]
        ang = np.arccos(np.dot(vec1, vec2)/(np.sqrt(np.dot(vec1, vec1))*np.sqrt(np.dot(vec2, vec2))))
        return translation_matrix(seg2[0] - seg1[0])*rotation_matrix(ang, np.cross(vec1, vec2), point=seg1[0])