'''
Created on Jun 16, 2013

@author: tel
'''
import numpy as np

class Port(object):
    def __init__(self, block, v0, v1):
        self.block = block
        self.v0 = v0
        self.v1 = v1
        self._stored_vertices = self.vertices
    
    def Transfer(self, newblock):
        return Port(newblock, self.v0, self.v1)
    
    def Set(self):
        self._stored_vertices = self.vertices
        
    def Recover(self):
        for i,ivertex in enumerate(self._stored_vertices):
            for j,jvertex in enumerate(self.block.hedra.get_vertices()):
                if np.allclose(ivertex, jvertex):
                    self.__setattr__('v%d' % i, j)
                    break
    
    @property
    def vertex_indices(self):
        return np.array((self.v0, self.v1))
    
    @property
    def vertices(self):
        return np.array([self.block.hedra.get_vertex(int(i)) for i in self.vertex_indices])
    
    @property
    def midpoint(self):
        return np.mean(self.vertices, 0)
    
    @property
    def theta(self):
        pass
    
    @property
    def width(self):
        return np.sqrt(np.sum((self.vertices[1] - self.vertices[0])**2))
        
class Loc(Port):
    def __init__(self, pnt0, pnt1):
        self.pnt0 = pnt0
        self.pnt1 = pnt1
    
    @property
    def vertices(self):
        return np.array((self.pnt0, self.pnt1))