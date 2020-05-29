#
# Intersection.py
#
#
from modules.Block import Block
from modules.IntersectionBlock import IntersectionBlock

# hello

class Intersection:
    #
    # Intersection class
    #

    # constructor
    def __init__(self, name=None):
        if name is not None:
            setattr(self, 'name', name)
        self.streets = []
        # intersectionEntryBlocks represent the end of a road and the entrance of an Intersection.
        # Those blocks are the only "IntersectionBlock" objects, they have to be special, because
        # they have more than one "nextBlock"
        self.intersectionEntranceBlocks = {  # todo: if direction exists...
            'north': IntersectionBlock(blockType='roadEnd', relatedIntersection_name=name),
            'east': IntersectionBlock(blockType='roadEnd', relatedIntersection_name=name),
            'south': IntersectionBlock(blockType='roadEnd', relatedIntersection_name=name),
            'west': IntersectionBlock(blockType='roadEnd', relatedIntersection_name=name)
        }
        # intersectionExitBlocks represent the entrance of a road and the exit of an Intersection.
        # They are normal "Block" objects
        self.intersectionExitBlocks = {  # todo: if direction exists...
            'north': Block(blockType='roadEntrance', relatedIntersection_name=name),
            'east': Block(blockType='roadEntrance', relatedIntersection_name=name),
            'south': Block(blockType='roadEntrance', relatedIntersection_name=name),
            'west': Block(blockType='roadEntrance', relatedIntersection_name=name)
        }
        self._init_intersectionBlocks()

    # sets up all the nextBlocks of the IntersectionBlocks (-> "intersectionEntranceBlocks"), the nextBlocks will be
    # set in a dictionary with keys: left straight and right, representing the turns a car can perform at an inters.
    def _init_intersectionBlocks(self):
        for entranceDirection, entranceBlock in self.intersectionEntranceBlocks.items():
            nextBlocks = {'left': None, 'straight': None, 'right': None}
            if entranceDirection == 'north':
                nextBlocks['left'] = self.intersectionExitBlocks['east']
                nextBlocks['straight'] = self.intersectionExitBlocks['south']
                nextBlocks['right'] = self.intersectionExitBlocks['west']
            if entranceDirection == 'east':
                nextBlocks['left'] = self.intersectionExitBlocks['south']
                nextBlocks['straight'] = self.intersectionExitBlocks['west']
                nextBlocks['right'] = self.intersectionExitBlocks['north']
            if entranceDirection == 'south':
                nextBlocks['left'] = self.intersectionExitBlocks['west']
                nextBlocks['straight'] = self.intersectionExitBlocks['north']
                nextBlocks['right'] = self.intersectionExitBlocks['east']
            if entranceDirection == 'west':
                nextBlocks['left'] = self.intersectionExitBlocks['north']
                nextBlocks['straight'] = self.intersectionExitBlocks['east']
                nextBlocks['right'] = self.intersectionExitBlocks['south']
            entranceBlock.set_nextBlock(nextBlocks)

    def addStreet(self, street, direction):
        if hasattr(self, direction):
            raise Exception('Intersection contains already a street in "{}"'.format(direction))
        else:
            # this block sets lane[0] as the "right hand side"-lane
            if not street.isConnected:  # the street is not connected to an intersection yet
                street.lanes[0].set_intersectionEntranceBlock(self.intersectionEntranceBlocks[direction])
                street.lanes[1].set_intersectionExitBlock(self.intersectionExitBlocks[direction])
                street.isConnected = True
            else:  # the street is already connected to an intersection
                street.lanes[1].set_intersectionEntranceBlock(self.intersectionEntranceBlocks[direction])
                street.lanes[0].set_intersectionExitBlock(self.intersectionExitBlocks[direction])
            self.streets.append(street)
            setattr(self, direction, street)


    def checkDirection(self, direction):
        if hasattr(self, direction):
            return False
        else:
            return True

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
