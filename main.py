#
# main.py
#
#

import sys

from modules.MapFunctions import createMap
from modules.Intersection import Intersection
from ea.ev3 import EV3_Config, ev3


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

        I1 = Intersection(name='1', N_connections=3)
        I2 = Intersection(name='2', N_connections=3)
        I3 = Intersection(name='3', N_connections=3)
        I4 = Intersection(name='4', N_connections=3)
        I5 = Intersection(name='5')

#        I1 = Intersection(name='1', N_connections=4)
#        I2 = Intersection(name='2', N_connections=4)
#        I3 = Intersection(name='3', N_connections=4)
#        I4 = Intersection(name='4', N_connections=4)


        # todo: intersections can be either with three connections (3-way-intersection) or with four connections (4-way-intersection).
        #  If both types exist, there has to be a multiple of four 3-way-intersections, otherwise not all the streets can be connected.
        #  -> implement try - error..

        streets = createMap([I1, I2, I3, I4, I5])

        intersections = [I1, I2, I3, I4, I5]
        nLength = len(intersections)

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
        ev3(cfg, intersections, streets)


if __name__ == '__main__':
    main()
