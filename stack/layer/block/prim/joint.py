'''
Created on Jun 13, 2013

@author: tel
'''

from hedra.hedra import Hedra
from prim import Cyl

class Joint(Hedra):
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
        
class MidpointTmat(Tmat):
    '''requires ang argument in mixin'ed constructor'''
    def SetTmat(self):
        self.mats.append(self.OverlaySegMat(self.lport.vertices, self.rport.vertices))
        self.mats.append(self.RotatePointMat(self.ang, self.lport.midpoint))
        super(MidpointTmat, self).SetTmat()
        
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
        cyl = Cyl(self.lport.width/2.0, 1)
        cyl.Transform(cyl.CenterAt(self.lport.midpoint))
        self.shapes.append(cyl)
        super(RoundMortar, self).SetMortar()
        
RoundJoint = type('RoundJoint', (Joint, MidpointTmat, RoundMortar), {})