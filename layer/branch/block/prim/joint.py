'''
Created on Jun 13, 2013

@author: tel
'''

from prim import Circ
from transformable.transformable import Transformable

class Joint(Transformable):
    def __init__(self, lport, rport, **kwargs):
        self.lport = lport
        self.rport = rport
        self.mats = []
        self.shapes = []
        for key,val in kwargs.items():
            self.__setattr__(key, val)
        self.SetTmat()
        self.SetMortar()
        

class Tmat(object):
    def SetTmat(self):
        if self.mats!=[]:
            tmat = self.mats[0]
            for mat in self.mats[1:]:
                tmat = mat.dot(tmat)
        else:
            tmat = None
        self.tmat = tmat
        
    def RetTmat(self, mats):
        tmat = mats[0]
        for mat in mats[1:]:
            tmat = mat.dot(tmat)
        return tmat
        
class MidpointTmat(Tmat):
    '''requires ang argument in mixin'ed constructor'''
    def SetTmat(self):
        self.mats.append(self.OverlaySegMat(self.lport.vertices, self.rport.vertices))
        self.mats.append(self.RotatePointMat(self.ang, self.lport.midpoint))
        super(MidpointTmat, self).SetTmat()
        
    def RetTamt(self):
        mats = []
        mats.append(self.OverlaySegMat(self.lport.vertices, self.rport.vertices))
        mats.append(self.RotatePointMat(self.ang, self.lport.midpoint))
        super(MidpointTmat, self).RetTmat(mats)
        
class Mortar(object):
    def SetMortar(self):
        if self.shapes!=[]:
            mortar = self.shapes[0]
            for shape in self.shapes[1:]:
                mortar.Union(shape)
        else:
            mortar = None
        self.mortar = mortar
    
class RoundMortar(Mortar):
    def SetMortar(self):
        circ = Circ(self.lport.width/2.0)
        circ.Transform(circ.CenterAt(self.lport.midpoint))
        self.shapes.append(circ)
        super(RoundMortar, self).SetMortar()
        
RoundJoint = type('RoundJoint', (Joint, MidpointTmat, RoundMortar), {})