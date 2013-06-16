'''
Created on Jul 15, 2011

@author: tel
'''
import unittest, mock, math

from stack.layer.block.prim.prim import Channel

class Test(unittest.TestCase):
    def setUp(self):
        self.layer = mock.Mock()
        self.layer.zpos = 0.0
        
    def tearDown(self):
        pass
    
    def testChannel(self):
        start_loc = ((0,3.0,0),(0,4.0,0))
        c1 = Channel(xdim=2,ydim=1,layer=self.layer,loc=start_loc)
        c2 = Channel(xdim=4,ydim=1,layer=self.layer,prev=c1)
        c3 = Channel(xdim=6,ydim=1,layer=self.layer,prev=c2)
        for i,c in enumerate((c1,c2,c3)):
            c.MoveToPos(offang=(i+1)*(math.pi/7.0))
        for c in (c2,c3):
            c1.Union(c)
        c1.hedra.save_mesh('channel.obj')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()