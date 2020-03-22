import cv2
import numpy as np



# magic values for river
HSV_MIN_THRESH = np.array([82, 0, 100])
HSV_MAX_THRESH = np.array([82, 140, 200])



def draw_contours_return_bin(image, hsv_image, color=(150, 100, 200)):
    """Draws contours of axe found in image"""

    h, w = image.shape[:-1] # remove last value because we don't need the channels
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH) # create the bin_image with the treshold values on the hsv image and not BGR
    # get the locations of the river then remove the grass

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(bin_image, 8, cv2.CV_32S)

    dilated_bin_image = cv2.dilate(bin_image, np.ones((3, 3), np.uint8), iterations=2)

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)
    contours, hierarchy = cv2.findContours(dilated_bin_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, color, 3)
    return result

def get_bin(image, hsv_image, color=(150, 100, 200)):
    """get contours of river found in image"""

    h, w = image.shape[:-1] # remove last value because we don't need the channels
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH) # create the bin_image with the treshold values on the hsv image and not BGR

    # get the locations of the river then remove the grass

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(bin_image, 8, cv2.CV_32S)
    dilated_bin_image = cv2.dilate(bin_image, np.ones((3, 3), np.uint8))

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)
    
    return result