#
# ev3a.py: An elitist (mu+mu) generational-with-overlap EA
#
#
# To run: python ev3a.py --input my_params.cfg
#
# Basic features of ev3a:
#   - Supports self-adaptive mutation
#   - Uses binary tournament selection for mating pool
#   - Uses elitist truncation selection for survivors
#   - Supports IntegerVector and Multivariate Individual types
#

import yaml
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from random import Random
import matplotlib.pyplot as plt

from ea.Population import *
from ea.Evaluator import *
from modules.MapFunctions import generateCars, simulateTraffic, setLightParams


# EV3 Config class
class EV3_Config:
    """
    EV3 configuration class
    """
    # class variables
    sectionName = 'EV3'
    options = {'populationSize': (int, True),
               'generationCount': (int, True),
               'randomSeed': (int, True),
               'crossoverFraction': (float, True),
               'trafficLightA': (float, False),
               'evaluator': (str, False),
               'minIntersectionTime': (float, False),
               'maxIntersectionTime': (float, False),
               'minNorthGreenRatio': (float, False)}

    # constructor
    def __init__(self, inFileName, nLength):
        # read YAML config and get EV3 section
        infile = open(inFileName, 'r')
        ymlcfg = yaml.safe_load(infile)
        infile.close()
        eccfg = ymlcfg.get(self.sectionName, None)
        if eccfg is None:
            raise Exception('Missing {} section in cfg file'.format(self.sectionName))

        # number of traffic light parameters
        self.nLength = nLength

        # iterate over options
        for opt in self.options:
            if opt in eccfg:
                optval = eccfg[opt]

                # verify parameter type
                if type(optval) != self.options[opt][0]:
                    raise Exception('Parameter "{}" has wrong type'.format(opt))

                # create attributes on the fly
                setattr(self, opt, optval)
            else:
                if self.options[opt][1]:
                    raise Exception('Missing mandatory parameter "{}"'.format(opt))
                else:
                    setattr(self, opt, None)

    # string representation for class data
    def __str__(self):
        return str(yaml.dump(self.__dict__, default_flow_style=False))


# Print some useful stats to screen
def printStats(pop, gen):
    print('Generation:', gen)
    avgval = 0
    maxval = pop[0].fit
    maxvalState = pop[0].state
    mutRate = pop[0].mutRate
    best_individual = pop[0]
    i = 0
    for ind in pop:
        i += 1
        avgval += ind.fit
        if ind.fit > maxval:  # the elements were sorted to begin with, so this will never be the case
            maxval = ind.fit
            best_individual = ind
            maxvalState = ind.state
            mutRate = ind.mutRate
        print(ind)

    print('Max fitness', maxval)
    print('MutRate', mutRate)
    print('Avg fitness', avgval / len(pop))
    print('Max Value State ' + str(maxvalState[0]) + '\t' +
          str(maxvalState[1]) + '\t' + str(maxvalState[2]) + '\t')
    print('Avg idleTime:', np.nanmean(np.array(best_individual.idleTimes)))
    print('')


# EV3:
#            
def ev3(cfg, intersections, streets):
    # start random number generators
    uniprng = Random()
    uniprng.seed(cfg.randomSeed)
    normprng = Random()
    normprng.seed(cfg.randomSeed + 101)

    # set static params on classes
    # (probably not the most elegant approach, but let's keep things simple...)
    Individual.uniprng = uniprng
    Individual.normprng = normprng
    Population.uniprng = uniprng
    Population.crossoverFraction = cfg.crossoverFraction

    TrafficLightExp.A = cfg.trafficLightA
    TrafficLightLin.A = cfg.trafficLightA

    MultivariateIndividual.nLength = cfg.nLength
    MultivariateIndividual.minIntersectionTime = cfg.minIntersectionTime
    MultivariateIndividual.maxIntersectionTime = cfg.maxIntersectionTime
    MultivariateIndividual.minNorthGreenRatio = cfg.minNorthGreenRatio

    if cfg.evaluator == 'trafficLightExp':
        MultivariateIndividual.fitFunc = TrafficLightExp.fitnessFunc
    elif cfg.evaluator == 'trafficLightLin':
        MultivariateIndividual.fitFunc = TrafficLightLin.fitnessFunc
    elif cfg.evaluator == 'trafficLightSimple':
        MultivariateIndividual.fitFunc = TrafficLightSimple.fitnessFunc
    else:
        raise Exception('Evaluator not found')

    MultivariateIndividual.learningRate = 1.0 / math.sqrt(cfg.nLength)

    Population.individualType = MultivariateIndividual

    # create initial Population (random initialization)
    population = Population(cfg.populationSize)

    cars = generateCars(streets, 400)
    # evolution main loop
    X = np.arange(0, cfg.generationCount)
    bestFit = np.arange(0, cfg.generationCount)
    Y = np.arange(0, cfg.populationSize)
    Z = np.zeros((len(Y), len(X)))

    for i in range(cfg.generationCount):
        simTime = 1500
        TrafficLightExp.simTime = simTime
        TrafficLightLin.simTime = simTime

        for ind in population:

            cars_ind = []
            for car in cars:
                car_ind = copy.copy(car)
                cars_ind.append(car_ind)

            for car_ind in cars_ind:
                car_ind.position.set_car(car_ind)

            setLightParams(intersections, ind.state)
            simulateTraffic(intersections, cars_ind, simTime)

            ind.setIdleTimes(cars_ind)

            for car in cars_ind:
                car.position.remove_car()

        maxval = population[0].fit
        for p in range(len(population)):
            Z[p][i] = population[p].fit
            if population[p].fit > maxval:
                maxval = population[p].fit

        bestFit[i] = maxval

        # create initial offspring population by copying parent pop
        offspring = population.copy()

        if i == 0:
            # print initial pop stats
            printStats(offspring, 0)

        # select mating pool
        offspring.conductTournament()

        # perform crossover
        offspring.crossover()

        # random mutation
        offspring.mutate()

        # update fitness values
        offspring.evaluateFitness()

        # survivor selection: elitist truncation using parents+offspring
        population.combinePops(offspring)
        population.truncateSelect(cfg.populationSize)

        # print population stats
        printStats(population, i + 1)

    f = plt.figure(0)
    ax = f.add_subplot(111, projection='3d')
    Xp, Yp = np.meshgrid(X, Y)
    ax.plot_surface(Xp, Yp, Z)
    ax.set_title('EA Traffic simulation')
    ax.set_xlabel('Generation count')
    ax.set_ylabel('Population')
    ax.set_zlabel('Fitness')

    plt.figure(1)
    plt.plot(X, bestFit)
    plt.title('EA Traffic simulation')
    plt.xlabel('Generation count')
    plt.ylabel('Best Fitness')
    plt.show()

    return [population[0].state[0], population[0].state[1], population[0].state[2]]
