import cv2
import numpy as np
import pyautogui
from threading import Thread
import time
import win32gui
import keyboard
import random
from pathfinding import astar

SPEED = 0.105
TIME_OFF = 0.15
BREAK_TIME = 1.8


class Bot:

    # function init to declare variables

    def __init__(self):
        self.should_stop = False

    def input(self, key, t):
        pyautogui.keyDown(key)
        time.sleep(t)
        pyautogui.keyUp(key)

    def movement(self, key):
        self.input(key, SPEED)
        time.sleep(TIME_OFF)

    def path(self, start, obj, g, draw):
        original = g.get_binary_matrix()
        print(f"path to {obj}")

        if obj == "axe":
            pickaxe = g.get_pos('A')
            return astar.run(original, start, pickaxe, g, draw)

        elif obj == "tree":
            print("searching for trees")
            tree = g.get_pos('t')
            return astar.run(original, start, tree, g, draw)
        
        elif obj == "rock":
            print("searching for rocks")
            rock = g.get_pos('k')
            return astar.run(original, start, rock, g, draw)

        else:
            raise Exception("bot: path: not a valid object")


    def move(self, obj, game, draw, player_pos):
        movement = self.path(player_pos, obj, game, draw)
        if movement != None:
            for vect in movement:
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
            #if obj == "axe":
            #    self.input("space", 0.1)
            
        else:
            print("Movement is null!")


        return player_pos

    def breaking(self, obj, player_pos, game):
        
        game.matrix[player_pos[0]][player_pos[1]] = 'M'  # Remove the 't'

        if player_pos[0] -1 > 0 and game.matrix[player_pos[0] - 1][player_pos[1]] == obj:
            self.input('z', BREAK_TIME)   
            return (player_pos[0] - 1,player_pos[1])


        elif player_pos[0] +1 < len(game.matrix) and  game.matrix[player_pos[0] + 1][player_pos[1]] == obj:
            self.input('s', BREAK_TIME)
            return (player_pos[0] + 1,player_pos[1])


        elif player_pos[1] -1 > 0 and  game.matrix[player_pos[0]][player_pos[1] - 1] == obj:
            self.input('q', BREAK_TIME)
            return (player_pos[0],player_pos[1]- 1)


        elif player_pos[1] +1 < len(game.matrix[0])  and  game.matrix[player_pos[0]][player_pos[1] + 1] == obj:
            self.input('d', BREAK_TIME)
            return (player_pos[0],player_pos[1] + 1)
        
        print(f"no {obj} are reachable")
        return None

    def rnd(self):
        for i in range(3):
            r = random.randrange(0, 4, 1)
            if    r == 0:
                self.movement('q')
            elif  r == 1:
                self.movement('d')
            elif  r == 2:
                self.movement('s')
            elif  r == 3:
                self.movement('z')






