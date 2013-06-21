'''
Created on Jul 15, 2011

@author: tel
'''
CHANW = 30

import unittest, mock, math
import pyPolyCSG as csg
import numpy as np

from stack.layer.block.block import Channel
from stack.layer.block.port import Loc
class Test(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def testChannel(self):
        start_loc = Loc((0,3.0,0),(0,4.0,0))
        c1 = Channel(length=2,width=CHANW,ang=0,loc=start_loc)
        c1.SetJoint()
        c1.Transform(c1.joint.tmat)
        c2 = Channel(length=4,width=CHANW,ang=1,prev=c1)
        c2.SetJoint()
        c2.Transform(c2.joint.tmat)
        c3 = Channel(length=5,width=CHANW,ang=.73,prev=c2)
        c3.SetJoint()
        c3.Transform(c3.joint.tmat)
        
        c1.hedra = c1.hedra + c2.hedra + c3.hedra + c2.joint.mortar.hedra + c3.joint.mortar.hedra
        
        c1.hedra.save_mesh('channel.obj')
        c1.Save2D('channel.eps')
        
    def testSpiralChannel(self):
        ang = math.pi/6
        start_loc = Loc((0,3.0,0),(0,4.0,0))
        c = Channel(length=2,width=CHANW,ang=0,loc=start_loc)
        c.SetJoint()
        c.Transform(c.joint.tmat)
        chans = [c]
        for i in range(1,19):
            cs = Channel(length=2+(i*.6),width=CHANW,ang=ang,prev=chans[-1])
            cs.SetJoint()
            cs.Transform(cs.joint.tmat)
            chans.append(cs)
        for chan in chans[1:]:
            c.hedra = c.hedra + chan.hedra + chan.joint.mortar.hedra
        
        c.hedra.save_mesh('spiral.obj')
        c.Save2D('spiral.eps')

def HReduce(func, lis, argnum=5):
    for i in range(int(np.ceil(math.log(len(lis), argnum)))):
        for j in reversed(range(int(np.ceil(len(lis)/float(argnum))))):
            for k in reversed(range((j*argnum) + 1, ((j+1)*argnum))):
                try:
                    lis[j*argnum].hedra = func(lis[j*argnum], lis.pop(k))
                except IndexError:
                    pass
    return lis[0]

if __name__ == "__main__":
#    import sys#;sys.argv = ['', 'Test.test']
#    unittest.main()
    #print np.sum(range(100))
    #print HReduce(lambda x,y: x+y, range(100))
    ang = 2*math.pi/7
    start_loc = Loc((0,30.0,0),(0,60.0,0))
    c = Channel(length=20,width=CHANW,ang=0,loc=start_loc)
    c.SetJoint()
    c.Transform(c.joint.tmat)
    chans = [c]
    for i in range(1,501):
        cs = Channel(length=20+(i*10),width=CHANW,ang=ang,prev=chans[-1])
        cs.SetJoint()
        cs.Transform(cs.joint.tmat)
        chans.append(cs)
    c = chans[0] + HReduce(lambda x,y: x.hedra + y.hedra, chans[1:])

    c.hedra.save_mesh('spiral.obj')
    c.Save2D('spiral.eps')
    
#    thedra = []
#    for i in range(0,50):
#        thedron = chans[1+(i*10)].hedra + chans[1+(i*10)].joint.mortar.hedra
#        for j,chan in enumerate(chans[2+(i*10):1+((i+1)*10)]):
#            try:
#                thedron = thedron + chan.hedra + chan.joint.mortar.hedra
#            except RuntimeError:
#                print i*10+j
#        thedra.append(thedron)
#    for i in range(0,50):
#        try:
#            c.hedra = c.hedra + thedra[i]
#        except RuntimeError:
#            print i