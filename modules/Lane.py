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
    def __init__(self, length):
        super().__init__()

        this.length = length
        this.blocks = []
        for i in range(0, length):
            blocks.append(Block())

    # string representation for class data
    def __str__(self):
        pass
