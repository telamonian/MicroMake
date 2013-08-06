'''
Created on Jun 24, 2013

@author: tel
'''
import math
import numpy as np
from copy import deepcopy
from transmat import rotation_matrix, translation_matrix

class Transformable(object):
    transformed = False
    Prim_transformed = False
    Block_transformed = False
    Branch_transformed = False
    Layer_transformed = False
    
    def _Trans(self, tmat, tmat_owner):
        if not self.__getattribute__(tmat_owner):
            self.__setattr__(tmat_owner, True)
            for child in self.children:
                child._Trans(tmat, tmat_owner)
    
    def _RetTrans(self, tmat):
        newb = deepcopy(self)
        newb._Trans(tmat)
        return newb
    
    def Trans(self, tmat):
        self._Trans(tmat, self.name + '_transformed')
            
    def RetTrans(self, tmat):
        return self._RetTrans(tmat)
    
    def SelfTrans(self):
        self._Trans(self.tmat,  self.name + '_transformed')
        
    def SelfRetTrans(self):
        self._RetTrans(self.tmat)
        
    def Copy(self):
        tmp = deepcopy(self)
        tmp.CleanRec()
        return tmp
    
    def Clean(self):
        self.transformed = False
        self.Prim_transformed = False
        self.Block_transformed = False
        self.Branch_transformed = False
        self.Layer_transformed = False
        
    def CleanRec(self):
        self.Clean()
        for child in self.children:
            child.Clean()
    
    @property
    def children(self):
        pass
    
    @staticmethod
    def OverlaySegMat(seg0, seg1):
        '''returns 4x4 transformation matrix that will overlay seg0 on seg1. each seg is a line segment represented by a list of two points'''
        vec0 = np.array(seg0[1]) - np.array(seg0[0])
        vec1 = np.array(seg1[1]) - np.array(seg1[0])
        axis = np.cross(vec0, vec1)
        if np.allclose([0,0,0],axis):
            axis = (0,0,1)
        if np.allclose(vec0,vec1):
            ang = 0
        elif np.allclose(vec0,-vec1):
            ang = math.pi
        else:
            ang = np.arccos(np.dot(vec0, vec1)/(np.sqrt(np.dot(vec0, vec0))*np.sqrt(np.dot(vec1, vec1))))
#        if np.isnan(ang):
#            ang = math.pi
        trans = np.array(seg1[0]) - np.array(seg0[0])
        return translation_matrix(trans).dot(rotation_matrix(ang, axis, point=seg0[0]))
    
    @staticmethod
    def RotatePointMat(ang, pnt, seg1=None, seg2=None):
        '''returns 4x4 transformation matrix that will rotate by ang (in radians) about pnt. 
        line segments seg1 and seg2 may optionally be specified in order to fix the axis of rotation as their cross product.
        each seg is a line segment represented by a list of two points. otherwise, rotation occurs about the z axis'''
        if seg1!=None and seg2!=None:
            vec1 = np.array(seg1[1]) - np.array(seg1[0])
            vec2 = np.array(seg2[1]) - np.array(seg2[0])
            if np.allclose(vec1,vec2):
                axis = (0,0,-1)
            else:
                axis = np.cross(vec1, vec2)
        else:
            axis = (0,0,-1)
        return rotation_matrix(ang, axis, point=pnt)
    
    @staticmethod
    def TranslateMat(pnt0, pnt1):
        '''returns 4x4 transformation matrix that translates from pnt0 to pnt1'''
        vec = np.array(pnt1) - np.array(pnt0)
        return translation_matrix(vec)
    
    @staticmethod
    def Midpoint(seg):
        return (np.array(seg[0]) + np.array(seg[1]))/2