import cv2
import numpy as np
from capture import windowcapture
import axe
import trees
import time
import detectplayer

# functions that allow you to work on a single screenshot instead of on the game

# function that shows the image

def debug_show(im):
    trees.draw_trees_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    axe.draw_axe_countours(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    detectplayer.draw_player(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    cv2.imshow("im", im)
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break


# function that saves the image

def debug_save(im):
    trees.draw_trees_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    axe.draw_axe_countours(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    detectplayer.draw_player(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    cv2.imwrite("../data/img_masked.png", im)


# functions that take a single screnshot of the game to work on it

def single_screenshot():
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
    cv2.imwrite("../data/img_debug.png", single_screenshot())


# functions to work on the image in BGR

# function to get the pixel color

def get_pixel_color(im, x, y):
    rows, cols = im.shape[:-1]
    if x < 0 and y < 0:
        raise Exception("get pixel: coordinate need to be positive!")
    if x < rows and y < cols:
        return im[y,x]

    raise Exception("get pixel: x and y out of range!")

# function to set the pixel color

def set_pixel_color(im, x, y, color):
    rows, cols = im.shape[:-1]
    if x < 0 and y < 0:
        raise Exception("get pixel: coordinate need to be positive!")
    if x < rows and y < cols:
        im[y,x] = color
        return im
    raise Exception("get pixel: x and y out of range!")

# function to set an area of pixels color

def set_area_color(im, x, y, color, size):
    half_size = size // 2
    x_half, y_half = x - half_size, y - half_size
    for i in range(size):
        for j in range(size):
            im = set_pixel_color(im, x_half + i, y_half + j, color)

    return im


# function to convert HSV percentage in 8bit value
def convert_HSV(color):
    return color * 255 / 100