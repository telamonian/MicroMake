'''
Created on Jun 4, 2013

@author: tel
'''

import pyPolyCSG as csg

from hedra import Hedra
from block_error import *

class Block(Hedra):
    pass
    
class SBlock(Block):
    def __init__(self, **kwargs):
        super(Channel, self).__init__(**kwargs)
    
    def Join(self, static, mobile, joint):
        