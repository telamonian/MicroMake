'''
Created on Jun 4, 2013

@author: tel
'''
import numpy as np
import math
from copy import deepcopy
from transformable.transformable import Transformable
from transformable.vertex import Vertex

class Prim(Transformable):
    def __init__(self, pnts, tmat=None):
        if tmat==None:
            self.tmat = np.identity(4)
        else:
            self.tmat = tmat
        self.neg = False
        self.vertices = []
        for pnt in pnts:
            self.vertices.append(Vertex(*pnt))
    
    def GetVertex(self, i, primtrans=False):
        if primtrans:
            return self.vertices[i]._RetTrans(self.tmat)
        else:
            return self.vertices[i]
    
    def GetVertices(self, primtrans=False):
        ret = []
        for i in range(len(self.vertices)):
            ret.append(self.GetVertex(i, primtrans))
        return ret
    
    def Level(self):
        zmov = self.zpos - self.curzpos
        self.hedra = self.hedra.translate(0,0,zmov)

    def CenterAt(self, pnt, centroid3d=False):
        '''translates self.vertices so that their centroid coincides with pnt'''
        return self.TranslateMat(self.centroid, pnt)
    
    def GetCentroid(self, primtrans=False):
        return np.mean(self.GetVertexCoords(primtrans), 0)
    
    def GetVertexCoords(self, primtrans=True):
        return [vertex.xyzd for vertex in self.GetVertices(primtrans)]
    
    @property
    def children(self):
        return self.vertices
    
    @property
    def curzpos(self):
        return self.GetCentroid()[2]
    
class Rect(Prim):
    def __init__(self, xdim, ydim, **kwargs):
        self.xdim = xdim
        self.ydim = ydim
        pnts=[(0,0),(0,ydim),(xdim,ydim),(xdim,0)]
        super(Rect, self).__init__(pnts, **kwargs)
        
class Ngon(Prim):
    def __init__(self, rad, sides=6, **kwargs):
        self.rad = rad
        self.sides = sides
        pnts = []
        #adding bump to all angles ensures that the 'bottom' of the polygon is paralle to the x-axis
        bump = math.pi*(1.0/sides - .5)
        for i in range(sides):
            pnts.append((rad*np.cos(bump + i*2.0*math.pi/sides), rad*np.sin(bump + i*2.0*math.pi/sides)))
        super(Ngon, self).__init__(pnts, **kwargs)
        
class Circ(Prim):
    def __init__(self, rad, prec=200, **kwargs):
        self.rad = rad
        self.prec = prec
        try:
            tmat = tmat.dot(Circ.TranslateMat((0,0,0),(rad,rad,0)))
        except NameError:
            tmat = Circ.TranslateMat((0,0,0),(rad,rad,0))
        pnts = []
        for i in range(prec):
            pnts.append((rad*np.cos(i*2.0*math.pi/prec), rad*np.sin(i*2.0*math.pi/prec)))
        super(Circ, self).__init__(pnts, tmat=tmat, **kwargs)