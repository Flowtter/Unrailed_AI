import cv2
import numpy as np
import pyautogui
from threading import Thread
import time
import win32gui
import keyboard

from pathfinding import astar

SPEED = 0.12 
TIME_OFF = 0.05
BREAK_TIME = 2.1


class Bot:

    # function init to declare variables

    def __init__(self, updateHZ):
        self.should_stop = False
        self.wait_time = 1/updateHZ
        self._thread_name = "Bot"

    # function start, give a thread to the object

    def start(self):
        self._thread = Thread(target=self.update, name=self._thread_name, args=())
        self._thread.daemon = True
        self._thread.start()
        return self

    # function update, replace self.frame by an image that has been screenshoted

    def update(self):
        while not self.should_stop: # changed True by self...
            start = time.time()
            delta = time.time() - start

            if keyboard.is_pressed("P"):
                self.stop()

            if delta < self.wait_time:
                time.sleep(self.wait_time - delta)

    # function that join the thread to then stop them

    def stop(self):
        self.should_stop = True
        self._thread.join()

    def input(self, key, t):
        pyautogui.keyDown(key)
        time.sleep(t)
        pyautogui.keyUp(key)

    def movement(self, key):
        self.input(key, SPEED)
        time.sleep(TIME_OFF)

    def path(self, start, obj, g, draw):
        original = g.get_binary_matrix()
        print("path: ")

        if obj == "axe":
            pickaxe = g.get_pos('A')
            return astar.run(original, start, pickaxe, g, draw)

        elif obj == "tree":
            tree = g.get_pos('t')
            return astar.run(original, start, tree, g, draw)

        else:
            raise Exception("bot: path: not a valid object")


    def move(self, obj, game, draw, player_pos):
        game.matrix[player_pos[0]][player_pos[1]] = 'M'
        movement = self.path(player_pos, obj, game, draw)
        i = 0
        for vect in movement:
            i+= 1
            x = player_pos[0] - vect[0]
            y = player_pos[1] - vect[1]
            player_pos = vect
            if    y > 0:
                self.movement('q')
            elif  y < 0:
                self.movement('d')
            elif  x < 0:
                self.movement('s')
            elif  x > 0:
                self.movement('z')
        if obj == "axe":
            self.input("space", 0.1)
        
        game.matrix[player_pos[0]][player_pos[1]] = 'P'

        return player_pos

    def breaking(self, obj, player_pos, game):
        
        game.matrix[player_pos[0]][player_pos[1]] = 'M'  # Remove the 't'

        if player_pos[0] -1 > 0 and game.matrix[player_pos[0] - 1][player_pos[1]] == obj:
            self.input('z', BREAK_TIME)   
            game.matrix[player_pos[0] - 1][player_pos[1]] = 'P'
            return (player_pos[0] - 1,player_pos[1])


        elif player_pos[0] +1 < len(game.matrix) and  game.matrix[player_pos[0] + 1][player_pos[1]] == obj:
            self.input('s', BREAK_TIME)
            game.matrix[player_pos[0] + 1][player_pos[1]] = 'P'
            return (player_pos[0] + 1,player_pos[1])


        elif player_pos[1] -1 > 0 and  game.matrix[player_pos[0]][player_pos[1] - 1] == obj:
            self.input('q', BREAK_TIME)
            game.matrix[player_pos[0]][player_pos[1] - 1] = 'P'
            return (player_pos[0],player_pos[1]- 1)


        elif player_pos[1] +1 < len(game.matrix[0])  and  game.matrix[player_pos[0]][player_pos[1] + 1] == obj:
            self.input('d', BREAK_TIME)
            game.matrix[player_pos[0]][player_pos[1] + 1] = 'P'
            return (player_pos[0],player_pos[1] + 1)
        
        print("no trees are reachable")
        return None





