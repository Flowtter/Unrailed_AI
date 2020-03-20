import cv2
import numpy as np
import debug

template = cv2.imread("../template.png", cv2.IMREAD_GRAYSCALE)
height, width = template.shape

def get_axe_location(image_gray):
    """Apply template matching to gray image
       and return axe location"""

    result = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)

    location = np.where(result >= 0.9)     # trust me that threshold is working
    return location

def get_contours(image, image_gray):
    cste_max = 500
    for point in zip(*get_axe_location(image_gray)[::-1]): # get the location of the axe, invert the list, draw each points
        if point[1] < int(cste_max - point[0] / 7.3):
            return point

def draw_contours(image, image_gray, color=(255, 0, 255)):
    point = get_contours(image, image_gray)
    if point != None:
        cv2.rectangle(image, (point[0] - 2, point[1] - 2), (point[0] + width + 2, point[1] + height + 2), color, 2)

def draw_and_return_contours(image, image_gray, color=(255, 0, 255)):
    point = get_contours(image, image_gray)
    if point != None:
        cv2.rectangle(image, (point[0] - 2, point[1] - 2), (point[0] + width + 2, point[1] + height + 2), color, 2)
        return point
    else:
        return[0,0]
