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
    def __init__(self, isGreen, direction, blockType='intermediate', relatedIntersection=None, greenRatio=0.2):    # todo: greenRatio default value = ?
        super().__init__(blockType, relatedIntersection)
        self.nextBlock = None
        self.isGreen = isGreen
        #self.direction = direction todo: BRAUCH ICH DIE DIRECTION HIER ÜBERHAUPT????

    def set_nextBlock(self, nextBlocks):    # 'nextBlocks' will be a dictionary wit 'left', 'right', and 'straight'
        self.nextBlock = nextBlocks

    def toggle_light(self):
        self.isGreen = not isGreen

    # string representation for class data
    def __str__(self):
        pass