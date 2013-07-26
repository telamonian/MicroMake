'''
Created on Jun 16, 2013

@author: tel
'''
import numpy as np
from prim.transformable.transformable import Transformable
from prim.transformable.vertex import Vertex

class Port(Transformable):
    def __init__(self, vertices):
        self.vertices = vertices
        
    def Overlay(self, other):
        return self.OverlaySegMat((self.GetVertex(0).xyz, self.GetVertex(-1).xyz), (other.GetVertex(0).xyz, other.GetVertex(-1).xyz))
    
    def MidpointRotate(self, other, ang):
        return self.RotatePointMat(ang, other.GetMidpoint())
    
    def OverlayMidpoint(self, other):
        return self.TranslateMat(self.GetMidpoint(), other.GetMidpoint())
    
    def GetVertex(self, i):
        return self.vertices[i]
    
    def GetVertices(self):
        return self.vertices
    
    def GetMidpoint(self):
        return np.mean(self.GetVertexCoords(), 0)
    
    def GetVertexCoords(self):
        return [vertex.xyzd for vertex in self.GetVertices()]
    
    @property
    def theta(self):
        pass
    
    @property
    def width(self):
        return np.sqrt(np.sum((self.GetVertex(-1).xyz - self.GetVertex(0).xyz)**2))

class MidPort(Port):
    def __init__(self, prim):
        self.prim = prim

    def GetVertices(self):
        return [Vertex(*self.prim.GetCentroid())]