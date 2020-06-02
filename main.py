#
# main.py
#
#

from builtins import Exception
import optparse
import sys
from modules.Block import Block
from modules.Intersection import Intersection
from modules.Street import Street
from random import randrange
from ea.ev3 import EV3_Config, ev3


def createMap(intersections):
    streets = []
    dict_inter = {}

    for d in range(len(intersections)):
        dict_inter[intersections[d]] = ['north', 'east', 'south', 'west']

#    names = ['Dunhua Rd.', 'Fuxing Rd.', 'Guangfu Rd.', 'Heping Rd.',
#             'Keelung Rd.', 'Roosevelt Rd.', 'Xinsheng Rd.', 'Xinyi Rd.',
#             'Zhongshan Rd', 'Zhongxiao Rd.', 'Anping Old St.',
#             'Ciaonan St.', 'Xinhua Old St.', 'Fukang St.', 'Hou St.',
#             'Huagang Rd.', 'Jingfeng St.']

    names = ['A', 'B', 'C', 'D',
             'E', 'F', 'G', 'H',
             'I', 'J', 'K',
             'L', 'M', 'N', 'O',
             'P', 'Q']

    # Create and add streets
    for i in range(len(intersections)):
        inter1 = intersections.pop(randrange(len(intersections)))

        if len(intersections) == 0:
            break

        while len(dict_inter[inter1]) > 0:
            inter1_dir_nr = randrange(len(dict_inter[inter1]))
            inter1_dir = dict_inter[inter1].pop(inter1_dir_nr)

            inter2_nr = randrange(len(intersections))
            # pick intersection with min streets to balance the map
            for j in range(len(intersections)):
                if len(intersections[inter2_nr]) > len(intersections[j]):
                    inter2_nr = j
            inter2 = intersections[inter2_nr]

            inter2_dir_nr = randrange(len(dict_inter[inter2]))
            inter2_dir = dict_inter[inter2].pop(inter2_dir_nr)

            length = randrange(4, 12)
            name = names.pop(randrange(len(names)))

            streets.append(Street(length=length, startIs=inter1, endIs=inter2, name=name))
            inter1.addStreet(street=streets[-1], direction=inter1_dir)
            inter2.addStreet(street=streets[-1], direction=inter2_dir)

    return streets


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

        for i in intersections:
            print(i)
            for street in i.streets:
                print(street)
                for lane in street.lanes:
                    print(lane)

        # Get EV3 config params
        cfg = EV3_Config(intersections, 'ea/my_params.cfg')

        # print config params
        print(cfg)

        # run EV3
        ev3(cfg)


if __name__ == '__main__':
    main()
