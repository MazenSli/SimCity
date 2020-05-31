#
# Street.py
#
#
from modules.Lane import Lane


class Street:
    #
    # Street class
    #

    # constructor
    def __init__(self, length, startIs, endIs, name=None):
        self.isConnected = False
        self.length = length
        self.startInter = startIs
        self.endInter = endIs
        # Lane[1] will be "facing" the opposite way of the street/Lane[0]
        self.lanes = [Lane(self.length, startIntersection=endIs, endIntersection=startIs),
                      Lane(self.length, startIntersection=startIs, endIntersection=endIs)]
        if name is not None:
            setattr(self, 'name', name)

    def __len__(self):
        return self.length

    # string representation for class data
    def __str__(self):
        s = 'Street: '
        if hasattr(self, 'name'):
            s += self.name + ', '
        s += 'contains ' + str(self.__len__()) + ' blocks.'
        return s

#    def defineEnds(self):
#        if self.lane[0].blocks[0].blocktype == 'intermediate':
#            self.lane[0].blocks[0].set_BlockType('first')
#        if self.lane[0].blocks[self.length-1].blocktype == 'intermediate':
#            self.lane[0].blocks[self.length-1].set_BlockType('last')
#        if self.lane[1].blocks[0].blocktype == 'intermediate':
#            self.lane[1].blocks[0].set_BlockType('first')
#        if self.lane[1].blocks[self.length-1].blocktype == 'intermediate':
#            self.lane[1].blocks[self.length-1].set_BlockType('last')
