'''
Created on Jul 3, 2011

@author: tel
'''

class Base(Exception):
    pass

class UnpositionedHedraError(Base):
    '''
    the hedra currently being initialized has no prespecified inlet location, nor is a previous block specified
    thus, the block has no idea where it should position itself
    '''
    def __init__(self):
        pass