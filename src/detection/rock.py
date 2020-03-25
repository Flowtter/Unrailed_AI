import cv2
import numpy as np

# dark bro in BGR : [ 68  87 105]
# dark bro in HSV : [144 56 11] in percentage
# dark bro in HSV : [144 142 28] in values

# light brown in BGR : [118 150 182]
# light brown in HSV : [142 56 41] in percentage
# light brown in HSV : [142 142 104] in values

# magic values for rocks
HSV_MIN_THRESH = np.array([14, 80, 100])
HSV_MAX_THRESH = np.array([16, 100, 200])


HSV_MIN_THRESH_SUB = np.array([16, 0, 0])
HSV_MAX_THRESH_SUB = np.array([16, 255, 255])

def _remove_random_from_mask(mask, nb_components, stats, w, h):
    """ algorithm that remove anything but rock"""

    for i in range(nb_components):
        if stats[i][2] < w//15:
            for y in range(stats[i][1], stats[i][1]+stats[i][3]+1):
                for x in range(stats[i][0], stats[i][0]+stats[i][2]+1):
                    if y >= 0 and x >= 0 and y < h and x < w:
                        mask[y][x] = 0

def draw_contours_return_bin(image, hsv_image, color=(255, 0, 150)):
    """Draws contours of rocks found in image"""

    h, w = image.shape[:-1] # remove last value because we don't need the channels
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH) # create the mask with the treshold values on the hsv image and not BGR
    bin_image2= cv2.inRange(hsv_image, HSV_MIN_THRESH_SUB, HSV_MAX_THRESH_SUB) # create the mask with the treshold values on the hsv image and not BGR

    # get the locations of the rocks then remove the grass

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(bin_image, 8, cv2.CV_32S)
    #_remove_random_from_mask(bin_image, nb_components, stats, w, h)

    dilated_bin_image = cv2.dilate(bin_image, np.ones((3, 3), np.uint8), iterations=0)
    dilated_bin_image2 = cv2.dilate(bin_image2, np.ones((3, 3), np.uint8), iterations=0)

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)
    result2 = cv2.bitwise_and(image, image, mask=dilated_bin_image2)

    result2 = cv2.bitwise_not(result2)
    result = cv2.bitwise_and(result, result2)


    contours, hierarchy = cv2.findContours(dilated_bin_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, color, 3)

    return result

def get_bin(image, hsv_image, color=(255, 0, 150)):
    """get contours of rocks found in image"""

    h, w = image.shape[:-1] # remove last value because we don't need the channels
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH) # create the mask with the treshold values on the hsv image and not BGR

    # get the locations of the rocks then remove the grass

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(bin_image, 8, cv2.CV_32S)
    _remove_random_from_mask(bin_image, nb_components, stats, w, h)

    dilated_bin_image = cv2.dilate(bin_image, np.ones((3, 3), np.uint8))


    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)

    return result
