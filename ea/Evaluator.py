#
# Evaluator.py
#
#

import numpy as np


class TrafficLightExp:
    simTime = None

    @classmethod
    def fitnessFunc(cls, idleTimes):
        #
        # summation of modified 1/x functions
        #
        fitness = 0

        for i in range(len(idleTimes)):
            fitness += (cls.simTime / (idleTimes[i] + 1/cls.simTime))

        return fitness


class TrafficLightLin:
    #
    # summation of linear functions
    #
    simTime = None

    @classmethod
    def fitnessFunc(cls, idleTimes):
        fitness = 0

        for i in range(len(idleTimes)):
            fitness += (cls.simTime - idleTimes[i])

        return fitness


class TrafficLightSimple:
    #
    # average of all idle times
    #
    simTime = None

    @classmethod
    def fitnessFunc(cls, idleTimes):

        fitness = 1/np.mean(np.array(idleTimes))

        return fitness
