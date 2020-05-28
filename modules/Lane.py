#
# Lane.py
#
#
import Block


class Lane:
    #
    # Lane class
    #

    # constructor
    def __init__(self, firstBlock, length, lastBlock):
        super().__init__()

        self.length = length
        self.blocks = []
        self.blocks.append(firstBlock)
        for i in range(0, length-2):
            insertBlock = Block()
            blocks[i].set_nextBlock(insertBlock)
            blocks.append(Block(insertBlock))
        self.blocks.append(lastBlock)



    # string representation for class data
    def __str__(self):
        pass
