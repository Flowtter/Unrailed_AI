import cv2
import numpy as np
from capture import windowcapture
import axe
import trees
import detectplayer
import time
import debug

ESC_KEY = 27

FRAME_RATE = 10
SLEEP_TIME = 1 / FRAME_RATE

"""Remove on last commit"""

DEBUG = False

if DEBUG:
    debug.debug_main()
    exit()



capture = windowcapture.WindowCapture("Unrailed!", FRAME_RATE) # We create the object WindowCapture that can capture the "Unrailed!"
capture.start() # Function in capture that start recording

while True:
    frame = capture.read()
    trees.draw_trees_contours(frame, cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))
    axe.draw_axe_countours(frame, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    detectplayer.draw_player(frame, cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))
    cv2.imshow("frame", frame)

    time.sleep(SLEEP_TIME)

    k = cv2.waitKey(1) & 0xFF
    if k == ESC_KEY:
        break

cv2.destroyAllWindows()
