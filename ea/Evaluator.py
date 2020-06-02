import math


# Multi-dimensional Rastrigrin function evaluator class
#
class Rastrigrin:
    nVars = None
    A = None

    @classmethod
    def fitnessFunc(cls, state):
        fitness = cls.A * cls.nVars

        for i in range(cls.nVars):
            fitness += state[i] * state[i] - cls.A * math.cos(2.0 * math.pi * state[i])

        return -fitness


class TrafficLights:
    pass
