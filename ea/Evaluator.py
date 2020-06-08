import math


class TrafficLightExp:
    A = None
    simTime = None

    @classmethod
    def fitnessFunc(cls, idleTimes):
        fitness = 0

        for i in range(len(idleTimes)):
            fitness += (1 / (idleTimes[i] + 1/cls.simTime))

        return fitness * cls.A
