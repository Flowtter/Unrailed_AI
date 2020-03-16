import cv2
import numpy as np
from capture import windowcapture

import axe
import trees
import detectplayer
import rock
import blackrock
import river
import the_map

import time
import pyautogui
import win32gui



def debug_main():
    """function to replace the main to keep it clean"""

    #save_screenshot()
    im = cv2.imread("../data/img_debug.png", cv2.COLOR_RGB2BGR)
    #debug_show(im)
    #print(convert_HSV(41))
    #print(get_pixel_color(im, 0, 0))
    debug_show(im)
    #debug_save(im)

# functions that allow you to work on a single screenshot instead of on the game

def debug_show(im):
    """function that shows the image"""
    the_map.draw_map_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    river.draw_river_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    blackrock.draw_blackrock_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    rock.draw_rock_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    trees.draw_trees_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    axe.draw_axe_countours(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    detectplayer.draw_player(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    cv2.imshow("im", im)
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

def show(im):
    """function that shows the image without edit"""
    cv2.imshow("im", im)
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

def debug_save(im):
    """function that saves the image"""
    the_map.draw_map_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    river.draw_river_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    blackrock.draw_blackrock_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    rock.draw_rock_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    trees.draw_trees_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    axe.draw_axe_countours(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    detectplayer.draw_player(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    cv2.imwrite("../data/img_masked.png", im)

def single_screenshot():
    """function that take a single screnshot of the game to work on it"""
    hwnd = win32gui.FindWindow(None, "Unrailed!")
    if not hwnd:
        raise Exception("Window not found!")

    l, t, r, d = win32gui.GetClientRect(hwnd)
    x, y = win32gui.ClientToScreen(hwnd, (l, t))
    if win32gui.GetForegroundWindow() != hwnd:
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.1)

    return cv2.cvtColor(
            np.asarray(pyautogui.screenshot(region=(
            x, y,
            *win32gui.ClientToScreen(hwnd,(r-x, d-y))
            ))),
            cv2.COLOR_RGB2BGR
        )
        
def save_screenshot():
    """function that take a single screnshot of the game and save it"""
    cv2.imwrite("../data/img_debug.png", single_screenshot())


# functions to work on the image in BGR

def get_pixel_color(im, x, y):
    """function to get the pixel color"""
    rows, cols = im.shape[:-1]
    if x < 0 and y < 0:
        raise Exception("get pixel: coordinate need to be positive!")
    if x < rows and y < cols:
        return im[y,x]

    raise Exception("get pixel: x and y out of range!")


def set_pixel_color(im, x, y, color):
    """function to set the pixel color"""
    rows, cols = im.shape[:-1]
    if x < 0 and y < 0:
        raise Exception("get pixel: coordinate need to be positive!")
    if x < rows and y < cols:
        im[y,x] = color
        return im
    raise Exception("get pixel: x and y out of range!")


def set_area_color(im, x, y, color, size):
    """function to set an area of pixels color"""
    half_size = size // 2
    x_half, y_half = x - half_size, y - half_size
    for i in range(size):
        for j in range(size):
            im = set_pixel_color(im, x_half + i, y_half + j, color)

    return im


def convert_HSV(color):
    """function to convert HSV percentage in 8bit value"""
    return color * 255 / 100