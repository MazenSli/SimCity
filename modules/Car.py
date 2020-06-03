#
# Car.py
#
#
import random
from modules.IntersectionBlock import IntersectionBlock

from modules.IntersectionBlock import IntersectionBlock


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
        self.nextTurn = 'straight'           # todo: 'left', 'straight', 'right'

    def set_nextTurn(self):
        randNum = random.random()

        if randNum < self.turnLeftProb:
            self.nextTurn = 'left'
        elif randNum > 1-self.turnRightProb:
            self.nextTurn = 'right'
        else:
            self.nextTurn = 'straight'

    def increment_idleTime(self):
        self.idleTime += 1

    def moveToNextBlock(self):
        if type(self.position) == IntersectionBlock:
            self.position = self.position.nextBlock[self.nextTurn]
            self.position.nextBlock[self.nextTurn].set_car(self)
        else:
            self.position.nextBlock.set_car(self)
            self.position = self.position.nextBlock

        self.position.remove_car()


    # todo: what should happen if there is a car in front of the car? (That car might move as well in this timestamp,
    #  so there is not necessarily a need to stop)
    #  ANSWER: For now i'll stop the car as long as there is a car in next block
    #          (which is actually "realistic" and probably causing traffic jam and "reaction time" at traffic lights)
    #  -> high number for length of street will make things more smooth there. (can still adjust the time step duration)
    def moveCar(self):         # this function will only affect cars located at "non-intersectionBlocks"!
        if type(self.position) == IntersectionBlock:
            return
        # -> car is located at a normal block ("non-intersectionBlock")

        if self.position.nextBlock.car():   # car won't move as long as there is another car in front of it
            self.idleTime += 1
            return
        else:                               # no car in nextBlock -> car can go
            self.moveToNextBlock()
