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
        self.car = None  # this attribute will be either None or a Car object, todo: this has to be renamed, since the name implies a boolean...
        self.nextBlock = None
        self.blockType = blockType
        self.relatedIntersection = relatedIntersection

    def set_nextBlock(self, block):         # will be called from lane
        self.nextBlock = block

    def remove_car(self):
        self.car = None

    def set_car(self, car):
        self.car = car
