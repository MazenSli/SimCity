#
# Car.py
#
#
import random

class Car:
    #
    # Car class
    #
    turnLeftProb = 0.1
    turnStraightProb = 0.7
    turnRightProb = 0.2

    # constructor
    def __init__(self, position):
        super().__init__()
        self.position = position  # block
        self.idleTime = 0
        self.nextTurn = 'straight'           # todo: 'left', 'straight', 'right'.

    # string representation for class data
    def __str__(self):
        return self.name

    def set_nextTurn(self):
        randNum = random.random()

        if randNum < turnLeftProb:
            self.nextTurn = 'left'
        elif randNum > 1-turnRightProb:
            self.nextTurn = 'right'
        else:
            self.nextTurn = 'straight'

    '''def checkOppositeSide(self):
        if self.position'''

    # todo: what should happen if there is a car in front of the car? (That car might move as well in this timestamp,
    #  so there is not necessarily a need to stop)
    #  ANSWER: For now i'll stop the car as long as there is a car in next block
    #          (which is actually "realistic" and probably causing traffic jam and "reaction time" at traffic lights)
    #  -> high number for length of street will make things more smooth there. (can still adjust the time step duration)
    def moveCar(self):         # will be called from lane

        if type(self.position) == IntersectionBlock:
            # car is located at an intersection
            self.position.relatedIntersection.processCars()
            return

        # car won't move as long as there is another car in front of it
        if self.position.nextBlock.hasCar():    # todo: hasCar = None functioniert wie 'False'?
            self.idleTime += 1
            return


        else:
            # car is not located at an intersection
            self.position = self.position.nextBlock()
