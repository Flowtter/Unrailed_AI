import cv2
import numpy as np
from capture import windowcapture
import axe
import trees
import time

def debug(path):
    frame = cv2.imread(path, cv2.COLOR_RGB2BGR)
    axe.draw_axe_countours(frame, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    trees.draw_trees_contours(frame, cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))
    cv2.imshow("frame", frame)
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break