import math


class TrafficLightExp:
    A = None

    @classmethod
    def fitnessFunc(cls, idleTimes):
        fitness = 0

        for i in range(len(idleTimes)):
            fitness += (1 / idleTimes[i])

        return fitness * cls.A
