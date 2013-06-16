'''
Created on Jun 4, 2013

@author: tel
'''
import numpy as np

from hedra.hedra import Hedra

class Prim(Hedra):
    '''all derived classes will require a self.botface attribute'''
    botface = None
    
    def Build(self):
        pass
    
    def Level(self):
        zmov = self.zpos - self.curzpos
        self.hedra = self.hedra.translate(0,0,zmov)
    
    def GetCentroid(self, centroid3d=False):
        '''returns the centroid of self.hedra. if centroid3d is true, centroid is based on all vertices in three dimensions.
        otherwise, centroid is determined based on bottom face'''
        if centroid3d:
            return np.mean(self.hedra.get_vertices(), 0)
        else:
            return np.mean([self.hedra.get_vertex(v) for v in self.hedra.get_face(self.botface)], 0)
    
    def CenterAt(self, pnt, centroid3d=False):
        '''translates self.hedra so that its centroid coincides with pnt'''
        return self.TranslateMat(self.GetCentroid(), pnt)
    
    @property
    def curzpos(self):
        return self.GetCentroid()[2]
    
class Rect(Prim):
    botface = 2
    def __init__(self, xdim, ydim, **kwargs):
        super(Rect, self).__init__(**kwargs)
        self.xdim = float(xdim)
        self.ydim = float(ydim)
        self.zpos = self.layer.zpos
        self.Build()
        
    def Build(self):
        self.hedra.make_box(self.xdim, self.ydim, 1.0)
        self.SetInlet((0,3))
        self.SetOutlet((1,2))