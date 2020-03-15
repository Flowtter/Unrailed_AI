import cv2
import numpy as np

template = cv2.imread("../template.png", cv2.IMREAD_GRAYSCALE)
height, width = template.shape

def get_axe_location(image_gray):
    """Apply template matching to gray image
       and return axe location"""

    result = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
    location = np.where(result >= 0.9)     # trust me that threshold is working 89
    return location

def draw_axe_countours(image, image_gray, color=(255, 0, 255)):
    """Draws the countours of the axes found in image"""

    for point in zip(*get_axe_location(image_gray)[::-1]):
        cv2.rectangle(image, (point[0] - 2, point[1] - 2), (point[0] + width + 2, point[1] + height + 2), color, 2)
