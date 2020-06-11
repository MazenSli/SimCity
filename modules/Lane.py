#
# Lane.py
#
#

from modules.Block import Block


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
        self.blocks.append(Block())            # this will not be the first block later, but the second block
        for i in range(0, length-3):    # setting all the blocks except the last one (the IntersectionBlock) here
            insertBlock = Block()
            self.blocks[i].set_nextBlock(insertBlock)
            self.blocks.append(insertBlock)

    # string representation for class data
    def __str__(self):
        retString = 'startInters: ' + str(self.startIntersection) + '   endInters: ' + str(self.endIntersection) + '\n'\
                    + 'first block of the lane is: ' + self.blocks[0].blockType\
                    + ' with related Inters: ' + str(self.blocks[0].relatedIntersection) + '\n'\
                    + 'last block of the lane is: ' + self.blocks[self.length-1].blockType\
                    + ' with related Inters: ' + str(self.blocks[self.length-1].relatedIntersection) + '\n'
        return retString

    # exitBlock is the first block of a road -> the block that represents the exit of an intersection
    def set_intersectionExitBlock(self, intersectionExitBlock):
        self.blocks.insert(0, intersectionExitBlock)
        intersectionExitBlock.set_nextBlock(self.blocks[1])

    # exitBlock is the first block of a road -> the block that represents the entrance of an intersection
    def set_intersectionEntranceBlock(self, intersectionEntranceBlock):
        self.blocks.append(intersectionEntranceBlock)
        self.blocks[len(self.blocks)-2].set_nextBlock(intersectionEntranceBlock)
