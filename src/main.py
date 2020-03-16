import cv2
import numpy as np
from capture import windowcapture

import axe
import trees
import detectplayer
import rock
import blackrock
import river
import the_map

import time
import debug

ESC_KEY = 27

FRAME_RATE = 10
SLEEP_TIME = 1 / FRAME_RATE

"""Remove on last commit"""

DEBUG = True

if DEBUG:
    debug.debug_main()
    exit()



capture = windowcapture.WindowCapture("Unrailed!", FRAME_RATE) # We create the object WindowCapture that can capture the "Unrailed!"
capture.start() # Function in capture that start recording

while True:
    frame = capture.read()

    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    the_map.draw_map_contours(frame, HSV)
    river.draw_river_contours(frame, HSV)
    blackrock.draw_blackrock_contours(frame, HSV)
    rock.draw_rock_contours(frame, HSV)
    trees.draw_trees_contours(frame, HSV)
    axe.draw_axe_countours(frame, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    detectplayer.draw_player(frame, HSV)


    cv2.imshow("frame", frame)

    time.sleep(SLEEP_TIME)

    k = cv2.waitKey(1) & 0xFF
    if k == ESC_KEY:
        break

capture.stop() # maybe should delete that
cv2.destroyAllWindows()
