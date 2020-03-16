import cv2
import numpy as np
from capture import windowcapture
from detection import axe, trees, player, rock, blackrock, river, terrain

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

capture = windowcapture.WindowCapture("Unrailed!", FRAME_RATE)
capture.start()

while True:
    start = time.time()
    frame = capture.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    terrain.draw_contours(frame, hsv_frame)
    river.draw_contours(frame, hsv_frame)
    blackrock.draw_contours(frame, hsv_frame)
    rock.draw_contours(frame, hsv_frame)
    trees.draw_contours(frame, hsv_frame)
    axe.draw_contours(frame, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    player.draw_contours(frame, hsv_frame)

    cv2.imshow("frame", frame)

    delta = time.time() - start
    if delta < SLEEP_TIME:
        time.sleep(SLEEP_TIME - delta)

    key = cv2.waitKey(1) & 0xFF
    if key == ESC_KEY:
        break

capture.stop()
cv2.destroyAllWindows()
