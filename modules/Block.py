#
# Block.py
#
#


class Block:
    #
    # Block class
    #

    # constructor
    def __init__(self, blockType='intermediate', relatedIntersection=None):
        super().__init__()
        self.hasCar = None  # this attribute will be either None or a Car object, todo: this has to be renamed, since the name implies a boolean...
        self.nextBlock = None
        self.blockType = blockType
        self.relatedIntersection = relatedIntersection

    # string representation for class data
    def __str__(self):
        return self.name

    def set_nextBlock(self, block):         # will be called from lane
        self.nextBlock = block