import numpy as np


class TrafficLightExp:
    A = None
    simTime = None

    @classmethod
    def fitnessFunc(cls, idleTimes):
        fitness = 0

        for i in range(len(idleTimes)):
            fitness += (cls.simTime / (idleTimes[i] + 1/cls.simTime))

        return fitness * cls.A


class TrafficLightLin:
    A = None
    simTime = None

    @classmethod
    def fitnessFunc(cls, idleTimes):
        fitness = 0

        for i in range(len(idleTimes)):
            fitness += (cls.simTime - idleTimes[i])

        return fitness * cls.A


class TrafficLightSimple:
    A = 1
    simTime = None

    @classmethod
    def fitnessFunc(cls, idleTimes):

        fitness = 1/np.mean(np.array(idleTimes))

        return fitness * cls.A
