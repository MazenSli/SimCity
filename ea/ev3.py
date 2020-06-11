#
# ev3.py: An elitist (mu+mu) generational-with-overlap EA
#
#
# Basic features of ev3a:
#   - Supports self-adaptive mutation
#   - Uses binary tournament selection for mating pool
#   - Uses elitist truncation selection for survivors
#   - Multivariate Individual types
#

from random import Random

import matplotlib.pyplot as plt
import yaml

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
               'evaluator': (str, False),
               'minIntersectionTime': (float, False),
               'maxIntersectionTime': (float, False),
               'minNorthGreenRatio': (float, False)}

    # constructor
    def __init__(self, inFileName, nLength, N_cars):
        # read YAML config and get EV3 section
        infile = open(inFileName, 'r')
        ymlcfg = yaml.safe_load(infile)
        infile.close()
        eccfg = ymlcfg.get(self.sectionName, None)
        if eccfg is None:
            raise Exception('Missing {} section in cfg file'.format(self.sectionName))

        # number of intersections
        self.nLength = nLength
        self.N_cars = N_cars

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

    for ind in pop:
        avgval += ind.fit
        print(ind)

    print('Max fitness', maxval)
    print('MutRate', mutRate)
    print('Avg fitness', avgval / len(pop))
    print('Max Value State ' + str(maxvalState[0]) + '\t' +
          str(maxvalState[1]) + '\t' + str(maxvalState[2]) + '\t')
    print('Avg idleTime:', np.nanmean(np.array(best_individual.idleTimes)))
    print('')


# Plot EV results
def plotEv(X, Y, Z, bestFit):
    # 3D plot
    # X: Generation count
    # Y: Population
    # Z: Fitness value
    f = plt.figure(0)
    ax = f.add_subplot(111, projection='3d')
    Xp, Yp = np.meshgrid(X, Y)
    ax.plot_surface(Xp, Yp, Z)
    ax.set_title('EA Traffic simulation')
    ax.set_xlabel('Generation count')
    ax.set_ylabel('Population')
    ax.set_zlabel('Fitness')

    # 2D plot
    # X: Generation count
    # Z: Best fitness value
    plt.figure(1)
    plt.plot(X, bestFit)
    plt.title('EA Traffic simulation')
    plt.xlabel('Generation count')
    plt.ylabel('Best Fitness')
    plt.show()


def ev3(cfg, intersections, streets):
    """
    EV3

    Args:
        cfg: configuration parameters
        intersections: list of intersection objects
        streets: list of street objects

    Returns:
        state: state of individual with best fitness value after the last generation
        (north green ratios,  intersection times and toggle times for all intersections)
    """

    # start random number generators
    uniprng = Random()
    uniprng.seed(cfg.randomSeed)
    normprng = Random()
    normprng.seed(cfg.randomSeed + 101)

    # set static params on classes
    Individual.uniprng = uniprng
    Individual.normprng = normprng
    Population.uniprng = uniprng
    Population.crossoverFraction = cfg.crossoverFraction

    TrafficLightExp.A = cfg.trafficLightA

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

    cars = generateCars(streets, cfg.N_cars)
    # evolution main loop

    X = np.arange(0, cfg.generationCount)
    Y = np.arange(0, cfg.populationSize)
    Z = np.zeros((len(Y), len(X)))
    bestFit = np.arange(0, cfg.generationCount)

    # evolution main loop
    for i in range(cfg.generationCount):
        simTime = 2000  # simTime determines how many time steps the simulation runs, this value should be
                        # adjusted whenever the length of the streets is changed
        TrafficLightExp.simTime = simTime

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

        # store best fitness elements for plot
        for p in range(len(population)):
            Z[p][i] = population[p].fit
        bestFit[i] = population[0].fit

        # create initial offspring population by copying parent pop
        offspring = population.copy()

        # print initial population stats
        if i == 0:
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

    plotEv(X, Y, Z, bestFit)

    return [population[0].state[0], population[0].state[1], population[0].state[2]]
