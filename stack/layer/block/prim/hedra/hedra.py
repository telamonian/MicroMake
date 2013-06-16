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
        
    def Transform(self, mat):
        '''transform hedra based on a 4x4 matrix'''
        flatmat = [j for i in mat for j in i]
        self.hedra = self.hedra.mult_matrix_4(flatmat)
        
    @staticmethod
    def OverlaySegMat(seg1, seg2):
        '''returns 4x4 transformation matrix that will overlay seg1 on seg2. each seg is a line segment represented by a list of two points'''
        vec1 = np.array(seg1[1]) - np.array(seg1[0])
        vec2 = np.array(seg2[1]) - np.array(seg2[0])
        ang = np.arccos(np.dot(vec1, vec2)/(np.sqrt(np.dot(vec1, vec1))*np.sqrt(np.dot(vec2, vec2))))
        if np.allclose(vec1,vec2):
            axis = (0,0,1)
        else:
            axis = np.cross(vec1, vec2)
        trans = np.array(seg2[0]) - np.array(seg1[0])
        return  translation_matrix(trans).dot(rotation_matrix(ang, axis, point=seg1[0]))
    
    @staticmethod
    def RotatePointMat(ang, pnt, seg1=None, seg2=None):
        '''returns 4x4 transformation matrix that will rotate by ang (in radians) about pnt. 
        line segments seg1 and seg2 may optionally be specified in order to fix the axis of rotation as their cross product.
        each seg is a line segment represented by a list of two points. otherwise, rotation occurs about the z axis'''
        if seg1!=None and seg2!=None:
            vec1 = np.array(seg1[1]) - np.array(seg1[0])
            vec2 = np.array(seg2[1]) - np.array(seg2[0])
            if np.allclose(vec1,vec2):
                axis = (0,0,1)
            else:
                axis = np.cross(vec1, vec2)
        return rotation_matrix(ang, axis, point=pnt)
    
    @staticmethod
    def TranslateMat(pnt1, pnt2):
        '''returns 4x4 transformation matrix that translates from pnt1 to pnt2'''
        vec = np.array(pnt2) - np.array(pnt1)
        return translation_matrix(vec)
    
    @staticmethod
    def Midpoint(seg):
        return (np.array(seg[0]) + np.array(seg[1]))/2
    
    '''
    deprecated methods left in to help with unit testing
    '''
    
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