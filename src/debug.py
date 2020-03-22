import cv2
import numpy as np
import time
import pyautogui
import win32gui
import imutils
from pathfinding import astar

from detection import axe, trees, player, rock, blackrock, river, terrain, green


from capture import windowcapture
from show_map import game_map

def debug_main():
    """function to replace the main to keep it clean"""

    #im = single_screenshot()

    im = cv2.imread("../test_data/img_debug.png", cv2.COLOR_RGB2BGR)
    im = cut(im)
    #im, im2 = do_map(im)

    game = game_map(20,36,22,16,10)  # (self, height, width, cell_size, refresh_rate):
    game.init_matrix()

    
    get_array_from_bin(game, im)


    game.print_matrix()
    #print()
    #game.print_binary()

    game.draw_matrix()
    im4 = game.draw_image()

    game2 = game_map(20,36,22,16,10)  # (self, height, width, cell_size, refresh_rate):
    game2.init_matrix()
    get_array_from_bin(game2, im)
    im5 = astar_map(game2)
    

    grid(im)

    show2([im, im4, im5])


def cut(im):
    im = rotate(im, -8)
    x, y = 0, 125
    h, w = 320, 800
    im = im[y:y+h, x:x+w]

    rows,cols = im.shape[:-1]


    a , b , c = [382,52],[500,50],[400,200]
    offsetx = 20
    d, e, f = [382 + offsetx ,52],[500 + offsetx,50],[400 ,200]

    pts1 = np.float32([a, b, c])
    pts2 = np.float32([d, e, f])

    dst = im #  Uh Oh

    M = cv2.getAffineTransform(pts1,pts2)
    dst = cv2.warpAffine(im,M,(cols,rows))

    return dst


def astar_map(g):
    start, end = (15,19), (19,6)
    print(g.get_matrix()[start[1]][start[0]])
    print(g.get_matrix()[end[1]][end[0]])

    try:
        original = g.get_binary_matrix()
        astar.run(original, start, end, g)
    except:
        print(" ")

    
    g.matrix_add(start[1], start[0], 'S')
    g.matrix_add(end[1], end[0], 'U')
    g.draw_matrix()
    

    return g.draw_image()


def unpack_array(arr, vall, game):
    for e in arr:
            game.matrix_add(e[0], e[1], vall)


def get_array_from_bin(game, im):
    x, y = player.get_pos(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV))

    bin_green = green.get_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV))
    bin_trees = trees.get_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    bin_rocks = rock.get_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    bin_black = blackrock.get_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    bin_river = river.get_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV ))
    bin_terrain = terrain.get_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV ))
    bin_axe = axe.get_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV ))
    
    #arrplayer = element(game, bin_player, bin_player, 6)
    arrtree = element(game, bin_trees, bin_trees, 3)
    arrrock = element(game, bin_rocks, bin_rocks, 4)
    arrblack = element(game, bin_black, bin_black, 3)
    arrriver = element(game, bin_river, bin_river, 3)
    arrmain = element(game, bin_green, bin_green, 5)
    areaxe = element(game, bin_axe, bin_axe, 3)

    arrout = element(game, bin_terrain, bin_terrain, 6)
    
    unpack_array(arrmain, 'M', game)
    unpack_array(arrriver,'R', game)
    unpack_array(arrblack, 'B', game)
    unpack_array(arrtree,'T', game)
    unpack_array(arrrock, 'K', game)
    unpack_array(arrout,  '0', game)


    game.matrix_add(areaxe[0][0], areaxe[0][1] + 1, 'A')  # offset

    game.matrix_add(x, y, 'P')

    for i in range (2):
        for j in range (20):
            game.matrix_add(i, j, '0')
    for j in range (20):
            game.matrix_add(35, j, '0')
        

    game.matrix_add(x//22, y//16, 'P')
    

def element(game, bin, im, nb):
    result = []
    for x in range (22, 810, 22):
            for y in range (0, 320, 16):
                arr0 = get_pixel_color(bin, x-10, y)
                arr1 = get_pixel_color(bin, x-5 , y)
                arr2 = get_pixel_color(bin, x+0 , y)
                
                arr3 = get_pixel_color(bin, x-10, y+12)
                arr4 = get_pixel_color(bin, x-5 , y+12)
                arr5 = get_pixel_color(bin, x+0 , y+12)

                arr6 = get_pixel_color(bin, x-10, y+7)
                arr7 = get_pixel_color(bin, x-5 , y+7)
                arr8 = get_pixel_color(bin, x+0 , y+7)

                arrE = [arr0, arr1, arr2, arr3, arr4, arr5, arr6, arr7, arr8]
                somme = 0
                for i in range (len(arrE)):
                    somme += (arrE[i][0] != 0 and arrE[i][1] != 0 and arrE[i][2] != 0)
                if somme >= nb:
                    result.append([x//22 - 1, y//16])  # minus one because magic
    return result


def grid(im):
    tiny_offset = 0
    
    for x in range (5, 900, 22):
            tiny_offset += 0.1
            for y in range (0, 400):
                im = set_pixel_color(im,  x + int(tiny_offset), y, (100,0,100))

    for y in range (0, 400, 16):
            for x in range (0, 900):
                im = set_pixel_color(im,  x, y, (100,0,100))


def dot(im):
    tiny_offset = 0
    for x in range (22, 810, 22):
        for y in range (0, 320, 16):
                
                im = set_area_color(im, x - 10, y , (0,0,255), 2)
                im = set_area_color(im, x - 5, y , (0,255,0), 2)
                im = set_area_color(im, x + 0, y , (0,255,255), 2)
                
                im = set_area_color(im, x - 10, y + 12, (255,0,0), 2)
                im = set_area_color(im, x - 5, y + 12, (255,0,255), 2)
                im = set_area_color(im, x + 0, y + 12, (255,255,0), 2)

                im = set_area_color(im, x - 10, y + 6, (255,255,255), 2)
                im = set_area_color(im, x - 5, y + 6, (50,50,50), 2)
                im = set_area_color(im, x + 0, y + 6, (150,150,150), 2)


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