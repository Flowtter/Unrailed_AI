import cv2
import numpy as np

# dark bro in BGR : [ 68  87 105]
# dark bro in HSV : [144 56 11] in percentage
# dark bro in HSV : [144 142 28] in values

# light brown in BGR : [118 150 182]
# light brown in HSV : [142 56 41] in percentage
# light brown in HSV : [142 142 104] in values

# magic values for rocks
HSV_MIN_THRESH = np.array([15, 90, 100]) # Treshold values, colors 
HSV_MAX_THRESH = np.array([15, 90, 200])

def _remove_random_from_mask(mask, nb_components, stats, w, h):
    """ algorithm that remove anything but rock"""
    for i in range(nb_components):
        if stats[i][2] < w//15:
            for y in range(stats[i][1], stats[i][1]+stats[i][3]+1):
                for x in range(stats[i][0], stats[i][0]+stats[i][2]+1):
                    if y >= 0 and x >= 0 and y < h and x < w:
                        mask[y][x] = 0

def draw_rock_contours(image, hsv_image, color=(255, 0, 150)): 
    """Draws countours of rocks found in image"""

    h, w = image.shape[:-1] # remove last value because we don't need the channels
    mask = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH) # create the mask with the treshold values on the hsv image and not BGR

    # get the locations of the rocks then remove the grass

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, 8, cv2.CV_32S)
    _remove_random_from_mask(mask, nb_components, stats, w, h)

    dilated_mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)

    # get the contours then draw them

    contours, hierarchy = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, color, 3)
