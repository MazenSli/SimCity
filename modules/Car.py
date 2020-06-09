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
        self.nextTurn = 'straight'
        self.isProcessed = False

    def set_nextTurn(self):
        randNum = random.random()

        if self.position.relatedIntersection.missing_dir is None:
            if randNum < self.turnLeftProb:
                self.nextTurn = 'left'
            elif randNum > 1 - self.turnRightProb:
                self.nextTurn = 'right'
            else:
                self.nextTurn = 'straight'
            return

        if 'left' not in self.position.nextBlock:
            if randNum < (self.turnLeftProb+self.turnRightProb):
                self.nextTurn = 'right'
            else:
                self.nextTurn = 'straight'
        elif 'right' not in self.position.nextBlock:
            if randNum < (self.turnLeftProb+self.turnRightProb):
                self.nextTurn = 'left'
            else:
                self.nextTurn = 'straight'
        elif 'straight' not in self.position.nextBlock:
            left = self.turnLeftProb+self.turnStraightProb/2
            if randNum < left:
                self.nextTurn = 'left'
            else:
                self.nextTurn = 'right'

    def increment_idleTime(self):
        self.idleTime += 1

    def moveToNextBlock(self):

        self.position.remove_car()
        if type(self.position) == IntersectionBlock:
            self.position.nextBlock[self.nextTurn].set_car(self)
            self.position = self.position.nextBlock[self.nextTurn]
            self.isProcessed = True
        else:
            self.position.nextBlock.set_car(self)
            self.position = self.position.nextBlock

        if type(self.position) == IntersectionBlock:
            self.set_nextTurn()     # todo: will cars change their mind regarding the direction they want to take after standing? I don't think so..

    # todo: what should happen if there is a car in front of the car? (That car might move as well in this timestamp,
    #  so there is not necessarily a need to stop)
    #  ANSWER: For now i'll stop the car as long as there is a car in next block
    #          (which is actually "realistic" and probably causing traffic jam and "reaction time" at traffic lights)
    #  -> high number for length of street will make things more smooth there. (can still adjust the time step duration)
    def move_laneCar(self):         # this function will only affect cars located at "non-intersectionBlocks"!
        if (type(self.position) is IntersectionBlock) or self.isProcessed:
            return
        # -> car is located at a normal block ("non-intersectionBlock")

        if self.position.nextBlock.car:   # car won't move as long as there is another car in front of it
            self.idleTime += 1
            return
        else:                               # no car in nextBlock -> car can go
            self.moveToNextBlock()
