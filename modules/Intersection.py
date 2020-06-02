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
        if name is not None:
            setattr(self, 'name', name)
        self.streets = []
        self.north_greenRatio = 0.5
        self.intersectionTime = 60
        self.toggleShift = 0  # e[0, intersectionTime] - toggle shift determines how long the traffic light will wait for the first toggle

        # intersectionEntryBlocks represent the end of a road and the entrance of an Intersection.
        # Those blocks are the only "IntersectionBlock" objects, they have to be special, because
        # they have more than one "nextBlock"
        self.intersectionEntranceBlocks = {     # todo: if direction exists...
                                                # todo: BlockType und relatedIntersection wurden zu testzwecken eingeführt und sind eventuell unnötig
            'north': IntersectionBlock(True, 'north', blockType='roadEnd', relatedIntersection=self),
            'east': IntersectionBlock(False, 'east', blockType='roadEnd', relatedIntersection=self),
            'south': IntersectionBlock(True, 'south', blockType='roadEnd', relatedIntersection=self),
            'west': IntersectionBlock(False, 'west', blockType='roadEnd', relatedIntersection=self)
        }
        # intersectionExitBlocks represent the entrance of a road and the exit of an Intersection.
        # They are normal "Block" objects
        self.intersectionExitBlocks = {  # todo: if direction exists...
            'north': Block(blockType='roadEntrance', relatedIntersection=self),
            'east': Block(blockType='roadEntrance', relatedIntersection=self),
            'south': Block(blockType='roadEntrance', relatedIntersection=self),
            'west': Block(blockType='roadEntrance', relatedIntersection=self)
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

    def set_greenRatio(self, north_greenRat):     # todo: greenRatio von jew. diagonalen intersectionBlocks muss gleich sein, die restl. sind 1-greenRatio.
            pass

    def toggle_lights(self):
        for direction, iBlock in self.intersectionEntranceBlocks.items():
            iBlock.toggle_light()

    def processCars(self,):
        # todo: hasCar setzen und dann diese function schreiben
        pass

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
