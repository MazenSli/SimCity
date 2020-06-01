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
    def __init__(self, blockType='intermediate', relatedIntersection_name=None):
        super().__init__(blockType, relatedIntersection_name)
        self.nextBlock = None

    def set_nextBlock(self, nextBlocks):    # 'nextBlocks' will be a dictionary wit 'left', 'right', and 'straight'
        self.nextBlock = nextBlocks



    # string representation for class data
    def __str__(self):
        pass