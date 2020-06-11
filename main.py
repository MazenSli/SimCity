#
# main.py
#
# To run: python main.py
#

import sys

from modules.MapFunctions import createExampleMap, createMap
from modules.Intersection import Intersection
from modules.Visualization import visualize_diamond, visualize
from ea.ev3 import EV3_Config, ev3
from random import uniform

#
# Main entry point
#


def diamond_intersection_setup(street_length_min, street_length_max):
    I1 = Intersection(name='10', N_connections=3, missing_dir='north')
    I2 = Intersection(name='20', N_connections=3, missing_dir='north')
    I3 = Intersection(name='30', N_connections=3, missing_dir='north')
    I4 = Intersection(name='01', N_connections=3, missing_dir='west')
    I5 = Intersection(name='11', N_connections=4)
    I6 = Intersection(name='21', N_connections=4)
    I7 = Intersection(name='31', N_connections=4)
    I8 = Intersection(name='41', N_connections=3, missing_dir='east')
    I9 = Intersection(name='12', N_connections=3, missing_dir='south')
    I10 = Intersection(name='22', N_connections=3, missing_dir='south')
    I11 = Intersection(name='32', N_connections=3, missing_dir='south')

    intersection_matrix = []
    col1 = [None, I4, None]
    col2 = [I1, I5, I9]
    col3 = [I2, I6, I10]
    col4 = [I3, I7, I11]
    col5 = [None, I8, None]

    intersection_matrix.append(col1)
    intersection_matrix.append(col2)
    intersection_matrix.append(col3)
    intersection_matrix.append(col4)
    intersection_matrix.append(col5)

    intersections = [I1, I2, I3, I4, I5, I6, I7, I8, I9, I10, I11]
    nLength = len(intersections)

    # create streets
    streets = createExampleMap(intersections, intersection_matrix, street_length_min, street_length_max)

    return intersections, streets, nLength

def intersection_setup(street_length_min, street_length_max):
    # IMPORTANT: intersections can be either with three connections (3-way-intersection) or with four connections (4-way-intersection).
    #  If both types exist, there has to be a multiple of four 3-way-intersections, otherwise not all the streets can be connected.

    # one allowed intersection setup for visualize function:
    # (has to consist of five intersections, they could also be all with N_connections = 4)
    I1 = Intersection(name='1', N_connections=3)
    I2 = Intersection(name='2', N_connections=3)
    I3 = Intersection(name='3', N_connections=3)
    I4 = Intersection(name='4', N_connections=3)
    I5 = Intersection(name='5', N_connections=4)

    intersections = [I1, I2, I3, I4, I5]

    nLength = len(intersections)

    # create streets
    streets = createMap(intersections, street_length_min, street_length_max)

    intersections = [I1, I2, I3, I4, I5]

    return intersections, streets, nLength


def main(argv=None):
    if argv is None:
        argv = sys.argv

        # for copy function
        sys.setrecursionlimit(1000000)

        N_cars = 600
        street_length_min = 20
        street_length_max = 100
        # simTime determines how many time steps the simulation runs, this value should be
        # adjusted whenever the length of the streets is changed. It will affect the runtime and performance of the EA
        simTime = 2000  # A reasonable value is at least the average street length times 15

        #intersections, streets, nLength = intersection_setup(street_length_min, street_length_max)
        intersections, streets, nLength = diamond_intersection_setup(street_length_min, street_length_max)

        # print generated intersections, street and lanes
        for i in intersections:
            print(i)
            for street in i.streets:
                print(street)
                for lane in street.lanes:
                    print(lane)

        # Get EV3 config params
        cfg = EV3_Config('ea/my_params.cfg', nLength, N_cars)

        # print config params
        print(cfg)

        # run EV3
        states = ev3(cfg, intersections, streets, simTime)

        # visualize map
        #visualize(intersections, streets, N_cars, states)
        visualize_diamond(intersections, streets, N_cars, states)


        # for comparison we can visualize the same traffic network without optimization
        #-----------------------------------------------------------------------------#
        #state_default = [[] for j in range(3)]
        #for i in range(nLength):
        #    state_default[0].append(0.5)
        #    state_default[1].append(60)
        #    state_default[2].append(uniform(0, 30))

        ##visualize(intersections, streets, N_cars, state_default)
        #visualize_diamond(intersections, streets, N_cars, state_default)
        # -----------------------------------------------------------------------------#

if __name__ == '__main__':
    main()
