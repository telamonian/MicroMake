'''
Created on Jul 24, 2013

@author: tel
mixer added by elosito 10/11/13
'''
import unittest, math
import numpy as np

from layer.layer import Layer
from layer.branch.branch import Branch
from layer.branch.block.block import Channel, Pinhole, HexWell, RectTrap, Split, Circle

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
    
#    def testHexHex(self):
#        testHexHex(self)

def testRectTrap(self=True):
    lay = Layer()
    
    inhole = Pinhole(width=100)
    right = Channel(length=6700, width=100)
    straight0= Channel(length=3500, width=100, ang=math.pi/4)
    straight1= Channel(length=3500, width=100, ang=-math.pi/2)
    straight2= Channel(length=2000, width=100, ang=-(3*math.pi)/4)
    outhole = Pinhole(width=100, out=True)
    blocks= [inhole, right, straight0, straight1, straight2, outhole]
    branch= Branch(blocks)
    lay.AddBranch(branch)
    
        
    straight3= Channel(length=3500, width=100, ang=-math.pi/4)
    straight4= Channel(length=3500, width=100, ang=math.pi/2)
    blocks=[right, straight3, straight4]
    branch= Branch(blocks)
    lay.AddBranch(branch)
    
    above = Channel(length=1200, width=100, ang=((3*math.pi)/4)+(-math.pi/2))
    mix1 = Channel(length=800, width=100, ang=(math.pi/2))
    mix2 = Channel(length=1600, width=100, ang=(-math.pi/2))
    mix3 = Channel(length=400, width=100, ang=(3*math.pi/2))
    mix4 = Channel(length=200, width=100, ang=(-3*math.pi/2))
    mix5 = Channel(length=600, width=100, ang=(math.pi/2))
    mix6 = Channel(length=2000, width=100, ang=(math.pi/2))
    mix7 = Channel(length=800, width=100, ang=(-3*math.pi/2))
    mix8= Channel(length=200, width=100, ang=(-math.pi/2))
    mix9 = Channel(length=1000, width=100, ang=(-math.pi/2))
    mix10 = Channel(length=2400, width=100, ang=(-math.pi/2))
    mix11 = Channel(length=1000, width=100, ang=(3*math.pi/2))
    mix12 = Channel(length=600, width=100, ang=(-math.pi/2))
    mix13 = Channel(length=400, width=100, ang=(-math.pi/2))
    mix14 = Channel(length=1200, width=100, ang=(math.pi/2))
    mix15 = Channel(length=600, width=100, ang=(-3*math.pi/2))
    mix16 = Channel(length=200, width=100, ang=(-3*math.pi/2))
    mix17 = Channel(length=400, width=100, ang=(math.pi/2))
    mix18 = Channel(length=800, width=100, ang=(-math.pi/2))
    mix19 = Channel(length=200, width=100, ang=(3*math.pi/2))
    mix20 = Channel(length=400, width=100, ang=(-math.pi/2))
    mix21a= Channel(length=10, width=100, ang=(-3*math.pi/2))
    mix21 = Circle(width=100, rad=200, tang=math.pi/6)
    mix21b= Channel(length=10, width=100, ang=0)
    #mix21 = Channel(length=400, width=100, ang=(-3*math.pi/2))
    mix22 = Channel(length=400, width=100, ang=(-math.pi/2))
    mix23 = Channel(length=200, width=100, ang=(-3*math.pi/2))
    mix24 = Channel(length=800, width=100, ang=(-3*math.pi/2))
    mix25 = Channel(length=400, width=100, ang=(math.pi/2))
    mix26 = Channel(length=200, width=100, ang=(-math.pi/2))
    mix27 = Channel(length=600, width=100, ang=(3*math.pi/2))
    mix28 = Channel(length=1200, width=100, ang=(-math.pi/2))
    mix29 = Channel(length=400, width=100, ang=(-math.pi/2))
    mix30 = Channel(length=600, width=100, ang=(math.pi/2))
    mix31 = Channel(length=1000, width=100, ang=(-3*math.pi/2))
    mix32 = Channel(length=2400, width=100, ang=(-3*math.pi/2))
    mix33 = Channel(length=1000, width=100, ang=(math.pi/2))
    mix34 = Channel(length=200, width=100, ang=(math.pi/2))
    mix35 = Channel(length=800, width=100, ang=(-3*math.pi/2))
    mix36 = Channel(length=2000, width=100, ang=(-math.pi/2))
    mix37 = Channel(length=600, width=100, ang=(-math.pi/2))
    mix38 = Channel(length=200, width=100, ang=(-math.pi/2))
    mix39 = Channel(length=400, width=100, ang=(3*math.pi/2))
    mix40 = Channel(length=1600, width=100, ang=(-3*math.pi/2))
    mix41 = Channel(length=800, width=100, ang=(math.pi/2))
    belowm = Channel(length=1200, width=100, ang=(-math.pi/2))
    trap = RectTrap(width=100, rad=200, mwidth=30, mdepth=60, tang=math.pi/6)
    below = Channel(length=1200, width=100)
    left1= Channel(length=100, width=100, ang=(-math.pi/2))
    left = Channel(length=800, width=150)#, ang=(-math.pi/2)
    outhole = Pinhole(width=150, out=True)
    blocks = [straight1, above, mix1, mix2, mix3, mix4, mix5, mix6, mix7, mix8, mix9, mix10, mix11, mix12, mix13, mix14, mix15, mix16, mix17, mix18, mix19, mix20,mix21a, mix21,mix21b, mix22, mix23, mix24, mix25, mix26, mix27, mix28, mix29, mix30, mix31, mix32, mix33, mix34, mix35, mix36, mix37, mix38, mix39, mix40, mix41, belowm, trap, below, left1,left, outhole]
    branch = Branch(blocks)
    
    lay.AddBranch(branch)
    
    inhole.Place(((0,0,0),(0,100,0)))
    lay.Build()
    lay.Draw('mixer_trap.ps')

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
    split0 = Split(width=width, length=2*2500, ang=-math.pi/2)
    split1 = Split(width=width, length=2*1250, ang=math.pi/6)
    split2 = Split(width=width, length=2*600, ang=math.pi/6)
    
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
    trap = RectTrap(width=width, rad=200, mwidth=30+30*np.random.rand(), mdepth=30+30*np.random.rand(), tang=2*math.pi/9)
    below = Channel(length=400, width=width)
    ditch = Channel(length=400, width=width, ang=math.pi/6)
    
    blocks = [split2, above, trap, below, ditch]
    trap0 = Branch(blocks)
    
    trap1 = trap0.Copy()
    trap1.blocks[1].outnum = 1
    trap1.blocks[1].props['ang'] = -math.pi/6
    trap1.blocks[2].props['mwidth'] = 30 + 30*np.random.rand()
    trap1.blocks[2].props['mdepth'] = 30 + 30*np.random.rand()
    trap1.blocks[2].props['tang'] = 4*math.pi/9
    
    extra_traps = []
    for i, split in enumerate([split3, split5, split6]):
        for j, t in enumerate([trap0, trap1]):
            tmp = t.Copy()
            tmp.blocks[0] = split
            tmp.blocks[2].props['mwidth'] = 30 + 30*np.random.rand()
            tmp.blocks[2].props['mdepth'] = 30 + 30*np.random.rand()
            tmp.blocks[2].props['tang'] = 2*(i*2+j+3)*math.pi/9
            extra_traps.append(tmp)
            
    left = Channel(length=9000, width=width, ang=(math.pi/3))
    outhole = Pinhole(width=width, out=True)
    
    blocks = [ditch, left, outhole]
    bottom = Branch(blocks)
    
    branches = [top0, top1, top2, top3, trap0, trap1] + extra_traps + [bottom]
    lay0.AddBranches(branches)
    
    inhole.Place(((0,0,0),(0,100,0)))
    
    lay1 = lay0.Copy()
    lay1.tmat = Layer.RotatePointMat(math.pi/2, (4000,10000,0))
    lay0.Build()
    lay1.Build()
    
    lay0.Draw('layer_splittraps.ps', lay1)

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