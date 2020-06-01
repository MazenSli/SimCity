#
# Car.py
#
#


class Car:
    #
    # Car class
    #

    # constructor
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.idleTime = 0

    # string representation for class data
    def __str__(self):
        return self.name

    # todo: what should happen if there is a car in front of the car? (That car might move as well in this timestamp,
    #  so there is not necessarily a need to stop)
    #  ANSWER: For now i'll stop the car as long as there is a car in next block
    #          (which is actually "realistic" and probably causing traffic jam and "reaction time" at traffic lights)
    #  -> high number for length of street will make things more smooth there. (can still adjust the time step duration)
    def moveCar(self):         # will be called from lane
        # car won't move as long as there is another car in front of it
        if self.position.nextBlock.hasCar():
            return

        if type(self.position) == IntersectionBlock:
            # car is located at an intersection
            pass

        else:
            # car is not located at an intersection
            self.position = self.position.nextBlock()
