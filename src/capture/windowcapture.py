import cv2
import numpy as np
import pyautogui
from threading import Thread
import time
import win32gui



class WindowCapture:

    # function init to declare variables

    def __init__(self, window_name, capture_rate, over):
        self.window_name = window_name
        self._thread_name = window_name + " Capture"

        self.wait_time = 1/capture_rate

        self.should_over = over

        self.frame = self.screenshot()
        self.should_stop = False

    # function start, give a thread to the object

    def start(self):
        self._thread = Thread(target=self.update, name=self._thread_name, args=())
        self._thread.daemon = True
        self._thread.start()
        return self

    # function update, replace self.frame by an image that has been screenshoted

    def update(self):
        while not self.should_stop: # changed True by self...
            start = time.time()

            self.frame = self.screenshot()

            delta = time.time() - start
            if delta < self.wait_time:
                time.sleep(self.wait_time - delta)

    # function that return the image

    def read(self):
        return self.frame

    # function that join the thread to then stop them

    def stop(self):
        self.should_stop = True
        self._thread.join()

    # function that take the screenshot of the game, self.window_name

    def screenshot(self):
        hwnd = win32gui.FindWindow(None, self.window_name)
        if not hwnd:
            raise Exception("Window not found!")

        if win32gui.GetForegroundWindow() != hwnd and self.should_over:
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            self.should_over = False

        l, t, r, d = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (l, t))

        return cv2.cvtColor(
                np.asarray(pyautogui.screenshot(region=(
                x, y,
                *win32gui.ClientToScreen(hwnd,(r-x, d-y))
                ))),
                cv2.COLOR_RGB2BGR
            )

    def force_update(self):
        return self.screenshot()







