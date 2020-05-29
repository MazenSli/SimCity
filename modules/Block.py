#
# Block.py
#
#


class Block:
    #
    # Block class
    #

    # constructor
    def __init__(self, blockType='intermediate', relatedIntersection_name=None):
        super().__init__()
        self.hasCar = False
        self.nextBlock = None
        self.blockType = blockType
        self.relatedIntersection_name = relatedIntersection_name

    # string representation for class data
    def __str__(self):
        return self.name

    def set_nextBlock(self, block):         # will be called from lane
        self.nextBlock = block