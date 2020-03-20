import cv2
import numpy as np
import time
import pyautogui
import win32gui
import imutils

from detection import axe, trees, player, rock, blackrock, river, terrain, green


from capture import windowcapture
from show_map import game_map

def debug_main():
    """function to replace the main to keep it clean"""

    #im = single_screenshot()

    im = cv2.imread("../test_data/img_debug.png", cv2.COLOR_RGB2BGR)
    im, im2 = do_map(im)

    show2([im, im2])


def do_map(im):
    im = rotate(im, -8.5)
    x, y = 0, 115
    h, w = 330, 800
    im = im[y:y+h, x:x+w]

    rows,cols = im.shape[:-1]


    a , b , c = [382,52],[500,50],[400,200]
    offsetx = 24
    d, e, f = [382 + offsetx ,52],[500 + offsetx,50],[400 ,200]

    pts1 = np.float32([a, b, c])
    pts2 = np.float32([d, e, f])

    dst = im #  Uh Oh

    M = cv2.getAffineTransform(pts1,pts2)
    dst = cv2.warpAffine(im,M,(cols,rows))

    im = dst

    axe.draw_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))

    bin_green = green.draw_contours_return_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV ))

    mean_x, mean_y = player.draw_and_return_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))

    mean_x//=23
    mean_y//=18

    bin_trees = trees.draw_contours_return_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    bin_rocks = rock.draw_contours_return_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    bin_black = blackrock.draw_contours_return_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    bin_river = river.draw_contours_return_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV ))
    bin_terrain = terrain.draw_contours_return_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV ))

    mega_bin = bin_green + bin_trees + bin_rocks + bin_black + bin_river + bin_terrain

    x, y = mega_bin.shape[:-1]

    game = game_map(20,35,23,10)  # (self, height, width, cell_size, refresh_rate):
    game.init_matrix()
    game.draw_cell()


    arrtree = element(game, bin_trees, bin_trees, 6)
    arrrock = element(game, bin_rocks, bin_rocks, 3)
    arrblack = element(game, bin_black, bin_black, 5)
    arrriver = element(game, bin_river, bin_river, 3)
    arrmain = element(game, bin_green, bin_green, 3)

    arrout = element(game, bin_terrain, bin_terrain, 4)

    for e in arrmain:
        game.draw_main(e[0], e[1])

    for e in arrtree:
        game.draw_tree(e[0], e[1])

    for e in arrrock:
        game.draw_rock(e[0], e[1])

    for e in arrblack:
        game.draw_black(e[0], e[1])

    for e in arrriver:
        game.draw_river(e[0], e[1])
    



    for e in arrout:
        game.draw_out(e[0], e[1])
    for i in range (2):
        for j in range (20):
            game.draw_out(i, j)
    for j in range (20):
            game.draw_out(34, j)



    im2 = game.draw_image()


    game.draw_player(mean_x, mean_y)

    return im, im2



def element(game, bin, im, nb):
    tiny_offset = 0
    result = []
    for x in range (0, 790, 22):
        for y in range (0, 322, 18):
                l = int(tiny_offset)
                arr = get_pixel_color(bin, x-12 - l , y)
                arr1 = get_pixel_color(bin, x-5 - l , y)
                arr2 = get_pixel_color(bin, x+2 - l , y)
                
                arr3 = get_pixel_color(bin, x-12 - l , y+12)
                arr4 = get_pixel_color(bin, x-5 - l , y+12)
                arr5 = get_pixel_color(bin, x+2 - l , y+12)

                arr6 = get_pixel_color(bin, x-12 - l , y+7)
                arr7 = get_pixel_color(bin, x-5 - l , y+7)
                arr8 = get_pixel_color(bin, x+2 - l , y+7)

                arrE = [arr, arr1, arr2, arr3, arr4, arr5, arr6, arr7, arr8]
                somme = 0
                for i in range (len(arrE)):
                    somme += (arrE[i][0] != 0 and arrE[i][1] != 0 and arrE[i][2] != 0)
                if somme >= nb: # !=
                    result.append([x//23, y//18])
    grid(im)
    return result


def grid(im):
    tiny_offset = 0
    
    for x in range (0, 820, 23):
            tiny_offset += 0.8
            for y in range (0, 330):
                l = int(tiny_offset)
                im = set_pixel_color(im,  x - l + 3, y, (100,0,100))
    tiny_offset = 0

    for y in range (0, 350, 19):
            tiny_offset += 1.2
            for x in range (0, 750):
                l = int(tiny_offset)
                im = set_pixel_color(im,  x , y - l + 0, (100,0,100))

def dot(im):
    tiny_offset = 0
    for x in range (0, 790, 22):
        for y in range (0, 322, 18):
                l = int(tiny_offset)
                
                im = set_area_color(im, x - 12 - l, y , (0,0,255), 2)
                im = set_area_color(im, x - 5 - l, y , (0,255,255), 2)
                im = set_area_color(im, x + 2 - l, y , (255,0,255), 2)
                
                im = set_area_color(im, x - 12 - l, y + 12, (0,0,255), 2)
                im = set_area_color(im, x - 5 - l, y + 12, (0,255,255), 2)
                im = set_area_color(im, x + 2 - l, y + 12, (255,0,255), 2)

                im = set_area_color(im, x - 12 - l, y + 6, (0,0,255), 2)
                im = set_area_color(im, x - 5 - l, y + 6, (0,255,255), 2)
                im = set_area_color(im, x + 2 - l, y + 6, (255,0,255), 2)


def rotate(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

# functions that allow you to work on a single screenshot instead of on the game

def debug_show(im):
    """function that shows the image"""
    hsv_frame = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    #terrain.draw_contours(im, hsv_frame)
    river.draw_contours(im, hsv_frame)
    blackrock.draw_contours(im, hsv_frame)
    rock.draw_contours(im, hsv_frame)
    trees.draw_contours_return_bin(im, hsv_frame)
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

def show2(ims):
    """function that shows the images without edit"""
    for i in range (len(ims)):
        cv2.imshow("im_" + str(i) , ims[i])
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
    cv2.imwrite("../test_data/img_masked2.png", im)

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
    if x < cols and y < rows:
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
    return im
    #raise Exception("get pixel: x and y out of range!" + str(y) + " " + str(rows))


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