#
# Intersection.py
#
#
from modules.Block import Block
from modules.IntersectionBlock import IntersectionBlock


class Intersection:
    #
    # Intersection class
    #

    # constructor
    def __init__(self, name=None):
        self.streets = []
        self.intersectionBlocks = {         # todo: if direction exists...
            'north': IntersectionBlock(),
            'east': IntersectionBlock(),
            'south': IntersectionBlock(),
            'west': IntersectionBlock()
        }
        if name is not None:
            setattr(self, 'name', name)

    def addStreet(self, street, direction):
        if hasattr(self, direction):
            raise Exception('Intersection contains already a street in "{}"'.format(direction))
        else:
            if not street.isConnected:
                street.lanes[1].set_intersectionBlock(direction)
            else:
                street.lanes[0].set_intersectionBlock(direction)
            self.streets.append(street)
            setattr(self, direction, street)
            if not street.isConnected:
                street.isConnected = True

    def checkDirection(self, direction):
        if hasattr(self, direction):
            return False
        else:
            return True

    def get_intersectionBlock(self, direction):
        return self.intersectionBlocks[direction]

    def __len__(self):
        return len(self.streets)

    # string representation for class data
    def __str__(self):
        s = 'Intersection: '

        if hasattr(self, 'name'):
            s += self.name + ', '
        s += 'contains ' + str(self.__len__()) + ' streets ('

        containsName = False
        for st in self.streets:
            if hasattr(st, 'name'):
                s += st.name + ', '
                containsName = True

        if containsName:
            s = s[:-2]

        s += ').'
        return s
