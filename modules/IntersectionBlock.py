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
    def __init__(self, isGreen, blockType='intermediate', relatedIntersection=None):    # todo: greenRatio default value = ?
        super().__init__(blockType, relatedIntersection)
        self.nextBlock = None
        self.isGreen = isGreen

    def set_nextBlock(self, nextBlocks):    # 'nextBlocks' will be a dictionary wit 'left', 'right', and 'straight'
        self.nextBlock = nextBlocks

    def toggle_light(self):
        self.isGreen = not self.isGreen