#
# MapFunctions.py
#
#

from random import randrange, shuffle
from modules.Street import Street
from modules.Car import Car
import copy
from modules.Lane import Lane
from modules.IntersectionBlock import IntersectionBlock
from modules.Block import Block


def createMap(intersections):
    streets = []
    dict_inter = {}

    for d in range(len(intersections)):
        dict_inter[intersections[d]] = intersections[d].directions

    print(dict_inter)

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
    # shuffle intersections (for some randomness) then arrange intersections, so that the 4-way-intersections come first
    shuffle(intersections)
    for i in range(len(intersections)):
        if len(intersections[i].directions) == 4:
            inter = intersections.pop(i)
            intersections.insert(0, inter)
    for i in range(len(intersections)):
        inter1 = intersections.pop(0)   # we can always pop the first element, since the list was already shuffled

        if len(intersections) == 0:
            break

        while len(dict_inter[inter1]) > 0:
            inter1_dir_nr = randrange(len(dict_inter[inter1]))      # nr = index
            inter1_dir = dict_inter[inter1].pop(inter1_dir_nr)

            inter2_nr = randrange(len(intersections))
            # pick intersection with min streets to balance the map
            for j in range(len(intersections)):
                if len(intersections[inter2_nr]) > len(intersections[j]):
                    inter2_nr = j
            inter2 = intersections[inter2_nr]

            inter2_dir_nr = randrange(len(dict_inter[inter2]))
            inter2_dir = dict_inter[inter2].pop(inter2_dir_nr)

            length = randrange(22, 44)
            name = names.pop(randrange(len(names)))

            streets.append(Street(length=length, startIs=inter1, endIs=inter2, name=name))
            inter1.addStreet(street=streets[-1], direction=inter1_dir)
            inter2.addStreet(street=streets[-1], direction=inter2_dir)

    return streets

def createExampleMap(intersections, i_mat):
    streets = []
    dict_inter = {}
    for d in range(len(intersections)):
        dict_inter[intersections[d]] = intersections[d].directions

    N_columns = 5
    N_rows = 3

    for row in range(N_rows):
        for col in range(N_columns):
            if (col == 0 and row == 0) or (col == 0 and row == 2) or (col == 0 and row == 1) or (col == 4 and row == 1) or (col == 4 and row == 0) or (col == 4 and row == 2):
                continue
            dict_inter_copy = copy.copy(dict_inter)
            for direction in dict_inter_copy[i_mat[col][row]]:
                if direction == 'north':
                    length = randrange(22, 44)
                    streets.append(Street(length=length, startIs=i_mat[col][row], endIs=i_mat[col][row-1]))
                    i_mat[col][row].addStreet(street=streets[-1], direction='north')
                    i_mat[col][row-1].addStreet(street=streets[-1], direction='south')
                    dict_inter[i_mat[col][row-1]].remove('south')
                if direction == 'east':
                    length = randrange(22, 44)
                    if i_mat[col+1][row] is None:
                        streets.append(Street(length=length, startIs=i_mat[col][row], endIs=i_mat[4][1]))
                        i_mat[col][row].addStreet(street=streets[-1], direction='east')
                        if i_mat[col][row] is i_mat[3][0]:
                            i_mat[4][1].addStreet(street=streets[-1], direction='north')
                            dict_inter[i_mat[4][1]].remove('north')
                        elif i_mat[col][row] is i_mat[3][2]:
                            i_mat[4][1].addStreet(street=streets[-1], direction='south')
                            dict_inter[i_mat[4][1]].remove('south')
                    else:
                        length = randrange(22, 56)
                        streets.append(Street(length=length, startIs=i_mat[col][row], endIs=i_mat[col+1][row]))
                        i_mat[col][row].addStreet(street=streets[-1], direction='east')
                        i_mat[col+1][row].addStreet(street=streets[-1], direction='west')
                        dict_inter[i_mat[col+1][row]].remove('west')
                if direction == 'south':
                    length = randrange(22, 44)
                    streets.append(Street(length=length, startIs=i_mat[col][row], endIs=i_mat[col][row+1]))
                    i_mat[col][row].addStreet(street=streets[-1], direction='south')
                    i_mat[col][row+1].addStreet(street=streets[-1], direction='north')
                    dict_inter[i_mat[col][row+1]].remove('north')
                if direction == 'west':
                    length = randrange(22, 44)
                    if i_mat[col-1][row] is None:
                        streets.append(Street(length=length, startIs=i_mat[col][row], endIs=i_mat[0][1]))
                        i_mat[col][row].addStreet(street=streets[-1], direction='west')
                        if i_mat[col][row] is i_mat[1][0]:
                            i_mat[0][1].addStreet(street=streets[-1], direction='north')
                            dict_inter[i_mat[0][1]].remove('north')
                        elif i_mat[col][row] is i_mat[1][2]:
                            i_mat[0][1].addStreet(street=streets[-1], direction='south')
                            dict_inter[i_mat[0][1]].remove('south')
                    else:
                        length = randrange(22, 44)
                        streets.append(Street(length=length, startIs=i_mat[col][row], endIs=i_mat[col-1][row]))
                        i_mat[col][row].addStreet(street=streets[-1], direction='west')
                        i_mat[col-1][row].addStreet(street=streets[-1], direction='east')
                        dict_inter[i_mat[col-1][row]].remove('east')

    return streets

def generateCars(streets, N_cars=6):
    # todo

    cars = []

    # todo: diese funktion ist schlecht.. es sollte jeder 'intermediate' Block die gleiche Chance haben ein
    #  Auto zu bekommen, momentan sind lanes im Vorteil, die zuerst gefragt werden.
    # todo: NUR ZUM TEST
    leftCars = N_cars
    for s in streets:
        for lane in s.lanes:
            newCar_position = lane.blocks[1]
            newCar = Car(newCar_position)
            cars.append(newCar)
            newCar_position.set_car(newCar)
            leftCars -= 1
            if leftCars == 0:
                return cars


def setTrafficLightParameters(intersections, state):
    pass


def simulateTraffic(intersections, cars):
    # todo
    pass
