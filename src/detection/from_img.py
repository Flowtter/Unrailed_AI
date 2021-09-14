import cv2
import numpy as np


def get_img_location(image_gray, template, treshold):
    """Apply template matching to gray image
       and return img location"""
    result = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
    location = np.where(result >= treshold)
    return location


def get_img_minimap(image_gray, template, treshold):
    result = []
    try:
        for point in zip(*get_img_location(image_gray, template, treshold)[::-1]):
            result.append((point[0] + template.width // 2,
                          point[1] + template.height // 2))
        return result
    except:
        print("get_img_minimap: Could not find the img")
