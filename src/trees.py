import cv2
import numpy as np

# magic values for trees and grass
HSV_MIN_THRESH = np.array([43, 165, 101])
HSV_MAX_THRESH = np.array([73, 176, 255])

def _remove_grass_from_mask(mask, nb_components, stats, w, h):
    for i in range(nb_components):
        if stats[i][2] < w//53:
            for y in range(stats[i][1], stats[i][1]+stats[i][3]+1):
                for x in range(stats[i][0], stats[i][0]+stats[i][2]+1):
                    if y >= 0 and x >= 0 and y < h and x < w:
                        mask[y][x] = 0

def draw_trees_contours(image, hsv_image, color=(0, 255, 0)):
    """Draws countours of trees found in image"""

    h, w = image.shape[:-1]
    mask = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH)
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, 8, cv2.CV_32S)
    _remove_grass_from_mask(mask, nb_components, stats, w, h)

    dilated_mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)

    contours, hierarchy = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, (255, 0, 0), 3)
