import cv2
import numpy as np
import time
import pyautogui
import win32gui
import imutils

from detection import axe, trees, player, rock, blackrock, river, terrain


from capture import windowcapture
from show_map import game_map

def debug_main():
    """function to replace the main to keep it clean"""

    im = cv2.imread("../test_data/img_debug.png", cv2.COLOR_RGB2BGR)
    im = rotate(im, -8)

    mean_x, mean_y = player.draw_and_return_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    mean_x//=15
    mean_y//=40

    mean_x_axe, mean_y_axe = axe.draw_and_return_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    mean_x_axe//=15
    mean_y_axe//=40



    game = game_map(20,40,20,10) 
    game.init_matrix()
    game.draw_cell()

    game.draw_axe(mean_x_axe, mean_y_axe)

    game.draw_player(mean_y, mean_y)
    im2 = game.draw_image()

    #show(im2)
    show2(im, im2)

    #show(game.draw_player(mean_x,mean_y), im)

    #save_screenshot()

    #debug_show(im)
    #print(convert_HSV(41))
    #print(get_pixel_color(im, 0, 0))
    #debug_show(im)
    #debug_save(im)

# functions that allow you to work on a single screenshot instead of on the game

def rotate(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def debug_show(im):
    """function that shows the image"""
    hsv_frame = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    terrain.draw_contours(im, hsv_frame)
    river.draw_contours(im, hsv_frame)
    blackrock.draw_contours(im, hsv_frame)
    rock.draw_contours(im, hsv_frame)
    trees.draw_contours(im, hsv_frame)
    axe.draw_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    player.draw_contours(im, hsv_frame)
    cv2.imshow("im", im)
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

def show(im):
    """function that shows the image without edit"""
    cv2.imshow("im1", im)
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

def show2(im, im2):
    """function that shows the image without edit"""
    cv2.imshow("im1", im2)
    debug_show(im)
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

def debug_save(im):
    """function that saves the image"""
    hsv_frame = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    terrain.draw_contours(im, hsv_frame)
    river.draw_contours(im, hsv_frame)
    blackrock.draw_contours(im, hsv_frame)
    rock.draw_contours(im, hsv_frame)
    trees.draw_contours(im, hsv_frame)
    axe.draw_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    player.draw_contours(im, hsv_frame)
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
    cv2.imwrite("../test_data/img_debug.png", single_screenshot())


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
    if x < cols and y < rows:
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