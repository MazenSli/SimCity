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
        
#        I1 = Intersection(name='Shilin')
#        I2 = Intersection(name='Zhongshan')
#        I3 = Intersection(name='Beimen')
#        I4 = Intersection(name='Longshan')

        I1 = Intersection(name='1')
        I2 = Intersection(name='2')
        I3 = Intersection(name='3')
        I4 = Intersection(name='4')

        streets = createMap([I1, I2, I3, I4])

        intersections = [I1, I2, I3, I4]
        nLength = len(intersections) * 3

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
        ev3(cfg, intersections)


if __name__ == '__main__':
    main()
