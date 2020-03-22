import cv2
import numpy as np


HSV_MIN_THRESH_YELLOW = np.array([20, 150, 150]) # Treshold values, colors in HSV
HSV_MAX_THRESH_YELLOW = np.array([35, 210, 255])

# magic values for river
HSV_MIN_THRESH = np.array([82, 0, 150])
HSV_MAX_THRESH = np.array([90, 200, 255])

def _remove_river_from_bin_image(bin_image, nb_components, stats, w, h):
    """ algorithm that remove anything but river"""

    for i in range(nb_components):
        if stats[i][2] < w//20:
            for y in range(stats[i][1], stats[i][1]+stats[i][3]+1):
                for x in range(stats[i][0], stats[i][0]+stats[i][2]+1):
                    if y >= 0 and x >= 0 and y < h and x < w:
                        bin_image[y][x] = 0

def draw_contours_return_bin(image, hsv_image, color=(150, 100, 200)):
    """Draws contours of river found in image"""

    h, w = image.shape[:-1] # remove last value because we don't need the channels
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH) # create the bin_image with the treshold values on the hsv image and not BGR
    bin_image += cv2.inRange(hsv_image, HSV_MIN_THRESH_YELLOW, HSV_MAX_THRESH_YELLOW)
    # get the locations of the river then remove the grass

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(bin_image, 8, cv2.CV_32S)
    _remove_river_from_bin_image(bin_image, nb_components, stats, w, h)

    dilated_bin_image = cv2.dilate(bin_image, np.ones((3, 3), np.uint8), iterations=2)

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)
    contours, hierarchy = cv2.findContours(dilated_bin_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, color, 3)
    return result

def get_bin(image, hsv_image, color=(150, 100, 200)):
    """get contours of river found in image"""

    h, w = image.shape[:-1] # remove last value because we don't need the channels
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH) # create the bin_image with the treshold values on the hsv image and not BGR
    bin_image += cv2.inRange(hsv_image, HSV_MIN_THRESH_YELLOW, HSV_MAX_THRESH_YELLOW)
    # get the locations of the river then remove the grass

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(bin_image, 8, cv2.CV_32S)
    _remove_river_from_bin_image(bin_image, nb_components, stats, w, h)

    dilated_bin_image = cv2.dilate(bin_image, np.ones((3, 3), np.uint8))

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)
    
    return result