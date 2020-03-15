import cv2
import numpy as np
from capture import windowcapture
import axe
import trees
import time

ESC_KEY = 27

FRAME_RATE = 30
SLEEP_TIME = 1 / FRAME_RATE

capture = windowcapture.WindowCapture("Unrailed!", 10)
capture.start()

def debug():
    frame = cv2.imread("../data/img_2.png", cv2.COLOR_RGB2BGR)
    axe.draw_axe_countours(frame, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    trees.draw_trees_contours(frame, cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))
    cv2.imshow("frame", frame)
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == ESC_KEY:
            break



debug()

"""
while True:
    frame = capture.read()
    axe.draw_axe_countours(frame, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    trees.draw_trees_contours(frame, cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))

    cv2.imshow("frame", frame)

    time.sleep(SLEEP_TIME)

    k = cv2.waitKey(1) & 0xFF
    if k == ESC_KEY:
        break

cv2.destroyAllWindows()
"""