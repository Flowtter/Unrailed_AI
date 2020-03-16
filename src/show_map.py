import numpy as np
import cv2
from threading import Thread
import time

import debug

class game_map:

    # function init to declare variables

    def __init__(self, height, width, cell_size, refresh_rate):
        self.height = height
        self.width  = width
        self.cell_size = cell_size

        self.wait_time = 1/refresh_rate

        self.should_stop = False

        self.matrix = []

        self.im = np.zeros((self.height * self.cell_size, self.width * self.cell_size, 3), np.uint8)

    def start(self):
        self._thread = Thread(target=self.update, name=self._thread_name, args=())
        self._thread.daemon = True
        self._thread.start()
        return self

    # function update, replace self.frame by an image that has been screenshoted

    def update(self):
        while not self.should_stop:
            start = time.time()

            self.frame = 1

            delta = time.time() - start
            if delta < self.wait_time:
                time.sleep(self.wait_time - delta)

    # function that return the image

    def read(self):
        return self.frame

    # function that join the thread to then stop them

    def stop(self):
        self.should_stop = True
        self._thread.join()

    def init_matrix(self):
        matrix = []
        for i in range (self.height):
            local = []
            for j in range (self.width):
                local.append(0)
            matrix.append(local)
        self.matrix = np.array(matrix)

    def draw_cell(self):
        size_x = self.width * self.cell_size
        size_y = self.height * self.cell_size

        for y in range (0,size_y ):
            for x in range (0, size_x ):
                if x % self.cell_size == 0 or y % self.cell_size == 0:
                    debug.set_pixel_color(self.im, x, y, (0,255,0))
                else:
                    debug.set_pixel_color(self.im, x, y, (100,100,100))

    def draw_player(self, i, j):
        for y in range (1, self.cell_size):
            for x in range (1, self.cell_size):
                debug.set_pixel_color(self.im, x+i*self.cell_size, y+j*self.cell_size, (0, 100, 255))

    def draw_axe(self, i, j):
        for y in range (1, self.cell_size):
            for x in range (1, self.cell_size):
                debug.set_pixel_color(self.im, x+i*self.cell_size, y+j*self.cell_size, (255, 0, 255))


    def draw_image(self):
        return self.im