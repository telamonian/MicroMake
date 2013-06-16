'''
Created on Jun 13, 2013

@author: tel
'''

from hedra.hedra import Hedra

class Joint(Hedra):
    def __init__(self, inlet, outlet, ang):
        self.inlet = inlet
        self.outlet = outlet
        self.ang = ang
        self.SetTmat()
        self.SetMortar()
    
    def SetTmat(self):
        self.tmat = self.hedra.