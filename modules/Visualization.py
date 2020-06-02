#
# Visualization.py
#
#
import numpy as np
import os
import time
import pygame as game
import random

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


class SimObj:
    def __init__(self, x_loc, y_loc, color_r=255, color_g=255, color_b=255):
        self.location = np.array((x_loc, y_loc))
        self.color = game.Color(color_r, color_g, color_b)

    def set_location(self, loc_x, loc_y):
        self.location = np.array((loc_x, loc_y))

    def draw(self):
        game.draw.circle(window.screen, self.color, self.location, 5)


def run(intersections):
    t0 = time.perf_counter()
    time_counter = 0
    while window.running:
        event_update()
        if (time.perf_counter() - t0) >= time_per_frame:
            # update
            time_counter += 1
            time_past = (time.perf_counter() - t0)
            #update_physics(time_past)
            render(intersections)
            t0 = time.perf_counter()
            if time_counter >= 2:
                # slower event...
                for i in intersections:
                    i.set_location(i.location[0]+int(5*random.uniform(-1, 1)), i.location[1])
                time_counter = 0


def event_update():
    for event in game.event.get():
        if event.type == game.QUIT:
            window.running = False


def render(intersections):
    window.screen.fill((0, 0, 0))
    for i in intersections:
        i.draw()
    game.display.flip()


intersections = [SimObj(600, 100), SimObj(650, 150), SimObj(700, 200), SimObj(750, 250), SimObj(800, 300)]

window = WindowWrapper()

run(intersections)
