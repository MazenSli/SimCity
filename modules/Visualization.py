#
# Visualization.py
#
#
import numpy as np
import os
import time
import pygame as game
import random

from modules.Intersection import Intersection
from modules.Street import Street
from modules.MapFunctions import createMap, createExampleMap, generateCars

# 1920x1080
time_per_frame = 0.016667  # seconds


class WindowWrapper:
    def __init__(self):
        (self.width, self.height) = (1920, 1080)
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1920/2 - self.width / 2, 1080/2 - self.height / 2)
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
    def __init__(self, x_loc, y_loc, intersection, color_r=255, color_g=255, color_b=255):
        self.location = np.array((x_loc, y_loc))
        self.color = game.Color(color_r, color_g, color_b)
        self.intersection = intersection
        self.width = 80
        self.height = 80
        self.enterExit_width = 10
        self.enterExit_height= 10
        self.rect = game.Rect(x_loc-self.width/2, y_loc-self.height/2, self.width, self.height)
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
            'west': Point(x_loc - self.width / 2, y_loc - self.height / self.CONST),
        }
        self._init_blocks()

    def set_location(self, loc_x, loc_y):
        self.location = np.array((loc_x, loc_y))

    def draw(self, window):
        game.draw.rect(window.screen, self.color, self.rect)
        for dir, entrance in self.entrancePoints.items():
            game.draw.rect(window.screen, game.Color(255, 50, 70), game.Rect(entrance.x_loc-self.enterExit_width/2, entrance.y_loc-self.enterExit_height/2, self.enterExit_width, self.enterExit_height))
        for dir, iExit in self.exitPoints.items():
            game.draw.rect(window.screen, game.Color(100, 150, 165), game.Rect(iExit.x_loc-self.enterExit_width/2, iExit.y_loc-self.enterExit_height/2, self.enterExit_width, self.enterExit_height))

    def _init_blocks(self):
        for dir, block in self.intersection.intersectionEntranceBlocks.items():
            block.visualizationPoint = self.entrancePoints[dir]
        for dir, block in self.intersection.intersectionExitBlocks.items():
            block.visualizationPoint = self.exitPoints[dir]


def init_setup_blockPositions(streets, window):
    for street in streets:
        for lane in street.lanes:
            i = 0
            for block in lane.blocks:
                # we already set the visualizationPoints for the first and last block
                if i is 0:
                    i += 1
                    continue
                lane_visual_length_x = (lane.blocks[lane.length-1].visualizationPoint.x_loc - lane.blocks[0].visualizationPoint.x_loc)
                lane_visual_length_y = (lane.blocks[lane.length-1].visualizationPoint.y_loc - lane.blocks[0].visualizationPoint.y_loc)
                block_vector = Point(lane_visual_length_x * i/(lane.length-1), lane_visual_length_y * i/(lane.length-1))
                block.visualizationPoint = block_vector.add_vector(lane.blocks[0].visualizationPoint)
                i += 1
                if i is lane.length-1:
                    break


def draw_streets(streets, window):
    block_color = game.Color(80, 80, 170)
    block_radius = 3
    car_color = game.Color(255, 165, 0)
    car_radius = 6

    for street in streets:
        for lane in street.lanes:
            for block in lane.blocks:
                if block.car:
                    game.draw.circle(window.screen, car_color, (int(block.visualizationPoint.x_loc), int(block.visualizationPoint.y_loc)), car_radius)
                else:
                    game.draw.circle(window.screen, block_color, (int(block.visualizationPoint.x_loc), int(block.visualizationPoint.y_loc)), block_radius)
            game.draw.line(window.screen, game.Color(80, 80, 170), (lane.blocks[0].visualizationPoint.x_loc, lane.blocks[0].visualizationPoint.y_loc), (lane.blocks[lane.length-1].visualizationPoint.x_loc, lane.blocks[lane.length-1].visualizationPoint.y_loc), 2)


def run(simIntersections, streets, window):
    t0 = time.perf_counter()
    time_counter = 0
    while window.running:
        event_update(window)
        if (time.perf_counter() - t0) >= time_per_frame:
            # update
            time_counter += 1
            time_past = (time.perf_counter() - t0)
            #update_physics(time_past)
            render(simIntersections, streets, window)
            t0 = time.perf_counter()
            if time_counter >= 2:
                # slower event...
                # for i in simIntersections:
                #     i.set_location(i.location[0]+int(5*random.uniform(-1, 1)), i.location[1])
                time_counter = 0


def event_update(window):
    for event in game.event.get():
        if event.type == game.QUIT:
            window.running = False


def render(intersections, streets, window):
    window.screen.fill((0, 0, 0))
    for i in intersections:
        i.draw(window)
    draw_streets(streets, window)
    game.display.flip()


def visualize(intersections, streets):
    screen_width = 1920
    screen_height = 1080

    window = WindowWrapper()
    simIntersections = [SimIntersection(int(2*screen_width/6), 1*screen_height/4, intersections[0]),
                        SimIntersection(int(3*screen_width/6), 1*screen_height/4, intersections[1]),
                        SimIntersection(int(4*screen_width/6), 1*screen_height/4, intersections[2]),
                        SimIntersection(int(1*screen_width/6), 2*screen_height/4, intersections[3]),
                        ]

    init_setup_blockPositions(streets, window)

    run(simIntersections, streets, window)

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
    generateCars(streets)

    screen_width = 1920
    screen_height = 1080

    window = WindowWrapper()
    simIntersections = [SimIntersection(int(2 * screen_width / 6), 1 * screen_height / 4, intersections[0]),
                        SimIntersection(int(3 * screen_width / 6), 1 * screen_height / 4, intersections[1]),
                        SimIntersection(int(4 * screen_width / 6), 1 * screen_height / 4, intersections[2]),
                        SimIntersection(int(1 * screen_width / 6), 2 * screen_height / 4, intersections[3]),
                        SimIntersection(int(2 * screen_width / 6), 2 * screen_height / 4, intersections[4]),
                        SimIntersection(int(3 * screen_width / 6), 2 * screen_height / 4, intersections[5]),
                        SimIntersection(int(4 * screen_width / 6), 2 * screen_height / 4, intersections[6]),
                        SimIntersection(int(5 * screen_width / 6), 2 * screen_height / 4, intersections[7]),
                        SimIntersection(int(2 * screen_width / 6), 3 * screen_height / 4, intersections[8]),
                        SimIntersection(int(3 * screen_width / 6), 3 * screen_height / 4, intersections[9]),
                        SimIntersection(int(4 * screen_width / 6), 3 * screen_height / 4, intersections[10])]

    init_setup_blockPositions(streets, window)

    run(simIntersections, streets, window)

visualize_example()