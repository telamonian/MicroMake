'''
Created on Jun 4, 2013

@author: tel
'''
import numpy as np

from hedra import Hedra
from hedra_error import UnpositionedPrimError
from transmat import rotation_matrix

class Prim(Hedra):
    def Build():
        pass
        
class Channel(Prim):
    def __init__(self, xdim, ydim, **kwargs):
        super(Channel, self).__init__(**kwargs)
        self.xdim = float(xdim)
        self.ydim = float(ydim)
        self.zpos = self.layer.zpos
    
    def Build(self):
        self.hedra.box(self.xdim, self.ydim, 1.0)
        verts = self.hedra.get_vertices().tolist()
        self.inlets[0] = (verts[0],verts[3])
        self.outlets[0] = (verts[1],verts[2])
        self.SegToSeg(self.inlets[0], self.loc)
        
    def Join(self, soutlet_name, other, ooutlet_name):
        pass