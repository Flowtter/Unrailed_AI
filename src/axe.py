import cv2
import numpy as np
import debug

# Open the template of the axe and get the size of it
template = cv2.imread("../template.png", cv2.IMREAD_GRAYSCALE)
height, width = template.shape

def get_axe_location(image_gray):
    """Apply template matching to gray image
       and return axe location"""

    result = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)

    location = np.where(result >= 0.9)     # trust me that threshold is working
    return location

def draw_axe_countours(image, image_gray, color=(255, 0, 255)):
    """Draws the countours of the axes found in image"""
    csteMAX = 500
    for point in zip(*get_axe_location(image_gray)[::-1]): # get the location of the axe, invert the list, draw each points
        if point[1] < int(csteMAX - point[0] / 7.3 ) :
            cv2.rectangle(image, (point[0] - 2, point[1] - 2), (point[0] + width + 2, point[1] + height + 2), color, 2)



