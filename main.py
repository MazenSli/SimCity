#
# main.py
#
#

import sys

from modules.MapFunctions import createMap, createExampleMap
from modules.Intersection import Intersection
from ea.ev3 import EV3_Config, ev3
from modules.Visualization import visualize_diamond
from copy import deepcopy

#
# Main entry point
#
def main(argv=None):
    if argv is None:
        argv = sys.argv

        sys.setrecursionlimit(10000)
        
#        I1 = Intersection(name='Shilin')
#        I2 = Intersection(name='Zhongshan')
#        I3 = Intersection(name='Beimen')
#        I4 = Intersection(name='Longshan')

#        I1 = Intersection(name='1', N_connections=3)
#        I2 = Intersection(name='2', N_connections=3)
#        I3 = Intersection(name='3', N_connections=3)
#        I4 = Intersection(name='4', N_connections=3)
#        I5 = Intersection(name='5')

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
        streets = createExampleMap(intersections, intersection_matrix)

        nLength = len(intersections)

        # todo: intersections can be either with three connections (3-way-intersection) or with four connections (4-way-intersection).
        #  If both types exist, there has to be a multiple of four 3-way-intersections, otherwise not all the streets can be connected.
        #  -> implement try - error..

#        streets = createExampleMap([I1, I2, I3, I4, I5])

        for i in intersections:
            print(i)
            for street in i.streets:
                print(street)
                for lane in street.lanes:
                    print(lane)

        # Get EV3 config params
        cfg = EV3_Config('ea/my_params.cfg', nLength)

        # print config params
        print(cfg)

        # run EV3
        states = ev3(cfg, intersections, streets)

        visualize_diamond(intersections, streets, states)




if __name__ == '__main__':
    main()
