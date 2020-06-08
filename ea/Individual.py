#
# Individual.py
#
#

import math


# Base class for all individual types
#
class Individual:
    """
    Individual
    """
    minMutRate = 1e-100
    maxMutRate = 1
    learningRate = None
    uniprng = None
    normprng = None
    fitFunc = None

    def __init__(self):
        self.idleTimes = []
        self.fit = self.__class__.fitFunc(self.idleTimes)
        self.mutRate = [self.uniprng.uniform(0.9, 0.1) for k in range(3)]  # use "normalized" sigma

    def mutateMutRate(self):
        for k in range(3):
            self.mutRate[k] = self.mutRate[k] * math.exp(self.learningRate * self.normprng.normalvariate(0, 1))
            if self.mutRate[k] < self.minMutRate: self.mutRate[k] = self.minMutRate
            if self.mutRate[k] > self.maxMutRate: self.mutRate[k] = self.maxMutRate

    def evaluateFitness(self):
        if self.fit is None:
            self.fit = self.__class__.fitFunc(self.idleTimes)


# Multivariate real representation class
#
class MultivariateIndividual(Individual):
    """
    MultivariateIndividual
    """
    nLength = None
    minIntersectionTime = None
    maxIntersectionTime = None

    minNorthGreenRatio = None

    def __init__(self):
        self.state = [[] for j in range(3)]

        for i in range(self.nLength):
            self.state[0].append(self.uniprng.uniform(0, 1))
            self.state[1].append(self.uniprng.uniform(self.minIntersectionTime, self.maxIntersectionTime))
            self.state[2].append(self.uniprng.uniform(0, self.state[0][i] * self.state[1][i]))

        super().__init__()  # call base class ctor

    def crossover(self, other):
        # perform crossover "in-place"
        alpha = [self.uniprng.random() for i in range(3)]

        for i in range(self.nLength):
            for k in range(3):
                tmp = self.state[k][i] * alpha[k] + other.state[k][i] * (1 - alpha[k])
                other.state[k][i] = self.state[k][i] * (1 - alpha[k]) + other.state[k][i] * alpha[k]
                self.state[k][i] = tmp

            # north green ratio limits
            if self.state[0][i] > 1-self.minNorthGreenRatio: self.state[0][i] = 1-self.minNorthGreenRatio
            if self.state[0][i] < self.minNorthGreenRatio: self.state[0][i] = self.minNorthGreenRatio
            if other.state[0][i] > 1-self.minNorthGreenRatio: other.state[0][i] = 1-self.minNorthGreenRatio
            if other.state[0][i] < self.minNorthGreenRatio: other.state[0][i] = self.minNorthGreenRatio

            # intersection time limits
            if self.state[1][i] > self.maxIntersectionTime:
                self.state[1][i] = self.maxIntersectionTime
            if self.state[1][i] < self.minIntersectionTime:
                self.state[1][i] = self.minIntersectionTime
            if other.state[1][i] > self.maxIntersectionTime:
                other.state[1][i] = self.maxIntersectionTime
            if other.state[1][i] < self.minIntersectionTime:
                other.state[1][i] = self.minIntersectionTime

            # toggle shift limits
            if self.state[2][i] > self.state[0][i] * self.state[1][i]:
                self.state[2][i] = self.state[0][i] * self.state[1][i]
            if self.state[2][i] < 0:
                self.state[2][i] = 0
            if other.state[2][i] > self.state[0][i] * self.state[1][i]:
                other.state[2][i] = self.state[0][i] * self.state[1][i]
            if other.state[2][i] < 0:
                other.state[2][i] = 0

        self.fit = None
        other.fit = None

    def mutate(self):
        self.mutateMutRate()  # update mutation rate

        for i in range(self.nLength):
            self.state[0][i] = self.state[0][i] + self.mutRate[0] * self.normprng.normalvariate(0, 1)
            if self.state[0][i] > 1-self.minNorthGreenRatio: self.state[0][i] = 1-self.minNorthGreenRatio
            if self.state[0][i] < self.minNorthGreenRatio: self.state[0][i] = self.minNorthGreenRatio

            self.state[1][i] = self.state[1][i] + \
                               (self.maxIntersectionTime - self.minIntersectionTime) * self.mutRate[1] \
                               * self.normprng.normalvariate(0, 1)
            if self.state[1][i] > self.maxIntersectionTime:
                self.state[1][i] = self.maxIntersectionTime
            if self.state[1][i] < self.minIntersectionTime:
                self.state[1][i] = self.minIntersectionTime

            self.state[2][i] = self.state[2][i] + \
                               (self.state[0][i] * self.state[1][i] - 0) * self.mutRate[2] \
                               * self.normprng.normalvariate(0, 1)
            if self.state[2][i] > self.state[0][i] * self.state[1][i]:
                self.state[2][i] = self.state[0][i] * self.state[1][i]
            if self.state[2][i] < 0:
                self.state[2][i] = 0

        self.fit = None

    def evaluateFitness(self):
        if self.fit is None:
            self.fit = self.__class__.fitFunc(self.idleTimes)

    def setIdleTimes(self, cars):
        self.idleTimes = []
        for car in cars:
            self.idleTimes.append(car.idleTime)
        # update fitness values
        self.fit = self.__class__.fitFunc(self.idleTimes)

    def __str__(self):
        str_ind = ''
        params = ['NorthGreenRatio', 'IntersectionTime', 'ToggleTime']
        for k in range(len(params)):
            str_ind += '\t' + params[k] + ': ' + str(self.state[k]) + '\t' + \
                      '%0.8e' % self.fit + '\t' + '%0.8e' % self.mutRate[k]
        return str_ind
