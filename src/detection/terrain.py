import cv2
import numpy as np

# magic values for the map
HSV_MIN_THRESH = np.array([0, 0, 65])
HSV_MAX_THRESH = np.array([180, 255, 255])

HSV_MIN_THRESH_2 = np.array([0, 0, 0])
HSV_MAX_THRESH_2 = np.array([180, 255, 63])

def _remove_all_from_bin_image(bin_image, nb_components, stats, w, h):
    """Sets everything but terrain to 0 in binary image"""

    for i in range(nb_components):
        if stats[i][2] < w//2:
            for y in range(stats[i][1], stats[i][1]+stats[i][3]+1):
                for x in range(stats[i][0], stats[i][0]+stats[i][2]+1):
                    if y >= 0 and x >= 0 and y < h and x < w:
                        bin_image[y][x] = 0

def draw_contours_return_bin(image, hsv_image, color=(0, 0, 0)):
    """Draws contours of the terrain found in image"""

    h, w = image.shape[:-1] # remove last value because we don't need the channels
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH) # create the bin_image with the treshold values on the hsv image and not BGR
    bin_image += cv2.inRange(hsv_image, HSV_MIN_THRESH_2, HSV_MAX_THRESH_2)
    # get the locations of the river then remove the grass

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(bin_image, 8, cv2.CV_32S)
    _remove_all_from_bin_image(bin_image, nb_components, stats, w, h)

    dilated_bin_image = cv2.dilate(bin_image, np.ones((3, 3), np.uint8), iterations=2)

    
    dilated_bin_image = cv2.bitwise_not(dilated_bin_image, dilated_bin_image)

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)



    contours, hierarchy = cv2.findContours(dilated_bin_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, color, 3)
    return result

def get_bin(image, hsv_image, color=(0, 0, 0)):
    """get contours of the terrain found in image"""

    h, w = image.shape[:-1] # remove last value because we don't need the channels
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH) # create the bin_image with the treshold values on the hsv image and not BGR
    bin_image += cv2.inRange(hsv_image, HSV_MIN_THRESH_2, HSV_MAX_THRESH_2)
    # get the locations of the river then remove the grass

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(bin_image, 8, cv2.CV_32S)
    _remove_all_from_bin_image(bin_image, nb_components, stats, w, h)

    dilated_bin_image = cv2.dilate(bin_image, np.ones((3, 3), np.uint8))

    
    dilated_bin_image = cv2.bitwise_not(dilated_bin_image, dilated_bin_image)


    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)

    return result