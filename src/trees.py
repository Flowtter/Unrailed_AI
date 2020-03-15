import cv2
import numpy as np

# magic values for trees and grass
HSV_MIN_THRESH = np.array([43, 165, 101])
HSV_MAX_THRESH = np.array([73, 176, 255])

def _remove_grass_from_mask(mask, nb_components, stats, w, h):
    print(w//53)
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

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, 8, cv2.CV_32S)
    for i in range(nb_components):
        if stats[i][2] < w-20 and stats[i][3] < h-20:
            cv2.rectangle(image, (stats[i][0], stats[i][1]), (stats[i][0]+stats[i][2], stats[i][1]+stats[i][3]), color, 2)
