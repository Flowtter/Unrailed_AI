import cv2
import numpy as np
import time
import sys
import axe
import trees
import screenshot as sc

FRAME_RATE = 30
SLEEP_TIME = 1 / FRAME_RATE

while True:

    frame = cv2.cvtColor(np.asarray(sc.screenshot(":D")), cv2.COLOR_RGB2BGR)
    axe.draw_axe_countours(frame, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    trees.draw_trees_contours(frame, cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))

    cv2.imshow("image", frame)

    time.sleep(SLEEP_TIME)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:     # escape key
        break

cv2.destroyAllWindows()
