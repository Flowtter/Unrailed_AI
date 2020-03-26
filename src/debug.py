import cv2
import numpy as np
import time
import pyautogui
import win32gui
import imutils
from pathfinding import astar
from show import show_map

from detection import axe, pickaxe, trees, player, rock, blackrock, river, terrain, green

from player import bot
from capture import windowcapture


def debug_main(game):
    """function to replace the main to keep it clean"""
    im =  single_screenshot()
    #im = cut(im)
    #im = cv2.imread("../test_data/img_debug_save.png", cv2.COLOR_RGB2BGR)
    im = cut(im)

    axe_pos = axe.get_axe_minimap(im, cv2.cvtColor(im,cv2.COLOR_BGR2GRAY))
    pickaxe_pos = pickaxe.get_axe_minimap(im, cv2.cvtColor(im,cv2.COLOR_BGR2GRAY))

    bin_green = green.get_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV))
    arrmain = element(game, bin_green, bin_green, 3)
    unpack_array(arrmain, 'M', game)

    bin_p = player.get_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV))
    arrplayer = element(game, bin_p, bin_p, 3)
    unpack_array(arrplayer, 'P', game)

    if pickaxe_pos != None:
        for i in range (len(axe_pos)):
            axe_pos[i] = (axe_pos[i][0]//22, axe_pos[i][1]//16)
            unpack_array(axe_pos, 'A', game, (0,-1))
    
    if pickaxe_pos != None:
        for i in range (len(pickaxe_pos)):
            pickaxe_pos[i] = (pickaxe_pos[i][0]//22, pickaxe_pos[i][1]//16)
            unpack_array(pickaxe_pos, 'I', game, (0,-1))


    game.draw_matrix()
    im2 = game.draw_image()

    

    cv2.imshow("t", im2)



    debug_show(im)

def test(im, p_bot, game, last, mode, change, tried, random):
    
    set_array_from_bin(game, im)

    if random:
        player_pos = p_bot.rnd(15)
        return 0, last


    if change == False:
        try:
            if mode == "rock":
                player_pos = game.get_pos('P')[0]
                player_pos, last = p_bot.move("rock", game, False, player_pos, last)
                p_bot.breaking('K', player_pos, game)
            else:
                player_pos = game.get_pos('P')[0]
                player_pos, last = p_bot.move("tree", game, False, player_pos, last)
                p_bot.breaking('T', player_pos, game)
            return 0, last
        except:
            print("> PLAYER NOT FOUND, TRYING TO REVERSE PATH... ")
            player_pos = p_bot.rnd(3)
            return 0, last
    
    else:
        try:
            player_pos = game.get_pos('P')[0]
            if mode == "tree":
                player_pos = p_bot.move("pickaxe", game, False, player_pos, last)
                print("> FIND THE PICKAXE, WAITING FOR CONFIRMATION...")
                return -1, last
            
            elif mode == "rock":
                player_pos = p_bot.move("axe", game, False, player_pos, last)
                print("> FIND THE AXE, WAITING FOR CONFIRMATION...")
                return -1, last
        except:
            if mode == "tree":
                print("> COULD NOT FIND THE PICKAXE, RETRYING...")
            else:
                print("> COULD NOT FIND THE AXE, RETRYING...")
            return tried + 1, last

def debug_game():
    #im = single_screenshot()

    im = cv2.imread("../test_data/img_debug.png", cv2.COLOR_RGB2BGR)
    im = cut(im)
    #im, im2 = do_map(im)

    game = show_map.game_map(20,36,22,16,10)  # (self, height, width, cell_size, refresh_rate):
    game.init_matrix()

    
    set_array_from_bin(game, im)

    game.draw_matrix()
    im4 = game.draw_image()

    show2([im, im4])


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
    player = g.get_pos('P')
    tree = g.get_pos('t')
    start = player[0]

    # pour opti il faut ajoyter les contours, les M avec un T à coté deviennent V, je vérifie ces valuers là

    try:
        original = g.get_binary_matrix()
        end = astar.run(original, start, tree, g)
    except:
        print(" ")

    
    g.matrix_add(start[1], start[0], 'P')
    g.matrix_add(end[1], end[0], 'U')
    g.draw_matrix()
    

    return g.draw_image()


def unpack_array(arr, vall, game, offset = (0,0)):
    for e in arr:
        try:
            game.matrix_add(e[0] - offset[0], e[1] - offset[1], vall)
        except:
            pass  # FIXME


def set_array_from_bin(game, im):
    
    bin_player = player.get_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV))
    
    arrplayer = element(game, bin_player, bin_player, 3)

    bin_green = green.get_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV))
    bin_trees = trees.get_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    bin_rocks = rock.get_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    bin_black = blackrock.get_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    bin_river = river.get_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV ))
    bin_terrain = terrain.get_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV ))

    axe_pos = axe.get_axe_minimap(im, cv2.cvtColor(im,cv2.COLOR_BGR2GRAY))
    pickaxe_pos = pickaxe.get_axe_minimap(im, cv2.cvtColor(im,cv2.COLOR_BGR2GRAY))
    

    arrtree = element(game, bin_trees, bin_trees, 3)
    arrrock = element(game, bin_rocks, bin_rocks, 5)
    arrblack = element(game, bin_black, bin_black, 3)
    arrriver = element(game, bin_river, bin_river, 3)
    arrmain = element(game, bin_green, bin_green, 3)

    arrout = element(game, bin_terrain, bin_terrain, 6)

    unpack_array(arrrock, 'K', game)
    unpack_array(arrmain, 'M', game)
    unpack_array(arrriver,'R', game)
    unpack_array(arrblack, 'B', game)
    unpack_array(arrtree,'T', game)
    unpack_array(arrout,  '0', game)
    
    unpack_array(arrplayer, 'P', game, (0,-1))

    if pickaxe_pos != None:
        for i in range (len(axe_pos)):
            axe_pos[i] = (axe_pos[i][0]//22, axe_pos[i][1]//16)
            unpack_array(axe_pos, 'A', game, (0,-1))
    
    if pickaxe_pos != None:
        for i in range (len(pickaxe_pos)):
            pickaxe_pos[i] = (pickaxe_pos[i][0]//22, pickaxe_pos[i][1]//16)
            unpack_array(pickaxe_pos, 'I', game, (0,-1))


    game.replace_letter('t', 'M', 'T')
    game.replace_letter('k', 'M', 'K')


    for i in range (2):
        for j in range (20):
            game.matrix_add(i, j, '0')
    for j in range (20):
            game.matrix_add(35, j, '0')
    

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

# ??????????????? ^^^^^^^^^
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
    #player.draw_contours_return_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV))
    #green.draw_contours_return_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV))
    #trees.draw_contours_return_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    #rock.draw_contours_return_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    #blackrock.draw_contours_return_bin(im, cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
    #river.draw_contours_return_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV ))
    #terrain.draw_contours_return_bin(im, cv2.cvtColor(im,cv2.COLOR_BGR2HSV ))
    pos = axe.get_axe_minimap(im, cv2.cvtColor(im,cv2.COLOR_BGR2GRAY))
    axe.draw_contours(im, cv2.cvtColor(im,cv2.COLOR_BGR2GRAY))
    pickaxe.draw_contours(im, cv2.cvtColor(im,cv2.COLOR_BGR2GRAY))
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


def save_single():
    """function that take a single screnshot of the game and save it"""
    cv2.imwrite("../test_data/img_debug_save.png",rotate(single_screenshot(), -8))


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