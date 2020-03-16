import cv2
import numpy as np

# magic values for the map
HSV_MIN_THRESH = np.array([0, 0, 65]) # Treshold values, colors 
HSV_MAX_THRESH = np.array([120, 255, 255])

def _remove_river_from_mask(mask, nb_components, stats, w, h):
    """ algorithm that remove anything but map"""
    for i in range(nb_components):
        if stats[i][2] < w//5:
            for y in range(stats[i][1], stats[i][1]+stats[i][3]+1):
                for x in range(stats[i][0], stats[i][0]+stats[i][2]+1):
                    if y >= 0 and x >= 0 and y < h and x < w:
                        mask[y][x] = 0

def draw_map_contours(image, hsv_image, color=(0, 0, 0)): 
    """Draws countours of map found in image"""

    h, w = image.shape[:-1] # remove last value because we don't need the channels
    mask = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH) # create the mask with the treshold values on the hsv image and not BGR

    # get the locations of the river then remove the grass

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, 8, cv2.CV_32S)
    _remove_river_from_mask(mask, nb_components, stats, w, h)

    dilated_mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)

    # get the contours then draw them

    contours, hierarchy = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, color, 3)
