import os, sys
import cv2
import numpy as np
import time
import pyautogui
import win32gui
import imutils
import keyboard

from colorama import init, Fore, Back, Style

from player import bot
from capture import windowcapture
from show import show_map
from show import printer
from functions import *
from detection import trees, player, rock, blackrock, river, terrain, green, axe, pickaxe
from layout import Layout

import functions

init(convert=True)

#sys.stderr = object
os.system('cls')

ESC_KEY = 27
FRAME_RATE = 5
SLEEP_TIME = 1 / FRAME_RATE

run = True
mode = "tree"

if len(sys.argv) == 1:
    layout_mode = "qwerty"
else:
    if sys.argv[1] == "azerty" or sys.argv[1] == "qwerty":
        layout_mode = sys.argv[1]
    else:
        raise Exception("argument should be 'azerty' or 'qwerty'")

l = Layout(layout_mode)

capture = windowcapture.WindowCapture("Unrailed!", FRAME_RATE, True)
p = printer.Printer(40, l)
p_bot = bot.Bot(l)

print(Fore.WHITE +
      f"""> This project has been made by Flowtter! Thanks for using it !
    keybind:
    F1: Quit
    F2: Pause Bot  
    {l.change}: Change Mode
    {l.ok}: Positive Confirmation
    {l.no}: Negative Confirmation
    {l.random}: Randomize movements
    {l.drop}: Emergency drop Item
    """)

# create map
game = show_map.game_map(20, 36, 22, 16, 10)
game.init_matrix()

# pick the axe and move out of the train station
p_bot.input('space', 0.1)
time.sleep(0.3)
p_bot.input('s', 0.5)

# start the bot
p.start()

# var for the main loop
tried = 0
change = False
random = False

# last obj
last = []
for i in range(15):
    last.append((0, 0))

# main loop
while True:

    #region KEY

    key = p.key()

    if key == 'F1':
        print(
            Fore.WHITE +
            "> This project has been made by Flowtter! Thanks for using it !")
        break
    elif key == 'F2':
        if run:
            print(Fore.YELLOW + "> I'M WAITING!")
            run = False
        else:
            print(Fore.YELLOW + "> I'M STARTING!")
            run = True
    elif key == l.change:  # and not change:
        print(Fore.MAGENTA + "> I'M CHANGING TARGET")
        change = True
    elif key == l.ok:  # and change:
        change = False
        print(Fore.GREEN + "> Thanks for the confirmation")
        p_bot.input("space", 0.3)

        if mode == "tree":
            mode = "rock"
        else:
            mode = "tree"

        tried = 0
    elif key == l.drop:
        change = False
        print(Fore.RED + "> EMERGENCY DROP")
        p_bot.input("space", 0.3)
        print(Fore.RED + "> WAITING FOR YOUR CALL")
        run = False
    elif key == l.no:  # and change:
        change = False
        tried = 0
        if mode == "tree":
            print(Fore.BLUE + "> I'M SORRY, BACK TO CHOPPING")
        else:
            print(Fore.BLUE + "> I'M SORRY, BACK TO MINING")
    elif key == l.random:
        random = True
        change = False
        print(Fore.YELLOW + "> WANT SOME RANDOM ? :)")

    #endregion

    if run:

        game.draw_matrix()
        im2 = game.draw_image()
        cv2.imshow("frame2", im2)

        game.init_matrix()
        start = time.time()

        frame = capture.force_update()  # uh oh
        im = functions.cut(frame)

        if tried != -1:
            tried, last = functions.test(im, p_bot, game, last, mode, change,
                                         tried, random)

        random = False

        if tried >= 15:
            change = False
            if mode == "tree":
                print("> I'M SORRY, BACK TO CHOPPING")
            else:
                print("> I'M SORRY, BACK TO MINING")
            tried = 0

        functions.draw(im)
        functions.grid(im)

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
