import pyautogui
import win32gui

def screenshot(window_title=None):
    if window_title:
        hwnd = win32gui.FindWindow(None, "Unrailed!")
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            im = pyautogui.screenshot(region=(x, y, x1, y1))
            return im
        else:
            print('Window not found!')
    else:
        im = pyautogui.screenshot()
        return im