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
from modules.MapFunctions import createMap

# 1920x1080
time_per_frame = 0.016667  # seconds

# todo: ERSTMAL MIT MASTER/ALGORITHM MERGEN, DANN VISU PROGRAMMIEREN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
            'north': Point(x_loc + self.width / self.CONST, y_loc - self.height / 2),
            'east': Point(x_loc + self.width / 2, y_loc + self.height / self.CONST),
            'south': Point(x_loc - self.width / self.CONST, y_loc + self.height / 2),
            'west': Point(x_loc - self.width / 2, y_loc - self.height / self.CONST),
        }
        self.exitPoints = {
            'north': Point(x_loc - self.width / self.CONST, y_loc - self.height / 2),
            'east': Point(x_loc + self.width / 2, y_loc - self.height / self.CONST),
            'south': Point(x_loc + self.width / self.CONST, y_loc + self.height / 2),
            'west': Point(x_loc - self.width / 2, y_loc + self.height / self.CONST)
        }
        self._init_blocks()

    def set_location(self, loc_x, loc_y):
        self.location = np.array((loc_x, loc_y))

    def draw(self, window):
        game.draw.rect(window.screen, self.color, self.rect)
        for dir, entrance in self.entrancePoints.items():
            game.draw.rect(window.screen, game.Color(255,50,70), game.Rect(entrance.x_loc-self.enterExit_width/2, entrance.y_loc-self.enterExit_height/2, self.enterExit_width, self.enterExit_height))
        for dir, iExit in self.exitPoints.items():
            game.draw.rect(window.screen, game.Color(100,150,165), game.Rect(iExit.x_loc-self.enterExit_width/2, iExit.y_loc-self.enterExit_height/2, self.enterExit_width, self.enterExit_height))

    def _init_blocks(self):
        for dir, block in self.intersection.intersectionEntranceBlocks.items():
            block.visualizationPoint = self.entrancePoints[dir]
        for dir, block in self.intersection.intersectionExitBlocks.items():
            block.visualizationPoint = self.exitPoints[dir]


def draw_streets(streets, window):
    for street in streets:
        for lane in street.lanes:
            # todo: drawline between lane[0] and lane[lane.length-1]
            game.draw.line(window.screen, game.Color(80,80,170), (lane.blocks[0].visualizationPoint.x_loc, lane.blocks[0].visualizationPoint.y_loc), (lane.blocks[lane.length-1].visualizationPoint.x_loc, lane.blocks[lane.length-1].visualizationPoint.y_loc), 2)


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
    window = WindowWrapper()
    simIntersections = [SimIntersection(300, 500, intersections[0]),
                        SimIntersection(950, 200, intersections[1]),
                        SimIntersection(1700, 500, intersections[2]),
                        SimIntersection(950, 900, intersections[3]),
                        SimIntersection(950, 500, intersections[4])]

    draw_streets(streets, window)

    run(simIntersections, streets, window)


I1 = Intersection(name='1', N_connections=3)

I2 = Intersection(name='2', N_connections=3)
I3 = Intersection(name='3', N_connections=3)
I4 = Intersection(name='4', N_connections=3)
I5 = Intersection(name='5')

anyIntersections = [I1, I2, I3, I4, I5]

anyStreets = createMap([I1, I2, I3, I4, I5])

visualize(anyIntersections, anyStreets)

