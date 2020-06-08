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
from copy import deepcopy
from random import Random

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
               'minIntersectionTime': (float, False),
               'maxIntersectionTime': (float, False)}

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
    mutRate = pop[0].mutRate
    for ind in pop:
        avgval += ind.fit
        if ind.fit > maxval:
            maxval = ind.fit
            mutRate = ind.mutRate
        print(ind)

    print('Max fitness', maxval)
    print('MutRate', mutRate)
    print('Avg fitness', avgval / len(pop))
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

    MultivariateIndividual.nLength = cfg.nLength
    MultivariateIndividual.minIntersectionTime = cfg.minIntersectionTime
    MultivariateIndividual.maxIntersectionTime = cfg.maxIntersectionTime
    MultivariateIndividual.fitFunc = TrafficLightExp.fitnessFunc
    MultivariateIndividual.learningRate = 1.0 / math.sqrt(cfg.nLength)

    Population.individualType = MultivariateIndividual

    # create initial Population (random initialization)
    population = Population(cfg.populationSize)

    # print initial pop stats
    printStats(population, 0)

    # evolution main loop
    for i in range(cfg.generationCount):

        cars = generateCars(streets, 60)
        simTime = 60
        TrafficLightExp.simTime = simTime

        for ind in population:
            cars_ind = deepcopy(cars)

            setLightParams(intersections, ind.state)
            simulateTraffic(intersections, cars_ind, simTime)

            ind.setIdleTimes(cars_ind)
            for car in cars_ind:
                car.position.remove_car()
            for car in cars:
                car.position.remove_car()

        # create initial offspring population by copying parent pop
        offspring = population.copy()

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

