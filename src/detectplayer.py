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
HSV_MIN_THRESH_BLUE = np.array([81, 146, 119]) # Treshold values, colors in HSV
HSV_MAX_THRESH_BLUE = np.array([83, 148, 121])

HSV_MIN_THRESH_RED = np.array([0, 190, 140]) # Treshold values, colors in HSV
HSV_MAX_THRESH_RED = np.array([10, 210, 255])



def _remove_train_station_from_mask(mask, nb_components, stats, w, h):
    """ algorithm that remove the grass"""
    for i in range(nb_components):
        if stats[i][3] < w//100:
            for y in range(stats[i][1], stats[i][1]+stats[i][3]+1):
                for x in range(stats[i][0], stats[i][0]+stats[i][2]+1):
                    if y >= 0 and x >= 0 and y < h and x < w:
                        mask[y][x] = 0


def draw_player(image, hsv_image, color=(0, 100, 255)): 
    """Draws countours of the player found in image"""

    h, w = image.shape[:-1] # remove last value because we don't need the channels
    mask = cv2.inRange(hsv_image, HSV_MIN_THRESH_BLUE, HSV_MAX_THRESH_BLUE) # create the mask with the treshold values on the hsv image and not BGR
    

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, 8, cv2.CV_32S)
    _remove_train_station_from_mask(mask, nb_components, stats, w, h)
    
    
    mask2= cv2.inRange(hsv_image, HSV_MIN_THRESH_RED, HSV_MAX_THRESH_RED) # create the mask with the treshold values on the hsv image and not BGR


    # get the locations of the player then remove the train station



    # add both mask

    mask += mask2
    dilated_mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)

    # get the contours then draw them

    contours, hierarchy = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, color, 3)
