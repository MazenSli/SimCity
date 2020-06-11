#
# Visualization.py
#
#
import numpy as np
import os
import time
import pygame as game
import random
import copy

from modules.Intersection import Intersection
from modules.MapFunctions import createMap, createExampleMap, generateCars, setLightParams

# 1920x1080
time_per_frame = 0.016667  # seconds


class WindowWrapper:
    def __init__(self):
        (self.width, self.height) = (1920, 1080)
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1920 / 2 - self.width / 2, 1080 / 2 - self.height / 2)
        game.display.init()
        self.screen = game.display.set_mode((self.width, self.height))
        game.display.flip()
        self.running = True


class Point:
    def __init__(self, x_loc, y_loc):
        self.x_loc = x_loc
        self.y_loc = y_loc

    def add_vector(self, vector):
        self.x_loc = self.x_loc + vector.x_loc
        self.y_loc = self.y_loc + vector.y_loc

        return self


class SimIntersection:
    def __init__(self, x_loc, y_loc, intersection, color_r=150, color_g=150, color_b=150):
        self.location = np.array((x_loc, y_loc))
        self.color = game.Color(color_r, color_g, color_b)
        self.intersection = intersection
        self.width = 60
        self.height = 60
        self.enterExit_width = 10
        self.enterExit_height = 10
        self.rect = game.Rect(x_loc - self.width / 2, y_loc - self.height / 2, self.width, self.height)
        self.CONST = 6
        self.entrancePoints = {
            'north': Point(x_loc - self.width / self.CONST, y_loc - self.height / 2),
            'east': Point(x_loc + self.width / 2, y_loc - self.height / self.CONST),
            'south': Point(x_loc + self.width / self.CONST, y_loc + self.height / 2),
            'west': Point(x_loc - self.width / 2, y_loc + self.height / self.CONST)
        }
        self.exitPoints = {
            'north': Point(x_loc + self.width / self.CONST, y_loc - self.height / 2),
            'east': Point(x_loc + self.width / 2, y_loc + self.height / self.CONST),
            'south': Point(x_loc - self.width / self.CONST, y_loc + self.height / 2),
            'west': Point(x_loc - self.width / 2, y_loc - self.height / self.CONST)
        }
        self._init_blocks()

    def set_location(self, loc_x, loc_y):
        self.location = np.array((loc_x, loc_y))

    def draw(self, window):
        game.draw.rect(window.screen, self.color, self.rect)
        light_pos = copy.deepcopy(self.entrancePoints)
        for direction, point in light_pos.items():
            if direction == 'north':
                light_pos[direction] = point.add_vector(Point(-15, -9))
            if direction == 'east':
                light_pos[direction] = point.add_vector(Point(7, -15))
            if direction == 'south':
                light_pos[direction] = point.add_vector(Point(14, 7))
            if direction == 'west':
                light_pos[direction] = point.add_vector(Point(-9, 13))

        for dir, entrance in self.intersection.intersectionEntranceBlocks.items():
            if entrance.isGreen:
                red_green = game.Color(0, 200, 0)
            else:
                red_green = game.Color(200, 0, 0)
            game.draw.rect(window.screen, red_green, game.Rect(light_pos[dir].x_loc - self.enterExit_width / 2,
                                                               light_pos[dir].y_loc - self.enterExit_height / 2,
                                                               self.enterExit_width * 1.2, self.enterExit_height * 1.2))
        for dir, entrance in self.intersection.intersectionEntranceBlocks.items():
            game.draw.rect(window.screen, game.Color(0, 0, 0),
                           game.Rect(entrance.visualizationPoint.x_loc - self.enterExit_width / 2,
                                     entrance.visualizationPoint.y_loc - self.enterExit_height / 2,
                                     self.enterExit_width, self.enterExit_height))
        for dir, iExit in self.exitPoints.items():
            game.draw.rect(window.screen, game.Color(0, 0, 0),
                           game.Rect(iExit.x_loc - self.enterExit_width / 2, iExit.y_loc - self.enterExit_height / 2,
                                     self.enterExit_width, self.enterExit_height))

    def _init_blocks(self):
        for dir, block in self.intersection.intersectionEntranceBlocks.items():
            block.visualizationPoint = self.entrancePoints[dir]
        for dir, block in self.intersection.intersectionExitBlocks.items():
            block.visualizationPoint = self.exitPoints[dir]
        if self.intersection.N_connections == 3:
            self.entrancePoints.pop(self.intersection.missing_dir)
            self.exitPoints.pop(self.intersection.missing_dir)


def init_setup_blockPositions(streets):
    for street in streets:
        for lane in street.lanes:
            i = 0
            for block in lane.blocks:
                # we already set the visualizationPoints for the first and last block
                if i is 0:
                    i += 1
                    continue
                lane_visual_length_x = (lane.blocks[lane.length - 1].visualizationPoint.x_loc - lane.blocks[
                    0].visualizationPoint.x_loc)
                lane_visual_length_y = (lane.blocks[lane.length - 1].visualizationPoint.y_loc - lane.blocks[
                    0].visualizationPoint.y_loc)
                block_vector = Point(lane_visual_length_x * i / (lane.length - 1),
                                     lane_visual_length_y * i / (lane.length - 1))
                block.visualizationPoint = block_vector.add_vector(lane.blocks[0].visualizationPoint)
                i += 1
                if i is lane.length - 1:
                    break


def draw_streets(streets, window):
    block_color = game.Color(120, 140, 210)
    block_radius = 3
    car_color = game.Color(255, 165, 0)
    car_radius = 6

    for street in streets:
        for lane in street.lanes:
            game.draw.line(window.screen, game.Color(120, 140, 210),
                           (lane.blocks[0].visualizationPoint.x_loc, lane.blocks[0].visualizationPoint.y_loc), (
                           lane.blocks[lane.length - 1].visualizationPoint.x_loc,
                           lane.blocks[lane.length - 1].visualizationPoint.y_loc), 2)
            for block in lane.blocks:
                if not block.car:
                    game.draw.circle(window.screen, block_color,
                                     (int(block.visualizationPoint.x_loc), int(block.visualizationPoint.y_loc)),
                                     block_radius)
            for block in lane.blocks:
                if block.car:
                    game.draw.circle(window.screen, car_color,
                                     (int(block.visualizationPoint.x_loc), int(block.visualizationPoint.y_loc)),
                                     car_radius)

    # todo: something like this would be cool for performance while visualizing but not priority.
    '''def init_screen(window, intersections, streets): 
        window.screen.fill((0, 0, 0))
        for i in intersections:
            i.draw(window)
        draw_streets(streets, window)
        game.display.flip()
    
        return game.display.get_surface()'''


def run(simIntersections, streets, cars, window):
    t0 = time.perf_counter()
    time_counter = 0
    a = 0
    render(window, simIntersections, streets)
    # traffic_grid = init_screen(window, simIntersections, streets)
    while window.running:
        event_update(window)
        if (time.perf_counter() - t0) >= time_per_frame:
            # update
            time_counter += 1
            time_past = (time.perf_counter() - t0)
            # update_physics(time_past)
            t0 = time.perf_counter()
            if time_counter >= 2:
                # slower event...
                a += 1
                print(a)
                if a >= 2000:
                    window.running = False
                #for car in cars:
                #    print('car position:', car.position, '   position of care hasCar? - ', car.position.car)
                render(window, simIntersections, streets)  # this function is a hardcore bottleneck
                for simInter in simIntersections:
                    simInter.intersection.process_intersection()
                for car in cars:
                    car.move_laneCar()
                for car in cars:
                    car.isProcessed = False
                time_counter = 0


def event_update(window):
    for event in game.event.get():
        if event.type == game.QUIT:
            window.running = False


def render(window, intersections, streets):
    window.screen.fill((0, 0, 0))
    for i in intersections:
        i.draw(window)
    draw_streets(streets, window)
    game.display.flip()


def visualize(intersections, streets, cars):
    screen_width = 1920
    screen_height = 1080

    window = WindowWrapper()

    simIntersections = [SimIntersection(int(1 * screen_width / 4), 1 * screen_height / 4, intersections[0]),
                        SimIntersection(int(3 * screen_width / 4), 1 * screen_height / 4 - 150, intersections[1]),
                        SimIntersection(int(1 * screen_width / 2), 2 * screen_height / 4, intersections[2]),
                        SimIntersection(int(1 * screen_width / 4) - 150, 3 * screen_height / 4 - 150, intersections[3]),
                        SimIntersection(int(3 * screen_width / 4) - 150, 3 * screen_height / 4, intersections[4])
                        ]

    init_setup_blockPositions(streets)

    run(simIntersections, streets, cars, window)


def visualize_example():
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
    cars = generateCars(streets, 700)

    screen_width = 1920
    screen_height = 1080

    window = WindowWrapper()
    simIntersections = [SimIntersection(int(2 * screen_width / 6)-100, 1 * screen_height / 6, intersections[0]),
                        SimIntersection(int(3 * screen_width / 6), 1 * screen_height / 6, intersections[1]),
                        SimIntersection(int(4 * screen_width / 6)+100, 1 * screen_height / 6, intersections[2]),
                        SimIntersection(int(1 * screen_width / 6)-150, 2 * screen_height / 4, intersections[3]),
                        SimIntersection(int(2 * screen_width / 6)-100, 2 * screen_height / 4, intersections[4]),
                        SimIntersection(int(3 * screen_width / 6), 2 * screen_height / 4, intersections[5]),
                        SimIntersection(int(4 * screen_width / 6)+100, 2 * screen_height / 4, intersections[6]),
                        SimIntersection(int(5 * screen_width / 6)+150, 2 * screen_height / 4, intersections[7]),
                        SimIntersection(int(2 * screen_width / 6)-100, 5 * screen_height / 6, intersections[8]),
                        SimIntersection(int(3 * screen_width / 6), 5 * screen_height / 6, intersections[9]),
                        SimIntersection(int(4 * screen_width / 6)+100, 5 * screen_height / 6, intersections[10])]

    init_setup_blockPositions(streets)

    run(simIntersections, streets, cars, window)

    a = []
    i = 0
    for car in cars:
        i += 1
        print('car', i, '~ ~ ~', 'idleTime: <> <>', car.idleTime)
        a.append(car.idleTime)
    print(np.mean(a))


def visualize_diamond(intersections, streets, states=None):

    for street in streets:
        for lane in street.lanes:
            for block in lane.blocks:
                block.remove_car()

    cars = generateCars(streets, 600)

    screen_width = 1920
    screen_height = 1080

    setLightParams(intersections, states)

    window = WindowWrapper()
    simIntersections = [SimIntersection(int(2 * screen_width / 6)-100, 1 * screen_height / 6, intersections[0]),
                        SimIntersection(int(3 * screen_width / 6), 1 * screen_height / 6, intersections[1]),
                        SimIntersection(int(4 * screen_width / 6)+100, 1 * screen_height / 6, intersections[2]),
                        SimIntersection(int(1 * screen_width / 6)-150, 2 * screen_height / 4, intersections[3]),
                        SimIntersection(int(2 * screen_width / 6)-100, 2 * screen_height / 4, intersections[4]),
                        SimIntersection(int(3 * screen_width / 6), 2 * screen_height / 4, intersections[5]),
                        SimIntersection(int(4 * screen_width / 6)+100, 2 * screen_height / 4, intersections[6]),
                        SimIntersection(int(5 * screen_width / 6)+150, 2 * screen_height / 4, intersections[7]),
                        SimIntersection(int(2 * screen_width / 6)-100, 5 * screen_height / 6, intersections[8]),
                        SimIntersection(int(3 * screen_width / 6), 5 * screen_height / 6, intersections[9]),
                        SimIntersection(int(4 * screen_width / 6)+100, 5 * screen_height / 6, intersections[10])]

    init_setup_blockPositions(streets)

    run(simIntersections, streets, cars, window)

    a = []
    i = 0
    for car in cars:
        i += 1
        print('car', i, '~ ~ ~', 'idleTime: <> <>', car.idleTime)
        a.append(car.idleTime)
    print(np.mean(a))


#visualize_example()

'''I1 = Intersection()
I2 = Intersection()
I3 = Intersection()
I4 = Intersection()

intersections = [I1, I2, I3, I4]

streets = createMap(intersections)

intersections = [I1, I2, I3, I4]

cars = generateCars(streets)

visualize(intersections, streets, cars)
'''
'''I1 = Intersection(name='1', N_connections=3)
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

cars = generateCars(streets, 200)
visualize(intersections, streets, cars)

a = []
i = 0
for car in cars:
    i += 1
    print('car', i, '~ ~ ~', 'idleTime: <> <>', car.idleTime)
    a.append(car.idleTime)
print(np.mean(np.array(a)))'''
