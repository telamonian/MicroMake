'''
Created on Jun 4, 2013

@author: tel
'''
import numpy as np

from hedra import Hedra
from transmat import rotation_matrix

class Prim(Hedra):
    pass
        
class Channel(Prim):
    def __init__(self, len, wid, loc=)