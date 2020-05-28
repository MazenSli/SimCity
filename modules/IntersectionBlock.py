#
# IntersectionBlock.py
#
#
from modules.Block import Block


class IntersectionBlock(Block):
    #
    # Lane class
    #

    # constructor
    def __init__(self):
        super().__init__()
        self.nextBlock = None

    def set_nextBlock(self, nextBlocks):    # this will be called from Intersection
        self.nextBlock = nextBlocks



    # string representation for class data
    def __str__(self):
        pass