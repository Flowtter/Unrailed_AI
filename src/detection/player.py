import cv2
import numpy as np

# dark yellow in BGR : [33 148 163]
# dark yellow in HSV : [54 80 64] in percentage
# dark yellow in HSV : [54 200 163] in values

# light yellow in BGR : [ 52 235 255]
# light yellow in HSV : [ 54 80 100] in percentage
# light yellow in HSV : [54 200 255] in values
"""
HSV_MIN_THRESH = np.array([24, 190, 150]) # Treshold values, colors in HSV
HSV_MAX_THRESH = np.array([31, 210, 255])
"""

# dark red in BGR : [ 35  48 161]
# dark red in HSV : [ 6 78 63] in percentage
# dark red in HSV : [6 199 160] in values

# light red in BGR : [56 76 255]
# light red in HSV : [6 78 100] in percentage
# light red in HSV : [6 199 255] in values
"""
HSV_MIN_THRESH = np.array([0, 190, 140]) # Treshold values, colors in HSV
HSV_MAX_THRESH = np.array([10, 210, 255])
"""

# dark blue in BGR : [ 95 115  49]
# dark blue in HSV : [162 57 45] in percentage
# dark blue in HSV : [162 145 114] in values
"""
HSV_MIN_THRESH = np.array([0, 190, 140]) # Treshold values, colors in HSV
HSV_MAX_THRESH = np.array([10, 210, 255])
"""

# magic values for the player
HSV_MIN_THRESH_RED = np.array([1, 180, 150])
HSV_MAX_THRESH_RED = np.array([5, 220, 255])


def draw_contours_return_bin(image, hsv_image, color=(0, 100, 255)):
    """Draws contours of the terrain found in image"""

    h, w = image.shape[:
                       -1]  # remove last value because we don't need the channels
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH_RED, HSV_MAX_THRESH_RED)
    # get the locations of the river then remove the grass

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(
        bin_image, 8, cv2.CV_32S)

    dilated_bin_image = cv2.dilate(bin_image,
                                   np.ones((3, 3), np.uint8),
                                   iterations=2)

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)

    contours, hierarchy = cv2.findContours(dilated_bin_image,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, color, 3)
    return result


def get_bin(image, hsv_image, color=(0, 100, 255)):
    """get contours of the terrain found in image"""

    h, w = image.shape[:
                       -1]  # remove last value because we don't need the channels
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH_RED, HSV_MAX_THRESH_RED)
    # get the locations of rivers then remove the grass

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(
        bin_image, 8, cv2.CV_32S)
    dilated_bin_image = cv2.dilate(bin_image, np.ones((3, 3), np.uint8))

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)
    return result
