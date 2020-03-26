import os, sys
import cv2
import numpy as np
import time
import pyautogui
import win32gui
import imutils
from player import bot
from capture import windowcapture
from show import show_map
import debug
from show import printer

from colorama import init, Fore, Back, Style

import keyboard

from detection import trees, player, rock, blackrock, river, terrain, green, axe, pickaxe

init(convert=True)

#sys.stderr = object

ESC_KEY = 27

FRAME_RATE = 5
SLEEP_TIME = 1 / FRAME_RATE

"""Remove on last commit"""

DEBUG = False

run = True

mode = "tree"

capture = windowcapture.WindowCapture("Unrailed!", FRAME_RATE, True)
p = printer.Printer(40)
p_bot = bot.Bot()


os.system('cls')

print("> This project has been made by Naexys! Thanks for using it ! \n keybind: \n F1: Quit \n F2: Pause Bot \n P: Change Mode \n C: Positive Confirmation \n N: Negative Conformation\n M: Randomize movements \n L: Emergency drop Item")

game = show_map.game_map(20,36,22,16,10)  # (self, height, width, cell_size, refresh_rate):

game.init_matrix()


if DEBUG:
    debug.debug_main(game)
    exit()


p_bot.input('space', 0.1)
time.sleep(0.3)
p_bot.input('s', 0.5)


p.start()

time.sleep(1)

tried = 0
change = False
random = False

last = []
for i in range(15):
    last.append((0,0))

while True:

    key = p.key()

    if key == 'F1':
        print("> This project has been made by Naexys! Thanks for using it !")
        break
    elif key == 'F2':
        if run:
            print("> Bot is waiting!")
            run = False
        else:
            print("> Bot is starting!")
            run = True
    elif key == 'P':
        print("> CHANGING TARGET")
        change = True
    elif key == 'C':
        change = False
        print("> GOT THE CONFIRMATION")
        p_bot.input("space", 0.3)

        if mode == "tree":
            mode = "rock"
        else:
            mode = "tree"

        tried = 0

    elif key == 'L':
        change = False
        print("> EMERGENCY DROP")
        p_bot.input("space", 0.3)
        change = True

    elif key == 'N':
        change = False
        if mode == "tree":
            print("> SORRY, BACK TO CHOPPING")
        else:
            print("> SORRY, BACK TO MINING")

    elif key == 'M':
        random = True
        change = False
        print("> WANT SOME RANDOM ? :)")
    

    if run:
        game.draw_matrix()
        im2 = game.draw_image()
        
        game.init_matrix()
        start = time.time()

        frame = capture.force_update()
        
        im = debug.cut(frame)

        #bug car image rotate

        
        cv2.imshow("frame2", im2)

        if tried != -1:
            tried, last = debug.test(im, p_bot, game, last, mode, change, tried, random)

        random = False

        if tried >= 15: #  If the bot do not find the object
            change = False
            if mode == "tree":
                print("> SORRY, BACK TO CHOPPING")
            else:
                print("> SORRY, BACK TO MINING")
            tried = 0
        
        
        player.draw_contours_return_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV))
        axe.draw_contours(im, cv2.cvtColor(im,cv2.COLOR_BGR2GRAY ))
        pickaxe.draw_contours(im, cv2.cvtColor(im,cv2.COLOR_BGR2GRAY ))

        #green.draw_contours_return_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV))
        #trees.draw_contours_return_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
        #rock.draw_contours_return_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
        #blackrock.draw_contours_return_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
        #river.draw_contours_return_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV ))
        #terrain.draw_contours_return_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV ))

        debug.grid(im)
        cv2.imshow("frame1", im)


        delta = time.time() - start
        if delta < SLEEP_TIME:
            time.sleep(SLEEP_TIME - delta)

        key = cv2.waitKey(1) & 0xFF
        if key == ESC_KEY:
            break
    else:
        time.sleep(1)

cv2.destroyAllWindows()
