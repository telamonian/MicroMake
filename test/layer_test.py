'''
Created on Jul 24, 2013

@author: tel
'''
import unittest, math

from layer.layer import Layer
from layer.branch.branch import Branch
from layer.branch.block.block import Channel, Pinhole, HexWell, RectTrap

class Test(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
#    def testRectTrap(self):
#        testRectTrap(self)
#        
#    def testHexWell(self):
#        testHexWell(self)
        
    def testHexHex(self):
        testHexHex(self)

def testRectTrap(self=True):
    lay = Layer()
    
    inhole = Pinhole(100)
    right = Channel(800, 100)
    above = Channel(2000, 100, ang=(-math.pi/2))
    trap = RectTrap(width=100, rad=200, mwidth=30, mdepth=60, tang=math.pi/6)
    bellow = Channel(2000, 100)
    left = Channel(800, 100, ang=(-math.pi/2))
    outhole = Pinhole(100, out=True)
    inhole.Place(((0,0,0),(0,100,0)))
    blocks = [inhole, right, above, trap, bellow, left, outhole]
    branch = Branch(blocks)
    
    lay.AddBranch(branch)
    
    lay.Build()
    lay.Draw('layer_trap.ps')

def testHexWell(self):
    lay = Layer()
    
    inhole = Pinhole(100)
    right = Channel(800, 100)
    above = Channel(2000, 100, ang=(-math.pi/2))
    hexwell = HexWell(100)
    bellow = Channel(2000, 100)
    left = Channel(800, 100, ang=(-math.pi/2))
    outhole = Pinhole(100, out=True)
    inhole.Place(((0,0,0),(0,100,0)))
    blocks = [inhole, right, above, hexwell, bellow, left, outhole]
    branch = Branch(blocks)
    
    lay.AddBranch(branch)
    
    lay.Build()
    lay.Draw('layer_hexwell.ps')

hexmoves = {0:[4,1],1:[3,0],2:[2,5],3:[1,4],4:[0,3],5:[5,2]}

def testHexHex(self):
    lay = Layer()
    perside = 10
    rad = 400
    cmult = 2.5
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
#        for k in range(i-1):
#            cur.append(HexWell(100, outnum=hexmoves[5][0], innum=hexmoves[5][1]))
        lay.AddBranch(Branch(cur, noprev=noprev))
        prev = cur[1]
        noprev=False
        
    per = [prev]
    per.append(Channel((perside-.5)*rad*cmult, width=width, ang=2*math.pi/3))
    for i in range(5):
        per.append(Channel((perside-.5)*rad*cmult, width=width, ang=math.pi/3))
    lay.AddBranch(Branch(per))
    
    for i in range(2):
        for j in range(2):
            ports = [per[3 + i*3]]
            ports.append(Channel((perside-.5)*rad*cmult/2, width=width, ang=-j*2*math.pi/3))
            ports.append(Pinhole(width=width, out=True))
            lay.AddBranch(Branch(ports))
    
    first.Place(((0,0,0),(0,100,0)))
    lay.Build()
    lay.Draw('layer_hexhex.ps')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()