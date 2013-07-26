'''
Created on Jun 29, 2013

@author: tel
'''
import unittest, math, cairo 
from layer.branch.branch import Branch
from layer.branch.block.block import Channel, Pinhole, RectTrap
from layer.branch.block.port import Port
from layer.branch.block.prim.transformable.vertex import Vertex

def DrawBranch(branch, fname):
    pnttoum = .002834646
    f = open(fname, 'w')
    surface = cairo.PSSurface(f, 10000, 10000)
    surface.set_device_offset(5000,5000)
    ctx = cairo.Context(surface)
    ctx.scale(pnttoum, pnttoum)
    ctx.set_source_rgb(0, 0, 0)
    for block in branch.blocks + branch.mortars:
        for prim in block.prims:
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
    
def DrawBranches(branches, fname):
    pnttoum = .002834646
    f = open(fname, 'w')
    surface = cairo.PSSurface(f, 10000, 10000)
    surface.set_device_offset(5000,5000)
    ctx = cairo.Context(surface)
    ctx.scale(pnttoum, pnttoum)
    ctx.set_source_rgb(0, 0, 0)
    for branch in branches:
        for block in branch.blocks + branch.mortars:
            for prim in block.prims:
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

class Test(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
#    def testChannel(self):
#        loc = Port((Vertex(200,300,0),Vertex(200,400,0)))
#        blocks = []
#        for i in range(1,100):
#            blocks.append(Channel(length=200+i*100,width=100, ang=(2*math.pi)/7.1))
#        branch = Branch(loc, blocks)
#        branch.Build()
#        DrawBranch(branch,'branch.ps')
        
    def testPinhole(self):
        loc = Channel(10, 100, tmat=Channel.TranslateMat((200,300,0), (200,400,0))).GetOutport()
        inhole = Pinhole(100)
        right = Channel(800, 100)
        down = Channel(2000, 100, ang=(-math.pi/2))
        left = Channel(800, 100, ang=(-math.pi/2))
        outhole = Pinhole(100, out=True)
        blocks = [inhole, right, down, left, outhole]
        branch = Branch(loc, blocks)
        branch.Build()
        DrawBranch(branch,'pinhole.ps')
        
#    def testRectTrap(self):
#        loc = Channel(10, 100, tmat=Channel.TranslateMat((200,300,0), (200,400,0))).GetOutport()
#        inhole = Pinhole(100)
#        right = Channel(800, 100)
#        above = Channel(2000, 100, ang=(-math.pi/2))
#        trap = RectTrap(width=100, rad=200, mwidth=30, mdepth=60, tang=math.pi/6)
#        bellow = Channel(2000, 100)
#        left = Channel(800, 100, ang=(-math.pi/2))
#        outhole = Pinhole(100, out=True)
#        blocks = [inhole, right, above, trap, bellow, left, outhole]
#        branch1 = Branch(loc, blocks)
#        branch1.Build()
#        loc = Channel(10, 100, tmat=Channel.TranslateMat((200,300,0), (200,400,0))).GetOutport()
#        inhole = Pinhole(100)
#        right = Channel(1600, 100)
#        above = Channel(2100, 100, ang=(-math.pi/2))
#        trap = RectTrap(width=100, rad=100, mwidth=30, mdepth=60, tang=2.496)
#        bellow = Channel(2100, 100)
#        left = Channel(1600, 100, ang=(-math.pi/2))
#        outhole = Pinhole(100, out=True)
#        blocks = [inhole, right, above, trap, bellow, left, outhole]
#        branch2 = Branch(loc, blocks)
#        branch2.Build()
#        DrawBranches([branch1, branch2], 'trap.ps')

    def testRectTrap(self):
        loc = Channel(10, 100, tmat=Channel.TranslateMat((0,0,0), (200,400,0))).GetOutport()
        inhole = Pinhole(100)
        right = Channel(800, 100)
        above = Channel(2000, 100, ang=(-math.pi/2))
        trap = RectTrap(width=100, rad=200, mwidth=30, mdepth=60, tang=math.pi/6)
        bellow = Channel(2000, 100)
        left = Channel(800, 100, ang=(-math.pi/2))
        outhole = Pinhole(100, out=True)
        blocks = [inhole, right, above, trap, bellow, left, outhole]
        branch1 = Branch(loc, blocks)
        #branch2 = branch1.RetTrans(Branch.TranslateMat((0,0,0),(0,0,0)))
        branch1.Build()
        
        #branch2.Build()

        DrawBranches([branch1], 'trap.ps')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()