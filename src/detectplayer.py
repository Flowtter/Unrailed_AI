import cv2
import numpy as np

# dark yellow in BGR : [33 148 163]
# dark yellow in HSV : [54 80 64] in percentage
# dark yellow in HSV : [54 200 163] in values

# light yellow in BGR : [ 52 235 255]
# light yellow in HSV : [ 54 80 100] in percentage
# dark yellow in HSV : [54 200 255] in values

# magic values for the player
HSV_MIN_THRESH = np.array([24, 190, 150]) # Treshold values, colors in HSV
HSV_MAX_THRESH = np.array([31, 210, 255])


def draw_player(image, hsv_image, color=(0, 100, 255)): 
    """Draws countours of trees found in image"""

    h, w = image.shape[:-1] # remove last value because we don't need the channels
    mask = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH) # apply the mask with the treshold values on the hsv image and not BGR
    
    # get the locations of the trees then remove the grass

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, 8, cv2.CV_32S)

    dilated_mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)

    # get the contours then draw them

    contours, hierarchy = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, color, 3)
