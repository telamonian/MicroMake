'''
Created on Jun 5, 2013

@author: tel
'''
import pyPolyCSG as csg

class Hedra(object):
    def __init__(self):
        self.hedra = csg.polyhedron()
    
    def Union(self, other):
        self.hedra = self.hedra + other.hedra

    def Diff(self, other):
        self.hedra = self.hedra - other.hedra
        
    def SymDiff(self, other):
        self.hedra = self.hedra ^ other.hedra
        
    def Intersect(self, other):
        self.hedra = self.hedra * other.hedra