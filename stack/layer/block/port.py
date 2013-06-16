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
        
    def Set(self):
        self._stored_vertices = self.vertices
        
    def Recover(self):
        for i,ivertex in enumerate(self._stored_vertices):
            for j,jvertex in enumerate(self.hedra.get_vertices()):
                if np.allclose(ivertex, jvertex):
                    self.__setattr__('v%d' % i, j)
                    break
    
    @property
    def vertex_indices(self):
        return np.array((self.v0, self.v1))
    
    @property
    def vertices(self):
        return np.array([self.hedra.get_vertex(i) for i in self.vertex_indices])
    
    @property
    def midpoint(self):
        return np.mean(self.vertices, 0)