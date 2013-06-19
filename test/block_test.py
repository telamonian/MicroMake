'''
Created on Jul 15, 2011

@author: tel
'''
CHANW = 1

import unittest, mock, math

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
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    #unittest.main()
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