import math


class TrafficLightExpLin:
    A = None
    simTime = None

    @classmethod
    def fitnessFunc(cls, idleTimes):
        fitness = 0

        for i in range(len(idleTimes)):
            fitness += (cls.simTime - idleTimes[i])

        return fitness * cls.A
