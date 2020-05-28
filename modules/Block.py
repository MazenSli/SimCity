#
# Block.py
#
#


class Block:
    #
    # Block class
    #

    # constructor
    def __init__(self):
        super().__init__()
        self.hasCar = False
        self.nextBlock = None

    # string representation for class data
    def __str__(self):
        return self.name

    def set_nextBlock(self, block):         # todo: will be called from lane (?)
        self.nextBlock = block

