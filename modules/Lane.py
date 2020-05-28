#
# Lane.py
#
#
from modules.Block import Block
from modules.IntersectionBlock import IntersectionBlock


class Lane:
    #
    # Lane class
    #

    # constructor       --> assuming every street will end in an Intersection
    def __init__(self, length, startIntersection, endIntersection):
        super().__init__()

        self.length = length
        self.blocks = []
        self.startIntersection = startIntersection
        self.endIntersection = endIntersection
        self.blocks.append(Block())            # maybe later for visualization this block has to know it is the "firstBlock"
        for i in range(0, length-1):    # setting all the blocks except the last one (the IntersectionBlock) here
            insertBlock = Block()
            self.blocks[i].set_nextBlock(insertBlock)
            self.blocks.append(insertBlock)

    # string representation for class data
    def __str__(self):
        pass

    def set_intersectionBlock(self, direction):
        self.blocks.append(self.endIntersection.get_intersectionBlock(direction))
        self.blocks[len(self.blocks)-2].set_nextBlock(self.endIntersection.get_intersectionBlock(direction))
