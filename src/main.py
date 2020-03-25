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

import keyboard

from detection import axe, trees, player, rock, blackrock, river, terrain, green

ESC_KEY = 27

FRAME_RATE = 5
SLEEP_TIME = 1 / FRAME_RATE

"""Remove on last commit"""

DEBUG = False

if DEBUG:
    debug.debug_main()
    exit()

run = True

mode = "tree"

capture = windowcapture.WindowCapture("Unrailed!", FRAME_RATE, True)
p = printer.Printer(20)
p_bot = bot.Bot()

print("> This project has been made by Naexys! Thanks for using it !")

game = show_map.game_map(20,36,22,16,10)  # (self, height, width, cell_size, refresh_rate):

p_bot.input('space', 0.1)
time.sleep(2.3)
p_bot.input('s', 0.5)


game.init_matrix()

p.start()

time.sleep(1)

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
        if mode == "tree":
            mode = "rock"
        else:
            mode = "tree"

    if run:
        game.draw_matrix()
        im2 = game.draw_image()
        
        game.init_matrix()
        start = time.time()

        frame = capture.force_update()
        
        im = debug.cut(frame)

        
        cv2.imshow("frame2", im2)

        debug.test(im, p_bot, game, mode)
        
        player.draw_contours_return_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV))
        axe.draw_contours_return_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV ))

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

cv2.destroyAllWindows()
