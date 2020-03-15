import cv2
import numpy as np
import time
import sys
import axe
import trees

image = cv2.imread("..\data\img_2.png")

axe.draw_axe_countours(image, cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
trees.draw_trees_contours(image, cv2.cvtColor(image, cv2.COLOR_BGR2HSV))

cv2.imshow("image", image)

cv2.waitKey(0)
cv2.destroyAllWindows()
