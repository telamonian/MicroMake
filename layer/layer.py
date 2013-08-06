'''
Created on Jul 18, 2013

@author: tel
'''
import cairo
import numpy as np
from branch.block.prim.transformable.transformable import Transformable

class Layer(Transformable):
    name = 'Layer'
    
    def __init__(self, branches=None, tmat=None):
        if branches==None:
            self.branches = []
        else:
            self.branches = branches
        if tmat==None:
            self.tmat = np.identity(4)
        else:
            self.tmat = tmat
    
    def AddBranch(self, branch):
        self.branches.append(branch)
        
    def AddBranches(self, branches):
        for branch in branches:
            self.AddBranch(branch)
    
    def Build(self):
        #position all of the primitives wrt their blocks
        for branch in self.branches:
            for block in branch.blocks:
                if not block.go:
                    block.Go()
                for prim in block.prims:
                    if prim.transformed==False:
                        prim.SelfTrans()
        #join together all the blocks that should be joined
        for branch in self.branches:
            for prev, block in zip(branch.blocks[:-1], branch.blocks[1:]):
                if block.transformed==False:
                    block.Join(prev)
        #apply optional branch transform
        for branch in self.branches:
            if branch.transformed==False:
                branch.SelfTrans()
        #apply optional layer transform
        if self.transformed==False:
            self.SelfTrans()
    
    def Draw(self, fname, *args):
        pnttoum = .002834646
        f = open(fname, 'w')
        surface = cairo.PSSurface(f, 10000, 10000)
        surface.set_device_offset(4000,4000)
        ctx = cairo.Context(surface)
        ctx.scale(pnttoum, pnttoum)
        ctx.set_source_rgb(0, 0, 0)
        for layer in [self] + list(args):
            for branch in layer.branches:
                if branch.blocks[0].placed:
                    blocks = branch.blocks
                else: 
                    blocks = branch.blocks[1:]
                for block in blocks:
                    for prim in block.children:
                        if prim.neg:
                            ctx.set_source_rgb(255,255,255)
                        else:
                            ctx.set_source_rgb(0,0,0)
                        ctx.move_to(*prim.GetVertexCoords(False)[0][0:2])
                        for pnt in prim.GetVertexCoords(False):
                            ctx.line_to(*pnt[0:2])
                        ctx.close_path()
                        ctx.fill()
                        ctx.set_line_width(.01)
                        ctx.stroke()
        surface.flush()
        surface.finish()
        f.close()
    
    @property
    def children(self):
        return self.branches