'''
Created on Jul 24, 2013

@author: tel
'''
import unittest, math
import numpy as np

from layer.layer import Layer
from layer.branch.branch import Branch
from layer.branch.block.block import Channel, Pinhole, HexWell, RectTrap, Split

class Test(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def testRectTrap(self):
        testRectTrap(self)
        
    def testHexWell(self):
        testHexWell(self)
    
    def testSplitTraps(self):
        testSplitTraps(self)
    
    def testHexHex(self):
        testHexHex(self)

def testRectTrap(self=True):
    lay = Layer()
    
    inhole = Pinhole(width=100)
    right = Channel(length=800, width=100)
    above = Channel(length=2000, width=100, ang=(-math.pi/2))
    trap = RectTrap(width=100, rad=200, mwidth=30, mdepth=60, tang=math.pi/6)
    below = Channel(length=2000, width=100)
    left = Channel(length=800, width=100, ang=(-math.pi/2))
    outhole = Pinhole(width=100, out=True)
    blocks = [inhole, right, above, trap, below, left, outhole]
    branch = Branch(blocks)
    
    lay.AddBranch(branch)
    
    inhole.Place(((0,0,0),(0,100,0)))
    lay.Build()
    lay.Draw('layer_trap.ps')

def testHexWell(self=True):
    lay = Layer()
    
    inhole = Pinhole(width=100)
    right = Channel(length=800, width=100)
    above = Channel(length=736, width=100, ang=(-math.pi/3))
    hexwell = HexWell(width=100, ang=2*math.pi/3)
    below = Channel(length=1500, width=100, ang=3*math.pi/2, outnum=3)
    left = Channel(length=800, width=100, ang=(-math.pi/3))
    outhole = Pinhole(width=100, out=True)
    blocks = [inhole, right, above, hexwell, below, left, outhole]
    branch = Branch(blocks)
    
    lay.AddBranch(branch)
    
    inhole.Place(((0,0,0),(0,100,0)))
    lay.Build()
    lay.Draw('layer_hexwell.ps')
    
def testSplitTraps(self=True):
    width = 100
    lay0 = Layer()
    
    inhole = Pinhole(width=width)
    right = Channel(length=4000, width=width)
    split0 = Split(width=width, length=2500, ang=-math.pi/2)
    split1 = Split(width=width, length=1250, ang=math.pi/6)
    split2 = Split(width=width, length=600, ang=math.pi/6)
    
    blocks = [inhole, right, split0, split1, split2]
    top0 = Branch(blocks)
    
    split3 = split2.Copy()
    split3.outnum = 1
    split3.props['ang'] = -math.pi/6
    
    blocks = [split1, split3]
    top1 = Branch(blocks)
    
    split4 = split1.Copy()
    split4.outnum = 1
    split4.props['ang'] = -math.pi/6
    split5 = split2.Copy()
    
    blocks = [split0, split4, split5]
    top2 = Branch(blocks)
    
    split6 = split3.Copy()
    
    blocks = [split4, split6]
    top3 = Branch(blocks)
    
    above = Channel(length=2000, width=width, ang=math.pi/6)
    trap = RectTrap(width=width, rad=200, mwidth=30, mdepth=60, tang=2*math.pi/9)
    below = Channel(length=400, width=width)
    ditch = Channel(length=400, width=width, ang=math.pi/6)
    
    blocks = [split2, above, trap, below, ditch]
    trap0 = Branch(blocks)
    
    trap1 = trap0.Copy()
    trap1.blocks[1].outnum = 1
    trap1.blocks[1].props['ang'] = -math.pi/6
    trap1.blocks[2].props['tang'] = 4*math.pi/9
    
    extra_traps = []
    for i, split in enumerate([split3, split5, split6]):
        for j, t in enumerate([trap0, trap1]):
            tmp = t.Copy()
            tmp.blocks[0] = split
            tmp.blocks[2].props['tang'] = 2*(i*2+j+3)*math.pi/9
            extra_traps.append(tmp)
            
    left = Channel(length=6000, width=width, ang=(math.pi/3))
    outhole = Pinhole(width=width, out=True)
    
    blocks = [ditch, left, outhole]
    bottom = Branch(blocks)
    
    branches = [top0, top1, top2, top3, trap0, trap1] + extra_traps + [bottom]
    lay0.AddBranches(branches)
    
    inhole.Place(((0,0,0),(0,100,0)))
    lay0.Build()
    
#    lay1 = lay0.Copy()
#    lay1.Trans(Layer.RotatePointMat(math.pi/2, (4000,10000,0)))
    
    lay0.Draw('layer_splittraps.ps')

hexmoves = {0:[4,1],1:[3,0],2:[2,5],3:[1,4],4:[0,3],5:[5,2]}

def testHexHex(self=True):
    lay = Layer()
    perside = 20
    rad = 400
    cmult = 3
    width = 100
    hexchanwidth = 10
    
    first = HexWell(width=hexchanwidth, rad=rad, cmult=cmult)
    prev = first
    noprev = True
    for i in range(1,perside):
        cur = [prev]
        cur.append(HexWell(width=hexchanwidth, rad=rad, cmult=cmult, outnum=0, innum=3))
        for j in range(6):
            if j < 5:
                sidelen = i
            else:
                sidelen = i-1
            for k in range(sidelen):
                cur.append(HexWell(width=hexchanwidth, rad=rad, cmult=cmult, outnum=hexmoves[j][0], innum=hexmoves[j][1]))
        lay.AddBranch(Branch(cur, noprev=noprev))
        prev = cur[1]
        noprev=False
        
    per = [prev]
    per.append(Channel(length=(perside-.5)*rad*cmult, width=width, ang=2*math.pi/3))
    for i in range(5):
        per.append(Channel(length=(perside-.5)*rad*cmult, width=width, ang=math.pi/3))
    lay.AddBranch(Branch(per))
    
    for i in range(2):
        for j in range(2):
            ports = [per[3 + i*3]]
            ports.append(Channel(length=(perside-.5)*rad*cmult/2, width=width, ang=-j*2*math.pi/3))
            ports.append(Pinhole(width=width, out=True))
            lay.AddBranch(Branch(ports))
    
    first.Place(((0,0,0),(0,100,0)))
    lay.Build()
    lay.Draw('layer_hexhex.ps')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()