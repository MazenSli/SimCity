#
# MapFunctions.py
#
#

from random import randrange
from modules.Street import Street
from modules.Car import Car
from modules.Lane import Lane
from modules.IntersectionBlock import IntersectionBlock
from modules.Block import Block


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


def generateCars(intersections):
    # todo

    cars = []

    for i in intersections:
        for street in i.streets:
            nCars = len(street)
            for lane in street.lanes:
                pass

    return cars


def setTrafficLightParameters(intersections, state):
    pass


def simulateTraffic(intersections, cars):
    # todo
    pass
